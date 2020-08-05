from colorama import Fore, Style, Back
#author:mvaouli
# Version 2.0
## Show menu ##
print(Fore.GREEN + 81 * '-'+ Style.RESET_ALL)
print(Fore.LIGHTWHITE_EX + Style.BRIGHT +"              █████╗ ██╗  ██╗████████╗ █████╗ ██╗ ██████╗ ███╗   ██╗             "+ Style.RESET_ALL);
print(Fore.LIGHTWHITE_EX + Style.BRIGHT +"             ██╔══██╗██║ ██╔╝╚══██╔══╝██╔══██╗██║██╔═══██╗████╗  ██║             "+ Style.RESET_ALL);
print(Fore.LIGHTWHITE_EX + Style.BRIGHT +"             ███████║█████╔╝    ██║   ███████║██║██║   ██║██╔██╗ ██║             "+ Style.RESET_ALL);
print(Fore.LIGHTWHITE_EX + Style.BRIGHT +"             ██╔══██║██╔═██╗    ██║   ██╔══██║██║██║   ██║██║╚██╗██║             "+ Style.RESET_ALL);
print(Fore.LIGHTWHITE_EX + Style.BRIGHT +"             ██║  ██║██║  ██╗   ██║   ██║  ██║██║╚██████╔╝██║ ╚████║             "+ Style.RESET_ALL);
print(Fore.LIGHTWHITE_EX + Style.BRIGHT +"             ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝             "+ Style.RESET_ALL);
print(Fore.LIGHTWHITE_EX + Style.BRIGHT +" ██╗   ██╗███████╗██████╗ ███████╗██╗ ██████╗ ███╗   ██╗    ██████╗     ██████╗  "+ Style.RESET_ALL);
print(Fore.LIGHTWHITE_EX + Style.BRIGHT +" ██║   ██║██╔════╝██╔══██╗██╔════╝██║██╔═══██╗████╗  ██║    ╚════██╗   ██╔═████╗ "+ Style.RESET_ALL);
print(Fore.LIGHTWHITE_EX + Style.BRIGHT +" ██║   ██║█████╗  ██████╔╝███████╗██║██║   ██║██╔██╗ ██║     █████╔╝   ██║██╔██║ "+ Style.RESET_ALL);
print(Fore.LIGHTWHITE_EX + Style.BRIGHT +" ╚██╗ ██╔╝██╔══╝  ██╔══██╗╚════██║██║██║   ██║██║╚██╗██║    ██╔═══╝    ████╔╝██║ "+ Style.RESET_ALL);
print(Fore.LIGHTWHITE_EX + Style.BRIGHT +"  ╚████╔╝ ███████╗██║  ██║███████║██║╚██████╔╝██║ ╚████║    ███████╗██╗╚██████╔╝ "+ Style.RESET_ALL);
print(Fore.LIGHTWHITE_EX + Style.BRIGHT +"   ╚═══╝  ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝    ╚══════╝╚═╝ ╚═════╝  "+ Style.RESET_ALL);
print(Fore.WHITE+"                               M A I N - M E N U                                 "+ Style.RESET_ALL)
print(Fore.GREEN + 81 * '-'+ Style.RESET_ALL)
print(Fore.GREEN +'1:' + Fore.WHITE + ' Analyze Bro HTTP Sample Using Default Model                                   ' + Style.RESET_ALL),
print(Fore.GREEN +'2:' + Fore.WHITE + ' Analyze PCAP Sample Using Default Model',Fore.RED + "(Bro must be installed!)              " + Style.RESET_ALL),
print(Fore.GREEN +'3:' + Fore.WHITE + ' Analyze Bro HTTP Sample Using Phishing Model                                  ' + Style.RESET_ALL),
print(Fore.GREEN +'4:' + Fore.WHITE + ' Demo                                                                          '+ Style.RESET_ALL),
print(Fore.GREEN + 81 * '-'+ Style.RESET_ALL)

## Get input ###
choice = input(Fore.WHITE + 'Enter your choice' + Fore.GREEN + ' (1-4)'+ Fore.GREEN+':' + Style.RESET_ALL)
### Convert string to int type ##
choice = int(choice)

### Take action as per selected menu-option ###
if choice == 1:
    print("")
elif choice == 2:
    print("")
elif choice == 3:
    print("")
elif choice == 4:
    print("")
else:  ## default ##
    print(Fore.RED+"Invalid number. Try again..."+ Style.RESET_ALL)