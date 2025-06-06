import paramiko


def ssh_and_run_command(hostname, port, username, password, command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    stdout_data = ""
    stderr_data = ""
    try:
        ssh.connect(hostname=hostname, port=port, username=username, password=password)
        stdin, stdout, stderr = ssh.exec_command(command)
        stdout_data = stdout.read().decode()
        stderr_data = stderr.read().decode()
    except paramiko.SSHException as exc:
        stderr_data = str(exc)
    finally:
        ssh.close()

    return stdout_data, stderr_data
