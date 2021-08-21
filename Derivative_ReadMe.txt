You can use this program to do analytical differentiation of any continuous function if its derivative is known.

->Adding a function into the function list:
Calc.Function_dic[<function name string>]=<function defination>

example
def exp(x):
	return pow(2.7183,x)
Calc.Function_dic["exp"]=exp

->Adding a function into the differentiable function list:
DerFn.Function_dic[<function name string>]=<function defination>

example
def exp(x):
	return Calc.const(2.7183)^x
DerFn.Function_dic["exp"]=exp

->Paring the string:
Calc.Parse(<Function String>)

example
s="exp(x)"
p=Calc.Parse(s,['x'])

->Evaluating a function value at a specific variable value:
<Parsed Function>.Evaluate(<Dictionary with variable char as key and variable's value as value>)

example
s="exp(x)"
p=Calc.Parse(s,['x'])
value=p.evaluate({x:2})#evaluating the function at x=2

->Finding derivative of the function:
Differentiate(<Parsed Function>,<with respect to variable char>)

example
s="exp(x)"
p=Calc.Parse(s,['x'])
dp=Diffentiate(p,'x')



