from __future__ import print_function
import httplib2
import os
from email.mime.text import MIMEText
import base64

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.send'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Auto-emailer'

def send_email(to, subject, body):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    m = MIMEText(body)
    # add the to field of the message
    m['to'] = to
    # add the from field of the message
    m['from'] = 'pdmxdd@gmail.com'
    # add the subject field of the message
    m['subject'] = subject
    # Encode your MIMEText object as bytes and decode it as 'utf-8'
    raw = base64.urlsafe_b64encode(m.as_bytes()).decode('utf-8')
    # body of the message is a dictionary mapped to 'raw' is the MIMEText object that was decoded, and re-encoded
    body = {'raw': raw}
    # Create a messages object from your service object
    messages = service.users().messages()
    # create and send your message using your messages object, and .execute()
    message = messages.send(userId='me', body=body).execute()



def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    # create a MIMEText object, that contains the body of the message
    m = MIMEText('this is a test')
    # add the to field of the message
    m['to'] = 'paul@launchcode.org'
    # add the from field of the message
    m['from'] = 'pdmxdd@gmail.com'
    # add the subject field of the message
    m['subject'] = 'TEST'
    # Encode your MIMEText object as bytes and decode it as 'utf-8'
    raw = base64.urlsafe_b64encode(m.as_bytes()).decode('utf-8')
    # body of the message is a dictionary mapped to 'raw' is the MIMEText object that was decoded, and re-encoded
    body = {'raw': raw}
    # Create a messages object from your service object
    messages = service.users().messages()
    # create and send your message using your messages object, and .execute()
    message = messages.send(userId='me', body=body).execute()


if __name__ == '__main__':
    main()