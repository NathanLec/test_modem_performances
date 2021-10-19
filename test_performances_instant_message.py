import subprocess
import random as rd

# Reception of the text with the modems

HOST = "192.168.0.190"
PORT = "9200"

name_receive_file = '/dev_ws/src/file_receive.txt'

subprocess.run("nc %s %s >> %s" % (HOST,PORT,name_receive_file),shell=True)


# Send file with ssh

command = open("%s.txt"%(name_receive_file),"r+")
txt = command.read()
command.close()

user = 'ubuntu'
host = '192.168.7.253'
pw = 'nathan1003'

file = "dev_ws/src/file1.txt"

command = 'echo %s | cat >> %s' % (txt,file)

subprocess.run("sshpass -p %s ssh %s@%s '%s'" % (pw,user,host,command), shell=True)