#!/bin/bash

# This script is called on reboot after installing a new kernel

sudo dnf remove -y eupnea-*-kernel || true # this will fail as the wildcard will catch the booted kernel
