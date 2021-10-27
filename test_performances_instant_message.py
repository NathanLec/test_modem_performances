import subprocess
import time

# Reception of the text with the modems
while True:
    HOST = "192.168.0.189"
    PORT = "9200"

    name_receive_file = 'file_receive.txt'

    subprocess.run('echo "" | cat > %s' %(name_receive_file),shell=True)

    GO = False
    LEN = 0


    subprocess.run("nc -W 1 %s %s >> %s" %  (HOST,PORT,name_receive_file),shell = True)

    while not(GO):
        a = str(subprocess.check_output("cat %s" %(name_receive_file),shell=True))
        if len(a) == LEN:
            GO = True
        else:
            LEN = len(a)
            subprocess.run("nc -w 1 %s %s >> %s" % (HOST,PORT,name_receive_file),shell=True)

# Send file with ssh

    command = open("%s"%(name_receive_file),"r+")
    txt = command.read()
    command.close()

    txt = txt.replace("\n","")

    user = 'ubuntu'
    host = '192.168.140.253'
    pw = 'nathan1003'

    file = "dev_ws/src/file1.txt"

    command = 'echo %s | cat > %s' % (txt,file)

    subprocess.run("sshpass -p %s ssh %s@%s '%s'" % (pw,user,host,command), shell=True)

    time.sleep(2)

 # Send confirmation for the sent

    subprocess.run("echo 'OK' | nc -N %s %s" % (HOST,PORT),shell=True)

