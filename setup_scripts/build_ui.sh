#! /bin/bash

# build front end
cd ~/db/ui && npm run build &&

# delete old build files
if [[ -e /var/www/html/index.html && -d /var/www/html/assets ]]; then
  read -p "Are you sure you want to delete 'assets' and 'index.html' from '/var/www/html'? (y/n): " confirm
  if [[ $confirm == [yY] ]]; then
    sudo rm -rf /var/www/html/assets &&
    sudo rm /var/www/html/index.html
    echo "old build files removed."
  fi
fi

# move build files
sudo mv ~/db/ui/dist/assets /var/www/html &&
sudo mv ~/db/ui/dist/index.html /var/www/html &&
sudo cp ~/db/ui/public/favicon.ico /var/www/html &&
echo "build files replaced."