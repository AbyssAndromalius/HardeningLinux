# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 10:29:42 2017

@author: abyss
"""

def valid_yesno(entry):
    yes = {'yes','y', 'ye'}
    no = {'no','n',''}    
    if entry in yes:
        return True
    elif entry in no:
        return False
    else : 
        print ("Layer 8 issue, skipping")
        return False            

def doyouwant(whattodo):
    entry=input("Do you want to "+whattodo+"? (y/N)").lower()        
    if valid_yesno(entry) is True :
        return True
