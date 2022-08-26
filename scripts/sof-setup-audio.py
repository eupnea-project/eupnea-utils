#!/usr/bin/env python3

import argparse
import os
import subprocess as sp
from pathlib import Path
import urllib.request


def process_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--no-pulseaudio", "--no-pa",
        action="store_true",
        dest="no_pa",
        default=False,
        help="Do not install pulseaudio"
    )
    parser.add_argument(
        "--offline", "--local-files",
        action="store_true",
        dest="local_files",
        default=False,
        help="Use local files instead of downloading from github"
    )
    return parser.parse_args()


def download_files():
    print("Removing old configs")
    sp.run(["sudo", "rm", "-rf", str(Path.home()) + "/.config/eupnea/audio"])
    sp.run(["mkdir", "-p", str(Path.home()) + "/.config/eupnea/audio"])
    print("Downloading files from github")
    path = str(Path.home()) + "/.config/eupnea/audio/"


def install_pa():
    print("Installing pulseaudio")
    print("Writing alsa-reload")
    print("Removing old files")
    sp.run(["sudo", "rm", "-f", "/etc/systemd/system/alsa-reload.service"])
    sp.run(["sudo", "rm", "-f", "/etc/pulse/default.pa"])
    sp.run(["sudo", "rm", "-f", "/lib/firmware/intel/sof*"])
    sp.run(["sudo", "rm", "-f", "/etc/modprobe.d/alsa-breath.conf"])
    # Not sure if this one is needed
    # sp.run(["sudo", "rm", "-f", "/etc/asound.conf"])


if __name__ == "__main__":
    print("Processing args")
    args = process_args()
    if not args.local_files:
        download_files()
# if not args.no_pa:
#     install_pa()
