A command line script to Execute SSH commands on a remote system.

Execute SSH commands remotely. Usage: python3 sshrun.py user@remoteIP password command

positional arguments:

	Address               Address of remote system, usage: user@remoteIP
  	Password              Password of remote system

optional arguments:
  
  	-h, --help            s				show this help message and exit
  	-C Command            				Command to be executed, example: sudo su && ls
  	-p port               				SSH Port to be used (Optional)
  	-sc Scanopenports     				Usage: sc t/ sc T/ sc 1 (Optional)
  	-o Show output after executing commands		Usage: o t/ o T/ o 1 (Optional)
