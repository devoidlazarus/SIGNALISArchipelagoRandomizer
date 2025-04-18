# SIGNALIS Archipelago Randomizer Setup Guide

### Setup requirements
 - A legally-obtained copy of SIGNALIS
	 - Only the Steam version has been tested
 - [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases) version 0.5.0 or higher
	 - Please consult the [Archipelago Setup Guide](https://archipelago.gg/tutorial/) for instructions on how to install Archipelago
 - [MelonLoader](https://github.com/LavaGang/MelonLoader) version 0.5.7
 - The latest `ArchipelagoSignalis.zip`, `Signalis.yaml`, and `signalis.apworld` files from the [Releases page](https://github.com/devoidlazarus/SIGNALISArchipelagoRandomizer/releases)


### Mod installation steps
1. Launch SIGNALIS at least once after installing it in order to setup the necessary game files, then close it after it loads into the main menu
2. Download MelonLoader 0.5.7 and open `MelonLoader.Installer.exe`
3. When prompted for a game executable during MelonLoader installation, locate your `signalis.exe` file
   - Default location for a Steam installation of SIGNALIS is `C:\Program Files (x86)\Steam\steamapps\common\SIGNALIS`
4. After MelonLoader is finished installing, open SIGNALIS again to let MelonLoader setup the required mod support files. You can close the game again after it loads into the main menu
5. Copy the `ArchipelagoSignalis.dll` and `Archipelago.MultiClient.Net.dll` files you downloaded and paste them into the newly-created `Mods` folder located in your SIGNALIS installation directory
6. Launch SIGNALIS
7. Open the Settings menu and select Enter Archipelago Connection
8. Enter your Archipelago slot name, server, and port information
   - It is a known issue at the moment that you cannot see the cursor when entering your Archipelago connection settings. Please use the `Tab` key to select different fields of the form
9. Select Done
   - If you cannot locate your cursor to select Done, hold down `Alt` and press `Tab` to exit the game window momentarily, line up your visible cursor with where the Done button would be, press `Tab` until the SIGNALIS window is selected, and then release `Alt`
10. Exit the Settings menu
11. Select Continue
    - If you have no existing save files, skip to step 15
12. Select Begin Anew

Any time you launch SIGNALIS to play an existing randomized save file, repeat steps #9-15 to successfully load into your save and connect to Archipelago.

### Generating and hosting an Archipelago seed
Please consult the [Archipelago generation guide](https://archipelago.gg/tutorial/Archipelago/setup/en#generating-a-game) for general instructions on how to generate a random seed for the SIGNALIS mod to read and follow.

To generate a game with SIGNALIS in it, follow the steps below:

 1. Copy the `signalis.apworld` file you downloaded into the `\lib\worlds` folder in your Archipelago installation directory
    - Default location: `C:\ProgramData\Archipelago\lib\worlds`
 2. Edit the `Signalis.yaml` file that you downloaded to match your game preferences (setting difficulty, setting the Artifact ending as your win condition, etc.)
 3. Save the changes made to your `Signalis.yaml` file and copy this file into the `Players` folder in your Archipelago installation
    - Default location: `C:\ProgramData\Archipelago\Players`
 4. Open the Archipelago Launcher
 5. Select Generate and let the process run. When the terminal window closes, generation has finished
 6. Upload the newly-created`AP_#######.zip` file from the `output` folder to [the Archipelago website](https://archipelago.gg/uploads) to host the game.
    - Default location: `C:\ProgramData\Archipelago\output`

