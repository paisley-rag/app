#! /bin/bash

# these commands are used to "reset" systemd after making changes to the unit file (e.g., test.service)
# sudo systemctl stop test.service

sudo systemctl daemon-reload
sudo systemctl enable test.service
sudo systemctl start test.service
systemctl status test.service
