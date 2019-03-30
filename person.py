#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 22:07:44 2017

@author: fanchang
"""

class Person:
    def __init__(self, name, age, pay=0, job=None):
        self.name = name
        self.age = age
        self.pay = pay
        self.job = job      
        
    def lastName(self):
        return self.name.split()[-1]
    
    def giveRaise(self, percent):
        self.pay *= (1.0 + percent)
   
     
if __name__ == '__main__':
    bob = Person('Bob Smith', 42, 30000, 'Software')
    sue = Person('Sue Smith', 45, 40000, 'Hardware')
    print(bob.name, sue.pay)
    
    print(bob.name.split()[-1])
    sue.pay *= 1.10
    print(sue.pay)