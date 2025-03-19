from worlds.AutoWorld import World
from .Items import SignalisItemClassification, SignalisItem, item_dict
from .Locations import SignalisLocationClassification, SignalisLocation, location_dict
from worlds.generic.Rules import set_rule, add_rule
from BaseClasses import ItemClassification, Region
from .Regions import regions


class SignalisWorld(World):
    game = "Signalis"
    print("yay")
    base_id = 1027202200
    item_name_to_id = {item: id for id, item in enumerate(item_dict.keys(), base_id)}
    location_name_to_id = {location: id for id, location in enumerate(location_dict.keys(), base_id)}
    print(item_name_to_id)

    def create_item(self, item: str) -> SignalisItem:
        return SignalisItem(item, item_dict[item][0], self.item_name_to_id[item], self.player)
    
    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        # menu_region.add_locations(self.location_name_to_id, SignalisLocation)
        self.multiworld.regions.append(menu_region)

        # Adds items to their respective levels in logic
        for region in regions:
            region_object = Region(region, self.player, self.multiworld)
            region_locations = {key: value for key, value in self.location_name_to_id.items() if location_dict[key][1] == region}
            region_object.add_locations(region_locations, SignalisLocation)
            self.multiworld.regions.append(region_object)
    
    def create_items(self) -> None:
        for item_key, item_value in item_dict.items():
            for count in range(item_value[2]):
                self.multiworld.itempool.append(self.create_item(item_key))
    
    def set_rules(self):
        self.multiworld.get_region("Menu", self.player).connect(self.multiworld.get_region("Penrose Wreck", self.player))
        self.multiworld.get_region("Penrose Wreck", self.player).connect(self.multiworld.get_region("Installation AEON", self.player), None,
            lambda state: state.has("Adhesive Tape", self.player) and state.has("Airlock Key (Broken)", self.player))
        # set_rule(self.multiworld.get_location("", self.player),
                 # lambda state: state.has("Adhesive Tape", self.player) and state.has("Airlock Key (Broken)", self.player))