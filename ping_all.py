#!/usr/bin/python3

import subprocess
import concurrent.futures

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def ping(host):
    return (subprocess.run(['ping', '-c', '1', '-w', '2', host], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode, host)

def main():
    print("Write list of hosts, each with new line. To end list enter a single dot\n.")
    ip_list = []
    s = ""
    while s != ".":
        s = input()
        ip_list.append(s)

    with concurrent.futures.ThreadPoolExecutor(80) as executor:
        results = [executor.submit(ping, ip) for ip in ip_list[:-1]]

        for t in concurrent.futures.as_completed(results):
            if t.result()[0] == 0:
                print(f'{bcolors.OKGREEN}OK\t| {t.result()[1]}{bcolors.ENDC}')
            else:
                print(f'{bcolors.FAIL}FAIL\t| {t.result()[1]}{bcolors.ENDC}') 

if __name__ == "__main__":
    main()
