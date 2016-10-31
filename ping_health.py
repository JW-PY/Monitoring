#!/usr/bin/env python2.7
import os

#This function loads all the devices into the dictionary named HOST
def load_hosts():
    with open("hosts.txt") as HostFile:
       for line in HostFile:
            (key, val) = line.split()
            HOST[(key)] = val

if __name__ == '__main__':
    # List of devices to iterate over
    HOST = {}
    health = 0
    newline = '\n'
    failed_devices = []
	
    #load all the devices into the HOST dictionary
    load_hosts()
	
	# Loop through the host file and ping each host
    for i in HOST:
        response = os.system("/usr/sbin/fping -r 7 " + i)
        print "ping", HOST[i], response
        if response != 0:
            health = 1
            failed_devices.append(HOST[i])
			
	# Create failed email message
    f = open('company_fail_email.txt', 'w')
    f.write ('ICMP connectivity test to the following device(s) failed: ')
    f.write (newline)
    f.write (newline)
    f.close()
	
    # Write all failed devices to the failure email file
    for i in failed_devices:
        f = open('company_fail_email.txt', 'a')
        f.write (i)
        f.write (newline)
        f.close()

    # Check the response variable to see if any ping attempts failed
    if response == 0:
        print "Sending SUCCESS email"
        os.system('mail -s "SUCCESSFUL company network device connectivity test" first.last@company.com < /home/erm_users/username/scripts/company/company_success_email.txt')
    else:
        print "Sending FAIL email"
        os.system('mail -s "FAILED company network device connectivity test" first.last@company.com < /home/erm_users/username/scripts/company/company_fail_email.txt')
    
	# Delete failed email file for next test
    try:
        os.remove ('company_fail_email.txt')
    except:
        pass
