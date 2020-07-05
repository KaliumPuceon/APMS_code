#!/usr/bin/env python

import re
import subprocess

keyfile = "/home/pi/.ssh/isc_key"
port = "42069"
username_ipaddress = "apms_relay@178.62.246.247"

# checks if there is an existing ssh process running in the background:
def ssh_running():
    try:	
        out = subprocess.check_output("pgrep -x ssh", shell=True)
        print(out)
    except subprocess.CalledProcessError as e:
        print("Waiting for SSH connection")

	run_ssh()

# runs the ssh reverse tunnel
def run_ssh():
    try:
	ssh_command= "ssh -o ServerAliveInterval 30 -i %s -N -R %s:localhost:22 %s" % (keyfile, port, username_ipaddress)
	ssh_output = subprocess.check_output(ssh_command, shell=True)
	if not ssh_output:
	    print("Successful")
    except subprocess.CalledProcessError as e:
        print("Reverse shell failed")

if __name__ == "__main__":
    ssh_running()
