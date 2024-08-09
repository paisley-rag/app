#! /bin/bash

sudo rm -rf /var/www/html/assets
sudo rm /var/www/html/index.html
sudo rm /var/www/html/vite.svg

sudo cp -r ~/ui/dist/. /var/www/html
