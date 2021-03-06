#! /usr/bin/env python

# Client and server for udp (datagram) echo.
#
# Usage: udpecho -s [port]            (to start a server)
# or:    udpecho -c host [port] <file (client)

import sys
from socket import *

ECHO_PORT = 50000 + 7
BUFSIZE = 1024

def main():
    if len(sys.argv) < 2:
        usage()
    if sys.argv[1] == '-s':
        server()
    elif sys.argv[1] == '-c':
        client()
    else:
        usage()

def usage():
    sys.stdout = sys.stderr
    print 'Usage: udpecho -s [port]            (server)'
    print 'or:    udpecho -c [host IP address] [port] <file (client)'
    sys.exit(2)

def server():
    if len(sys.argv) > 2:
        port = eval(sys.argv[2])
    else:
        port = ECHO_PORT
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(('', port))
    print 'udp echo server ready'
    while 1:
        data, addr = s.recvfrom(BUFSIZE)
        numWords = len(data.split())
        numChars = 0
        for i in data.split():
            numChars += len(i)+1
        if data == "-1\n":
            break
        print 'server received %d words and %d chars from %r' % (numWords, numChars, addr)
        data += "||" + str(numWords) + "||" + str(numChars)
        s.sendto(data, addr)

def client():
    if len(sys.argv) < 3:
        usage()
    host = sys.argv[2]
    if len(sys.argv) > 3:
        port = eval(sys.argv[3])
    else:
        port = ECHO_PORT
    addr = host, port
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(('', 0))
    print 'udp echo client ready, reading stdin'
    while 1:
        line = sys.stdin.readline()
        if not line:
            break
        s.sendto(line, addr)
        data, fromaddr = s.recvfrom(BUFSIZE)
        data2 = data.split("||")
        numWords = int(data2[1])
        numChars = int(data2[2])
        print 'client received %d words and %d chars from %r' % (numWords, numChars, fromaddr)

main()
