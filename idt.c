#include <windows.h>
#include <excpt.h>
#include <stdio.h>

#define DEBUG	0
#define EndUserModeAddress (*(UINT_PTR*)0x7FFE02B4)

typedef LONG (NTAPI *NTSETLDTENTRIES)(DWORD, DWORD, DWORD, DWORD, DWORD, DWORD);

unsigned long
get_idt_base (void)
{
	unsigned char	idtr[6];
	unsigned long	idt	= 0;

	_asm sidt idtr
	idt = *((unsigned long *)&idtr[2]);
	
	return (idt);
}

unsigned long
get_ldtr_base (void)
{
	unsigned char   ldtr[5] = "\xef\xbe\xad\xde";
	unsigned long   ldt			= 0;

	_asm sldt ldtr
	ldt = *((unsigned long *)&ldtr[0]);

	return (ldt);
}

unsigned long
get_gdt_base (void)
{
	unsigned char   gdtr[6];
	unsigned long   gdt	= 0;

	_asm sgdt gdtr
	gdt = *((unsigned long *)&gdtr[2]);

	return (gdt);
}

void
check_idt_base (void)
{
	unsigned int 	idt_base	= 0;

	idt_base = get_idt_base ();

	printf ("[+] Test 1: IDT\n");	
	printf ("IDT base: 0x%x\n", idt_base);
	
	if ((idt_base >> 24) == 0xff) {
		printf ("Result  : VMware detected\n\n");
		return;
	}

	else {
		printf ("Result  : Native OS\n\n");
		return;
	}
}

void
check_ldt_base (void)
{
	unsigned int	ldt_base	= 0;

	ldt_base = get_ldtr_base ();

	printf ("\n[+] Test 2: LDT\n");
	printf ("LDT base: 0x%x\n", ldt_base);
	
	if (ldt_base == 0xdead0000) {
		printf ("Result  : Native OS\n\n");
		return;
	}

	else {
		printf ("Result  : VMware detected\n\n");
		return;
	}
}

void
check_gdt_base (void)
{
	unsigned int	gdt_base	= 0;

	gdt_base 	= get_gdt_base ();

	printf ("\n[+] Test 3: GDT\n");
	printf ("GDT base: 0x%x\n", gdt_base);

	if ((gdt_base >> 24) == 0xff) {
		printf ("Result  : VMware detected\n\n");
		return;
	}

	else {
		printf ("Result  : Native OS\n\n");
		return;
	}
}

// Alfredo Andr�s Omella's (S21sec) STR technique
void
check_mem (void)
{
	unsigned char	mem[4] = {0, 0, 0, 0};

	__asm str mem;

	printf ("\n[+] Test 4: STR\n");
	printf ("STR base: 0x%02x%02x%02x%02x\n", mem[0], mem[1], mem[2], mem[3]);

	if ((mem[0] == 0x00) && (mem[1] == 0x40))
		printf ("Result  : VMware detected\n\n");
	else
		printf ("Result  : Native OS\n\n");
}

void
check_register_stack_1 (void)
{
	unsigned int	a, b;

	__try {
		__asm {

			// save register values on the stack
			push eax			
			push ebx
			push ecx
			push edx
			
			// perform fingerprint
			mov eax, 'VMXh'	    // VMware magic value (0x564D5868)
			mov ecx, 0Ah		// special version cmd (0x0a)
			mov dx, 'VX'		// special VMware I/O port (0x5658)
			
			in eax, dx			// special I/O cmd
			
			mov a, ebx			// data 
			mov b, ecx			// data	(eax gets also modified but will not be evaluated)

			// restore register values from the stack
			pop edx
			pop ecx
			pop ebx
			pop eax
		}
	} __except (EXCEPTION_EXECUTE_HANDLER) {}

	#if DEBUG == 1
	printf ("\n [ a=%x ; b=%d ]\n\n", a, b);
	#endif

	printf ("\n[+] Test 5: VMware \"get version\" command\n");
	
	if (a == 'VMXh') {		// is the value equal to the VMware magic value?
		printf ("Result  : VMware detected\nVersion : ");
			if (b == 1)
				printf ("Express\n\n");
			else if (b == 2)
				printf ("ESX\n\n");
			else if (b == 3)
				printf ("GSX\n\n");
			else if (b == 4)
				printf ("Workstation\n\n");
			else 
				printf ("unknown version\n\n");
	}
	else 
		printf ("Result  : Native OS\n\n");
}

void
check_register_stack_2 (void)
{
	unsigned int	a	= 0;

	__try {
		__asm {

			// save register values on the stack
			push eax
			push ebx
			push ecx
			push edx
			
			// perform fingerprint
			mov eax, 'VMXh'		// VMware magic value (0x564D5868)
			mov ecx, 14h		// get memory size command (0x14)
			mov dx, 'VX'		// special VMware I/O port (0x5658)
			
			in eax, dx			// special I/O cmd
			
			mov a, eax			// data 

			// restore register values from the stack
			pop edx
			pop ecx
			pop ebx
			pop eax
		}
	} __except (EXCEPTION_EXECUTE_HANDLER) {}

	printf ("\n[+] Test 6: VMware \"get memory size\" command\n");
	
	if (a > 0)
		printf ("Result  : VMware detected\n\n");
	else 
		printf ("Result  : Native OS\n\n");
}

int 
helper_cdesc_detect (LPEXCEPTION_POINTERS lpep)
{
		printf ("\n[+] Test 7: VMware emulation mode\n");
	
		if ((UINT_PTR)(lpep->ExceptionRecord->ExceptionAddress) > EndUserModeAddress)
			printf ("Result  : VMware detected (emulation mode detected)\n\n");
		else
			printf ("Result  : Native OS or VMware without emulation mode\n"
							"          (enabled acceleration)\n\n");

		return (EXCEPTION_EXECUTE_HANDLER);
}

void __declspec(naked) 
helper_csdesc_switchcs ()
{
		__asm {
				pop eax
				push 0x000F
				push eax
				retf
		}
}

// Derek Soeder's (eEye Digital Security) VMware emulation test
void
check_csdesc (void)
{
		NTSETLDTENTRIES ZwSetLdtEntries;
		LDT_ENTRY csdesc;

		ZwSetLdtEntries = (NTSETLDTENTRIES)GetProcAddress (GetModuleHandle ("ntdll.dll"), "ZwSetLdtEntries");

		memset (&csdesc, 0, sizeof (csdesc));
		
		csdesc.LimitLow = (WORD)(EndUserModeAddress >> 12);
		csdesc.HighWord.Bytes.Flags1 = 0xFA;
		csdesc.HighWord.Bytes.Flags2 = 0xC0 | ((EndUserModeAddress >> 28) & 0x0F);
		
		ZwSetLdtEntries (0x000F, ((DWORD*)&csdesc)[0], ((DWORD*)&csdesc)[1], 0, 0, 0);

		__try {
				helper_csdesc_switchcs();
				__asm {
            or eax, -1
            jmp eax
        }
    }
    __except (helper_cdesc_detect (GetExceptionInformation())) { }
}

int
main (void)
{

	check_idt_base ();
	check_gdt_base();
	check_ldt_base ();
	check_lpep ();
	check_mem ();
	check_register_stack_1 ();
	check_register_stack_2 ();

	return 0;
}