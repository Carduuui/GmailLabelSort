import os.path
from google.oauth2.credentials import Credentials 
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']


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

    search_terms = [
        'Bewerbung',
        '"Duales Studium"',
        'Onlinetest',
        'Online-Test',
        '"Online Test"',
        'Interview'
    ]

    all_message_ids = set()

    timeFilter = ""

    print("1: Letzte 7 Tage aktualisieren")
    print("2: 100 Emails aktualisieren")

    inputEingabe = input('Zahl eingeben:')

    if inputEingabe == "1":
        timeFilter = " newer_than:7d"
    else:
        print("normale 100 emails")

    for term in search_terms:
        try:
            query = term + timeFilter
            result = service.users().messages().list(userId='me', q=query).execute()
            messages = result.get('messages', [])
            for msg in messages:
                all_message_ids.add(msg['id'])
            print(f"Suchbegriff '{term}': {len(messages)} E-Mails gefunden")
        except Exception as e:
            print(f"Fehler bei Suchbegriff '{term}': {e}")

        print(f"\nInsgesamt {len(all_message_ids)} eindeutige E-Mails gefunden")

        if not all_message_ids:
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
        label_object = {
            'name': label_name,
            'labelListVisibility': 'labelShow',
            'messageListVisibility': 'show'
        }
        created_label = service.users().labels().create(userId='me', body=label_object).execute()
        label_id = created_label['id']
        print(f"Label '{label_name}' wurde automatisch erstellt")

    labeled_count = 0
    for msg_id in all_message_ids:
        try:
            service.users().messages().modify(
                userId='me',
                id=msg_id,
                body={'addLabelIds': [label_id]}
            ).execute()
            labeled_count += 1
        except Exception as e:
            print(f"Fehler beim Labeln der Nachricht {msg_id}: {e}")

    print(f"{labeled_count} E-Mails wurden mit dem Label '{label_name}' versehen")

if __name__ == '__main__':
    main()    
