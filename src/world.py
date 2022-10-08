
import actor_defs
import constants
import map
import actor_spawn_tiles

DEFAULT_HIT_PAUSE = 0.05

class World:
    def __init__(self):
        self.player = None
        self.actors = {}
        self.enemies = {}
        self.projectiles = {}
        self.items = {}
        self.npcs = {}
        self.explosions = {}
        self.next_actor_uid = 0
        # Also in draw order, bottom to top.
        self.actor_collections = {
            actor_defs.ActorType.item : self.items,
            actor_defs.ActorType.npc : self.npcs,
            actor_defs.ActorType.enemy : self.enemies,
            actor_defs.ActorType.projectile : self.projectiles,
            actor_defs.ActorType.explosion : self.explosions,
        }

        self.gold = 0
        self.crystals = 0

        self.hit_pause = 0

        self.map = map.Map({
            "world" : self,
            "tilemap" : 0,
        })

        p_index = actor_spawn_tiles.g_spawns["player"]
        self.add_actor(
            "player", 
            (p_index % constants.TILEMAP_TILES_WIDE)*8, 
            (p_index // constants.TILEMAP_TILES_WIDE)*8
        )
        cam = self.map.cam
        pos = self.player.sprite.position
        x = (pos[0] // cam.rect.w) * cam.rect.w
        y = (pos[1] // cam.rect.h) * cam.rect.h
        cam.set_position(x, y)

    def do_hit_pause(self, secs=DEFAULT_HIT_PAUSE):
        self.hit_pause = secs

    def screen_unload(self):
        for k in list(self.actors.keys()):
            a = self.actors[k]
            if a.type is not actor_defs.ActorType.player:
                self.remove_actor(k)

        assert(len(self.actors) == 1)

    def screen_load(self):
        assert(len(self.actors) == 1)

        c = constants

        scr_x = self.map.cam.rect.x // c.SCREEN_W
        scr_y = self.map.cam.rect.y // c.VIEW_H
        scr_index = scr_x + scr_y * c.TILEMAP_SCREENS_WIDE
        screen_dict = actor_spawn_tiles.g_spawns.get(scr_index)
        if not screen_dict:
            return

        for tile_index, name in screen_dict.items():
            self.add_actor(
                name, 
                (tile_index % c.TILEMAP_TILES_WIDE)*8, 
                (tile_index // c.TILEMAP_TILES_WIDE)*8
            )

    def add_actor(self, name, x, y):
        defin = actor_defs.defs.get(name)
        assert(defin)

        theActor = defin["create"](self, defin, x, y)
        theActor.uid = self.next_actor_uid
        self.actors[self.next_actor_uid] = theActor
        if theActor.type == actor_defs.ActorType.player:
            self.player = theActor
        else:
            self.actor_collections[theActor.type][theActor.uid] = theActor
        self.next_actor_uid += 1

    def remove_actor(self, uid):
        theActor = self.actors.get(uid)
        assert(theActor)

        del self.actors[uid]
        if theActor.type == actor_defs.ActorType.player:
            self.player = None
        else:
            del self.actor_collections[theActor.type][theActor.uid]

    def is_player_alive(self):
        return not self.player.is_dead()

    def attack_player(self, params):
        if self.player.check_hit(params):
            self.do_hit_pause()

    def player_attacked(self, params):
        for a in self.actors.values():
            if a.type != actor_defs.ActorType.player:
                if a.check_hit(params):
                    self.do_hit_pause()

    def update(self):
        self.map.update()

        self.player.update()

        for a_dict in self.actor_collections.values():
            for a in a_dict.values():
                a.update()

        on_remove_callbacks = []
        for k in list(self.actors.keys()):
            a = self.actors[k]
            if not a.is_alive:
                if a.on_dead_removal_func:
                    on_remove_callbacks.append(a.on_dead_removal_func)
                self.remove_actor(k)

        for f in on_remove_callbacks:
            f()

    def draw(self):
        self.map.draw()

        for a_dict in self.actor_collections.values():
            for a in a_dict.values():
                a.draw()

        self.player.draw()
