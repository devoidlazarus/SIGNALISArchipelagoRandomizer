from Options import Toggle, PerGameCommonOptions
from dataclasses import dataclass

class ArtifactEnding(Toggle):
    """Set goal to Artifact ending?"""
    display_name = "Goal is Artifact ending"
    default = 0

class DeathLink(Toggle):
    """Turn on deathlink?"""
    display_name = "Deathlink"
    default = 0

@dataclass
class SignalisOptions(PerGameCommonOptions):
     ending_artifact: ArtifactEnding
     deathlink: DeathLink
    