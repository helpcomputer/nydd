
import actor_defs
import constants
import map

class World:
    def __init__(self):
        self.player = None
        self.actors = {}
        self.enemies = {}
        self.projectiles = {}
        self.items = {}
        self.npcs = {}
        self.next_actor_uid = 0
        # Also in draw order, bottom to top.
        self.all_actors = {
            actor_defs.ActorType.item : self.items,
            actor_defs.ActorType.npc : self.npcs,
            actor_defs.ActorType.enemy : self.enemies,
            actor_defs.ActorType.projectile : self.projectiles,
        }

        self.hp = constants.START_HP
        self.mp = constants.START_MP
        self.gold = 0
        self.crystals = 0
        self.weapon = None

        self.map = map.Map({
            "world" : self,
            "tilemap" : 0,
        })

        self.add_actor("player", 99*8, 123*8)
        #self.add_actor("player", 124*8, 137*8)

        self.add_actor("old_lady", 151*8, 137*8)
        self.add_actor("octoman", 117*8, 137*8)

        #print(self.all_actors)

        cam = self.map.cam
        pos = self.player.sprite.position
        x = (pos[0] // cam.rect.w) * cam.rect.w
        y = (pos[1] // cam.rect.h) * cam.rect.h
        cam.set_position(x, y)

    def add_actor(self, name, x, y):
        defin = actor_defs.defs.get(name)
        assert(defin)

        theActor = defin["create"](self, defin, x, y)
        theActor.uid = self.next_actor_uid
        self.actors[self.next_actor_uid] = theActor
        if theActor.type == actor_defs.ActorType.player:
            self.player = theActor
        else:
            self.all_actors[theActor.type][theActor.uid] = theActor
        self.next_actor_uid += 1

    def remove_actor(self, uid):
        theActor = self.actors.get(uid)
        assert(theActor)

        del self.actors[uid]
        if theActor.type == actor_defs.ActorType.player:
            self.player = None
        else:
            del self.all_actors[theActor.type][theActor.uid]

    def update(self):
        self.map.update()

        self.player.update()

        for a_dict in self.all_actors.values():
            for a in a_dict.values():
                a.update()

    def draw(self):
        self.map.draw()

        for a_dict in self.all_actors.values():
            for a in a_dict.values():
                a.draw()

        self.player.draw()
