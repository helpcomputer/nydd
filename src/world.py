
import actor_defs
import constants
import map

class World:
    def __init__(self):
        self.actors = []
        self.player = None
        self.hp = constants.START_HP
        self.mp = constants.START_MP
        self.gold = 0
        self.crystals = 0
        self.weapon = None

        self.map = map.Map({
            "world" : self,
            "tilemap" : 0,
        })

        self.player = self.add_actor("player", 99*8, 123*8)

        self.add_actor("old_lady", 151*8, 137*8)

        self.map.cam.set_position(
            self.player.sprite.position[0],
            self.player.sprite.position[1]
        )

        #print("Assigned player as {}".format(self.player))

    def add_actor(self, name, x, y):
        defin = actor_defs.defs.get(name)
        assert(defin)

        theActor = defin["create"](self, defin, x, y)
        self.actors.append(theActor)

        return theActor

    def update(self):
        self.map.update()

    def draw(self):
        self.map.draw()
