#! /bin/bash

# get global-bundle.pem for docdb
cd ~ && wget https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem &&

	# setup postgres
	bash ~/db/setup_scripts/setup_postgres.sh &&

	# Copy `celery.service` and `test.service` to `/etc/systemd/system`
	sudo cp ~/db/systemd/celery.service ~/db/systemd/test.service /etc/systemd/system &&
	sudo systemctl daemon-reload &&

	# Give permissions for backend server and celery start scripts for use by systemd
	sudo chmod +x /home/ubuntu/db/util/start_server.sh &&
	sudo chmod +x /home/ubuntu/db/util/start_celery.sh &&

	# Configure nginx
	sudo cp ~/db/nginx/default /etc/nginx/sites-enabled &&
	sudo cp ~/db/nginx/nginx.conf /etc/nginx &&
	sudo systemctl reload nginx

# initialize api key db; add first generated API key to .env (additional API key changes must be manual)
# cd ~ && python ~/db/util/init_api_db.py

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
sudo cp ~/db/ui/dist/assets /var/www/html &&
	sudo cp ~/db/ui/dist/index.html /var/www/html &&
	sudo cp ~/db/ui/public/favicon.ico /var/www/html &&
	echo "build files replaced."

# start the server / celery
sudo systemctl start test.service
sudo systemctl start celery.service
