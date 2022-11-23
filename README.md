# Eupnea-scipts

Various post install scripts for eupnea, written in python. Run `scriptname --help` to see all available cli options for each script.

### Collect-logs

Useful for quickly gathering all needed logs for debugging audio and other issues.

1. Collects logs about hardware and audio.
2. Manually runs pipewire/pulseaudio
3. Creates a tar with all logs

### postinstall

Runs on first boot and after eupnea scripts updates. It will:

* Resize the root partition to fill the SD card if the image option was chosen in depthboot or running EupneaOS.
* Set a hostname based on the board name
* Applies some device specific fixes, i.e. touchscreen fixes, except **audio** fixes. (Those are done in the audio
  script)

### install-ectool

Compiles the ectool locally to control fans and other chromebook specific hardware.  
Currently broken.

### install-to-internal

Installs EupneaOS/Depthboot to internal storage. Uses rsync to copy files.

### manage-kernels

Kernel manage script. Has the following features:

* Update current kernel to the latest version. Automatically triggered by eupnea-update every 24 hours.
* Switch to a different kernel type
* Backup current kernel
* Restore backed up kernel

### modify-cmdline

Modify the kernel command line. Can also restore a stock config. Backs up the kernel to the second kernel partition
automatically.

### setup-zram

Guides the user through a zram setup.  
Not yet finished.

### update-scripts

Updates the scripts to the latest version. Automatically triggered by eupnea-update every 24 hours.
