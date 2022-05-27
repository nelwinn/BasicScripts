A command line script to Execute SSH commands on a remote system.



Usage: python3 sshrun.py user@remoteIP password command

positional arguments:
  Address     Address of remote system, usage: user@remoteIP
  Password    Password of remote system
  Command     Command to be executed, example: sudo su && ls

optional arguments:
  -h, --help  show this help message and exit
  -p port     SSH Port to be used (Optional)
