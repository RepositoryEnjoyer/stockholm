
# Stockholm

This small proyect is an introduction to how ransomware works. Stockholm encrypts the contents of a directory, in this case named "infection", including subdirectories. It encrypts the exact same extensions affected by the Wannacry ransomware so files with no encryption
are safe.

You need python for the proyect to work and some modules to be installed but shouldn't be hard for you to find them.

# Options

 - -v to see the version of the program.
 - -r to decrypt the directory. It requires the '.key' file as an argument to work so try to not eliminate the file.
 - -h or --help for well... help.
 - -s or --silent to keep things quiet. It works with the rest of the flags.

Theoretically speaking, if you change the HOME directory of the user, the script will also work there as long as the "/infection" folder is also there but you shound't play with that. Obviously, the directory can be changed but since you don't want to mess with your own stuff, you shouldn't do it.

 
