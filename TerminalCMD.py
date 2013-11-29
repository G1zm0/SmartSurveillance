import os
output = os.popen("sudo nmap -sP -n 145.94.45.0/24 | grep MAC")
lines = output.read().splitlines() #go from file to string, to list of strings

print lines.pop()[13:30] #Print first three characters of the string
