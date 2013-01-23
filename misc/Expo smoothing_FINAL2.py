from scipy.optimize import minimize
import numpy as np
from pandas import *

#----------------------------------------------------
#-------- Create Function ------------
#----------------------------------------------------
def SingleExponentialSmoothing(Input,N,Alpha,test=0):

    # Create data frame
    df = DataFrame(Input, columns=['Revenue'])

    # Add Cummulative sums
    df['CummSum'] = df['Revenue'].cumsum()

    # Initial forecast = actual
    # we multiply by 1.0 to prevent numbers getting rounded to int
    df['SingleExpo'] = df['Revenue'][0]*1.0

    Num = N
    a = Alpha

    # Single Exponential Smoothing
    for i in range(Num):

        # We skip the first one since its a guess
        if (i > 0):

            # Get the previous value and previous forecast
            yPrev = df['Revenue'][i-1]
            fPrev = df['SingleExpo'][i-1]
            #print yPrev, fPrev

            # forecast for period i
            df['SingleExpo'][i] = a * yPrev + (1.0 - a) * fPrev
            #print df['SingleExpo'][i]


    # Track Errors
    df['Error'] = df['Revenue'] - df['SingleExpo']
    df['MFE'] = (df['Error']).mean()
    df['MAD'] = np.fabs(df['Error']).mean()
    df['MSE'] = np.sqrt(np.square(df['Error']).mean())
    df['TS'] = np.sum(df['Error'])/df['MAD']

    #print Alpha, df.MAD[0]

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
fun = lambda x: SingleExponentialSmoothing(data,len(data),x[0])

## Contraints
cons = ({'type': 'ineq', 'fun': lambda x:  x[0] - 0.100}, # x - 0.1 >= 0
        {'type': 'ineq', 'fun': lambda x:  0.900 - x[0]}) # 0.9-x>=0


## Bounds (note sure what this is yet)
bnds = (None,None)

## Solver
res = minimize(fun, 0.500, method='SLSQP', bounds=bnds, constraints=cons)

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
result = SingleExponentialSmoothing(data,len(data),res.x,1)
print result

