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
cd ~ && python ~/db/util/init_api_db.py