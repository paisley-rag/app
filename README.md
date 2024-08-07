# Evals notes

Sets up Python3, pip, pipenv, git, and clones the repo\
Installs the necessary packages\
Sets up a local postgres db\
Runs the evals.py file



## Steps to set up brand new EC2 instance:
```
sudo apt-get install python3
sudo apt install -y git
git clone https://github.com/2405-team3/db
sudo apt install python3-pip -y
sudo apt install pipenv
cd db
pipenv --python /usr/bin/python3
pipenv install
```
```
git checkout eval
pipenv shell
```
```
pipenv install
bash setup_postgres.sh
```
[ create and populate .env with PG_USER=paisley, PG_PASSWORD=paisley_rules, PG_DATABASE=paisley_evals, OPENAI_API_KEY=... ]
```
python3 evals.py
```

- Test Edit
