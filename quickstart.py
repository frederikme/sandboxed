from sandboxed import is_sandboxed

# chance will be between 0 and 1, whereas 0 is a real machine and 1 a virtual machine
chance = is_sandboxed(logging=True)
