import zipfile
import sys
import argparse
from threading import Thread

def extract_file(z_file,pwd):
        try:        
            z_file.extractall(pwd=pwd)
            print("Password found: "+pwd)
            exit(0)
        except:
            pass

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('-f','--file',type=str,help='Zip file path')
    parser.add_argument('-d','--dict',type=str,help="Passwords dictionary file path")
    args=parser.parse_args()

    passwords=open(args.dict,'r')
    zip_file=zipfile.ZipFile(args.file)
    for pwd in passwords.readlines():
        p=pwd.strip('\n')
        # res=extract_file(zip_file,p)
        t=Thread(target=extract_file,args=(zip_file,p))
        t.start()

if __name__=="__main__":
    main()
