# Eupnea-scipts

Various scripts for eupnea, written in python. Run `scriptname --help` to see all available cli options for
each script.
These scripts are packaged as eupnea-scripts in the repo GitHub repositories:

* [Ubuntu/Pop!_OS](https://github.com/eupnea-linux/apt-repo)
* [Fedora](https://github.com/eupnea-linux/rpm-repo)
* [Arch](https://github.com/eupnea-linux/arch-repo)

There are two types of scripts:

* user-scripts(installed to /usr/bin): scripts that can be run by the user
* system-scripts(installed to /usr/lib/eupnea): scripts that are not designed to be run by the user directly

## User scripts

### collect-logs

Useful for quickly gathering all needed logs for debugging audio and other issues.

1. Collects logs about hardware and audio.
2. Manually runs pipewire/pulseaudio
3. Creates a tar with all logs

### install-to-internal

Installs EupneaOS/Depthboot to internal storage. Uses rsync to copy files.
Will become a system script once the gui apps are finished.

### modify-cmdline

Modify the kernel command line. Can also restore a stock config. Backs up the kernel to the second kernel partition
automatically.

## System scripts

### install-kernel

Used by kernel packages to flash new kernels.

### modify-packages

Sometimes the system update script needs to install/remove a package from a eupnea system. This is not possible from
within a postinstall script of a package, as its run while the package is installed -> lock files prevent the package
manager from running. Therefore, a systemd updater script is run, which will wait for the package-manager to finish and
then re/install/remove the necessary packages.

### postinstall

Runs on first boot. It will:

* Resize the root partition to fill the whole drive.
* Set a hostname based on the board name.
* Applies some device specific fixes, i.e. touchscreen fixes, except **audio** fixes. (Those are done in the audio
  script)

### update-scripts

Old manual scripts updater. Only included for legacy reasons. Not needed anymore due to the switch to packages in v1.1.