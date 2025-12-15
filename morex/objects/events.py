from morex import MorexPlace
import random
import copy
from morex import logging


class MorexEvent:
    def __init__(self, obj, lang):
        self.sid: str = obj['id']
        self.disname: str = obj['disname'][lang]
        self.description: str = obj['description'][lang]
        self.start: int = obj['start']
        self.end: int = obj['end']
        self.default_features: dict = obj['features']
        self.has_quests: bool = obj['quests']
        self._location: dict = obj['location_overrides']
        self.notify_start: bool = obj['notifications']['start']  
        self.notify_before_end: int | bool = obj['notifications']['before_end']
        self.notify_end: bool = obj['notifications']['end']

    def __bool__(self):
        return True
        
    def location_overrides(self, location: MorexPlace):
        # location_sid: [{"min_chance", "max_chance", search_obj}]
        items = copy.deepcopy(location.loottable)
        if location.name in self._location:
            # yeah you should probably use the thing to get the item 
            # but that's gonna be done later 
            chance = random.randint(1, 10000)
            injection = None
            for i in self._location[location.name]:
                if i['min_chance'] <= chance <= i['max_chance']:
                    injection = i['search_obj']
            for i in items:
                if i['item'] == 'event':
                    i.update(injection)
                    break
            else:
                logging.warn(f"Location {location.displayname} doesn't have event item that could be replaced.")
                return items
            return items
        for i in items:
            if i['item'] == 'event':
                i.update(i['fallback'])
        return items

            
            


