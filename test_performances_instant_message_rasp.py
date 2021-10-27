
import subprocess
import random as rd
import time


def random_message(leng):
    tic = time.time()
    txt = ''
    for k in range(leng):
        lettre = rd.randint(65,90)
        txt = txt + chr(lettre)
    tac = time.time()
    print("message : ",tac-tic)
    return txt

def send_message(leng):
    ## Variables

    name_receive_file = 'file1.txt'


    ## Creation of the random text

    txt = random_message(leng)

    print(txt)

    ## Send file with modems

    HOST = "192.168.0.198"
    PORT = "9200"


    txtlen = str(len(txt))


    subprocess.run("echo '%s' | nc -W 1 %s %s" % (txt,HOST,PORT),shell=True)


    ## Wait for the acknoledge

        ## Importation of the texts
    receive = open("%s"%(name_receive_file),"r+")
    text_receive = receive.read()
    receive.close()
    subprocess.run("echo "" | cat > %s" %(name_receive_file),shell=True)
    RESULT = comparison(txt, text_receive)
    return RESULT



    ## Code of comparison

def comparison(text_send,text_receive):
    length = 0
    diff = 0
    gap = 0

    long1 = len(text_send)
    long2 = len(text_receive)-1

    long = long1
    text_l = text_send
    text_s = text_receive

    if long1 != long2:
        length = long1-long2
        if long1 < long2:
            long = long1
            text_s = text_send
            text_l = text_receive
        else:
            long = long2

    for k in range(long):
        if k+gap < max(long1,long2):
            if text_s[k] != text_l[k+gap]:
                if k+gap+1 < max(long1,long2):
                    if text_l[k+gap+1] == text_s[k]:
                        gap += 1
                    else:
                        diff += 1
                else:
                    diff += 1
    return (length,diff,gap)


# M = random_message(10**7)
# G = random_message(10**7)
# for k in range(8):
#     A = M[0:10**k]
#     B = G[0:10**k]
#     print(k,'  ',comparison(A,B))



Value = [10, 20, 50, 100, 200, 500, 1000, 2000]

RESULT = []
k = 0

for long in Value:
    tic = time.time()
    (r1,r2,r3) = send_message(long)
    t = time.time()-tic
    RESULT.append((t,r1,r2,r3))
print(RESULT)
