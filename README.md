# IE-Website

## Install components
```bash
sudo apt-get update
sudo apt-get install python-pip 
```

### Setting up Virtual Environment and Install Requirements
```bash
sudo pip install virtualenv
python3 -m venv myvenv
source myvenv/bin/activate
pip install -r requirements-local.txt
```

### Running the website locally
```bash
Update settings.py:
  1. Make DEBUG = True
  2. In DATABASES option , uncomment the commented and comment the uncomment 
cd ~/ie-website
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

