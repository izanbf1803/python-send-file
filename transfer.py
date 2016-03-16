import socket, os, sys, json, time, random

_BUFFER = 65535
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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

def JSONsock(name,data):
    msg = {"name":name,"data":data}
    json_msg = json.dumps(msg)
    return json_msg

def cls():
    os.system("cls")

def excep(exception):
    print("\n\n\n\tERROR: "+exception)
    input()
    main()

def start(sel,info):
    if sel == 1:
        client(info)
    elif sel == 2:
        server(info)
    else:
        print("ERROR")
        input()
        main()

def main():
    cls()
    info = socket.gethostbyname(socket.gethostname())+"  |  "+socket.gethostname()
    os.system('title " '+info+' "')
    selection = int(input("\nEnviar(1) o recivir(2) archivo?  escribe '1' / '2' -> "))
    if selection == 1 or selection == 2:
        start(selection,info)

def client(info):
    os.system('title " '+info+'  |  Emisor'+' "')
    host = input("\n\n\n\tIP: ")
    if host == "local":
        host = socket.gethostbyname(socket.gethostname())
    port = int(input("\n\n\tPUERTO: "))          
    _file = input("\n\n\tArchivo a enviar: ")
    _type_index = _file.rfind(".")
    if _type_index != -1:
        _file_name = _file[:_type_index]
        _file_type = _file[_type_index:len(str(_file))]
    else:
        _file_name = _file
        _file_type = ""
    try:
        f = open(_file,"rb")
    except:
        excep("Archivo erróneo")
    print("\n\nEsperando al servidor...\n\n")
    while True:
        time.sleep(0.005)
        try:
            s.connect((host, port))
            break
        except:
            pass

    s.send(JSONsock("filename",(_file_name+'('+randSTR()+')'+_file_type)).encode("ascii"))
    file_size = os.path.getsize(_file)
    time.sleep(0.05)
    s.send(JSONsock("filesize",str(file_size)).encode("ascii"))
    time.sleep(0.05)

    print ("Enviando:")
    l = f.read(_BUFFER)
    sent = 0
    while (l):
        try:
            s.send(l)
            l = f.read(_BUFFER)
            sent += sys.getsizeof(l)
            percentage = (sent / file_size)*100
            print ("Enviando ( "+"%.0f" % percentage+"% )...")
        except:
            excep("Conexión perdida")
    f.close()
    s.shutdown(1)
    print ("Enviando ( 100% )...")
    print ("\n\n\tENVÍO COMPLETADO!!!\n\n")
    print ("ESPERANDO RESPUESTA...\n\n")
    print ("\n\t-SERVIDOR: "+s.recv(_BUFFER).decode("ascii")+"\n\n")  
    input()

    try:
        main()
    except:
        print("\nERROR")
        input()
        main()

def server(info):
    os.system('title " '+info+'  |  Receptor'+' "')
    host = socket.gethostbyname(socket.gethostname())
    port = int(input("\n\n\tPUERTO: "))            

    print ("\n\n\tEsperando conexión...\n\n")

    s.bind((host, port))
    s.listen(5)
    while True:
        c, addr = s.accept()
        print ("Conexión desde: ", addr)

        file_name = json.loads(c.recv(_BUFFER).decode("ascii")) 
        file_size = json.loads(c.recv(_BUFFER).decode("ascii"))
        if file_size["name"] == "filesize":
            file_size = int(file_size["data"])
        recived = 0
        if file_name["name"] == "filename":
            f = open(file_name["data"],"wb")
            print ("Recibiendo: "+str(file_size)+" bytes - "+file_name["data"])
            l = c.recv(_BUFFER)
            while True:
                f.write(l)
                l = c.recv(_BUFFER)
                recived += sys.getsizeof(l)
                percentage = (recived / file_size)*100
                print ("Recibiendo ( "+"%.0f" % percentage+"% )...")
                if not l:
                    break
            f.close()
            print ("Recibiendo ( 100% )...")
            print ("\n\n\tARCHIVO RECIVIDO")
            c.send(("Gracias por conectarte!").encode("ascii"))
            c.close()
            input()

main()