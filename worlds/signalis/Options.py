from Options import Toggle, Choice, PerGameCommonOptions
from dataclasses import dataclass

class ArtifactEnding(Toggle):
    """Set goal to Artifact ending?"""
    display_name = "Goal is Artifact ending"
    default = 0

class Difficulty(Choice):
    """What difficulty do you wish to play on?"""
    display_name = "Difficulty"
    option_casual = 0
    option_normal = 1
    option_survival = 2 
    default = 1

class DeathLink(Toggle):
    """Turn on deathlink?"""
    display_name = "Deathlink"
    default = 0

class EarlyBK(Toggle):
    """Randomize the items needed to get to the first Save Room?"""
    display_name = "Early BK"
    default = 0

@dataclass
class SignalisOptions(PerGameCommonOptions):
     ending_artifact: ArtifactEnding
     deathlink: DeathLink
     early_bk: EarlyBK
    