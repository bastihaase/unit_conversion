"""SI Conversion

This module processes an input expression of non-SI units
and returns a JSON object that contains
the same expression in SI units and the conversion factor.


Example:
        

Attributes:
    unit_table (dict): A dictionary whose keys correspond to all non-SI
                       units that we consider. To each such key,
                       we associate a list of two elements containing
                       a string representing the SI unit and
                       the conversion factor
    si_set (set): A set of all SI units that correspond to the non-SI units
                  This allows us to evaluate mixed expressions where some
                  units are SI and some are not
"""

import re
import math
import json

unit_table = {'L': ['m^3', 1000],
              'litre': ['m^3', 1000],
              'h': ['s', 3600],
              'hour': ['s', 3600],
              'min': ['s', 60],
              'minute': ['s', 60],
              'd': ['s', 86400],
              u"\u00b0": ['rad', math.pi / 180],
              'degree': ['rad', math.pi / 180],
              '\'': ['rad', math.pi / 108000],
              '\"': ['rad', math.pi / 648000],
              'second': ['rad', math.pi / 648000],
              'ha': ['m^2', 10000],
              'hectar': ['m^2', 10000],
              't': ['kg', 1000],
              'tonne': ['kg', 1000]}

si_set = set(['m', 's', 'rad', 'kg', 'm^2', 'm^3'])

def convert(expression):
    """ Given an expression of non-SI units, returns JSON containing SI expression and conversion factor

    As we walk through the string, we use two variables to
    determine whether the current unit is on
    the numerator or denominator of the simplified expression.
    We interpret /() as a fraction
    To give an example:
                    a/(b*c/(d/e))
    We have:
            expression    level
                a           1
                b           2
                c           2
                d           3
                e           3
    If we simplify the expression, we see that odd levels end up in
    the numerator, while even levels end up in the denominator
                  (a*d/e)/(b*c)

    Args:
        expression (str): Non SI-unit expression.
    
    Returns:
        json_si (JSON): JSON object with attributes "unit"
                        and "multiplication_factor".
                        "unit" contains the equivalent of the
                        input expression with SI units
                        while 'multiplication_factor'
                        contains the conversion factor.
    """
    # split string into SI-Units, brackets and operands
    # we use strip to remove white space
    l = [x.strip() for x in re.split(r"(/\(|\(|\)|\*|/)", expression) if x]

    # Setup variables
    last_operation = '*'
    multiplier = 1
    level = 1
    brackets = []

    for i in range(len(l)):
        # if it is a non-SI unit, convert it
        if l[i] in unit_table:
            l[i], factor = unit_table[l[i]]
            multiplier *= _determine_factor(level, last_operation, factor)
        # check if it is operands or bracket
        elif l[i] == '/(':
            level += 1
            last_operation = '*'
            brackets.append(l[i])
        elif l[i] == '/':
            last_operation = '/'
        elif l[i] == '*':
            last_operation = '*'
        elif l[i] == '(':
            brackets.append(l[i])
        elif l[i] == ')':
            if brackets == []:
                return "Too few open brackets."
            else:
                if brackets.pop() == '/(':
                    level -= 1
        # If it is not an SI unit, then the expression is invalid
        elif l[i] not in si_set:
            return "Invalid expression " + l[i]
    if brackets != []:
        return "Too many open brackets."

    # prepare output as JSON
    si = {"units": "".join(l), "multiplication_factor": _round_sig(multiplier)}
    json_si = json.dumps(si)

    return json_si


def _determine_factor(level, last_operation, factor):
    """ determines whether the conversion factor should be multiplied or divided by factor
    
    The function reads three inputs from the command line:
    input file, output file and a file containing a single
    integer, the percentile value. It checks that there are
    enough arguments and passes them on to the reader.
    
    Args:
        level (int): integer describing on which level the fraction of the
                     expression we are.
                     After simplification, factors with an odd level
                     are in the numerator and factors with an even level
                     are in the denominator
        last_operation (str):  str that is either "/" or "*"
        factor (float): conversion factor
    
    Returns:
            factor or 1/factor depending on level and last_operation_operation
    """
    if last_operation == '*' and level % 2 == 1:
        return factor
    elif last_operation == '*' and level % 2 == 0:
        return 1 / factor
    elif last_operation == '/' and level % 2 == 0:
        return factor
    elif last_operation == '/' and level % 2 == 1:
        return 1 / factor
    else:
        return -1


def _round_sig(x, sig=14):
    """ rounding x to 14 significant places
    
    Args:
        x (float): the float to be rounded
    Returns:
        sig (int): number of significant places
                   default = 14
    """
    return round(x, sig-int(math.floor(math.log10(abs(x))))-1)
