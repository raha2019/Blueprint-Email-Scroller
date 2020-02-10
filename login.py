ORG_EMAIL = "@gmail.com"
FROM_EMAIL = "WALLEblueprint" + ORG_EMAIL
FROM_PWD = "W@LL3blueprint"
SMTP_SERVER = "imap.gmail.com"

import smtplib
import time
import imaplib
import email

def read_email_from_gmail():
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
        mail.select('inbox')

        type, data = mail.search(None, 'ALL')
        mail_ids = data[0]

        id_list = mail_ids.split()

        for i in reversed(id_list):
            typ, data = mail.fetch(latest_email_id, '(RFC822)' )

            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1].decode('utf-8'))
                    email_subject = msg['mysubject']
                    print('From : ' + email_from + '\n')

    except Exception as e:
        print ("ex")

read_email_from_gmail()