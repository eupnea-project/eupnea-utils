#!/bin/bash

# This script is called on reboot after installing a new kernel

# one of the following commands will fail due to dnf preventing the removal of the currently running kernel
# this is fine, we just want to remove the other kernel
sudo dnf remove -y eupnea-mainline-kernel || true
sudo dnf remove -y eupnea-chromeos-kernel || true

# delete systemd service
rm /usr/lib/systemd/system/eupnea-kernel-autoremove.service
