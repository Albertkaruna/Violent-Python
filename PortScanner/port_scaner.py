from socket import *
import argparse
import sys
from threading import Thread,Semaphore

screenlock=Semaphore(value=1)

import nmap

def nmap_scan(host,port):
    scanner=nmap.PortScanner()
    scanner.scan(host,port)
    state=scanner[host]['tcp'][int(port)]['state']
    name=scanner[host]['tcp'][int(port)]['name']
    print('[+] '+host+' tcp/'+port+' - '+name+' - '+state)

def conn_scan(host,port):
    try:
        skt=socket(AF_INET,SOCK_STREAM)
        skt.connect((host,port))
        skt.send('ThirdNitrogen\n'.encode())
        result=skt.recv(1000)
        screenlock.acquire()
        print("Scanning port "+str(port))
        print("Port {0}/TCP open".format(port))
        print("[+] "+str(result))
        skt.close()
    except:
        e=sys.exc_info()
        screenlock.acquire()
        print(e)
        print("Port {0}/TCP closed".format(port))
    finally:
        screenlock.release()
        skt.close()

def port_scan(host,ports):
    try:
        target_ip=gethostbyname(host)
    except:
        print('[-] Cannot resolve {0}: Unknown host'.format(host))
    try:
        target_name=gethostbyaddr(target_ip)
        print("[+] Scan result for {0}".format(target_name[0]))
    except:
        print("[+] Scan result for {0}".format(target_ip))
    setdefaulttimeout(10)
    for port in ports:
        # nmap_scan(target_ip,port)
        thread=Thread(target=nmap_scan,args=(host,port))
        thread.start()


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('-H','--host',help='Target host',default='127.0.0.1')
    parser.add_argument('-p','--port',help='Target port(s)',default='21,22,23,80')
    args=parser.parse_args()
    host=args.host
    ports=str(args.port).split(',')
    if (host==None) or (ports[0]==None):
        print("[-] You must specify host and port(s)")
        exit(0)
    port_scan(host,ports)


if __name__=="__main__":
    main()