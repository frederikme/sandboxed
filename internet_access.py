import os
import subprocess

'''
This class will check whether there is 'real' connection to the internet.

Every method of this class will return a value between 0 and 1.
With a value closer to 0 thinking it's sandboxed and 
     a value closer to 1 thinking it's a valid machine.
'''
class InternetAccess:

    @staticmethod
    def basic_ping():
        '''
        Basic ping function -> checks if wifi is enabled.
        :return: did_succeed: 1 if wifi is enabled, 0 if wifi is disabled
        '''

        did_succeed = 1

        try:
            # -c 4 indicates it will ping 4 times to google.com
            # -> 64 bytes from 172.217.168.206: icmp_seq=0 ttl=119 time=21.761 ms
            output = subprocess.check_output("ping -c 4 google.com", shell=True)

            # somehow check if ping is normal?
            for o in output.decode().split('\n'):
                if 'time=' in o:
                    latency = o.split('time=')[-1].split(" ms")[0]
                    #print(latency)

        # if wifi is disabled, then output will be
        except subprocess.CalledProcessError as e:
            # -> 'ping: cannot resolve google.com: Unknown host'
            output = e.output
            did_succeed = 0.01

        return did_succeed

    @staticmethod
    def advanced_ping():
        # request for webpage, scrape with beautifulsoup
        # make other request
        return

