### Communication test with the modems ###
### Using the burst messages of the Evologics Modems ###

### This algorithm, in the Raspberry Pi 4, send a message through the modems and wait for a send from the Computer throught the SSH compare the result ###


import subprocess
import random as rd
import time


def random_message(leng):                   # Random message creation with the length
    tic = time.time()                       # Initialization of the time counter for the creation of the message
    txt = ''
    for k in range(leng):
        lettre = rd.randint(65,90)          # Random capital letter with the ASCII code
        txt = txt + chr(lettre)
    tac = time.time()                       #Time of the creation of the message
    print("message : ",tac-tic)
    return txt

def send_message(leng):                     # Send the message of a determined length and wait for the Computer acknoledge
    ## Variables

    name_receive_file = 'file1.txt'         # Creation of the file where you will receive the acknoledge message from the Raspberry (THINK TO CHANGE IN THE COMPUTER ALGORITHM)

    ## Creation of the random text

    txt = random_message(leng)              # Creation of the random message
    print(txt)

    ## Send file with modems

    HOST = "192.168.0.198"                  # IP address of the modem
    PORT = "9200"

    subprocess.run("echo '%s' | nc -W 1 %s %s" % (txt,HOST,PORT),shell=True)    # Send the message as a Burst message through the modems and wait for a 1 ligne answer ( -W 1 ) which be the OK answer


    ## Wait for the acknowledge

    ## Importation of the texts
    receive = open("%s"%(name_receive_file),"r+")                               # Read and write over the old receive file, and wait for the next text.
    text_receive = receive.read()
    receive.close()
    subprocess.run("echo "" | cat > %s" %(name_receive_file),shell=True)        # Write over the file
    RESULT = comparison(txt, text_receive)
    return RESULT


    ## Code of comparison

def comparison(text_send,text_receive):                     # Compare the 2 texts with 3 parameters
    length = 0                                              # Difference of the length of the two files
    diff = 0                                                # Difference of the caracters
    gap = 0                                                 # If their is a removed caracter, and all the rest is identical, the gap will increase of 1 and their will be no diff

    long1 = len(text_send)
    long2 = len(text_receive)-1

    long = long1
    text_l = text_send
    text_s = text_receive

    if long1 != long2:                                      # If the length is different
        length = long1-long2                                # Put the value of the difference between the 2 texts
        if long1 < long2:                                   # Choose the shorter text, to see if their is a additionnal caracter or a remove caracter
            long = long1
            text_s = text_send
            text_l = text_receive
        else:
            long = long2

    for k in range(long):                                   # In the range of the shorter message
        if k+gap < max(long1,long2):                        # Try if the gap is not out of range
            if text_s[k] != text_l[k+gap]:                  # If the two caracters are differents :
                if k+gap+1 < max(long1,long2):                  # If the next caracter is in range, and 
                    if text_l[k+gap+1] == text_s[k]:                # If the next caracter is identical with the previous caracter,
                        gap += 1                                    # It should be a gap
                    else:
                        diff += 1                               # else it just a difference
                else:
                    diff += 1
    return (length,diff,gap)                                # Result of the comparison



# M = random_message(10**7)
# G = random_message(10**7)
# for k in range(8):
#     A = M[0:10**k]
#     B = G[0:10**k]
#     print(k,'  ',comparison(A,B))



Value = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]    # Length of the different messages to send

RESULT = []
k = 0

for long in Value:
    tic = time.time()
    (r1,r2,r3) = send_message(long)
    t = time.time()-tic
    RESULT.append((long,t,r1,r2,r3))
    print(RESULT[-1])
print("""


""")
print(RESULT)
