import os
import psutil
import subprocess
import platform

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
        r"C:\WINDOWS\system32\drivers\vmci.sys",
        r"C:\WINDOWS\system32\drivers\vmsci.sys",
        r"C:\WINDOWS\system32\drivers\vmx_svga.sys"
    ]

    _PROCESSES = [
        "vboxservices.exe",
        "vboxservice.exe",
        "vboxtray.exe",
        "xenservice.exe",
        "VMSrvc.exe",
        "vemusrvc.exe",
        "VMUSrvc.exe",
        "qemu-ga.exe",
        "prl_cc.exe",
        "prl_tools.exe",
        "vmtoolsd.exe",
        "df5serv.exe",
    ]

    @staticmethod
    def check_vm_registry_keys():
        did_succeed = 1

        for key in FileSystem._KEYS:
            try:
                reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
                winreg.OpenKey(reg, key)

                did_succeed = 0.2
            except:
                # no such key or not Windows as os
                continue

        return did_succeed

    @staticmethod
    def check_vm_files():
        did_succeed = 1

        for filepath in FileSystem._FILES:
            if os.path.exists(filepath):
                did_succeed = 0.1

        return did_succeed

    @staticmethod
    def check_vm_processes():
        did_succeed = 1

        for process in FileSystem._PROCESSES:
            if process.lower() in (p.name().lower() for p in psutil.process_iter()):
                did_succeed = 0.1

        return did_succeed

    # get passwords en cookie files etc
    # if user has no files that indicate that it's a valid used computer
    # perhaps even look at time the files were edited

    @staticmethod
    def check_cookies_browser():
        return

    @staticmethod
    # only works for Windows
    def check_wifi_connections():
        '''
        This function will detect how many stored wifi access points the computer has.
        Ideally, a laptop has been connected on multiple wifi access points.
        If only been accessed to 1 wifi point that's fine (for example Desktop PC),
        but this must increase overall suspicion
        '''
        # Will increase to 1, if multiple wifi connections
        did_succeed = 0.98

        if os.name == 'nt':
            try:
                data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')
                profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
                if len(profiles) > 1:
                    did_succeed = 1
            except:
                pass
        else:
            # if not windows, then just increase to 1
            did_succeed = 1

        return did_succeed

    @staticmethod
    def check_application_files():
        '''
        A 'normal' computer mostly has a lot of application files and data.
        If that's not the case, we're most likely inside a virtual machine.
        '''

        did_succeed = 1

        path = ''
        if os.name == 'nt':  # Windows
            path = os.getenv('localappdata')
        elif os.name == 'posix':
            path = os.getenv('HOME')
            if platform.system().lower() == 'darwin':  # MacOS
                path += '/Library/Application Support/'
            else:  # Linux: TODO: Don't use Linux so no idea where to look
                path += '/.config/'

        input_path = path
        amount = len(os.listdir(input_path))

        if amount < 25:
            did_succeed = 0.85
        elif amount < 30:
            did_succeed = 0.90
        elif amount < 40:
            did_succeed = 0.95
        elif amount < 50:
            did_succeed = 0.97
        elif amount < 60:
            did_succeed = 0.98
        elif amount < 70:
            did_succeed = 0.99

        return did_succeed
