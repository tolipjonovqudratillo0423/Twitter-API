
import random 
import string

def create_code(chars = string.digits,size = 6):
        
        return ''.join(random.choice(chars) for _ in range(size))


print(create_code())