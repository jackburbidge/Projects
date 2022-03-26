'''
This set of classes contains standard methods that seem to be missing from
most libraries.
'''
import numpy as np


class standard:
    '''
    Methods that take floats or integers as inputs.
    '''
    @staticmethod
    def truncate(x, digits):
        '''
        A fuction that truncates a float to a given number of digits and returns
        a float.
        '''
        if type(x) == 'int':
            return x

        x = str(float(x))
        idx = x.find('.')
        return float(x[:idx + digits + 1])

class vector:
    '''
    Methods that take lists or arrays as inputs.
    '''
    @staticmethod
    def truncate(x, digits):
        '''
        A fuction that truncates a vector's objects to a given number of digits
        and returns a vector.
        '''

        return (np.array(x) * 10**digits).astype(int) / (10**digits)
