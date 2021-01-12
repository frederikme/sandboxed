from internet_access import InternetAccess
from specs import Specs
from file_system import FileSystem

'''
Every method in called in the function 'is_sandboxed' will return a value between 0 and 1.
With a value closer to 0 thinking it's sandboxed and closer to 1 thinking it's a valid machine.

The question remains, how can we test whether we're inside a virtual machine?

- internet access:
    => When reverse engineering an malware-executable, access to the internet is most of the times restricted or even disabled

- specifications of the machine (specs):
    
'''
def is_sandboxed():

    validness = 1.0

    validness *= InternetAccess.basic_ping()

    validness *= Specs.check_disk_space()
    validness *= Specs.check_ram_space()
    validness *= Specs.check_cpu_cores()

    validness *= FileSystem.check_registry_keys()
    validness *= FileSystem.check_files()
    validness *= FileSystem.check_processes()



    return validness

if __name__ == '__main__':
    validness = is_sandboxed()
    print(f'for now the chance of being in a virtual environment is {100 - validness * 100}%')
