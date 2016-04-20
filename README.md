# freshdesk_backup
Backup for freshdesk.com
Script use freshdesk API to create local sqlite database with:
- Contacts
- Companies
- Groups
- Tickets
- Conversations

To use script you must enter API and freshdesk url in app.py

###Usage:
```
virtualenv -p /usr/bin/python3 venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```
