# systemd files

- `test.service` needs to go in `/etc/systemd/system/`
- `celery.service` needs to go in `/etc/systemd/system/`

If any changes are made to the above files, reload them using
`sudo systemctl daemon-reload`