### Communication test with the modems ###
### Using the burst messages of the Evologics Modems ###

### This algorithm, in the computer, wait for a send from the Raspberry throught the modems and send back the result, in order to compare. ###

### Press control C when the modems stop to transmit (end of the noise of the transmission) and when the algorith told you to. ###

import subprocess
import time

subprocess.run("nc -w 1 %s %s" %  ('192.168.0.189','9200'),shell = True)


## Reception of the text with the modems
while True:
    # IP address of the modem
    HOST = "192.168.0.189"
    PORT = "9200"

    # File where the receive message is writen
    name_receive_file = 'file_receive.txt'

    # Write above the file, make it empty for the others messages
    subprocess.run('echo "" | cat > %s' %(name_receive_file),shell=True)

    # Initialization of the receive loop
    GO = False   # Do you have to leave the loop or not
    LEN = 0      # Condition of length of the message
    pr = 1       # Question for the printing part

    # Wait for the first message which arrive ( -W 1 ) to enter the loop and add it in the file
    subprocess.run("nc -W 1 %s %s >> %s" %  (HOST,PORT,name_receive_file),shell = True)

    tic = time.time()
    texte = ''
    # Receive loop

    while not(GO):
        a = str(subprocess.check_output("cat %s" %(name_receive_file),shell=True)).split(",")[-1][:-5]                 # Read the current text in the received file
        if a[-6:]=="FIN000":
            GO = True
        else:
            texte = texte + a
            subprocess.run("nc -W 1 %s %s >> %s" % (HOST,PORT,name_receive_file),shell=True)            # And you listen for one more second, trying to get more informations
#        print(a)                                                    # It can print the output of the text file, if you want to compare yourself
#    print("time receive = ",time.time()-tic)                        # This line print the time that the modems had to receive the all file. It is only informative, because it require your stop action
    print(texte)
## Send file with ssh
    command = open("%s"%(name_receive_file),"r+")                                               # Open the receive text file
    txt = command.read()                                                                        # Read the all text
    command.close()
    print("lu")                                                                  # Change the text to make it similar to the send one (remove the caracters created by python and the subprocess library)

    user = 'ubuntu'                                                                             # IP address and password for the Raspberry Pi SSH connexion
    host = '192.168.1.253'
    pw = 'nathan1003'

    file = "dev_ws/src/test_modem_performances/file1.txt"                                                               # Name of the file in the Raspberry Pi, take care to write the same in the Raspberry pi algorithm

    command = 'echo %s | cat > %s' % (texte,file)                                                 # Command to write the text in this file

    subprocess.run("sshpass -p %s ssh %s@%s '%s'" % (pw,user,host,command), shell=True)         # Use of sshpass to automate the write

    time.sleep(2)                                                                               # Time wait for the command to finish in the raspberry

 ## Send confirmation for the sent through the modem

    subprocess.run("echo 'AT*SENDIM,2,255,noack,OK' | nc -N %s %s" % (HOST,PORT),shell=True)                          # When all these steps are finished, sent of the confirmation throught the Modems
    subprocess.run("nc -W 1 %s %s" %  (HOST,PORT),shell = True)
    print("new")
