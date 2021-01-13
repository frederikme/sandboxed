import os
import subprocess
import requests
import socket

'''
This class will check whether there is 'real' connection to the internet.
'''
class InternetAccess:

    @staticmethod
    def check_basic_ping(amount=4, host='google.com'):
        if os.name == 'nt':
            # windows based
            command = f"ping -w {amount} {host}"
        else:
            # linux based
            command = f"ping -c {amount} {host}"

        description = f"BASIC PING makes {amount} pings to {host}."
        score = 5
        explanation = None

        try:
            # -> 64 bytes from 172.217.168.206: icmp_seq=0 ttl=119 time=21.761 ms
            output = subprocess.check_output(command, shell=True)

            # somehow check if ping is normal?
            for o in output.decode().split('\n'):
                if 'time=' in o:
                    latency = o.split('time=')[-1].split(" ms")[0]

        # if wifi is disabled, then output will be
        except subprocess.CalledProcessError as e:
            # -> 'ping: cannot resolve google.com: Unknown host'
            score = 3
            explanation = "BASIC PING indicates that your wifi is disabled."

        return score, description, explanation

    @staticmethod
    def check_download_file():

        description = f"DOWNLOAD FILE check if http get-request is possible."
        score = 5
        explanation = None

        try:
            r = requests.get('http://ipv4.download.thinkbroadband.com/20MB.zip')
            if r.status_code != 200:
                score = 3
                explanation = f"Status code is {r.status_code}, which is not 200 like expected."
        except Exception as e:
            score = 3
            explanation = f"Something went wrong, but should not give benefit of doubt.\nexception: {e}."

        return score, description, explanation

    @staticmethod
    def check_http_post():
        description = f"POST REQUEST check if http post-request is possible."
        score = 5
        explanation = None

        try:
            r = requests.post("http://bugs.python.org", data={'number': 12524, 'type': 'issue', 'action': 'show'})
            if r.status_code != 200:
                score = 3
                explanation = f"Status code is {r.status_code}, which is not 200 like expected."
        except Exception as e:
            score = 3
            explanation = f"Something went wrong, but should not give benefit of doubt.\nexception: {e}."

        return score, description, explanation

    @staticmethod
    def check_sockdnsreq():
        '''
        With sockets you go on the level lower and actually control the connection and send/receive raw bytes. 
        HTTP connection is a protocol that runs on a socket. 
        HTTP connection is a higher-level abstraction of a network connection.
        '''
        description = f"SOCKET REQUEST to check if lower level socket dns requests are possible."
        score = 5
        explanation = None

        try:
            addr1 = socket.gethostbyname('google.com') # 172.217.168.206
            socket.gethostbyname('yahoo.com')
            socket.gethostbyname('facebook.com')
            socket.gethostbyname('instagram.com')
        except Exception as e:
            score = 3
            explanation = f"Something went wrong, but should not give benefit of doubt.\nexception: {e}."

        return score, description, explanation
