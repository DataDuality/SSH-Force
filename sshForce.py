#!/usr/bin/python3

import argparse
import os
import sys
import subprocess
from time import sleep

logo = """\

███████╗███████╗██╗  ██╗      ███████╗ ██████╗ ██████╗  ██████╗███████╗
██╔════╝██╔════╝██║  ██║      ██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔════╝
███████╗███████╗███████║█████╗█████╗  ██║   ██║██████╔╝██║     █████╗
╚════██║╚════██║██╔══██║╚════╝██╔══╝  ██║   ██║██╔══██╗██║     ██╔══╝
███████║███████║██║  ██║      ██║     ╚██████╔╝██║  ██║╚██████╗███████╗
╚══════╝╚══════╝╚═╝  ╚═╝      ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚══════╝

"""
parser = argparse.ArgumentParser(description='This tool can be used to conduct a dictionary attack on an encrypted ssh private key')
parser.add_argument('-k', '--key', type=str, metavar='', required='True', help='Location of the encrypted ssh private key')
parser.add_argument('-w', '--wordlist', type=str, metavar='', required='True', help='Location of wordDlist to attack with')
parser.add_argument('-o', '--output', type=str, metavar='', required='True', help='Name of the decrypted file.')
args = parser.parse_args()

def failMarker():
    return "[\033[91m-\033[00m]"

def passMarker():
    return "[\033[92m+\033[00m]"

def startAttack(List):
    for each in List:
        if each == "":
            continue
        returnValue = subprocess.call("/usr/bin/openssl rsa -in {0} -out ./{1} -passin pass:\'{2}\' 2>/dev/null".format(args.key, args.output, each), shell=True)
        if returnValue == 0:
            print("\n"+passMarker() + " ATTEMPT: \"{0}\" is the password".format(each)+"\n")
            if (os.path.exists("./{0}".format(args.output))):
                print("\n*** Decrypted private key stored in \033[92m{0}\033[00m ***\n".format(args.output))
            return
        else:
            print(failMarker()+" ATTEMPT: \"{0}\" Failed".format(each))
    print("\n\033[91mNO PASSWORD WAS FOUND !\033[00m\n")
    return

def start():
    if (os.path.exists(args.key) and os.path.exists(args.wordlist)):
        with open(args.wordlist, 'r') as file:
            wordList = file.read().splitlines()
        print("\nTotal Passwords: " + str(len(wordList)) + "\n")
        sleep(3)
        startAttack(wordList)
    else:
        if (not(os.path.exists(args.key)) and not(os.path.exists(args.wordlist))):
            print("***\nFILE ERROR: Neither Key nor wordlist was found.\n***")
            sys.exit(0)
        else:
            print("***\nFILE ERROR: Key file not found\n***" if not(os.path.exists(args.key)) else "\n***FILE ERROR: Wordlist not found\n***")
            sys.exit(0)
    return

if __name__ == '__main__':
    print(logo)
    sleep(3)
    start()
    print("\nProgram Terminating . . .\n")
