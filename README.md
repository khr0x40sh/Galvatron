#Galvatron
  Powershell fork (with upgrades) of the Monohard botnet (Carlos Ganoza P.). Default creds are admin/admin

  1. Features

     Utilizes Internet Explorer as the C2 channel
     Checks in via an obfuscated POST disguised as a login attempt
     Posts back stdout and stderr of commands run
     Contains an udpflood module for DDoS tests
     Supports download and upload of files

  2. Install

     Server
	Requires typical LAMP setup.
	Run install.sh for default setup. This assumes /var/www as your apache content directory.  Change the install script as needed.
	This will setup the server in a default state.  User assumes risk of using default installation. Login via /bot/login.php

     Client
	Run galvatron.ps1 from the client directory either via the file or in memory.  If using udpflood, ensure either the udpflood.ps1 file is local or can be accessed in memory.
	Ensure script is being run in x86 mode as currently the IE COM object on 64 bit seems buggy.

Twitter:  @khr0x40sh
Email:    khr0x40sh@gmail.com
Site:	  http://khr0x40sh.wordpress.com
