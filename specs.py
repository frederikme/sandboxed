import shutil
import psutil

class Specs:
    @staticmethod
    def check_disk_space():
        did_succeed = 1

        total, used, free = shutil.disk_usage("./")

        # put amount in gigabytes
        total = total / (2 ** 30)
        used = used / (2**30)
        free = free / (2 ** 30)

        print("Total: %d GiB" % (total))
        print("Used: %d GiB" % (used))
        print("Free: %d GiB" % (free))

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

