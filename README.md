# Paisley

The backend server needs to be started along with a celery worker used to handle background tasks within the query route. See below.

Start/stop backend server:
`sudo systemctl start test.service`
`sudo systemctl stop test.service`

Check backend server logs:
`sudo systemctl status test.service`

Run backend server with logs in console:
`cd ~/db && pipenv shell`
`cd ~ && python -m db.server`


Start/stop Celery worker for background tasks:
`sudo systemctl start celery.service`
`sudo systemctl stop celery.service`

Run celery worker with logs in console:
`sudo -u ubuntu /home/ubuntu/.local/share/virtualenvs/db-grdQ2Ybz/bin/celery -A db.celery.tasks worker -l info`