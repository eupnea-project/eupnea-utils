#!/bin/bash

if [ "$1" == "post" ]; then
  echo "Fixing touchscreen on wakeup from sleep"
  bash /usr/lib/eupnea/fix-touchscreen.sh
fi
