from worlds.AutoWorld import World
from .Items import SignalisItem, item_dict
from .Locations import SignalisLocation, location_dict
from worlds.generic.Rules import set_rule
from BaseClasses import Region
from .Regions import regions


class SignalisWorld(World):
    game = "Signalis"
    print("yay")
    base_id = 1027202200
    item_name_to_id = {item: id for id, item in enumerate(item_dict.keys(), base_id)}
    location_name_to_id = {location: id for id, location in enumerate(location_dict.keys(), base_id)}
    print(item_name_to_id)

    def create_item(self, name: str) -> SignalisItem:
        return SignalisItem(name, item_dict[name][0], self.item_name_to_id[name], self.player)
    
    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        # menu_region.add_locations(self.location_name_to_id, SignalisLocation)
        self.multiworld.regions.append(menu_region)

        # Adds locations to their respective levels in logic
        for region in regions:
            region_object = Region(region, self.player, self.multiworld)
            region_locations: dict[str, int | None] = {key: value for key, value in self.location_name_to_id.items() if location_dict[key][1] == region}
            region_object.add_locations(region_locations, SignalisLocation)
            self.multiworld.regions.append(region_object)
    
    def create_items(self) -> None:
        for item_key, item_value in item_dict.items():
            for _ in range(item_value[2]):
                self.multiworld.itempool.append(self.create_item(item_key))
    
    def set_rules(self):
        self.multiworld.get_region("Menu", self.player).connect(self.multiworld.get_region("Penrose Wreck", self.player))
        
        # Penrose Wreck Logic
        self.multiworld.get_region("Penrose Wreck", self.player).connect(self.multiworld.get_region("Installation AEON", self.player), None,
            lambda state: state.has("Adhesive Tape", self.player) and state.has("Airlock Key (Broken)", self.player))
        
        # Installation AEON Logic
        self.multiworld.get_region("Installation AEON", self.player).connect(self.multiworld.get_region("Worker Barracks", self.player), None,
            lambda state: state.has("Classroom Key", self.player) and state.has("Receptionist Key", self.player))
        set_rule(self.multiworld.get_location("Protektor Key", self.player),
            lambda state: state.has("Receptionist Key", self.player))
        set_rule(self.multiworld.get_location("Pistol", self.player),
            lambda state: state.has("Protektor Key", self.player))
        set_rule(self.multiworld.get_location("Aperture Card", self.player),
            lambda state: state.has("Protektor Key", self.player))
        set_rule(self.multiworld.get_location("Classroom Key (Installation AEON)", self.player),
            lambda state: state.has("Aperture Card", self.player))
        set_rule(self.multiworld.get_location("Repair Patch (Installation AEON - Aula)", self.player),
            lambda state: state.has("Aperture Card", self.player))
        set_rule(self.multiworld.get_location("10mm Ammo (Installation AEON - Aula)", self.player),
            lambda state: state.has("Aperture Card", self.player))
        
       # Worker Barracks logic
        self.multiworld.get_region("Worker Barracks", self.player).connect(self.multiworld.get_region("Hospital Wing", self.player), None,
            lambda state: state.has("Identification Key", self.player))
        set_rule(self.multiworld.get_location("East Wing Key", self.player),
            lambda state: state.has("Service Hatch Key", self.player))
        set_rule(self.multiworld.get_location("10mm Ammo (Worker Barracks - Office)", self.player),
            lambda state: state.has("Service Hatch Key", self.player))
        set_rule(self.multiworld.get_location("Disposable Stun Prod (Worker Barracks - Office)", self.player),
            lambda state: state.has("Service Hatch Key", self.player))
        set_rule(self.multiworld.get_location("Repair Patch (Worker Barracks - First Aid)", self.player),         
            lambda state: state.has("Service Hatch Key", self.player))
        set_rule(self.multiworld.get_location("Plate of Eternity", self.player),
            lambda state: state.has("Service Hatch Key", self.player) and state.has("Broken Key, Top Half", self.player)
                                        and state.has("Broken Key, Bottom Half", self.player))
        set_rule(self.multiworld.get_location("Radio Module", self.player),
            lambda state: state.has("Service Hatch Key", self.player) and state.has("Broken Key, Top Half", self.player)
                                        and state.has("Broken Key, Bottom Half", self.player))
        set_rule(self.multiworld.get_location("Identification Key", self.player),
            lambda state: state.has("Service Hatch Key", self.player) and state.has("Radio Module", self.player))
        set_rule(self.multiworld.get_location("Repair Patch (Worker Barracks - Protektor Bathroom)", self.player),
            lambda state: state.has("East Wing Key", self.player))
        set_rule(self.multiworld.get_location("10mm Ammo (Worker Barracks - Store Room)", self.player),
            lambda state: state.has("East Wing Key", self.player))
        set_rule(self.multiworld.get_location("Mensa Key", self.player),
            lambda state: state.has("East Wing Key", self.player))
        set_rule(self.multiworld.get_location("10mm Ammo (Worker Barracks - Mensa, Top of Room)", self.player),
            lambda state: state.has("Mensa Key", self.player))
        set_rule(self.multiworld.get_location("10mm Ammo (Worker Barracks - Mensa, Bottom of Room)", self.player),
            lambda state: state.has("Mensa Key", self.player))
        set_rule(self.multiworld.get_location("Repair Patch (Worker Barracks - Mensa)", self.player),
            lambda state: state.has("Mensa Key", self.player))
        set_rule(self.multiworld.get_location("West Wing Key", self.player),
            lambda state: state.has("Mensa Key", self.player))
        set_rule(self.multiworld.get_location("Disposable Stun Prod (Worker Barracks - Rationing Office)", self.player),
            lambda state: state.has("Mensa Key", self.player))
        set_rule(self.multiworld.get_location("Broken Key, Top Half", self.player),
            lambda state: state.has("Mensa Key", self.player))
        set_rule(self.multiworld.get_location("10mm Ammo (Worker Barracks - Lockers)", self.player),
            lambda state: state.has("West Wing Key", self.player))
        set_rule(self.multiworld.get_location("Broken Key, Bottom Half", self.player),
            lambda state: state.has("West Wing Key", self.player))
        set_rule(self.multiworld.get_location("Disposable Stun Prod (Worker Barracks - Registry)", self.player),
            lambda state: state.has("West Wing Key", self.player))
        set_rule(self.multiworld.get_location("Repair Spray+ (Worker Barracks - Isolation)", self.player),
            lambda state: state.has("West Wing Key", self.player))
        # set_rule(self.multiworld.get_location("Key of Love", self.player),
            # lambda state: state.has("West Wing Key", self.player))

        # Hospital Wing logic
        self.multiworld.get_region("Hospital Wing", self.player).connect(self.multiworld.get_region("Protektor Levels", self.player), None,
            lambda state: state.has("Air Key", self.player) and state.has("Fire Key", self.player) and state.has("Gold Key", self.player)
                                        and state.has("Water Key", self.player) and state.has("Blank Key", self.player)
                                        and state.has_any(["Pistol", "Shotgun", "Revolver", "Rifle", "Submachine Gun"], self.player))
        set_rule(self.multiworld.get_location("Eidetic Module", self.player),
            lambda state: state.has("Radio Module", self.player))
        set_rule(self.multiworld.get_location("Incinerator Key", self.player),
            lambda state: state.has("Radio Module", self.player))
        set_rule(self.multiworld.get_location("Gold Key", self.player),
            lambda state: state.has("Video Cassette", self.player))
        set_rule(self.multiworld.get_location("Disposable Stun Prod (Hospital Wing - Pump Room)", self.player),
            lambda state: state.has("Pump Room Key", self.player))
        set_rule(self.multiworld.get_location("Disposable Stun Prod (Hospital Wing - Flooded Office)", self.player),
            lambda state: state.has("Pump Room Key", self.player))
        set_rule(self.multiworld.get_location("Water Key", self.player),
            lambda state: state.has("Pump Room Key", self.player))
        set_rule(self.multiworld.get_location("Repair Patch (Hospital Wing - Flooded Bathroom)", self.player),
            lambda state: state.has("Pump Room Key", self.player))
        set_rule(self.multiworld.get_location("10mm Ammo (Hospital Wing - Flooded Store Room)", self.player),
            lambda state: state.has("Pump Room Key", self.player))
        set_rule(self.multiworld.get_location("10mm Ammo (Hospital Wing - Sleeping Ward)", self.player),
            lambda state: state.has("Pump Room Key", self.player))
        set_rule(self.multiworld.get_location("Blank Key", self.player),
            lambda state: state.has("Pump Room Key", self.player))
        set_rule(self.multiworld.get_location("Examination Room Key", self.player),
            lambda state: state.has("Pump Room Key", self.player))
        set_rule(self.multiworld.get_location("Video Cassette", self.player),
            lambda state: state.has("Pump Room Key", self.player))
        set_rule(self.multiworld.get_location("12mm Ammo (Hospital Wing - Sleeping Ward)", self.player),
            lambda state: state.has("Pump Room Key", self.player))
        set_rule(self.multiworld.get_location("Air Key", self.player),
            lambda state: state.has("Pump Room Key", self.player) and state.has("10mm Socket", self.player) 
                                        and state.has("Socket Wrench Handle", self.player))
        set_rule(self.multiworld.get_location("Thermite Flare (Hospital Wing - Incinerator Room)", self.player),
            lambda state: state.has("Incinerator Room Key", self.player))
        set_rule(self.multiworld.get_location("Fire Key", self.player),
            lambda state: state.has("Incinerator Room Key", self.player))
        set_rule(self.multiworld.get_location("10mm Ammo (Hospital Wing - Surgery)", self.player),
            lambda state: state.has("Air Key", self.player) and state.has("Fire Key", self.player) and state.has("Gold Key", self.player)
                                        and state.has("Water Key", self.player) and state.has("Blank Key", self.player)
                                        and state.has_any(["Pistol", "Shotgun", "Revolver", "Rifle", "Submachine Gun"], self.player))