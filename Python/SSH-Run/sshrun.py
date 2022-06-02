import time
import paramiko
import argparse
import threading

parser = argparse.ArgumentParser(description="Execute SSH commands remotely.\n"
                                 "Usage: python3 sshrun.py user@remoteIP password command")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

parser.add_argument("-a", type=str, metavar="Address",
                    help="Address of remote system, usage: user@remoteIP")

parser.add_argument("-P", type=str, metavar="Password",
                    help="Password of remote system")

parser.add_argument("-C", type=str, metavar="Command",
                    help="Command to be executed, example: sudo su && ls")

parser.add_argument("-p", type=str, metavar="port",
                    help="SSH Port to be used (Optional)")


parser.add_argument("-sc", type=bool, metavar="Scanopenports",
                    help="Usage: sc t/sc T/sc 1 (Optional)")


args = parser.parse_args()
print(args)

password = args.P
port = args.p
command = args.C

if args.sc:
    if not "@" in args.a:
        print("Usage of -a flag: username@IP.Range")
        exit()
    username, remote_ip = args.a.split("@")
else:
    username, remote_ip = args.a.split("@")

if not command.endswith("exit"):
    command += " && exit"
if port is None:
    port = 22


def execute_command(remote_ip, print_output=True):
    try:
        ssh.connect(remote_ip,
                    username=username,
                    password=password, port=port,
                    look_for_keys=False, timeout=5)
    except Exception as e:
        return

    channel = ssh.invoke_shell()
    stdin = channel.makefile("wb")
    stdout = channel.makefile("r")

    stdin.write(command + "\n")
    if "sudo" in command or "su " in command:
        stdin.write(password + "\n")
    time.sleep(1)
    if print_output:
        for line in stdout:
            print(line)

    stdout.close()
    stdin.close()

    print(f"{remote_ip}: Success")


if args.sc:
    try:
        ip_start = ".".join(remote_ip.split(".")[:-1])
        if not remote_ip.endswith("0"):
            range_start = remote_ip.split(".")[-1]
        else:
            range_start = 0
    except ValueError:
        print("Wrong IP Range, exiting...")
        exit()
    for i in range(int(range_start), 256):
        remote_ip = f"{ip_start}.{i}"
        print(remote_ip)
        t = threading.Thread(target=execute_command, args=(remote_ip,))
        t.start()
else:
    execute_command(remote_ip, print_output=True)
