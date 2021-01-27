# sandbox-evasion
## Installation
sandboxed is now available on PyPi as a pip installation.
```
pip3 install sandboxed
```
## Usage
```
from sandboxed import is_sandboxed

# chance will be between 0 and 1, whereas 0 is a real machine and 1 a virtual machine
chance = is_sandboxed()

# optional parameter to turn logging off
chance = is_sandboxed(logging=False)

print(f"Chance of being inside a virtual machine is {chance*100}%.")
```

## Explanation of the techniques used
Sandboxed will look at 3 sections to determine whether he's inside a virtual machine.
As can be found below:
1. Specifications of the machine
2. Filesystem
3. Internet Access

### Specifications of the machine
Since VM (=virtual machines) tend to run upon real operating systems, VM's most of the time have worse specs.
Things that are taking into considerations:
1. Hard Drive Storage Amount
2. RAM Storage Amount
3. CPU (logical) Cores Amount
4. Serial Number of the PC
5. Model of the PC
5. Manufacturer 

### Filesystem on the PC
Some files directly point to VM that don't exist on real PCs and some files exsist on real PCs that don't exist on the VM.
Things that are being looked for:
1. Registry Keys (of VM)
2. Active Processes (of VM)
3. Specific Files (of VM)
4. Amount of Previous WIFI Connections 
5. Amount of Files on PC
6. Amount of Previous Logins on PC

### Internet Access
When Reverse Malware Engineering the VMs access to internet is most of the time limited or even turned off completetly to void letting the malware back out in the open. 
Few basic internet checks are:
1. Basic Ping
2. Downloading a File
3. HTTP Post Request
4. DNS Socket Request


