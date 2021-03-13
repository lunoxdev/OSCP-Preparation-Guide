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
