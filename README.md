# sandbox-evasion
## Installation
```
pip3 install sandboxed
```
### Usage
```
from sandboxed import is_sandboxed

# chance will be between 0 and 1, whereas 0 is a real machine and 1 a virtual machine
chance = is_sandboxed()

# optional parameter to turn logging off
chance = is_sandboxed(logging=False)

print(f"Chance of being inside a virtual machine is {chance*100}%.")
```

### Explanation of the techniques used
TODO
