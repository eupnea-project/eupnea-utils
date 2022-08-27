#!/usr/bin/env python3

import argparse
from pathlib import Path
import os
import sys
import shutil


def process_args():
    print("\033[95m" + "Processing args" + "\033[0m")
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', default="v2.2.x", help="Sof version to install, default: v2.2.x")
    parser.add_argument("--no-pulseaudio", "--no-pa", action="store_true", dest="no_pa", default=False,
                        help="Only install alsa")
    parser.add_argument("--offline", "--local-files", action="store_true", dest="local_files", default=False,
                        help="Use local files instead of downloading from github")
    return parser.parse_args()


def download_files() -> None:
    print("\033[94m" + "Removing old files" + "\033[0m")
    os.rmdir(home_path)
    os.rmdir("/tmp/eupnea-audio")
    os.rmdir("/tmp/sof-audio")
    Path(home_path).mkdir(parents=True, exist_ok=True)
    print("\033[94m" + "Downloading files from github" + "\033[0m")
    os.system("git clone --depth 1 https://github.com/eupnea-linux/python-scripts /tmp/eupnea-audio")
    os.system("git clone --depth 1 https://github.com/thesofproject/sof-bin /tmp/sof-audio")
    print("\033[94m" + "Copying files from tmp" + "\033[0m")
    shutil.copytree("cp /tmp/eupnea-audio/configs/", home_path, dirs_exist_ok=True)


def install_pa(local_files: bool, sof_version) -> None:
    if sof_version is None:
        sof_version = "v2.2.x"
    print("\033[95m" + "Installing pulseaudio" + "\033[0m")
    print("\033[94m" + "Removing old files" + "\033[0m")
    os.remove("/etc/systemd/system/alsa-reload.service")
    os.remove("/etc/pulse/default.pa")
    os.remove("/etc/modprobe.d/alsa-breath.conf")
    os.remove("/etc/asound.conf")
    if not local_files:
        # remove all old sof folders + files
        for directory in Path("/lib/firmware/intel/").glob("sof*"):
            try:
                directory.rmdir()
            except NotADirectoryError:
                directory.unlink()
        print("\033[95m" + "Installing sof-audio" + "\033[0m")
        shutil.copytree("/tmp/sof-audio/" + sof_version + "/sof", "/lib/firmware/intel/sof")
        shutil.copytree("/tmp/sof-audio/" + sof_version + "/sof-tplg", "/lib/firmware/intel/sof-tplg")
        shutil.copytree("/tmp/sof-audio/" + sof_version + "/tools" + sof_version[:sof_version.rfind(".")],
                        "/usr/local/bin/")
    print("\033[94m" + "Installing audio services" + "\033[0m")
    shutil.copyfile(home_path + "alsa-reload.service", "/etc/systemd/system/")
    os.system("sudo systemctl enable alsa-reload")
    print("\033[94m" + "Copying pa config" + "\033[0m")
    shutil.copyfile(home_path + "default.pa", "/etc/pulse/")
    print("\033[94m" + "Blacklising old drivers" + "\033[0m")
    shutil.copyfile(home_path + "alsa-breath.conf", "/etc/modprobe.d/")
    print("\033[94m" + "Copying asound.conf" + "\033[0m")
    shutil.copyfile(home_path + "asound.conf", "/etc/")


if __name__ == "__main__":
    # Elevate script to root
    if os.geteuid() != 0:
        with open("/tmp/eupnea-path", "w") as file:
            file.write(str(Path.home()) + "/.config/eupnea/audio")
        args = ['sudo', sys.executable] + sys.argv + [os.environ]
        os.execlpe('sudo', *args)
    try:
        with open("/tmp/eupnea-path", "r") as file:
            home_path = file.read()
    except FileNotFoundError:
        print('\033[91m' + "Please start script without sudo!")
        exit()
    args = process_args()
    if not args.local_files:
        download_files()
    if not args.no_pa:
        install_pa(args.local_files, args.version)
