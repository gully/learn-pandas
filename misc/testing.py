from scipy.optimize import minimize
import numpy as np
from pandas import *

#----------------------------------------------------
#-------- Create Function ------------
#----------------------------------------------------
def MovingAverage(Input,N,test=0):
    
    # Create data frame
    df = DataFrame(Input, columns=['Revenue'])

    # Add columns
    df['CummSum'] = df['Revenue'].cumsum()
    df['Mavg'] = rolling_mean(df['Revenue'], N)
    df['Error'] = df['Revenue'] - df['Mavg']
    df['MFE'] = (df['Error']).mean()
    df['MAD'] = np.fabs(df['Error']).mean()
    df['MSE'] = np.sqrt(np.square(df['Error']).mean())
    df['TS'] = np.sum(df['Error'])/df['MAD']

    print N, df.MAD[0]

    if test == 0:
        return df.MAD[0]
    else: return df

#----------------------------------------------------
#-------- Input ------------
#----------------------------------------------------
data = [1,2,3,4,5,5,5,5,5,5,5,5,5,5,5]


#----------------------------------------------------
#-------- SOLVER ------------
#----------------------------------------------------

## Objective Function
fun = lambda x: MovingAverage(data, x[0])

## Contraints
cons = ({'type': 'ineq', 'fun': lambda x:  x[0] - 2}, # N>=2
        {'type': 'ineq', 'fun': lambda x:  len(data) - x[0]}) # N<=len(data)


## Bounds (note sure what this is yet)
bnds = (0,None)

## Solver
res = minimize(fun, 1, method='SLSQP', bounds=bnds, constraints=cons)

##print res
##print res.status
##print res.success
##print res.njev
##print res.nfev
##print res.fun
##for i in res.x:
##    print i
##print res.message
##for i in res.jac:
##    print i
##print res.nit

# print final results
result = MovingAverage(data,res.x,1)
print result

