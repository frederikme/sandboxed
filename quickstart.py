from sandboxed import is_sandboxed

# certainty will be expressed with a value between 0 and 1, whereas closer to 0 is a real machine and closer to 1 a virtual machine
chance = is_sandboxed(logging=True)
