# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 16:16:44 2015

@author: rhmbp
"""

class find_amount(quantity, price):
    def __init__(self):
        pass
    
    def get_quantity(quantity):
        q = quantity * 4
        return q
        
    def get_price(price):
        #price per unit
        a = float(price)
        return a
        
    def final_answer(quantity, price):
         
         myQ = get_quantity(quantity)
         myP = get_price(price)
         
         final = myQ * myP
         
         return final
         
 #####################################################        
aNumber = find_amount()

print aNumber.final_answer(3, 1.5)   