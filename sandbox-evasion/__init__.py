from sandbox import Sandbox

def is_sandboxed(logging=True):
    sb = Sandbox(logging=logging)
    return sb.is_sandboxed()