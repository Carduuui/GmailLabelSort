import os.path
from google.oauth2.credentials import Credentials 
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

print("funktioniert")

def main():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail' , 'v1', credentials=creds)

    query = 'from:recruiting@enbw.com'
    result = service.users().messages().list(userId='me', q=query).execute()
    messages = result.get('messages', [])

    if not messages:
        print("Keine passenden Nachrichten gefunden.")
        return

    label_name = "Bewerbung"
    label_id = None
    labels = service.users().labels().list(userId='me').execute().get('labels', [])

    for label in labels:
        if label['name'].lower() == label_name.lower():
            label_id = label['id']
            break
            

    if not label_id:
        print(f'Label "{label_name}" nicht gefunden. Bitte in Gmail manuell anlegen')
        return

    for msg in messages:
        msg_id = msg['id']
        service.users().messages().modify(
            userId = 'me',
            id=msg_id,
            body={'addLabelIds': [label_id]}
        ).execute()

    print(f"{len(messages)} E-Mails wurden mit dem Label '{label_name}' versehen")

if __name__ == '__main__':
    main()    
