
import poplib
import string, random
import StringIO, rfc822
import logging

SERVER = "pop.gmail.com"
USER  = "WALLEblueprint@gmail.com"
PASSWORD = "W@LL3blueprint"

# connect to server
logging.debug('connecting to ' + SERVER)
server = poplib.POP3_SSL(SERVER)
#server = poplib.POP3(SERVER)

# login
logging.debug('logging in')
server.user(USER)
server.pass_(PASSWORD)

# list items on server
logging.debug('listing emails')
resp, items, octets = server.list()

# download the first message in the list
id, size = string.split(items[2])
resp, text, octets = server.retr(id)

# convert list to Message object
text = string.join(text, "\n")
file = StringIO.StringIO(text)
message = rfc822.Message(file)

# output message
print(message['From']),
print(message['Subject']),
#print(message.fp.read())   
 