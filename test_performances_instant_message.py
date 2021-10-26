import subprocess

# Reception of the text with the modems

HOST = "192.168.0.189"
PORT = "9200"

name_receive_file = 'file_receive.txt'

subprocess.run("nc -W 2 %s %s > %s" % (HOST,PORT,name_receive_file),shell=True)


# Send file with ssh

command = open("%s"%(name_receive_file),"r+")
txt = command.readlines(1)
command.close()

print(txt)

txt = str(txt)

txt = str(txt[:-4])

txt = txt.split(',')[-1]

print('texte= ', txt)

user = 'ubuntu'
host = '192.168.78.253'
pw = 'nathan1003'

file = "dev_ws/src/file1.txt"

command = 'echo %s | cat > %s' % (txt,file)

subprocess.run("sshpass -p %s ssh %s@%s '%s'" % (pw,user,host,command), shell=True)

# Send confirmation for the sent

subprocess.run("echo 'AT*SENDIM,2,255,noack,OK' | nc -N %s %s" % (HOST,PORT),shell=True)
subprocess.run("nc -W 1 %s %s" % (HOST,PORT),shell=True)

