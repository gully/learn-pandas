from scipy.optimize import minimize

## Objective Function
fun = lambda x: -1*(2*x[0] + 3*x[1])

## Contraints
#Equality constraint means that the constraint function result is to be zero

#equality contraints have to be in the form:
# This is not in the correct format: x = -2
# Make contraint greater than zero: x + 2 = 0

#-------------------------------------------------------------

#whereas inequality means that it is to be non-negative.

#inequality contraints have to be in the form:
# This is not in the correct format: 2x+y<=15
# Make contraint greater than zero: 0 <= 15 + -2x + -y 
cons = ({'type': 'ineq', 'fun': lambda x:  15 + -2*x[0] + -1*x[1]}, #15-2x-y>=0
         {'type': 'ineq', 'fun': lambda x: 20 + -1*x[0] + -3*x[1]}, #20-x-3y
         {'type': 'ineq', 'fun': lambda x: x[0]}, #x>=0
         {'type': 'ineq', 'fun': lambda x: x[1]}) #y>=0

## Bounds
bnds = ((None, None), (None, None))

## Solver
res = minimize(fun, (0, 0), method='SLSQP', bounds=bnds, constraints=cons)

print res
print res.status
print res.success
print res.njev
print res.nfev
print res.fun
for i in res.x:
    print i
print res.message
for i in res.jac:
    print i
print res.nit


##
##Max C = 2x + 3y
##
##constraints
##2x+y<=15
##x+3y<=20
##x>=0
##y>=0

##
##ans = (5,5)
