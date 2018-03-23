import paramiko
import os
import sys
import time

logger = paramiko.util.logging.getLogger()
# paramiko.util.log_to_file(sys.stdout)
USER = os.getenv("SSH_SAMPLE_USER")
HOST = os.getenv("SSH_SAMPLE_HOST")
PASS = os.getenv("SSH_SAMPLE_PASS")
ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.connect(HOST, username=USER, password=PASS, port=22, look_for_keys=False)
ssh_shell = ssh.invoke_shell()
time.sleep(2)
print(type(ssh_shell))
ssh_shell.send('ls -l')
time.sleep(2)
print(ssh_shell.recv(9999))
ssh.close()

