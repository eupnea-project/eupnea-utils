#!/usr/bin/env python3

import os
import sys
import argparse

from functions import *


# # parse arguments from the cli.
# def process_args():
#     parser = argparse.ArgumentParser()
#     parser.add_argument("-a", "--audio", action="store_true", dest="stable", default=False,
#                         help="Collect audio related logs only")
#     parser.add_argument("-h", "--hardware", action="store_true", dest="stable", default=False,
#                         help="Collect hardware related logs only")
#     return parser.parse_args()


def collect_audio_logs() -> None:
    def run_pulseaudio() -> None:
        bash("LANG=C pulseaudio -vvvv --log-time=1 > /tmp/logs-eupnea/pulseaudio_verbose.log 2>&1")

    print_status("Running alsa-info")
    with open("/tmp/logs-eupnea/alsa-info.log", "w") as f:
        f.write(bash("LANG=C alsa-info --stdout --with-aplay --with-amixer --with-alsactl --with-configs --with-devices"
                     " --with-packages"))

    print_status("Collecting pulseaudio logs")
    # get startup pulseaudio logs
    with open("/tmp/logs-eupnea/pulseaudio_startup.log", "w") as file:
        file.write(bash("systemctl --user status pulseaudio*"))
    # manually start pulseaudio and get verbose logs
    bash("systemctl --user stop pulseaudio*")
    Thread(target=run_pulseaudio, daemon=True).start()
    sleep(10)
    bash("killall pulseaudio")
    # restart pulseaudio
    bash("systemctl --user start pulseaudio")

    print_status("Collecting pipewire logs")
    try:
        with open("/tmp/logs-eupnea/pipewire.log", "w") as file:
            file.write(bash("systemctl --user status pipewire*"))
        with open("/tmp/logs-eupnea/wireplumber.log", "w") as file:
            file.write(bash("systemctl --user status wireplumber*"))
    except subprocess.CalledProcessError:
        print_error("pipewire is not installed, skipping")


def system_info() -> None:
    print_status("Collecting dmi")
    mkdir("/tmp/logs-eupnea/dmi")
    cpdir("/sys/class/dmi/id", "/tmp/logs-eupnea/dmi")

    print_status("Collecting pci devices")
    with open("/tmp/logs-eupnea/lspci.log", "w") as file:
        file.write(bash("LANG=C lspci -v"))

    print_status("Collecting kernel modules")
    with open("/tmp/logs-eupnea/lsmod.log", "w") as file:
        file.write(bash("LANG=C lsmod"))

    print_status("Collecting dmesg")
    with open("/tmp/logs-eupnea/dmesg.log", "w") as file:
        file.write(bash("LANG=C dmesg"))

    print_status("Collecting journalctl")
    with open("/tmp/logs-eupnea/journalctl.log", "w") as file:
        file.write(bash("LANG=C journalctl -b"))

    print_status("Collecting eupnea settings")
    cpfile("/etc/eupnea.json", "/tmp/logs-eupnea/eupnea-settings.log")


if __name__ == "__main__":
    if os.geteuid() == 0 and not path_exists("/tmp/username"):
        print_error("Please start the script as non-root/without sudo")
        exit(1)

    # args = process_args()

    rmdir("/tmp/logs-eupnea")
    mkdir("/tmp/logs-eupnea", create_parents=True)

    # pa logs need to be collected as user
    print_header("Collecting audio related logs")
    collect_audio_logs()

    # Restart script as root
    if not os.geteuid() == 0:
        # save username
        with open("/tmp/username", "w") as file:
            file.write(bash("whoami").strip())  # get non root username. os.getlogin() seems to fail in chroots
        sudo_args = ['sudo', sys.executable] + sys.argv + [os.environ]
        os.execlpe('sudo', *sudo_args)

    # read username
    with open("/tmp/username", "r") as file:
        user_id = file.read()
    rmfile("/tmp/username")

    print_header("Collecting hardware related logs")
    system_info()

    print_header("Packing logs")
    os.chdir("/tmp/logs-eupnea")
    bash("tar -czf ../eupnea-logs.tar.gz ./")
    cpfile("/tmp/eupnea-logs.tar.gz", f"/home/{user_id}/Downloads/eupnea-logs.tar.gz")
