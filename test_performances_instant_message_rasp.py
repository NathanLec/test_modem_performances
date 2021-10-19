import subprocess
import random as rd

# Creation of the random text

leng = 10
txt = ''
for k in range(leng):
    lettre = rd.randint(65,90)
    txt = txt + chr(lettre)

print(txt)
# Send file with ssh

user = 'ubuntu'
host = '192.168.7.253'
pw = 'nathan1003'

file = "dev_ws/src/file1.txt"

command = 'echo %s | cat >> %s' % (txt,file)

subprocess.run("sshpass -p %s ssh %s@%s '%s'" % (pw,user,host,command), shell=True)

# Send file with modems

HOST = "192.168.0.190"
PORT = "9200"

txtlen = str(len(txt))
subprocess.run("echo 'AT*SENDIM,%s,1,noack,%s' | nc -N %s %s" % (txtlen,txt,HOST,PORT),shell=True)


