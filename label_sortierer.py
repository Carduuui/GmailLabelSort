import os.path
from google.oauth2.credentials import Credentials 
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def get_or_create_label(service, label_name):
    labels = service.users().labels().list(userId='me').execute().get('labels', [])

    for label in labels:
        if label['name'].lower() == label_name.lower():
            return label['id']
    
    label_object = {
        'name': label_name,
        'labelListVisibility': 'labelShow',
        'messageListVisibility': 'show'
    }
    created_label = service.users().labels().create(userId='me', body=label_object)
    print(f"Label '{label_name}' wurde automatisch erstellt")
    return created_label['id']

def search_and_label_emails(service, search_terms, label_name, time_filter):
    message_ids = set()

    for term in search_terms:
        try:
            query = term + time_filter
            result = service.users().messages().list(userId='me', q=query).execute()
            messages = result.get('messages', [])
            for msg in messages:
                message_ids.add(msg['id'])
            print(f"'{label_name}' - Suchbegriff '{term}': {len(messages)} E-Mails gefunden")
        except Exception as e:
            print(f"'{label_name}' - Fehler bei Suchbegriff '{term}': {e}.")
        
    if not message_ids:
        print(f"'{label_name}' - Keine passenden Nachrichtn gefunden.")
        return 0

    label_id = get_or_create_label(service, label_name)

    labeled_count = 0
    for msg_id in message_ids:
        try:
            service.users().messages().modify(
                userId='me',
                id=msg_id,
                body={'addLabelIds': [label_id]}
            ).execute()
            labeled_count += 1
        except Exception as e:
            print(f"'{label_name}' - Fehler beim Labeln der Nachricht {msg_id}: {e}")

    print(f"'{label_name}' - {labeled_count} E-Mails wurden gelabelt")
    return labeled_count

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

    categories = {
        'Bewerbung': [
            'Bewerbung',
            '"Duales Studium"',
            'Onlinetest',
            'Online-Test',
            '"Online Test"',
            'Interview',
            '"Assessment Center'
        ],
        'Booking':[
            '"Booking.com"'
        ],
        'Online Bestellung':[
            '"Lieferando"'
        ]
    }

    print("1: Letzte 7 Tage aktualisieren")
    print("2: 100 Emails aktualisieren")

    inputEingabe = input('Zahl eingeben:')

    if inputEingabe == "1":
        time_filter = " newer_than:7d"
    else:
        time_filter = "older_than:3650d"
        print("normale 100 emails")

    total_labeled = 0
    for label_name, search_terms in categories.items():
        print(f"\n=== Verarbeite Kategorie: {label_name} ===")
        labeled_count = search_and_label_emails(service, search_terms, label_name, time_filter)
        total_labeled += labeled_count

    print(f"\n=== ZUSAMMENFASSUNG ===")
    print(f"Insgesamt {total_labeled} E-Mails wurden gelabelt")

if __name__ == '__main__':
    main()    
