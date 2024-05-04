import os
import subprocess
import logging

def setup_logger(log_file):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger

def get_screen_resolution(file_path):
    width = None
    height = None
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in reversed(lines):
            if "Requested resolution" in line:
                resolution = line.split(": ")[1].strip()
                width, height = map(int, resolution.split("x"))
                break
    
    return width, height

def find_resolution(width, height):
    resolutions = {
        (800, 600): 0,
        (1024, 768): 1,
        (1152, 864): 2,
        (1280, 720): 3,
        (1280, 800): 4,
        (1280, 960): 5,
        (1280, 1024): 6,
        (1360, 768): 7,
        (1366, 768): 8,
        (1400, 1050): 9,
        (1440, 900): 10,
        (1440, 1152): 11,
        (1600, 720): 12,
        (1600, 900): 13,
        (1600, 1024): 14,
        (1600, 1200): 15,
        (1680, 1050): 16,
        (1800, 1168): 17,
        (1920, 864): 18,
        (1920, 1080): 19,
        (1920, 1200): 20
    }
    return resolutions.get((width, height))

def update_config_resolution(file_path, selected_resolution):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        for i, line in enumerate(lines):
            if 'r_mode' in line:
                lines[i] = 'r_mode "{}"\n'.format(selected_resolution)
                break

        with open(file_path, 'w') as file:
            file.writelines(lines)

        logger.info("Value of r_mode in the file successfully changed to %s", selected_resolution)
    except FileNotFoundError:
        logger.error("Error: Config file not found.")
    except Exception as e:
        logger.error("An error occurred: %s", e)

if __name__ == "__main__":
    file_path = r'C:\Users\user\boosteroid-experience\logs\ResolutionHelperLog.txt'
    log_file = r'C:\Users\user\boosteroid-experience\logs\steam\the_evil_within_res.txt'
    logger = setup_logger(log_file)

    width, height = get_screen_resolution(file_path)
    selected_resolution = find_resolution(width, height)

    if selected_resolution is not None:
        logger.info("Current resolution: %s x %s", width, height)
        logger.info("Selected resolution from the list: %s", selected_resolution)

        file_path_steam = r"C:\Users\user\Saved Games\TangoGameworks\The Evil Within\base\the evil withinConfig.cfg"
        if os.path.exists(file_path_steam):
            update_config_resolution(file_path_steam, selected_resolution)
        else:
            logger.error("Error: Config file STEAM not found.")

    else:
        logger.error("Current resolution not found in the list.")

    steam_exe_path = r'C:\Program Files (x86)\Steam\steam.exe'

    app_id = "268050"

    command = f'"{steam_exe_path}" -applaunch {app_id} +set r_mode {selected_resolution}'

    subprocess.run(command, shell=True)
