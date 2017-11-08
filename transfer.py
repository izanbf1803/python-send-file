import socket, os, sys, json, time, random, argparse

_BUFFER = 65535
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

DEFAULT_PORT = 443
DEFAULT_MOTD = "Thanks!"

ERR_CL = "Connection lost"
ERR_FNF = "File not found"
ERR_NO = "You should be sender (-s) or receiver (-r)"
ERR_NoIP = "If you want to send the file you need to specify receiver's IP (-ip)"
ERR_NoF = "If you want to send the file you need to specify the filename (-f)"

def randSTR():
    randList = ["QWERTYUIOPASDFGHJKLZXCVBNM1234567890","qwertyuiopasdfghjklzxcvbnm"]
    fLoops = random.randint(10,20)
    loops = 0
    result = ""
    while fLoops >= loops:
        loops+=1
        rn = random.randint(0,1)
        result += random.choice(randList[rn])
    return result

def jsonFileInfo(name, size):
    msg = {'n':name, 's':size}
    json_msg = json.dumps(msg)
    return json_msg

def excep(exception):
    print("\nERROR:", exception)
    sys.exit(1)

def start(sel, info, args):
    if sel == 's':
        client(info, args)
    elif sel == 'r':
        server(info, args)
    else:
        excep("ARG PARSING ERROR")

def main():
    parser = argparse.ArgumentParser(description="Send and recive files fast as light")

    parser.add_argument("-r", action="store_true",
        help="Use it to be the receiver, you must specify -s (sender) or -r (reciver).")

    parser.add_argument("-s", action="store_true",
        help="Use it to be the sender, you must specify -s (sender) or -r (reciver).")

    parser.add_argument("-p", type=int, default=DEFAULT_PORT
        ,help="Port to use in communications, {a} by default".format(a=DEFAULT_PORT))

    parser.add_argument("-ip", type=str, 
        help="IP to send the file (Only required for sender)")

    parser.add_argument("-f", type=str, 
        help="file to send (Only required for sender)")

    parser.add_argument("-motd", type=str, default=DEFAULT_MOTD,
        help="Message to send to sender after file receiving")

    args = parser.parse_args()

    selection = ''
    if args.r:
        selection = 'r'
    elif args.s:
        selection = 's'
        if args.ip == None:
            excep(ERR_NoIP)
        if args.f == None:
            excep(ERR_NoF)

    info = "{a}:{b} | {c}".format(a=socket.gethostbyname(socket.gethostname()), b=args.p, c=socket.gethostname())

    if selection == 's' or selection == 'r':
        start(selection, info, args)
    else:
        excep(ERR_NO)

def client(info, args):
    os.system('title " '+info+'  |  Sender'+' "')
    host = args.ip
    if host == "local" or host == "localhost":
        host = socket.gethostbyname(socket.gethostname())
    port = args.p         
    _file = args.f
    _type_index = _file.rfind(".")
    if _type_index != -1:
        _file_name = _file[:_type_index]
        _file_type = _file[_type_index:len(str(_file))]
    else:
        _file_name = _file
        _file_type = ""
    try:
        f = open(_file, "rb")
    except:
        excep(ERR_FNF)
    print("\nWaiting for server response...\n")
    while True:
        time.sleep(0.2)
        try:
            s.connect((host, port))
            break
        except:
            pass

    # File info 'I'
    file_name = ''.join([_file_name, '(', randSTR(), ')', _file_type])
    file_size = os.path.getsize(_file)
    s.send(jsonFileInfo(file_name, file_size).encode("ascii"))

    l = f.read(_BUFFER)
    sent = 0
    while (l):
        try:
            s.send(l)
            l = f.read(_BUFFER)
            sent += sys.getsizeof(l)
            percentage = sent * 100 // file_size
            print ("\rSending... {a}%".format(a=percentage), end='')
        except:
            excep(ERR_CL)
    f.close()
    s.shutdown(1)
    print ("\rSending... 100%")
    print ("FILE SENT!")
    print ("WAITING FOR RESPONSE...")
    print ("->SERVER:", s.recv(_BUFFER).decode("ascii"))  

def server(info, args):
    os.system('title " '+info+'  |  Reciver'+' "')
    host = socket.gethostbyname(socket.gethostname())
    port = args.p          

    s.bind((host, port))
    s.listen(5)

    while True:
        print ("\nWaiting connection...\n")

        c, addr = s.accept()
        print ("Connection from: ", addr)

        file_info = json.loads(c.recv(_BUFFER).decode("ascii"))
        file_name = file_info['n']
        file_size = file_info['s']

        recived = 0
        f = open(file_name, "wb")
        print ("Receiving:", str(file_size), "bytes -", file_name)
        l = c.recv(_BUFFER)
        while True:
            f.write(l)
            l = c.recv(_BUFFER)
            recived += sys.getsizeof(l)
            percentage = recived * 100 // file_size
            print ("\rReceiving... {a}%".format(a=percentage), end='')
            if not l:
                break
        f.close()
        print ("\rReceiving... 100%")
        print ("FILE SAVED!")
        c.send(args.motd.encode("ascii"))
        c.close()

main()
