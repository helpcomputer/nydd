
from enum import Enum

import actor
import player.player_actor
import enemies.octoman
import explosion

class ActorType(Enum):
    player = 0
    enemy = 1
    projectile = 2
    item = 3
    npc = 4
    explosion = 5

BASE_STATS = {
    ActorType.player : {
        "attack" : 1,
        "defence" : 1,
        "hp_now" : 100,
        "hp_max" : 100,
        "mp_now" : 0,
        "mp_max" : 100,
    },
    ActorType.enemy : {
        "attack" : 1,
        "defence" : 1,
        "hp_now" : 100,
        "hp_max" : 100,
    },
    ActorType.projectile : {
        "attack" : 1,
        "timeout" : 1
    },
}

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
            },
            "climb" : {
                "frames" : ((240,160),),
                "frame_spd" : 0.15,
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
        "create" : enemies.octoman.Octoman,
        "type" : ActorType.enemy,
        "states" : {
            "walk" : {
                "frames" : ((192,224),(208,224)),
                "frame_spd" : 0.2
            },
            "attack" : {
                "frames" : ((192,208),(208,208)),
                "frame_spd" : 0.25,
                "loop" : False
            },
        },
        "size" : (16,16),
        "hitbox" : (1,0,14,16),
        "colour_key" : 1,
    },

    "explosion16" : {
        "create" : explosion.Explosion,
        "type" : ActorType.explosion,
        "states" : {
            "explode" : {
                "frames" : (
                    (0,240),(16,240),(32,240),(48,240),(64,240),(80,240)
                ),
                "frame_spd" : 0.06,
                "loop" : False
            },
        },
        "size" : (16,16),
    },
}
