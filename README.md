# SI-Unit conversion

Django App implementing a method to take an expression
in non-SI units and return a JSON object with the equivalent
expression in SI units and the conversion factor.

When deployed to a server, use

address_of_server/units/si?units=expression

to convert expression and compute the conversion factor.
