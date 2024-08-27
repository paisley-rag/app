#! /bin/bash

# get global-bundle.pem for docdb
cd ~ && wget https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem &&

# setup postgres
bash ~/db/setup_scripts/setup_postgres.sh &&

# Copy `celery.service` and `test.service` to `/etc/systemd/system`
sudo cp ~/db/systemd/celery.service ~/db/systemd/test.service /etc/systemd/system && 
sudo systemctl daemon-reload && 

# Start backend server
sudo chmod +x /home/ubuntu/db/util/start_server.sh &&
sudo systemctl start test.service &&

# Start celery background processing (used for evaluations)
sudo chmod +x /home/ubuntu/db/util/start_celery.sh &&
sudo systemctl start celery.service &&

# Configure nginx
sudo cp ~/db/nginx/default /etc/nginx/sites-enabled &&
sudo cp ~/db/nginx/nginx.conf /etc/nginx &&
sudo systemctl reload nginx
