import conversion as co
import unittest
import json
import math


class Test_Conversion(unittest.TestCase):
    """
    This class tests the  convert method defined in conversion.py
    
    It consists of three different tests.
    
    test_valid_convert tests four different valid examples and check whether the output is correct.

    test_wrong_brackets_convert tests if our method returns an error if the brackets of the input are not
    valid.
    
    test_illegal_units_convert tests if the convert method correctly deals with input containing expression
    that do not represent valid units.
    """
    def test_valid_convert(self):
        """tests four valid input strings of increasing complexity"""
        simple = 't'
        sol_simple = json.dumps({'units': 'kg', 'multiplication_factor': 1000})

        medium = 't*degree/ha'
        factor_medium = co._round_sig(1000 * (math.pi / 180) / 10000)
        sol_medium = json.dumps({'units': 'kg*rad/m^2', 'multiplication_factor': factor_medium})

        hard = 'ha*degree/(h*min/degree)'
        factor_hard = co._round_sig(10000 * math.pi / 180 / (3600 * 60 / (math.pi / 180)))
        sol_hard = json.dumps({'units': 'm^2*rad/(s*s/rad)', 'multiplication_factor': factor_hard})

        very_hard = 'ha/(t/(hour*min/(degree)*d)*\")'
        factor_very_hard = co._round_sig(10000 / (1000 / (3600 * 60 / (math.pi / 180) * 86400) * math.pi / 648000))
        sol_very_hard = json.dumps({'units': 'm^2/(kg/(s*s/(rad)*s)*rad)', 'multiplication_factor':  factor_very_hard})
        
        self.assertEqual(co.convert(simple), sol_simple)
        self.assertEqual(co.convert(medium), sol_medium)
        self.assertEqual(co.convert(hard), sol_hard)
        self.assertEqual(co.convert(very_hard), sol_very_hard)
        
    def test_wrong_brackets_convert(self):
        """tests if too few open or too many open brackets are correctly recognized"""
        too_many_open = '(degree*h)/(ha*(ha)'
        too_few_open = 'degree/(ha)*h)'
        self.assertEqual(co.convert(too_many_open), "Too many open brackets.")
        self.assertEqual(co.convert(too_few_open), "Too few open brackets.")

    def test_illegal_units_convert(self):
        """tests if illegal expressions are correctly recognized"""
        illegal_unit = 'blah'
        self.assertEqual(co.convert(illegal_unit), 'Invalid expression blah')


suite = unittest.TestLoader().loadTestsFromTestCase(Test_Conversion)
unittest.TextTestRunner(verbosity=2).run(suite)
