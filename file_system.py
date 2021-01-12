import os
import psutil
# registry keys can only be checked for Windows
if os.name == 'nt':
# winreg is a built in library for windows python users, no need to pip install
    import winreg

'''
This class is mostly aimed for Windows
I don't know how linux based operating systems act in a virtual machine
'''
class FileSystem:

    _KEYS = [
        r"SOFTWARE\Oracle\VirtualBox Guest Additions",
        r"HARDWARE\ACPI\DSDT\VBOX__",
        r"HARDWARE\ACPI\FADT\VBOX__",
        r"HARDWARE\ACPI\RSDT\VBOX__",
        r"SYSTEM\ControlSet001\Services\VBoxGuest",
        r"SYSTEM\ControlSet001\Services\VBoxMouse",
        r"SYSTEM\ControlSet001\Services\VBoxService",
        r"SYSTEM\ControlSet001\Services\VBoxSF",
        r"SYSTEM\ControlSet001\Services\VBoxVideo",
        r"SOFTWARE\VMware, Inc.\VMware Tools",
    ]

    _FILES = [
        r"C:\WINDOWS\system32\drivers\VBoxMouse.sys",
        r"C:\WINDOWS\system32\drivers\VBoxGuest.sys",
        r"C:\WINDOWS\system32\drivers\VBoxSF.sys",
        r"C:\WINDOWS\system32\drivers\VBoxVideo.sys",
        r"C:\WINDOWS\system32\vboxdisp.dll",
        r"C:\WINDOWS\system32\vboxhook.dll",
        r"C:\WINDOWS\system32\vboxmrxnp.dll",
        r"C:\WINDOWS\system32\vboxogl.dll",
        r"C:\WINDOWS\system32\vboxoglarrayspu.dll",
        r"C:\WINDOWS\system32\vboxoglcrutil.dll",
        r"C:\WINDOWS\system32\vboxoglerrorspu.dll",
        r"C:\WINDOWS\system32\vboxoglfeedbackspu.dll",
        r"C:\WINDOWS\system32\vboxoglpackspu.dll",
        r"C:\WINDOWS\system32\vboxoglpassthroughspu.dll",
        r"C:\WINDOWS\system32\vboxservice.exe",
        r"C:\WINDOWS\system32\vboxtray.exe",
        r"C:\WINDOWS\system32\VBoxControl.exe",
        r"C:\WINDOWS\system32\drivers\vmmouse.sys",
        r"C:\WINDOWS\system32\drivers\vmhgfs.sys",
        r"C:\WINDOWS\system32\drivers\vmusbmouse.sys",
        r"C:\WINDOWS\system32\drivers\vmkdb.sys",
        r"C:\WINDOWS\system32\drivers\vmrawdsk.sys",
        r"C:\WINDOWS\system32\drivers\vmmemctl.sys",
        r"C:\WINDOWS\system32\drivers\vm3dmp.sys",
    ]

    _PROCESSES = [
        "vboxservices.exe",
        "vboxservice.exe",
        "vboxtray.exe",
        "xenservice.exe",
        "VMSrvc.exe",
        "VMUSrvc.exe",
        "qemu-ga.exe",
        "prl_cc.exe",
        "prl_tools.exe",
    ]

    @staticmethod
    def check_registry_keys():
        did_succeed = 1

        for key in FileSystem._KEYS:
            try:
                reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
                k = winreg.OpenKey(reg, key)
                # if open key was succesful
                did_succeed = 0.01
            except:
                # no such key or not Windows as os
                continue

        return did_succeed

    @staticmethod
    def check_files():
        did_succeed = 1

        for filepath in FileSystem._FILES:
            if os.path.exists(filepath):
                did_succeed = 0.1

        return did_succeed

    @staticmethod
    def check_processes():
        did_succeed = 1

        for process in FileSystem._PROCESSES:
            if process.lower() in (p.name().lower() for p in psutil.process_iter()):
                did_succeed = 0.1

        return did_succeed

    # get passwords en cookie files etc
    # if user has no files that indicate that it's a valid used computer
    # perhaps even look at time the files were edited

    @staticmethod




