import psutil
import os
import subprocess
import math

class Specs:
    @staticmethod
    def check_hard_drive():
        pdisk = psutil.disk_usage('../')

        # put amount in gigabytes
        total = math.ceil(pdisk.total / (2 ** 30))
        used = pdisk.used / (2 ** 30)
        free = pdisk.free / (2 ** 30)
        percentage = pdisk.percent

        description = f"HARD DRIVE has a total storage of {total} GigaBytes."
        explanation = None

        # RED MASSIVE BAD
        if total < 60:
            score = 0
            explanation = "EVERY computer has at least 100 GiB."
        elif total < 100:
            score = 1
            explanation = "EVERY computer has at least 100 GiB."

        # ORANGE
        elif total < 200:
            score = 2
            explanation = "MOSTs computer have at least 200 GiB."
        elif total < 300:
            score = 3
            explanation = "AVERAGE computers have at least 300 GiB."

        # GREEN
        elif total < 500:
            score = 4 # almost perfect
        else:
            score = 5 # perfect score

        return score, description, explanation

    @staticmethod
    def check_ram_space():
        # get RAM and convert into gigabytes
        total = math.ceil(psutil.virtual_memory().total / (2 ** 30))

        description = f"RAM has a total storage of {total} GigaBytes."
        explanation = None

        # RED MASSIVE BAD
        if total < 2:
            score = 0
            explanation = "EVERY computer has at least 2 GiB."
        if total < 3:
            score = 1
            explanation = "MOST computers have at least 3 GiB."

        # ORANGE
        elif total < 4:
            score = 2
            explanation = "AVERAGE computer has at least 4 GiB."
        elif total < 8:
            score = 3
            explanation = "GOOD computers have at least 8 GiB."

        # GREEN
        elif total < 16:
            score = 4 # almost perfect
        else:
            score = 5 # perfect score

        return score, description, explanation

    @staticmethod
    def check_cpu_cores():
        # logical cores is most of the times double the physical
        logical_cores = psutil.cpu_count(logical=True) # most of the time double as physical
        physical_cores = psutil.cpu_count(logical=False)

        description = f"CPU has a total of {logical_cores} logical cores."
        explanation = None
        # if amount of cpu cores is uneven, then it's definitely a VM!
        # Most VM's have 1 CPU core, but all uneven amounts are never created by pc makers.

        # RED
        if logical_cores % 2 != 0:
            score = 0
            explanation = "EVERY computer should have an even amount of cpu cores."

        # ORANGE
        elif logical_cores < 4:
            score = 3
            explanation = "MOST computers have at least 4 logical cpu cores."

        # GREEN
        elif logical_cores < 8:
            score = 4
        else:
            score = 5

        return score, description, explanation

    @staticmethod
    def check_serial_number():
        # command only works if it's windows
        if os.name != 'nt':
            return 5, "SERIAL NUMBER is None.", "This test can only be run on Windows. Considering this test successful."

        serial = None
        explanation = None

        command = 'wmic bios get serialnumber'
        try:
            output = subprocess.check_output(command, shell=True)
            serial = output.decode().split('\n')[1].split(' ')[0]

            if str(serial) == "0":
                score = 0
                explanation = "Serial number CANNOT be 0 for a real computer."
            else:
                score = 5

        except Exception as e:
            score = 5
            explanation = f"Something went wrong, so giving benefit of the doubt. Considering this test successful.\nexception: {e}"

        description = f"SERIAL NUMBER is {serial}."

        return score, description, explanation

    # TODO add all known models of virtual machines
    _MODELS = [
        'virtualbox',
        'vmware'
    ]

    @staticmethod
    def check_model():
        # command only works if it's windows
        if os.name != 'nt':
            return 5, "MODEL is None.", "This test can only be run on Windows. Considering this test successful."

        model = None
        explanation = None

        command = 'wmic computersystem get model'
        try:
            output = subprocess.check_output(command, shell=True)
            model = output.decode().split('\n')[1].split(' ')[0]
            if model.lower() in Specs._MODELS:
                score = 0
                explanation = "MODEL has been linked to a virtual machine."
            else:
                score = 5

        except Exception as e:
            score = 5
            explanation = f"Something went wrong, so giving benefit of the doubt. Considering this test successful.\nexception: {e}"

        description = f"MODEL is {model}."

        return score, description, explanation

    # TODO add all known manufacturers of virtual machines
    _MANUFACTURER = [
        'innotek'
    ]

    @staticmethod
    def check_manufacturer():
        # command only works if it's windows
        if os.name != 'nt':
            return 5, "MANUFACTURER is None.", "This test can only be run on Windows. Considering this test successful."

        manufacturer = None
        explanation = None

        command = 'wmic computersystem get manufacturer'
        try:
            output = subprocess.check_output(command, shell=True)
            manufacturer = output.decode().split('\n')[1].split(' ')[0]
            if manufacturer.lower() in Specs._MANUFACTURER:
                score = 0
                explanation = "MANUFACTURER has been linked to a virtual machine."
            else:
                score = 5

        except Exception as e:
            score = 5
            explanation = f"Something went wrong, so giving benefit of the doubt. Considering this test successful.\nexception: {e}"

        description = f"MANUFACTURER is {manufacturer}."

        return score, description, explanation
