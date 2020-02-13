from socket import *
import argparse
import sys

def conn_scan(host,port):
    try:
        skt=socket(AF_INET,SOCK_STREAM)
        skt.connect((host,port))
        skt.send('ThirdNitrogen\n'.encode())
        result=skt.recv(1000)
        print("Port {0}/TCP open".format(port))
        print("[+] "+str(result))
        skt.close()
    except:
        e=sys.exc_info()
        # print(e)
        print("Port {0}/TCP closed".format(port))

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
        print("Scanning port "+port)
        conn_scan(target_ip,int(port))


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('-H','--host',help='Target host',default='127.0.0.1')
    parser.add_argument('-p','--port',help='Target port(s)',default='80,21,22')
    args=parser.parse_args()
    host=args.host
    ports=str(args.port).split(',')
    if (host==None) or (ports[0]==None):
        print("[-] You must specify host and port(s)")
        exit(0)
    port_scan(host,ports)


if __name__=="__main__":
    main()