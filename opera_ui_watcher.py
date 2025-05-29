import os
import json
import subprocess
import time

# Function to check if Opera GX is running
def is_opera_running():
    try:
        output = subprocess.check_output('tasklist', shell=True).decode()
        return "opera.exe" in output.lower()
    except Exception:
        return False

# Function to kill Opera GX
def kill_opera():
    try:
        subprocess.call("taskkill /f /im opera.exe", shell=True)
        print("Opera GX was running and has been closed.")
        time.sleep(2)
    except Exception as e:
        print(f"Failed to close Opera GX: {e}")

# Function to launch Opera GX
def launch_opera():
    opera_path = os.path.join(
        os.environ["USERPROFILE"],
        "AppData",
        "Local",  # Opera GX is usually installed under Local
        "Programs",
        "Opera GX",
        "launcher.exe"
    )
    if os.path.exists(opera_path):
        subprocess.Popen([opera_path])
        print("Opera GX has been launched.")
    else:
        print("Could not find Opera GX launcher. Please start it manually.")

# Main logic
user_profile = os.environ["USERPROFILE"]
local_state_path = os.path.join(
    user_profile,
    "AppData",
    "Roaming",  # If this fails, try changing to "Local"
    "Opera Software",
    "Opera GX Stable",
    "Local State"
)

# Close Opera GX if running
if is_opera_running():
    kill_opera()

# Edit the config
if not os.path.exists(local_state_path):
    print("Local State file not found. Make sure Opera GX is installed.")
else:
    try:
        with open(local_state_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if "gxx_flags" in data:
            data["gxx_flags"]["enabled"] = False
            data["gxx_flags"]["migrated"] = True
        else:
            data["gxx_flags"] = {"enabled": False, "migrated": True}

        with open(local_state_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)

        print("Old UI has been restored.")
        launch_opera()
    except Exception as e:
        print(f"Error while editing the file: {e}")
