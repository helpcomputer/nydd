
from enum import Enum

import actor
import player.player_actor

class ActorType(Enum):
    player = 0
    enemy = 1
    projectile = 2
    item = 3
    npc = 4

defs = {
    "player" : {
        "create" : player.player_actor.Player,
        "type" : ActorType.player,
        "states" : {
            "idle" : {
                "frames" : ((224,240),(240,240)),
                "frame_spd" : 0.5
            },
            "run" : {
                "frames" : ((224,224),(240,224)),
                "frame_spd" : 0.1
            },
            "attack" : {
                "frames" : ((224,208),(240,208)),
                "frame_spd" : 0.1,
                "loop" : False
            },
            "jump" : {
                "frames" : ((224,192),(240,192)),
                "frame_spd" : 0.15,
                "loop" : False
            },
            "fall" : {
                "frames" : ((240,176),),
                "frame_spd" : 0.15,
                "loop" : False
            }
        },
        "size" : (16,16),
        "hitbox" : (4,2,8,14)
    },
    
    "old_lady" : {
        "create" : actor.Actor,
        "type" : ActorType.npc,
        "states" : {
            "idle" : {
                "frames" : ((192,240),(208,240)),
                "frame_spd" : 1
            },
        },
        "size" : (16,16),
        "hitbox" : (4,2,8,14)
    },

    "octoman" : {
        "create" : actor.Actor,
        "type" : ActorType.enemy,
        "states" : {
            "walk" : {
                "frames" : ((192,224),(208,224)),
                "frame_spd" : 0.4
            },
        },
        "size" : (16,16),
        "hitbox" : (1,0,14,16),
        "colour_key" : 1,
    },
}
