
# Example:
#
# "helmet" : {
#     "add" : {
#         "defence" : 0.5
#     },
# },   
# "necklace" : {
#     "mult" : {
#         "attack" : 0.5,
#     }
# }

class Stats:
    def __init__(self, stats):
        self.base = {}
        self.modifiers = {}
        
        for k, v in stats.items():
            self.base[k] = v
        
    def get_base(self, id):
        return self.base[id]
        
    def add_modifier(self, id, modifier):
        self.modifiers[id] = {
            "add" : modifier.get("add", {}),
            "mult" : modifier.get("mult", {}),
        }
        
    def remove_modifier(self, id):
        del self.modifiers[id]
        
    def get(self, id):
        total = self.base.get(id, 0)
        multiplier = 0
        
        for v in self.modifiers.values():
            total += v["add"].get(id, 0)
            multiplier += v["mult"].get(id, 0)
            
        return total + (total * multiplier)
        
    def set(self, id, value):
        self.base[id] = value
