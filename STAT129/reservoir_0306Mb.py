import random
from random import randrange
import unittest


def rsample(stream, size=10):
    """
    Produce a simple random sample with `size` elements from `stream`
    """
    # TODO: Replace pass below with the actual code to implement reservoir sampling.
    # That's your assignment.
    # Then show that it works on the test cases and in the case described in the assignment.
    
    #fill reservoir and sample
    reservoir = list()
    i = 0
    for eleInStrm in stream:
        if i < size:
            reservoir.append(eleInStrm)
        else:
            des = random.choice(range(i))
            if des < size:
                reservoir[des] = eleInStrm
        i += 1
    return reservoir

class rsampleTest(unittest.TestCase):
    
    def test_defaults(self):
        s = rsample(range(20))
        self.assertEqual(len(s), 10)
        
    def test_too_small_input(self):
        d = range(5)
        s = rsample(d)
        self.assertEqual(set(s), set(d))

    def test_string(self):
        letters = 'abcdefghijklmnopqrstuvwxyz'
        s = rsample(letters, 26)
        self.assertEqual(set(s), set(letters))

prin = rsample(range(1000))
print(prin)