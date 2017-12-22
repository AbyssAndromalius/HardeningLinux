# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 10:29:42 2017

@author: abyss
"""

# Note : "if X is True" == if X, is True is optionnal but keept for my own understanding (if True = Success)  

Production = False

from valid import *
from randompass import *
import os
#import time
#import sys

def updateall():
    if Production == True :
        os.system('apt-get update')
        os.system('apt-get -y upgrade')
    else:
        print ("apt-get update")
        print ("apt-get -y upgrade")

def paquets():
    if Production == True :    
        os.system('apt-get -y install fail2ban lsof')
    else:
        print ('apt-get -y install fail2ban lsof')

def adduser():
    nbuser=int(input("How many users do you need to add ? (between 1 to 9) "))
    if nbuser > 0 and nbuser < 10: #CRASH if input is a string, to fix
        for x in range (0, nbuser):
            newuser=input("What is the name of the new account ? ")
            # WARNING NOT SECURE, CHANGE ASAP
            userpass = pass_generator()            
            # WARNING NOT SECURE, CHANGE ASAP    
            if Production == True :
                os.system('useradd '+newuser+' --create-home -s /bin/bash')
                os.system('mkdir /home/'+newuser+'/.ssh')
                os.system('touch /home/'+newuser+'/.ssh/authorized_keys')
                os.system('chown -R '+newuser+':'+newuser+' /home/'+newuser+'/.ssh')
                os.system('chmod 700 /home/'+newuser+'/.ssh')
                os.system('chmod 600 /home/'+newuser+'/.ssh/authorized_keys')
                os.system('echo '+newuser+':'+userpass+' | chpasswd')
                os.system('usermod -a -G sudo '+newuser+'')                               
                print ("!!! now use ssh-copy-id -i "+"${HOME}/.ssh/id_rsa.pub"+" "+newuser+":"+userpass+"@SERVER_IP")                
            else:
                print ('useradd '+newuser+' --create-home -s /bin/bash')
                print ('mkdir /home/'+newuser+'/.ssh')
                print ('touch /home/'+newuser+'/.ssh/authorized_keys')
                print ('chown -R '+newuser+':'+newuser+' /home/'+newuser+'/.ssh')
                print ('chmod 700 /home/'+newuser+'/.ssh')
                print ('chmod 600 /home/'+newuser+'/.ssh/authorized_keys')
                print ('echo '+newuser+':'+userpass+' | chpasswd')
                print ('usermod -a -G sudo '+newuser+'')   
                print ("!!! now use ssh-copy-id -i "+"${HOME}/.ssh/id_rsa.pub"+" "+newuser+":"+userpass+"@SERVER_IP")  
        
        input("IMPORTANT : Please add your public keys to the server NOW !")
        input("IMPORTANT : Please change your password NOW !")
        input("IMPORTANT : Last warning before shuting down root access")

    else :
        print ("Too many users or layer 8 issue, skipping")

# Let's start !

if doyouwant("update all your server") is True :
    updateall()
else : 
    print ("skipping update/upgrade")

if doyouwant("to setup hardening tools (fail2ban...)") is True :
    paquets()
else : 
    print ("skipping hardening tools (fail2ban...)")

if doyouwant("to add some users") is True :
    adduser()
else : 
    print ("skipping user creation")
    
print ("End of script !")



#useradd()

#paquets()