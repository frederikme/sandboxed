from sandboxed.sandbox import Sandbox
from sandboxed.file_system import FileSystem
from sandboxed.internet_access import *
from sandboxed.specs import *

def is_sandboxed(logging=True):
    sb = Sandbox(logging=logging)
    return sb.is_sandboxed()