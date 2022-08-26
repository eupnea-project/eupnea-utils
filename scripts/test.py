import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    '-v', '--version',
    default="v2.2.x",
    help="Sof version to install, default: v2.2.x"
)
parser.add_argument(
    "--no-pulseaudio", "--no-pa",
    action="store_true",
    dest="no_pa",
    default=False,
    help="Only install alsa"
)
parser.add_argument(
    "--offline", "--local-files",
    action="store_true",
    dest="local_files",
    default=False,
    help="Use local files instead of downloading from github"
)
print("\033[0m" + str(parser.parse_args()))
