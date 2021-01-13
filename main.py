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

    # Internet access
    validness *= InternetAccess.check_basic_ping()
    validness *= InternetAccess.check_download_file()
    validness *= InternetAccess.check_http_post()
    validness *= InternetAccess.check_sockdnsreq()

    # Specifications
    # Assigned specifications when making virtual machine, default when real machine
    validness *= Specs.check_disk_space()
    validness *= Specs.check_ram_space()
    validness *= Specs.check_cpu_cores()
    # Default given specifications by the (virtual/real) machine
    validness *= Specs.check_serial_number()
    validness *= Specs.check_model()
    validness *= Specs.check_manufacturer()

    # Internal file system
    # Specific searching for virtual machine related indicators
    validness *= FileSystem.check_vm_registry_keys()
    validness *= FileSystem.check_vm_files()
    validness *= FileSystem.check_vm_processes()
    # Indirectly trying to derive if it's an active user
    validness *= FileSystem.check_wifi_connections()
    validness *= FileSystem.check_application_files()


    return validness

if __name__ == '__main__':

    validness = is_sandboxed()
    print(f'for now the chance of being in a virtual environment is {100 - validness * 100}%')

    with open('mylog.txt', 'w+') as f:
        f.write(f'for now the chance of being in a virtual environment is {100 - validness * 100}%')

