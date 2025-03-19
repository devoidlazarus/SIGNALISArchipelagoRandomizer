from worlds.AutoWorld import World
from .Items import SignalisItemClassification, SignalisItem, item_dict
from .Locations import SignalisLocationClassification, SignalisLocation, location_dict
from worlds.generic.Rules import set_rule, add_rule


class SignalisWorld(World):
    game = "Signalis"
    print("yay")
    base_id = 1027202200
    item_name_to_id = {item: id for id, item in enumerate(item_dict.keys(), base_id)}
    location_name_to_id = {location: id for id, location in enumerate(location_dict.keys(), base_id)}
    print(item_name_to_id)

    def create_items(self) -> None:
        for item_key, item_value in item_dict.items():
            self.multiworld.itempool.append(SignalisItem()

    def set_rules(self):
        set_rule(self.multiworld.get_location("Airlock Key (Fixed)", self.player),
                 lambda state: state.has("Adhesive Tape", self.player) and state.has("Airlock Key (Broken)", self.player))