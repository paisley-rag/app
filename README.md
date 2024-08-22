# Paisley

The backend server needs to be started along with a celery worker used to handle background tasks within the query route. See below.

Start both services:
`sudo systemctl start test.service`
`sudo systemctl start celery.service`

Stop both services:
`sudo systemctl stop test.service`
`sudo systemctl stop celery.service`

Recent logs for either service:
`sudo systemctl status test.service`
`sudo systemctl status celery.service`

Full logs for either service:
`journalctl -u test.service` 
`journalctl -u celery.service` 



Run backend server with logs in console:
`cd ~/db && pipenv shell`
`cd ~ && python -m db.server`

Run celery worker with logs in console:
`sudo -u ubuntu /home/ubuntu/.local/share/virtualenvs/db-grdQ2Ybz/bin/celery -A db.celery.tasks worker -l info`