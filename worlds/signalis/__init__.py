from worlds.AutoWorld import World
from .Items import SignalisItem, item_dict
from .Locations import SignalisLocation, location_dict
from worlds.generic.Rules import set_rule
from BaseClasses import Region
from .Regions import regions
from .Options import SignalisOptions


class SignalisWorld(World):
    game = "Signalis"
    # print("yay")
    base_id = 1027202200
    item_name_to_id = {item: id for id, item in enumerate(item_dict.keys(), base_id)}
    location_name_to_id = {location: id for id, location in enumerate(location_dict.keys(), base_id)}
    # print(item_name_to_id)
    options_dataclass = SignalisOptions
    options: SignalisOptions

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
            if not self.options.ending_artifact.value:
                region_locations.pop("Key of Love", None)
                region_locations.pop("Key of Eternity", None)
                region_locations.pop("Key of Sacrifice", None)
            region_object.add_locations(region_locations, SignalisLocation)
            self.multiworld.regions.append(region_object)
    
    def create_items(self) -> None:
        for item_key, item_value in item_dict.items():
            for _ in range(item_value[2]):
                if not self.options.ending_artifact.value and (item_key == "Key of Love" or item_key == "Key of Eternity" or item_key == "Key of Sacrifice"):
                    pass
                else: 
                    self.multiworld.itempool.append(self.create_item(item_key))
    
    def set_rules(self):
        self.multiworld.get_region("Menu", self.player).connect(self.multiworld.get_region("Penrose Wreck", self.player))
        
        # Penrose Wreck Logic
        self.multiworld.get_region("Penrose Wreck", self.player).connect(self.multiworld.get_region("Installation AEON", self.player), None,
            lambda state: state.has_all(["Adhesive Tape", "Airlock Key (Broken)"], self.player))
        set_rule(self.multiworld.get_location("Broken Airlock Key", self.player),
            lambda state: state.has("Photograph (Ariane)", self.player))
        
        # Installation AEON Logic
        self.multiworld.get_region("Installation AEON", self.player).connect(self.multiworld.get_region("Worker Barracks", self.player), None,
            lambda state: state.has_all(["Classroom Key", "Receptionist Key"], self.player))
        set_rule(self.multiworld.get_location("Protektor Key", self.player),
            lambda state: state.has("Receptionist Key", self.player))
        set_rule(self.multiworld.get_location("Pistol", self.player),
            lambda state: state.has_all(["Protektor Key", "Receptionist Key"], self.player))
        set_rule(self.multiworld.get_location("Aperture Card", self.player),
            lambda state: state.has_all(["Protektor Key", "Receptionist Key"], self.player))
        set_rule(self.multiworld.get_location("Classroom Key (Installation AEON)", self.player),
            lambda state: state.has_all(["Aperture Card", "Receptionist Key"], self.player))
        set_rule(self.multiworld.get_location("Repair Patch (Installation AEON - Aula)", self.player),
            lambda state: state.has_all(["Protektor Key", "Receptionist Key"], self.player))
        set_rule(self.multiworld.get_location("10mm Ammo (Installation AEON - Aula)", self.player),
            lambda state: state.has_all(["Protektor Key", "Receptionist Key"], self.player))
        
       # Worker Barracks logic
        self.multiworld.get_region("Worker Barracks", self.player).connect(self.multiworld.get_region("Hospital Wing", self.player), None,
            lambda state: state.has("Identification Key", self.player))
        set_rule(self.multiworld.get_location("East Wing Key", self.player),
            lambda state: state.has_any(["Service Hatch Key", "West Wing Key"], self.player))
        set_rule(self.multiworld.get_location("10mm Ammo (Worker Barracks - Office)", self.player),
            lambda state: state.has_any(["Service Hatch Key", "West Wing Key"], self.player))
        set_rule(self.multiworld.get_location("Disposable Stun Prod (Worker Barracks - Office)", self.player),
            lambda state: state.has_any(["Service Hatch Key", "West Wing Key"], self.player))
        set_rule(self.multiworld.get_location("Repair Patch (Worker Barracks - First Aid)", self.player),         
            lambda state: state.has_any(["Service Hatch Key", "West Wing Key"], self.player))
        set_rule(self.multiworld.get_location("Plate of Eternity", self.player),
            lambda state: state.has_any(["Service Hatch Key", "West Wing Key"], self.player) and 
                            state.has_all(["Broken Key, Top Half", "Broken Key, Bottom Half"], self.player))
        set_rule(self.multiworld.get_location("Radio Module", self.player),
            lambda state: state.has_any(["Service Hatch Key", "West Wing Key"], self.player) and 
                            state.has_all(["Broken Key, Top Half", "Broken Key, Bottom Half"], self.player))
        set_rule(self.multiworld.get_location("Identification Key", self.player),
            lambda state: state.has_any(["Service Hatch Key", "West Wing Key"], self.player) and state.has("Radio Module", self.player))
        set_rule(self.multiworld.get_location("Repair Patch (Worker Barracks - Protektor Bathroom)", self.player),
            lambda state: state.has("East Wing Key", self.player) and state.has_any(["West Wing Key", "Service Hatch Key"], self.player))
        set_rule(self.multiworld.get_location("10mm Ammo (Worker Barracks - Store Room)", self.player),
            lambda state: state.has("East Wing Key", self.player) and state.has_any(["West Wing Key", "Service Hatch Key"], self.player))
        set_rule(self.multiworld.get_location("Mensa Key", self.player),
            lambda state: state.has("East Wing Key", self.player) and state.has_any(["West Wing Key", "Service Hatch Key"], self.player))
        set_rule(self.multiworld.get_location("10mm Ammo (Worker Barracks - Mensa, Top of Room)", self.player),
            lambda state: state.has_all(["Mensa Key", "East Wing Key"], self.player))
        set_rule(self.multiworld.get_location("10mm Ammo (Worker Barracks - Mensa, Bottom of Room)", self.player),
            lambda state: state.has_all(["Mensa Key", "East Wing Key"], self.player))
        set_rule(self.multiworld.get_location("Repair Patch (Worker Barracks - Mensa)", self.player),
            lambda state: state.has_all(["Mensa Key", "East Wing Key"], self.player))
        set_rule(self.multiworld.get_location("West Wing Key", self.player),
            lambda state: state.has_all(["Mensa Key", "East Wing Key"], self.player))
        set_rule(self.multiworld.get_location("Disposable Stun Prod (Worker Barracks - Rationing Office)", self.player),
            lambda state: state.has_all(["Mensa Key", "East Wing Key"], self.player))
        set_rule(self.multiworld.get_location("Broken Key, Top Half", self.player),
            lambda state: state.has_all(["Mensa Key", "East Wing Key"], self.player))
        set_rule(self.multiworld.get_location("10mm Ammo (Worker Barracks - Lockers)", self.player),
            lambda state: state.has("West Wing Key", self.player))
        set_rule(self.multiworld.get_location("Broken Key, Bottom Half", self.player),
            lambda state: state.has("West Wing Key", self.player))
        set_rule(self.multiworld.get_location("Disposable Stun Prod (Worker Barracks - Registry)", self.player),
            lambda state: state.has("West Wing Key", self.player))
        set_rule(self.multiworld.get_location("Repair Spray+ (Worker Barracks - Isolation)", self.player),
            lambda state: state.has("West Wing Key", self.player))
        if self.options.ending_artifact.value:
            set_rule(self.multiworld.get_location("Key of Love", self.player),
                lambda state: state.has_all(["West Wing Key", "Radio Module"], self.player))

        # Hospital Wing logic
        self.multiworld.get_region("Hospital Wing", self.player).connect(self.multiworld.get_region("Protektor Levels", self.player), None,
            lambda state: state.has_all(["Air Key", "Fire Key", "Gold Key", "Water Key", "Blank Key"], self.player)
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
            lambda state: state.has_all(["Pump Room Key", "10mm Socket", "Socket Wrench Handle"], self.player))
        set_rule(self.multiworld.get_location("Thermite Flare (Hospital Wing - Incinerator Room)", self.player),
            lambda state: state.has("Incinerator Room Key", self.player))
        set_rule(self.multiworld.get_location("Fire Key", self.player),
            lambda state: state.has("Incinerator Room Key", self.player))
        set_rule(self.multiworld.get_location("10mm Ammo (Hospital Wing - Surgery)", self.player),
            lambda state: state.has_all(["Air Key", "Fire Key", "Gold Key", "Water Key", "Blank Key"], self.player)
                                        and state.has_any(["Pistol", "Shotgun", "Revolver", "Rifle", "Submachine Gun"], self.player))
        set_rule(self.multiworld.get_location("10mm Socket", self.player),
            lambda state: state.has("Examination Room Key", self.player))
        set_rule(self.multiworld.get_location("Autoinjector (Hospital Wing - Exam Room)", self.player),
            lambda state: state.has("Examination Room Key", self.player))
        
        # Protektor Levels logic
        self.multiworld.get_region("Protektor Levels", self.player).connect(self.multiworld.get_region("Mines", self.player), None,
            lambda state: state.has_all(["Administrator's Key", "Fuse", "Maintenance Key"], self.player))
        set_rule(self.multiworld.get_location("10mm Ammo (Protektor Levels - Cleaning Room Hallway)", self.player),
            lambda state: state.has("Maintenance Key", self.player))
        set_rule(self.multiworld.get_location("12mm Ammo (Protektor Levels - STCR Dorm, 6th Floor)", self.player),
            lambda state: state.has("Maintenance Key", self.player))
        set_rule(self.multiworld.get_location("Repair Patch (Protektor Levels - Cleaning Room)", self.player),
            lambda state: state.has("Maintenance Key", self.player))
        set_rule(self.multiworld.get_location("Autoinjector (Protektor Levels - Cleaning Room)", self.player),
            lambda state: state.has("Maintenance Key", self.player))
        set_rule(self.multiworld.get_location("Repair Patch (Protektor Levels - Cleaning Room Hallway)", self.player),
            lambda state: state.has("Maintenance Key", self.player))
        set_rule(self.multiworld.get_location("Repair Patch (Protektor Levels - Workshop Hallway)", self.player),
            lambda state: state.has("Maintenance Key", self.player))
        set_rule(self.multiworld.get_location("Disposable Stun Prod (Protektor Levels - ARAR Dorm)", self.player),
            lambda state: state.has("Maintenance Key", self.player))
        set_rule(self.multiworld.get_location("10mm Ammo (Protektor Levels - ARAR Dorm)", self.player),
            lambda state: state.has("Maintenance Key", self.player))
        set_rule(self.multiworld.get_location("Shotgun Rounds (Protektor Levels - ARAR Dorm)", self.player),
            lambda state: state.has("Maintenance Key", self.player))
        set_rule(self.multiworld.get_location("Repair Spray (Protektor Levels - South STAR Dorm)", self.player),
            lambda state: state.has("Maintenance Key", self.player))
        set_rule(self.multiworld.get_location("Autoinjector (Protektor Levels - South STAR Dorm)", self.player),
            lambda state: state.has("Maintenance Key", self.player))
        set_rule(self.multiworld.get_location("Shotgun Rounds (Protektor Levels - Dining Room Hallway)", self.player),
            lambda state: state.has("Maintenance Key", self.player))
        set_rule(self.multiworld.get_location("10mm Ammo (Protektor Levels - Dining Room Hallway)", self.player),
            lambda state: state.has("Maintenance Key", self.player))
        set_rule(self.multiworld.get_location("10mm Ammo (Protektor Levels - Dining Room)", self.player),
            lambda state: state.has("Maintenance Key", self.player))
        set_rule(self.multiworld.get_location("Fuse", self.player),
            lambda state: state.has("Maintenance Key", self.player))
        set_rule(self.multiworld.get_location("10mm Ammo (Protektor Levels - East STAR Dorm)", self.player),
            lambda state: state.has("Maintenance Key", self.player))
        set_rule(self.multiworld.get_location("Shutter Gate Handle", self.player),
            lambda state: state.has_all(["Maintenance Key", "Fuse"], self.player))
        set_rule(self.multiworld.get_location("Repair Spray+ (Protektor Levels - FKLR Bedroom)", self.player),
            lambda state: state.has_all(["Maintenance Key", "Fuse"], self.player))
        set_rule(self.multiworld.get_location("Disposable Stun Prod (Protektor Levels - FKLR Bedroom)", self.player),
            lambda state: state.has_all(["Maintenance Key", "Fuse"], self.player))
        set_rule(self.multiworld.get_location("10mm Ammo (Protektor Levels - FKLR Bedroom)", self.player),
            lambda state: state.has_all(["Maintenance Key", "Fuse"], self.player))
        set_rule(self.multiworld.get_location("Flashlight Module", self.player),
            lambda state: state.has_all(["Maintenance Key", "Fuse"], self.player))
        set_rule(self.multiworld.get_location("Astrolabe", self.player),
            lambda state: state.has_all(["Maintenance Key", "Fuse", "Library Key"], self.player))
        set_rule(self.multiworld.get_location("Repair Spray (Protektor Levels - Library)", self.player),
            lambda state: state.has_all(["Maintenance Key", "Fuse", "Library Key"], self.player))
        set_rule(self.multiworld.get_location("Hummingbird Key", self.player),
            lambda state: state.has_all(["Maintenance Key", "Fuse", "Radio Module", "Broken Music Cassette"], self.player) and state.has("Adhesive Tape", self.player, 2))
        set_rule(self.multiworld.get_location("Disposable Stun Prod (Protektor Levels - KLBR Study)", self.player),
            lambda state: state.has_all(["Maintenance Key", "Fuse", "Hummingbird Key"], self.player))
        set_rule(self.multiworld.get_location("Eagle Key", self.player),
            lambda state: state.has_all(["Maintenance Key", "Fuse", "Hummingbird Key"], self.player))
        set_rule(self.multiworld.get_location("Autoinjector (Protektor Levels - Repair Bay)", self.player),
            lambda state: state.has_all(["Maintenance Key", "Flashlight Module"], self.player))
        set_rule(self.multiworld.get_location("Shotgun Rounds (Protektor Levels - Shooting Range)", self.player),
            lambda state: state.has_all(["Maintenance Key", "Flashlight Module"], self.player))
        set_rule(self.multiworld.get_location("12mm Ammo (Protektor Levels - Shooting Range)", self.player),
            lambda state: state.has_all(["Maintenance Key", "Flashlight Module"], self.player))
        set_rule(self.multiworld.get_location("Weapon Case", self.player),
            lambda state: state.has_all(["Maintenance Key", "Flashlight Module"], self.player))
        set_rule(self.multiworld.get_location("Island Key", self.player),
            lambda state: state.has_all(["Maintenance Key", "Flashlight Module"], self.player))
        set_rule(self.multiworld.get_location("10mm Ammo (Protektor Levels - Protektor Archive)", self.player),
            lambda state: state.has_all(["Maintenance Key", "Flashlight Module"], self.player))
        set_rule(self.multiworld.get_location("Hunter's Key", self.player),
            lambda state: state.has_all(["Maintenance Key", "Flashlight Module"], self.player))
        set_rule(self.multiworld.get_location("Adhesive Tape (Protektor Levels)", self.player),
            lambda state: state.has_all(["Maintenance Key", "Flashlight Module"], self.player))
        set_rule(self.multiworld.get_location("Shotgun Rounds (Protektor Levels - ADLR Bedroom)", self.player),
            lambda state: state.has_all(["Maintenance Key", "Flashlight Module", "Fuse"], self.player))
        set_rule(self.multiworld.get_location("Shotgun Rounds (Protektor Levels - STCR Dorm, 8th Floor)", self.player),
            lambda state: state.has_all(["Maintenance Key", "Flashlight Module", "Fuse"], self.player))
        set_rule(self.multiworld.get_location("Repair Spray+ (Protektor Levels - STCR Dorm, 8th Floor)", self.player),
            lambda state: state.has_all(["Maintenance Key", "Flashlight Module", "Fuse"], self.player))
        set_rule(self.multiworld.get_location("10mm Ammo (Protektor Levels - STCR Dorm, 8th Floor)", self.player),
            lambda state: state.has_all(["Maintenance Key", "Flashlight Module", "Fuse"], self.player))
        set_rule(self.multiworld.get_location("Repair Spray (Protektor Levels - STCR Dorm, 8th Floor)", self.player),
            lambda state: state.has_all(["Maintenance Key", "Flashlight Module", "Fuse"], self.player))
        set_rule(self.multiworld.get_location("12mm Ammo (Protektor Levels - STCR Dorm, 8th Floor)", self.player),
            lambda state: state.has_all(["Maintenance Key", "Flashlight Module", "Fuse"], self.player))
        if self.options.ending_artifact.value:
            set_rule(self.multiworld.get_location("Key of Eternity", self.player),
                lambda state: state.has_all(["Maintenance Key", "Flashlight Module", "Fuse", "Radio Module"], self.player))
        set_rule(self.multiworld.get_location("Shotgun Rounds (Protektor Levels - KLBR Bedroom)", self.player),
            lambda state: state.has_all(["Maintenance Key", "Flashlight Module", "Fuse", "Radio Module", "Hummingbird Key"], self.player))
        set_rule(self.multiworld.get_location("Postbox Key", self.player),
            lambda state: state.has_all(["Maintenance Key", "Flashlight Module", "Fuse", "Radio Module", "Hummingbird Key"], self.player))
        set_rule(self.multiworld.get_location("Administrator's Key", self.player),
            lambda state: state.has_all(["Maintenance Key", "Flashlight Module", "Fuse", "Eagle Key"], self.player))
        set_rule(self.multiworld.get_location("Owl Key", self.player),
            lambda state: state.has_all(["Maintenance Key", "Flashlight Module", "Shutter Gate Handle"], self.player))
        set_rule(self.multiworld.get_location("Disposable Stun Prod (Protektor Levels - EULR Dorm)", self.player),
            lambda state: state.has_all(["Maintenance Key", "Owl Key"], self.player))
        set_rule(self.multiworld.get_location("Broken Music Cassette", self.player),
            lambda state: state.has_all(["Maintenance Key", "Owl Key"], self.player))
        set_rule(self.multiworld.get_location("Workshop Key", self.player),
            lambda state: state.has_all(["Maintenance Key", "Island Key", "Radio Module"], self.player))
        set_rule(self.multiworld.get_location("12mm Ammo (Protektor Levels - Workshop)", self.player),
            lambda state: state.has_all(["Maintenance Key", "Workshop Key"], self.player))
        set_rule(self.multiworld.get_location("10mm Ammo (Protektor Levels - Workshop)", self.player),
            lambda state: state.has_all(["Maintenance Key", "Workshop Key"], self.player))
        set_rule(self.multiworld.get_location("Library Key", self.player),
            lambda state: state.has_all(["Maintenance Key", "Workshop Key"], self.player))
        
        # Mines logic
        self.multiworld.get_region("Mines", self.player).connect(self.multiworld.get_region("Nowhere", self.player), None,
            lambda state: True)
        set_rule(self.multiworld.get_location("12mm Ammo (Mineshaft - STAR/EULR Room)", self.player),
            lambda state: state.has("Flashlight Module", self.player))
        set_rule(self.multiworld.get_location("10mm Ammo (Mineshaft - STAR/EULR Room)", self.player),
            lambda state: state.has("Flashlight Module", self.player))
        
        # Nowhere logic
        self.multiworld.get_region("Nowhere", self.player).connect(self.multiworld.get_region("Corrupted Installation AEON", self.player), None,
            lambda state: state.has_all(["Plate of Balance", "Plate of Eternity", "Plate of Knowledge", "Plate of Love", "Plate of Sacrifice", "Plate of Flesh", 
                                         "Radio Module"], self.player))
        set_rule(self.multiworld.get_location("Repair Spray (Nowhere - Barbwire Room #1)", self.player),
            lambda state: state.has("Flashlight Module", self.player))
        set_rule(self.multiworld.get_location("Plate of Flesh", self.player),
            lambda state: state.has("Flashlight Module", self.player))
        set_rule(self.multiworld.get_location("Rusted Key", self.player),
            lambda state: state.has("Flashlight Module", self.player))
        set_rule(self.multiworld.get_location("Serpent Ring", self.player),
            lambda state: state.has_all(["Flashlight Module", "Radio Module"], self.player))
        set_rule(self.multiworld.get_location("Shotgun Rounds (Nowhere - Dark Hall)", self.player),
            lambda state: state.has_all(["Flashlight Module", "Radio Module"], self.player))
        set_rule(self.multiworld.get_location("10mm Ammo (Nowhere - Cage Piles #2)", self.player),
            lambda state: state.has("Radio Module", self.player))
        set_rule(self.multiworld.get_location("Nitro Express Ammo (Nowhere - Cage Piles #2)", self.player),
            lambda state: state.has("Radio Module", self.player))
        set_rule(self.multiworld.get_location("Signal Flare Shells (Nowhere - Crowded Room)", self.player),
            lambda state: state.has("Radio Module", self.player))
        set_rule(self.multiworld.get_location("Small Wooden Doll", self.player),
            lambda state: state.has("Radio Module", self.player))
        set_rule(self.multiworld.get_location("Shotgun Rounds (Nowhere - Crowded Room)", self.player),
            lambda state: state.has("Radio Module", self.player))
        set_rule(self.multiworld.get_location("Repair Spray+ (Nowhere - Hummingbird Corridor)", self.player),
            lambda state: state.has("Radio Module", self.player))
        set_rule(self.multiworld.get_location("Shotgun Rounds (Nowhere - Hummingbird Corridor)", self.player),
            lambda state: state.has("Radio Module", self.player))
        set_rule(self.multiworld.get_location("Grenade Shells (Nowhere - Lamp Room)", self.player),
            lambda state: state.has("Radio Module", self.player))
        set_rule(self.multiworld.get_location("Incense", self.player),
            lambda state: state.has("Radio Module", self.player))
        set_rule(self.multiworld.get_location("Incense", self.player),
            lambda state: state.has("Radio Module", self.player))
        set_rule(self.multiworld.get_location("10mm Ammo (Nowhere - Empress Room)", self.player),
            lambda state: state.has("Radio Module", self.player))
        set_rule(self.multiworld.get_location("Plate of Balance", self.player),
            lambda state: state.has_all(["Radio Module", "Large Wooden Doll", "Wooden Doll", "Small Wooden Doll"], self.player))
        set_rule(self.multiworld.get_location("Plate of Knowledge", self.player),
            lambda state: state.has_all(["Radio Module", "Serpent Ring", "Wedding Ring", "Regent's Ring"], self.player))
        set_rule(self.multiworld.get_location("12mm Ammo (Nowhere - Interrogation Room)", self.player),
            lambda state: state.has("Rusted Key", self.player))
        set_rule(self.multiworld.get_location("Wooden Doll", self.player),
            lambda state: state.has("Rusted Key", self.player))
        set_rule(self.multiworld.get_location("Grenade Shells (Nowhere - Interrogation Room)", self.player),
            lambda state: state.has("Rusted Key", self.player))
        set_rule(self.multiworld.get_location("Repair Spray (Nowhere - Barbwire Room #2)", self.player),
            lambda state: state.has_all(["Rusted Key", "Radio Module", "Flashlight Module"], self.player))
        set_rule(self.multiworld.get_location("Plate of Sacrifice", self.player),
            lambda state: state.has_all(["Rusted Key", "Radio Module", "Flashlight Module"], self.player))
        set_rule(self.multiworld.get_location("Plate of Love", self.player),
            lambda state: state.has("Incense", self.player))
        
        # Corrupted Installation AEON logic
        self.multiworld.get_region("Corrupted Installation AEON", self.player).connect(self.multiworld.get_region("Rotfront", self.player), None,
            lambda state: state.has("Classroom Key", self.player, 2))
        
        # Rotfront logic
        self.multiworld.get_region("Rotfront", self.player).connect(self.multiworld.get_region("End", self.player), None,
            lambda state: state.has_all(["Death", "Lovers", "Moon", "Star", "Sun", "Tower", "Patient Key", "Dial Ring"], self.player))
        set_rule(self.multiworld.get_location("Developing Tank", self.player),
            lambda state: state.has("Flashlight Module", self.player))
        set_rule(self.multiworld.get_location("Repair Spray+ (Rotfront - Atrium)", self.player),
            lambda state: state.has_any(["Flashlight Module", "Handwheel"], self.player))
        set_rule(self.multiworld.get_location("Signal Flare Shells (Rotfront - Hospital Hallway)", self.player),
            lambda state: state.has_any(["Flashlight Module", "Handwheel"], self.player))
        set_rule(self.multiworld.get_location("Autoinjector (Rotfront - Hospital Room)", self.player),
            lambda state: state.has_any(["Flashlight Module", "Handwheel"], self.player))
        set_rule(self.multiworld.get_location("Store Key", self.player),
            lambda state: state.has("Blue Diskette", self.player) and state.has_any(["Flashlight Module", "Handwheel"], self.player))
        set_rule(self.multiworld.get_location("Star", self.player),
            lambda state: state.has("Blue Diskette", self.player) and state.has_any(["Flashlight Module", "Handwheel"], self.player))
        set_rule(self.multiworld.get_location("12mm Ammo (Rotfront - Garbage Chute)", self.player),
            lambda state: state.has("Handwheel", self.player))
        set_rule(self.multiworld.get_location("Blue Diskette", self.player),
            lambda state: state.has("Handwheel", self.player))
        set_rule(self.multiworld.get_location("Acetone", self.player),
            lambda state: state.has("Handwheel", self.player))
        set_rule(self.multiworld.get_location("Disposable Stun Prod (Rotfront - Meat Grinder)", self.player),
            lambda state: state.has("Handwheel", self.player))
        set_rule(self.multiworld.get_location("Repair Spray (Rotfront - Public House)", self.player),
            lambda state: state.has("Handwheel", self.player))
        set_rule(self.multiworld.get_location("8mm Ammo (Rotfront - Public House)", self.player),
            lambda state: state.has("Handwheel", self.player))
        set_rule(self.multiworld.get_location("Shotgun Rounds (Rotfront - Public House)", self.player),
            lambda state: state.has("Handwheel", self.player))    
        set_rule(self.multiworld.get_location("Tower", self.player),
            lambda state: state.has("Handwheel", self.player))
        set_rule(self.multiworld.get_location("10mm Ammo (Rotfront - Metro Platform)", self.player),
            lambda state: state.has("Handwheel", self.player))
        set_rule(self.multiworld.get_location("Disposable Stun Prod (Rotfront - Metro Platform)", self.player),
            lambda state: state.has("Handwheel", self.player))
        set_rule(self.multiworld.get_location("Repair Spray (Rotfront - Computer Store)", self.player),
            lambda state: state.has("Handwheel", self.player))
        set_rule(self.multiworld.get_location("Patient Key", self.player),
            lambda state: state.has("Handwheel", self.player))
        set_rule(self.multiworld.get_location("12mm Ammo (Rotfront - Fire Escape)", self.player),
            lambda state: state.has("Handwheel", self.player))
        set_rule(self.multiworld.get_location("Disposable Stun Prod (Rotfront - Apartment North of Alley)", self.player),
            lambda state: state.has("Handwheel", self.player))
        set_rule(self.multiworld.get_location("Repair Spray (Rotfront - Apartment North of Alley)", self.player),
            lambda state: state.has("Handwheel", self.player))
        set_rule(self.multiworld.get_location("Thermite Flare (Rotfront - Butterfly Room)", self.player),
            lambda state: state.has("Handwheel", self.player))
        set_rule(self.multiworld.get_location("Nitro Express Ammo (Rotfront - Butterfly Room)", self.player),
            lambda state: state.has("Handwheel", self.player))
        set_rule(self.multiworld.get_location("Shotgun Rounds (Rotfront - Dentist Room)", self.player),
            lambda state: state.has("Handwheel", self.player))
        set_rule(self.multiworld.get_location("Repair Patch (Rotfront - Dentist Room)", self.player),
            lambda state: state.has("Handwheel", self.player))
        set_rule(self.multiworld.get_location("Red Diskette", self.player),
            lambda state: state.has("Handwheel", self.player))
        set_rule(self.multiworld.get_location("8mm Ammo (Rotfront - Dentist Room)", self.player),
            lambda state: state.has("Handwheel", self.player))
        set_rule(self.multiworld.get_location("Moon", self.player),
            lambda state: state.has("Handwheel", self.player))
        set_rule(self.multiworld.get_location("8mm Ammo (Rotfront - Photo Store)", self.player),
            lambda state: state.has_all(["Handwheel", "Store Key"], self.player))
        set_rule(self.multiworld.get_location("Developer Fluid", self.player),
            lambda state: state.has_all(["Handwheel", "Store Key"], self.player))
        set_rule(self.multiworld.get_location("Sun", self.player),
            lambda state: state.has_all(["Handwheel", "Developer Fluid", "Developing Tank"], self.player))
        set_rule(self.multiworld.get_location("Death", self.player),
            lambda state: state.has("Handwheel", self.player))
        set_rule(self.multiworld.get_location("Autoinjector (Rotfront - Book Store)", self.player),
            lambda state: state.has("Handwheel", self.player))
        if self.options.ending_artifact.value:
            set_rule(self.multiworld.get_location("Key of Sacrifice", self.player),
                lambda state: state.has("Handwheel", self.player))
        set_rule(self.multiworld.get_location("Lovers", self.player),
            lambda state: state.has("Acetone", self.player))
        set_rule(self.multiworld.get_location("Dial", self.player),
            lambda state: state.has_all(["Death", "Lovers", "Moon", "Star", "Sun", "Tower", "Patient Key"], self.player))
        
        print(self.options.ending_artifact.value)
        if self.options.ending_artifact.value:
            self.multiworld.completion_condition[self.player] = lambda state: state.can_reach("End", "Region", self.player) and state.has_all(["Key of Love", "Key of Eternity", "Key of Sacrifice"], self.player)
        else:
            self.multiworld.completion_condition[self.player] = lambda state: state.can_reach("End", "Region", self.player)
