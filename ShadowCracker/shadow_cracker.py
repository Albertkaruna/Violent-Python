import crypt

def crack_pass(hash): #$6$wuabrA7ZYljHwLRL$y0IpkcYGgRTLcqVZhIv/p2NLgLNHTEKTszC4AmTi1xRj1Pk/rlMMWV14zhY9L42Zpj7kLJCnpBIa1zJYjL4/r0
    hash_type=hash.split('$')[1] #$6 means SHA-512 hash algorithm used
    hash_salt=hash[0:19] # Salt -- #$6$wuabrA7ZYljHwLRL
 
    dict_file=open('rockyou.txt','r')
    for word in dict_file.readlines():
        word=word.strip('\n')
        hashed=crypt.crypt(word,hash_salt)
        # print(hashed)
        if hash==hashed:
            print("*** Password FOUND: "+word)
            return
    print("Password NOT FOUND")


def main():
    passfile=open('passwords.txt','r')
    for line in passfile.readlines():
        if ':' in line:
            username=line.split(':')[0]
            hash=line.split(':')[1].strip(' ')
            print("Cracking password for :"+username)
            crack_pass(hash)


main()