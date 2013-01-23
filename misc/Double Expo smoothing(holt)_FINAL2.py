from scipy.optimize import minimize
import numpy as np
from pandas import *

#----------------------------------------------------
#-------- Create Function ------------
#----------------------------------------------------
def DoubleExponentialSmoothing(Input,N,Alpha,Beta,test=0):

    # Create data frame
    df = DataFrame(Input, columns=['Revenue'])

    # Add Cummulative sums
    df['CummSum'] = df['Revenue'].cumsum()

    # Initial vallues for L and b
    df['L'] = df['Revenue'][0]*1.0
    df['b'] = 0.0

    # Initial forecast = actual
    # we multiply by 1.0 to prevent numbers getting rounded to int
    df['DoubleExpo'] = df['Revenue'][0]*1.0

    Num = N
    a = Alpha
    b = Beta

    # Single Exponential Smoothing
    for i in range(Num):

        # We skip the first one since its a guess
        if (i > 0):

            # Get the previous L and b
            LPrev = df['L'][i-1]
            bPrev = df['b'][i-1]
            #print LPrev, bPrev

            df['L'][i] = a * df['Revenue'][i] + (1.0 - a) * (LPrev + bPrev)
            df['b'][i] = b * (df['L'][i] - LPrev) + (1 - b) * bPrev

            # We skip the first two
            if (i > 1):
                # forecast for period i
                df['DoubleExpo'][i] = df['L'][i] + df['b'][i]
                #print df['DoubleExpo'][i]


    # Track Errors
    df['Error'] = df['Revenue'] - df['DoubleExpo']
    df['MFE'] = (df['Error']).mean()
    df['MAD'] = np.fabs(df['Error']).mean()
    df['MSE'] = np.sqrt(np.square(df['Error']).mean())
    df['TS'] = np.sum(df['Error'])/df['MAD']

    #print a,b, df.MAD[0]

    if test == 0:
        return df.MAD[0]
    else: return df

#----------------------------------------------------
#-------- Input ------------
#----------------------------------------------------
data = [112,
118,
132,
129,
121,
135,
148,
148,
136,
119,
104,
118,
115,
126,
141,
135,
125,
149,
170,
170,
158,
133,
114,
140,
145,
150,
178,
163,
172,
178,
199,
199,
184,
162,
146,
166,
171,
180,
193,
181,
183,
218,
230,
242,
209,
191,
172,
194,
196,
196,
236,
235,
229,
243,
264,
272,
237,
211,
180,
201,
204,
188,
235,
227,
234,
264,
302,
293,
259,
229,
203,
229,
242,
233,
267,
269,
270,
315,
364,
347,
312,
274,
237,
278,
284,
277,
317,
313,
318,
374,
413,
405,
355,
306,
271,
306
]


#----------------------------------------------------
#-------- SOLVER ------------
#----------------------------------------------------

## Objective Function
fun = lambda x: DoubleExponentialSmoothing(data,len(data),x[0],x[1])

## Contraints
cons = ({'type': 'ineq', 'fun': lambda x:  x[0] - 0.01}, # x - 0.1 >= 0
        {'type': 'ineq', 'fun': lambda x:  0.99 - x[0]}, # 0.9-x>=0
        {'type': 'ineq', 'fun': lambda x:  x[1] - 0.01}, # x - 0.1 >= 0
        {'type': 'ineq', 'fun': lambda x:  0.99 - x[1]}) # 0.9-x>=0

## Bounds (note sure what this is yet)
bnds = (None,None)

## Solver
res = minimize(fun, (0.5,0.5), method='SLSQP', bounds=bnds, constraints=cons)

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
result = DoubleExponentialSmoothing(data,len(data),res.x[0],res.x[1],1)
#print result
print result.to_string() #if data is supressed

