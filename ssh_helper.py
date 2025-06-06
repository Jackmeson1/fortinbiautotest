import paramiko

def ssh_and_run_command(hostname, port, username, password, command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, port, username, password)
    stdin, stdout, stderr = ssh.exec_command(command)
    return stdout.read().decode()
