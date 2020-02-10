import imaplib
import email
import os


def create_folder(folder_name="backup"):
    """
    Creates a folder to store all mails
    """
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


def extract_body(payload):
    """
    returns the email body from the payload
    """
    if isinstance(payload, str):
        return payload
    else:
        return '\n'.join([extract_body(part.get_payload()) for part in payload])


def create_connection(user_name, password):
    """
    logs into the email service provider using the provided username and password
    :return: connection object for imaplib
    """
    conn = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    try:
        conn.login(user_name, password)
    except Exception as e:
        print("Could not login", e)
    return conn


def show_mailBoxes(conn):
    """
    Displays the mail boxes in your email client
    :param conn: imaplib object
    """
    mailboxes = []
    for n, item in enumerate(conn.list()[1]):
        mailbox = item.decode("utf-8")
        mailboxes.append(mailbox[mailbox.index("\"/\"") + 4:])
        print(n, mailbox[mailbox.index("\"/\"") + 4:])
    return mailboxes


def select_mailbox(conn, mailbox):
    """
    select a mailbox to search through
    :param conn: imaplib object
    :param mailbox: name of the mailbox
    """
    conn.select(mailbox)


def save_email(num, subject, body):
    with open("backup/" + str(num.decode('utf-8')) + ".txt", "w") as f:
        f.write(subject)
        f.write("\n\n")
        f.write(body)


def get_emails(conn, search_param):
    count = 0
    typ, data = conn.search(None, search_param)
    try:
        for num in data[0].split():
            try:
                _, msg_data = conn.fetch(num, '(RFC822)')
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_string(response_part[1].decode("utf-8"))
                        subject = msg['subject']
                        payload = msg.get_payload()
                        body = extract_body(payload)
                        save_email(num, subject, body)
                        count += 1
                        if count % 100 == 0:
                            print(count, "Messages saved")
            except Exception as e:
                print("Couldnt Parse message:", num, e)
                pass
    except Exception as e:
        print("EXCEPTION OCCURED:", e)
        pass
        conn.logout()
    finally:
            conn.close()


if __name__ == '__main__':
    conn = create_connection("WALLEblueprint@gmail.com", "W@LL3blueprint")
    mailboxes = show_mailBoxes(conn)
    mailbox_choice = int(input("inbox"))
    select_mailbox(conn, mailboxes[mailbox_choice])
    create_folder()
    search_param = input("Enter the filter- Leave blank for ALL")
    if len(search_param) == 0:
        search_param = "ALL"
    get_emails(conn, search_param)