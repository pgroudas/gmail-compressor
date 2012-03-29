#!/usr/bin/env python

import imaplib
import email
import time
import os
import re

dates = {}

def ensure_dir(f):
  d = os.path.dirname(f)
  if not os.path.exists(d):
    os.makedirs(d)

MAILSERVERURL = 'imap.gmail.com'
MAILSERVERACCOUNT = 'test@theozer.com'

M=imaplib.IMAP4_SSL(MAILSERVERURL, 993)
M.login(MAILSERVERACCOUNT,'')
folder = '[Gmail]/All Mail'
status, count = M.select(folder)

status, uidstring = M.uid('SEARCH', 'ALL')
uids = uidstring[0].split()
for uid in uids:
  #status, data = M.fetch(uid, '(RFC822)')
  status, data = M.uid('FETCH', int(uid), '(UID FLAGS INTERNALDATE X-GM-MSGID X-GM-THRID X-GM-LABELS RFC822)')
  headers = data[0][0] + data[1]
  pattern = re.compile('(.+) \(X-GM-THRID (.+) X-GM-MSGID (.+) X-GM-LABELS (.+) UID (.+) RFC822 (.+) INTERNALDATE "(.+)" FLAGS (.+)\)')
  result = re.match(pattern, headers)
  messageID = result.group(3)
  flags = result.group(8)
  date = imaplib.Internaldate2tuple("INTERNALDATE \"" + result.group(7) + "\"")
  
  message = data[0][1]
  msg = email.message_from_string(message)

  if msg.is_multipart():
    for part in msg.walk():
      print {
      	"disposition": part.get('Content-Disposition'),
      	"encoding": part.get('Content-Transfer-Encoding'),
      	"type": part.get('Content-Type')
      }
      #if part.get('Content-Transfer-Encoding') == 'quoted-printable':
        #print part
      if str(part.get_payload()[0]).find("OperationalError") > -1:
        if part.is_multipart():
          continue
        else:
          filename = part.get('Content-Disposition')
          if filename:
            filename = "/".join([MAILSERVERURL, MAILSERVERACCOUNT, messageID, filename.replace('attachment; filename="', '').replace('"', '')])
            ensure_dir(filename)
            f = open(filename, 'w')
            f.write(part.get_payload().decode('base64'))
            f.close()
  #message = message.replace('ozer', 'aramburu')
  #print message

  #M.append(folder, flags.replace("\\", ""), date, message)
  #M.uid('FETCH', uid, '(UID FLAGS INTERNALDATE BODY[HEADER.FIELDS (FROM TO CC DATE SUBJECT X-GMAIL-RECEIVED MESSAGE-ID)])')
  #status, data = M.fetch(messages, '(RFC822)')
  #msg = email.message_from_string(data[0][1])
  #file = open(str(uid) + ".txt", 'w')
  #file.write(str(data))
  #file.close()
  
M.close()
M.logout()
