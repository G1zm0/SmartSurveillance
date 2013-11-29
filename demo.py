#!/usr/bin/python
# ---------------------------------------------------------------------------------------------
# Python / Skype4Py example that takes a skypename from command line parameter,
# checks if that skypename is in contact list and if yes then starts a call to that skypename.
#
# Tested with Skype4Py version 0.9.28.2 and Skype verson 3.5.0.214

import sys
import Skype4Py
import time
import os

# This variable will get its actual value in OnCall handler
CallStatus = 0

# Array with trusted MAC-addresses
trustedMacAddresses = ["B8:27:EB:98:04:68"]

# This is an array with the usernames of people to call
usernames = ["klaasmeun", "echo123"]
usernamesIndex = 0;

# Here we define a set of call statuses that indicate a call has been either aborted or finished
CallIsFinished = set ([Skype4Py.clsFailed, Skype4Py.clsFinished, Skype4Py.clsMissed, Skype4Py.clsRefused, Skype4Py.clsBusy, Skype4Py.clsCancelled]);

def AttachmentStatusText(status):
   return skype.Convert.AttachmentStatusToText(status)

def CallStatusText(status):
    return skype.Convert.CallStatusToText(status)

# This handler is fired when status of Call object has changed
def OnCall(call, status):
    global CallStatus
    CallStatus = status
    call.StartVideoSend()
    print 'Call int: ' + status
    print 'Call status: ' + CallStatusText(status)

# This handler is fired when Skype attatchment status changes
def OnAttach(status):
    print 'API attachment status: ' + AttachmentStatusText(status)
    if status == Skype4Py.apiAttachAvailable:
        skype.Attach()

# Returns a set with MAC-addresses in the network
def getMacAddresses():
    print 'Getting MAC-addresses'
    output = os.popen("sudo nmap -sP -n 192.168.0.0/24 | grep MAC")
    addresses = output.read().splitlines() #go from file to string, to list of strings
    
    #Cut out the MAC address portion, for every found MAC address
    for i in range(len(addresses)):
        addresses[i] = addresses[i][13:30]
        print addresses[i]
    return addresses

# Checks if a trusted MacAddress is connected to the network
def checkMacAddresses():
    macAddresses = getMacAddresses()
    for i in range(len(trustedMacAddresses)):
        if trustedMacAddresses[i] in macAddresses:
            print 'Trusted MAC address found'
            return 1
    print 'Mac address not found'
    return 0 
    

# Creating Skype object and assigning event handlers..
skype = Skype4Py.Skype()
skype.OnAttachmentStatus = OnAttach
skype.OnCallStatus = OnCall

# Starting Skype if it's not running already..
if not skype.Client.IsRunning:
    print 'Starting Skype..'
    skype.Client.Start()

# Attatching to Skype..
print 'Connecting to Skype..'
skype.Attach()

skype.PlaceCall(usernames[usernamesIndex])

breakFlag = 0;
alreadyDone = 1;

while (1):
    if CallStatus in CallIsFinished:
        if alreadyDone == 0:
            usernamesIndex += 1
            if(usernamesIndex >= len(usernames) or CallStatus == Skype4Py.clsFinished):
                breakFlag = 1
            else:
                print "Calling " + usernames[usernamesIndex]
                skype.PlaceCall(usernames[usernamesIndex])
                alreadyDone = 1
    else: 
        alreadyDone = 0
    if (breakFlag == 1):
        break

