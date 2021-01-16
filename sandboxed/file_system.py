import os
import psutil
import subprocess
import platform

# registry keys can only be checked for Windows
if os.name == 'nt':
# winreg is a built in library for windows python users, no need to pip install
    import winreg
    import win32net

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
        if os.name != 'nt':
            return 5, "VM REGISTRY KEYS are None.", "This test can only be run on Windows. Considering this test successful."

        score = 5
        description = f"REGISTRY KEYS will look for VM related keys."
        explanation = None

        for key in FileSystem._KEYS:
            try:
                reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
                winreg.OpenKey(reg, key)

                score = 0
                explanation = f"Found a key {key} which is related to VM."
            except:
                # no such key, which is good
                continue

        return score, description, explanation

    @staticmethod
    def check_vm_files():
        if os.name != 'nt':
            return 5, "VM RELATED FILES are None.", "This test can only be run on Windows. Considering this test successful."

        score = 5
        description = f"FILES will look for VM related files."
        explanation = None

        for filepath in FileSystem._FILES:
            if os.path.exists(filepath):
                score = 0
                explanation = f"Found a file {filepath} which is related to VM."

        return score, description, explanation

    @staticmethod
    def check_vm_processes():
        if os.name != 'nt':
            return 5, "VM RELATED PROCESSES are None.", "This test can only be run on Windows. Considering this test successful."

        score = 5
        description = f"PROCESSES will look for VM related processes."
        explanation = None

        try:
            for process in FileSystem._PROCESSES:
                for current_p in  psutil.process_iter():
                    if process.lower() == current_p.name().lower():
                        score = 0
                        explanation = f"Found a process: {process} which is related to VM."
                        break

        except psutil.AccessDenied:
            explanation = "Access to processes was denied. That's a good thing. Continuing."

        return score, description, explanation

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
        if os.name != 'nt':
            return 5, "STORED WIFI are None.", "This test can only be run on Windows. Considering this test successful."

        description = f"WIFI CONNECTIONS will look for stored wifi points."

        try:
            data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')
            profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]

            amount = len(profiles)

            explanation = f"Found {amount} stored wifi access points."
            if amount == 0:
                score = 1
            elif amount == 1:
                score = 3
            elif amount <= 5:
                score = 4
            else:
                score = 5

        except Exception as e:
            score = 3
            explanation = f"Something went wrong, this should not get benefit of the doubt.\nexception: {e}"

        return score, description, explanation

    @staticmethod
    def check_application_files():
        '''
        A 'normal' computer mostly has a lot of application files and data.
        If that's not the case, we're most likely inside a virtual machine.
        '''

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

        description = f"APPLICATION FILES will look for amount of stored files."
        explanation = f"Found {amount} files in {path}."

        if amount < 25:
            score = 1
            explanation = explanation + " Looks like a VM or a new PC."
        elif amount < 30:
            score = 2
            explanation = explanation + " Looks like a VM or a new PC."
        elif amount < 45:
            score = 3
            explanation = explanation + " Looks like a VM or rather unused PC."
        elif amount < 70:
            score = 4
        else:
            score = 5

        return score, description, explanation

    @staticmethod
    # only works for Windows
    def check_prev_logins():
        if os.name != 'nt':
            return 5, "PREV LOGINS are None.", "This test can only be run on Windows. Considering this test successful."


        users,nusers,_ = win32net.NetUserEnum(None,2)
        logons = 0
        for user in users:
            logons += int(user['num_logons'])

        description = f"PREV LOGINS will look for the amount of logins on the pc."
        explanation = f"Amount of logins on the pc is {logons}."

        if logons < 25:
            score = 1
            explanation = explanation + " Looks like a VM or a new PC."
        elif logons < 100:
            score = 2
            explanation = explanation + " Looks like a VM or a new PC."
        elif logons < 200:
            score = 3
            explanation = explanation + " Looks like a VM or rather unused PC."
        elif logons < 1000:
            score = 4
        else:
            score = 5

        return score, description, explanation
