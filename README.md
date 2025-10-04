# GmailLabelSort
It sorts your Emails by setting Labels, based on your configuration 
of the script.
## Setup
### Code
Change the Variable at line 73 to your need. The Label the Email gets and
the key words it should filter for.
### Google Clound Console
Create a OAuth 2.0 Desktop Client and add a Testuser
### Packages
Create a virtual enviroment
```bash
python3 -m venv venv
```
activate virtual enviroment
- Windows
```bash
venv\Scripts\acivate
```
- Linux/Mac
```bash
source venv/bin/activate
```
install Packages
```bash
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
```
## Run
```bash
python label_sortierer.py
```
