# Simple chat

## To run this project follow next steps.

1. Install Python 3.10. You can do it here https://www.python.org/downloads/
2. Set Up a Virtual Environment
```
# Install virtualenv if it's not installed
pip install virtualenv

# Create a virtual environment
virtualenv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate

# On Unix or MacOS
source venv/bin/activate
```
3. Install requirements
```
pip install -r requirements.txt
```
4. Create simple_chat/settings/local.py
```
from .main import *


SECRET_KEY = 'secret-key'
```
5. Run migration or load a db dump
```
# Run migrations to set up the database schema
python manage.py migrate

# Alternatively, load a database dump if available (make sure the dump file path is correct)
sqlite3 simple_chat/db.sqlite3 < simple_chat_dump.sql
```
6. Run the server
```
python manage.py runserver 8000
```