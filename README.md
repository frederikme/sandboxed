# sandbox-evasion
## Installation
sandboxed is now available on PyPi as a pip installation.
```
pip3 install sandboxed
```
## Usage
Certainty will be expressed with a value between 0 and 1, whereas closer to 0 is a real machine and closer to 1 a virtual machine.
```
from sandboxed import is_sandboxed

certainty = is_sandboxed()
certainty = is_sandboxed(logging=False)

print(f"Chance of being inside a virtual machine is {certainty*100}%.")

>>> Chance of being inside a virtual machine is 95%.
```

## Explanation of the techniques used
Sandboxed will look at 3 aspects to determine whether it's being run inside a virtual machine.
As can be found below:
1. [Specifications of the machine](#specifications-of-the-machine)
2. [Filesystem](#filesystem-on-the-pc)
3. [Internet Access](#internet-access)

### Specifications of the machine
Since VM (=virtual machines) tend to run upon real operating systems, VM's most of the time have rather bad specs.
Things that are taken into considerations:
1. Hard Drive Storage Amount
2. RAM Storage Amount
3. CPU (logical) Cores Amount
4. Serial Number of the PC
5. Model of the PC
5. Manufacturer of the PC

### Filesystem on the PC
Some files directly point to VM that don't exist on real PCs and some files exsist on real PCs that don't exist on the VM.
Things that are being looked for:
1. Registry Keys
2. Active Processes
3. Specific Files
4. Amount of Previous WIFI Connections 
5. Amount of Files on PC
6. Amount of Previous Logins on PC

### Internet Access
When Malware Reverse Engineering the VMs access to internet is most of the time limited or even blocked off completetly to avoid letting the malware back out in the open. 
Few basic internet checks are:
1. Basic Ping
2. Downloading a File
3. HTTP Post Request
4. DNS Socket Request


## Support the Repository
Feel free to make a pull request and contribute to this project.</br>
If you feel like buying me a drink:
* [Patreon](https://www.patreon.com/frederikme)
* [Paypal](https://paypal.me/frederikmees)
* [Buy Me A Coffee](https://www.buymeacoffee.com/frederikme)


