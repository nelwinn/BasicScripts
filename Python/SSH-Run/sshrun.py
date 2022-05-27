import time
import paramiko
import argparse

parser = argparse.ArgumentParser(description="Execute SSH commands remotely.\n"
                                 "Usage: python3 sshrun.py user@remoteIP password command")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

parser.add_argument("a", type=str, metavar="Address",
                    help="Address of remote system, usage: user@remoteIP")

parser.add_argument("P", type=str, metavar="Password",
                    help="Password of remote system")

parser.add_argument("-p", type=str, metavar="port",
                    help="SSH Port to be used (Optional)")

parser.add_argument("C", type=str, metavar="Command",
                    help="Command to be executed, example: sudo su && ls")

args = parser.parse_args()

username, remote_ip = args.a.split("@")
password = args.P
port = args.p
command = args.C

if not command.endswith("exit"):
    command += " && exit"
if port is None:
    port = 22
ssh.connect(remote_ip,
            username=username,
            password=password, port=port,
            look_for_keys=False, timeout=5)

channel = ssh.invoke_shell()
stdin = channel.makefile("wb")
stdout = channel.makefile("r")

stdin.write(command + "\n")
if "sudo" in command or "su " in command:
    stdin.write(password + "\n")
time.sleep(1)
for line in stdout:
    print(line)

stdout.close()
stdin.close()