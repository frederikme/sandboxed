import psutil
import os
import subprocess

class Specs:
    @staticmethod
    def check_disk_space():
        did_succeed = 1

        pdisk = psutil.disk_usage('./')
        print(pdisk)
        # put amount in gigabytes
        total = pdisk.total / (2 ** 30)
        used = pdisk.used / (2 ** 30)
        free = pdisk.free / (2 ** 30)
        percentage = pdisk.percent

        print(f"pstutil Total: {total} GiB")
        print(f"psutil Used: {used} GiB")
        print(f"psutil Free: {free} GiB")
        print(f"psutil Used/Total percentage: {percentage}")

        # if computer has less than 200 gigabytes of disk space, something is probably phishy
        if total < 60:
            did_succeed = 0.1
        elif total < 200:
            did_succeed = 0.5
        elif total < 300:
            did_succeed = 0.9
        elif total < 400:
            did_succeed = 0.95
        elif total < 500:
            did_succeed = 0.99

        # TODO: check out total/used or total/free ratio?

        return did_succeed

    @staticmethod
    def check_ram_space():
        did_succeed = 1

        # get RAM and convert into gigabytes
        total_ram = psutil.virtual_memory().total / (2 ** 30)
        print(psutil.virtual_memory().available / (2**30))
        print(f"Total RAM: {total_ram} GiB")

        if total_ram < 2:
            did_succeed = 0.01
        elif total_ram < 4:
            did_succeed = 0.5
        elif total_ram < 8:
            did_succeed = 0.9
        elif total_ram < 16:
            did_succeed = 0.99

        return did_succeed

    @staticmethod
    def check_cpu_cores():

        did_succeed = 1

        # logical cores is most of the times double the physical
        logical_cores = psutil.cpu_count(logical=True) # most of the time double as physical
        physical_cores = psutil.cpu_count(logical=False)

        # if amount of cpu cores is uneven, then it's definitely a VM!
        # Most VM's have 1 CPU core, but all uneven amounts are never created by pc makers.
        if logical_cores % 2 != 0:
            did_succeed = 0.01
        elif logical_cores < 4:
            did_succeed = 0.98
        elif logical_cores < 8:
            did_succeed = 0.99

        return did_succeed

    @staticmethod
    def check_serial_number():
        did_succeed = 1

        # command only works if it's windows
        if os.name != 'nt':
            return did_succeed

        command = 'wmic bios get serialnumber'
        try:
            output = subprocess.check_output(command, shell=True)
            serial = output.decode().split('\n')[1].split(' ')[0]
            if str(serial) == "0":
                did_succeed = 0.1

        except Exception as e:
            print(e)
            # don't know what error potentially could occur tbh
            did_succeed = 0.99

        return did_succeed

    # TODO add all known models of virtual machines
    _MODELS = [
        'virtualbox',
        'vmware'
    ]

    @staticmethod
    def check_model():
        did_succeed = 1

        # command only works if it's windows
        if os.name != 'nt':
            return did_succeed

        command = 'wmic computersystem get model'
        try:
            output = subprocess.check_output(command, shell=True)
            model = output.decode().split('\n')[1].split(' ')[0]
            if model.lower() in Specs._MODELS:
                did_succeed = 0.1

        except Exception as e:
            print(e)
            # don't know what error potentially could occur tbh
            did_succeed = 0.99

        return did_succeed

    # TODO add all known manufacturers of virtual machines
    _MANUFACTURER = [
        'innotek gmbh'
    ]

    @staticmethod
    def check_manufacturer():
        did_succeed = 1

        # command only works if it's windows
        if os.name != 'nt':
            return did_succeed

        command = 'wmic computersystem get manufacturer'
        try:
            output = subprocess.check_output(command, shell=True)
            manufacturer = output.decode().split('\n')[1].split(' ')[0]
            if manufacturer.lower() in Specs._MANUFACTURER:
                did_succeed = 0.1

        except Exception as e:
            print(e)
            # don't know what error potentially could occur tbh
            did_succeed = 0.99

        return did_succeed
