# -*- coding: utf-8 -*-
"""
Created on Sun Sep 10 14:03:25 2023

@author: Aviator
"""

import random
import time

def main():
    random.seed(time.time())
    while True:
        input('Press enter to roll the dice!')
        number = random.choice([x for x in range(1, 7)])
        if number == 6:
            print('Your number: ', number, '. Today is your lucky day!')
        else:
            print('Your number: ', number, '. Luck awaits you in the future!')
        
        inp = input('Wanna try again? Enter "Yes" or "No"\n')
        while not(inp.lower() in ['yes', 'no']):
            inp = input('Oopsie! I\'ve waited for something different. Try again\n')
        if inp.lower() == 'no':
            print('\nThanks for playing')
            break
        
        print('-------------------\n')
    

main()
