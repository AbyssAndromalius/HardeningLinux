# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 10:29:42 2017

@author: abyss
"""

#Let's break things and set that to True
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

def hardeningtools():
    if Production == True :    
        os.system('apt-get -y install fail2ban lsof')
    else:
        print ('apt-get -y install fail2ban lsof')
# Fail2ban configuration 
    if os.path.exists('/etc/fail2ban/jail.conf') :
        if os.path.exists('/etc/fail2ban/jail.local') is False :
            os.system('touch "/etc/fail2ban/jail.local"')
            #Edit configuration here            
            failconf = ("""
[ssh-ddos]
enabled = true 
[pam-generic] 
enabled = true
""")
            failfile = open('/etc/fail2ban/jail.local', 'a')
            failfile.write(failconf)            
            os.system('systemctl reload fail2ban.service')
            os.system('systemctl enable fail2ban.service')
    
def addsshusers():
    nbuser=int(input("How many users do you need to add ? (between 1 to 9) "))
    if nbuser > 0 and nbuser < 10: #CRASH if input is a string, to fix

     #y a surement moyen de faire ça plus propre que 512 ?
        if os.system('getent group ssh-users') == 512 & Production == True:
            print ("adding ssh-users group")            
            os.system('addgroup ssh-users')
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
                os.system('usermod -a -G ssh-users '+newuser+'')                               
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
                print ('usermod -a -G ssh-users '+newuser+'')
                print ("!!! now use ssh-copy-id -i "+"${HOME}/.ssh/id_rsa.pub"+" "+newuser+":"+userpass+"@SERVER_IP")
        input("IMPORTANT : Please add your public keys to the server NOW !")
        input("IMPORTANT : Please change your password NOW !")
        input("IMPORTANT : Last warning before shuting down root access")

## SSH Hardening (maybe I should write a function ?)
        if Production == True :
            os.system("sed -i -e 's/#?PermitRootLogin.*/PermitRootLogin no/g' '/etc/ssh/sshd_config'")
            os.system("sed -i -e 's/#?PasswordAuthentication yes/PasswordAuthentication no/g' '/etc/ssh/sshd_config'")
            os.system("sed -i -e 's/#?PubkeyAuthentication.*/PubkeyAuthentication yes/g' '/etc/ssh/sshd_config'")
            os.system("sed -i -e 's/#?UsePrivilegeSeparation.*/UsePrivilegeSeparation yes/g' '/etc/ssh/sshd_config'")
            sshconf = ("""
#Limit access to users of ssh-users
AllowGroups ssh-users
""")
            sshfile = open('/etc/ssh/sshd_config', 'a')
            sshfile.write(sshconf)
            os.system('systemctl reload sshd.service')
            os.system('systemctl enable sshd.service')
       
        else:
            print("sed -i -e 's/#?PermitRootLogin.*/PermitRootLogin no/g' '/etc/ssh/sshd_config'")
            print("sed -i -e 's/#?PasswordAuthentication yes/PasswordAuthentication no/g' '/etc/ssh/sshd_config'")
            print("sed -i -e 's/#?PubkeyAuthentication.*/PubkeyAuthentication yes/g' '/etc/ssh/sshd_config'")
            print("sed -i -e 's/#?UsePrivilegeSeparation.*/UsePrivilegeSeparation yes/g' '/etc/ssh/sshd_config'")
            sshconf = ("""
#Limit access to users of ssh-users
AllowGroups ssh-users
""")
            print ("will be added to /etc/ssh/sshd_config >>>"+sshconf )
            print ("Activation du service sshd + reboot sshd)
    else :
        print ("Too many users or layer 8 issue, skipping")

# Let's start !

if doyouwant("update all your server") :
    updateall()
else : 
    print ("skipping update/upgrade")

if doyouwant("to setup & configure hardening tools (fail2ban)") :
    hardeningtools()
else : 
    print ("skipping hardening tools (fail2ban)")

if doyouwant("to add some users and manage SSH") :
    addsshusers()
else : 
    print ("skipping user creation")
    
print ("End of script !")



##### TODO /etc/init.d/fail2ban restart + chkconfig