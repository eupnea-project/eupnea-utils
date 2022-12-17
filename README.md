# Eupnea-scipts

Various post install scripts for eupnea, written in python. Run `scriptname --help` to see all available cli options for
each script.
The scripts are sorted into 2 folders.

* user-scripts: scripts that can be run by the user
* system-scripts: scripts that are not designed to be run by the user

### collect-logs

Useful for quickly gathering all needed logs for debugging audio and other issues.

1. Collects logs about hardware and audio.
2. Manually runs pipewire/pulseaudio
3. Creates a tar with all logs

### eupnea-postinstall

Runs on first boot and after eupnea scripts updates. It will:

* Resize the root partition to fill the SD card if the image option was chosen in depthboot or running EupneaOS.
* Set a hostname based on the board name
* Applies some device specific fixes, i.e. touchscreen fixes, except **audio** fixes. (Those are done in the audio
  script)

### install-to-internal

Installs EupneaOS/Depthboot to internal storage. Uses rsync to copy files.

### manage-kernels

Kernel manager script. Has the following features:

* Update current kernel to the latest version. Automatically triggered by eupnea-update every 24 hours.
* Switch to a different kernel type
* Backup current kernel
* Restore backed up kernel

### modify-cmdline

Modify the kernel command line. Can also restore a stock config. Backs up the kernel to the second kernel partition
automatically.

### update-scripts

Old manual scripts updater. Only included for legacy reasons. Use packages instead:

* [Debian/Ubuntu/Pop!_OS](https://github.com/eupnea-linux/apt-repo)
* [Fedora](https://github.com/eupnea-linux/rpm-repo)
* [Arch](https://github.com/eupnea-linux/arch-repo)