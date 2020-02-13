# from socket import *
import argparse

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('-h','--host',help='Target host',default='127.0.0.1')
    parser.add_argument('-p','--port',help='Target ports',default='80,21,22')
    args=parser.parse_args()
    host=args.host
    ports=args.port
    print(host+' '+ports)
    
if __name__=="__main__":
    main()