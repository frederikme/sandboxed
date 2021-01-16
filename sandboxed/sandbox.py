from internet_access import InternetAccess
from specs import Specs
from file_system import FileSystem
import time, os

class Sandbox:

    def __init__(self, logging=False):
        self.logging = logging
        return

    def _normalize(self, values):
        normalization = 0
        for value in values:
            # 0 value means, ABORT -> return 0
            if value == 0:
                return 0
            elif value == 1:
                normalization -= 1
            elif value == 2:
                normalization += 0.5
            elif value == 3:
                normalization += 2
            else:
                normalization += value

        normalization = normalization / len(values)
        return normalization


    def is_sandboxed(self):
        s1 = self._check_specs()
        s2 = self._check_internet()
        s3 = self._check_file_system()

        final_score = self._normalize([s1, s2, s3])

        percentage = int(100 - ((final_score / 5) * 100))

        if self.logging:
            self._printout(10, f"Conclusion: {percentage}% chance of being in a virtual environment.\n")

        return percentage / 100

    def _check_file_system(self):
        self._printout(10, "FILESYSTEM")

        s1, d1, e1 = FileSystem.check_vm_registry_keys()
        s2, d2, e2 = FileSystem.check_vm_files()
        s3, d3, e3 = FileSystem.check_vm_processes()

        # Indirectly trying to derive if it's an active valid user
        s4, d4, e4 = FileSystem.check_wifi_connections()
        s5, d5, e5 = FileSystem.check_application_files()
        s6, d6, e6 = FileSystem.check_prev_logins()

        if self.logging:
            self._printout(score=s1, description=d1, extra=e1)
            self._printout(s2, d2, e2)
            self._printout(s3, d3, e3)

            self._printout(s4, d4, e4)
            self._printout(s5, d5, e5)
            self._printout(s6, d6, e6)

        return self._normalize([s1, s2, s3, s4, s5, s6])


    def _check_internet(self):
        '''
        Since internet calls are being called synchronously could take a while,
        we will printout the status after every call made.
        Looks like shitty code, is shtty code, but gives user a nicer quicker printout.
        '''
        self._printout(10, "INTERNET ACCESS")

        s1, d1, e1 = InternetAccess.check_basic_ping()
        if self.logging:
            self._printout(score=s1, description=d1, extra=e1)

        s2, d2, e2 = InternetAccess.check_download_file()
        if self.logging:
            self._printout(s2, d2, e2)

        s3, d3, e3 = InternetAccess.check_http_post()
        if self.logging:
            self._printout(s3, d3, e3)

        s4, d4, e4 = InternetAccess.check_sockdnsreq()
        if self.logging:
            self._printout(s4, d4, e4)

        return self._normalize([s1, s2, s3, s4])

    def _check_specs(self):
        self._printout(10, "SPECS OF THE SYSTEM")

        s1, d1, e1 = Specs.check_hard_drive()
        s2, d2, e2 = Specs.check_ram_space()
        s3, d3, e3 = Specs.check_cpu_cores()

        s4, d4, e4 = Specs.check_serial_number()
        s5, d5, e5 = Specs.check_model()
        s6, d6, e6 = Specs.check_manufacturer()

        if self.logging:
            self._printout(score=s1, description=d1, extra=e1)
            self._printout(s2, d2, e2)
            self._printout(s3, d3, e3)

            self._printout(s4, d4, e4)
            self._printout(s5, d5, e5)
            self._printout(s6, d6, e6)

        return self._normalize([s1, s2, s3, s4, s5, s6])

    def _printout(self, score, description, extra=None):

        # enable color in cmd for Windows
        if os.name == 'nt':
            os.system('color')

        _CLEAR = '\033[0m'
        _BOLD = '\033[1m'

        _RED = '\033[91m'
        _ORANGE = '\033[33m'
        _LIME = '\033[92m'


        _ITALIC = '\033[3m'
        _UNDERLINED = '\033[4m'
        _YELLOW =  '\033[93m'

        # 10 is for headers of sections
        if score == 10:
            import shutil
            width = shutil.get_terminal_size((80, 20)).columns
            spaces = (width - len(description))
            if spaces % 2 == 0:
                left_spaces = int(spaces / 2)
                right_spaces = int(left_spaces)
            else:
                left_spaces = int((spaces-1) / 2)
                right_spaces = int(left_spaces + 1)

            left = f'{_BOLD}{_ITALIC}{_UNDERLINED}{_YELLOW}' + left_spaces * ' '
            right = right_spaces * ' ' + f'{_CLEAR}'
            description = f'{left}{description}{right}'

        if score == 5:
            description = f'{_BOLD}{_LIME}[+++++] {description}{_CLEAR}'
        elif score == 4:
            description = f'{_BOLD}{_LIME}[++++-] {description}{_CLEAR}'
        elif score == 3:
            description = f'{_BOLD}{_ORANGE}[+++--] {description}{_CLEAR}'
        elif score == 2:
            description = f'{_BOLD}{_ORANGE}[++---] {description}{_CLEAR}'
        elif score == 1:
            description = f'{_BOLD}{_RED}[+----] {description}{_CLEAR}'
        elif score == 0:
            description = f'{_BOLD}{_RED}[-----] {description}{_CLEAR}'

        # make it a bit more exciting
        print()
        print(description)
        time.sleep(0.2)
        if extra:
            print(f"-> {extra}")
            time.sleep(1)
        time.sleep(1.5)
