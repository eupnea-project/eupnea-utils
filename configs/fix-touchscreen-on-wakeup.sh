#!/bin/bash

if [ "$1" == "pre" ]; then
  echo "Fixing touchscreen on wakeup from sleep"
  bash /usr/lib/eupnea/fix-touchscreen.sh
fi
