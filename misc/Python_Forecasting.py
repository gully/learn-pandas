from pandas import *
from scipy.optimize import minimize

#----------------------------------------------------
#-------- Create Functions ------------
#----------------------------------------------------

def MovingAverage(Input,N,test=0):

    # Create data frame
    df = DataFrame(Input, columns=['Revenue'])

    # Add columns
    df['CummSum'] = df['Revenue'].cumsum()
    df['Mavg'] = rolling_mean(df['Revenue'], N)
    df['MaError'] = df['Revenue'] - df['Mavg']
    df['MaMFE'] = (df['MaError']).mean()
    df['MaMAD'] = np.fabs(df['MaError']).mean()
    df['MaMSE'] = np.sqrt(np.square(df['MaError']).mean())
    df['MaTS'] = np.sum(df['MaError'])/df['MaMAD']

    if test == 0:
        return df.MaMAD[0]
    else: return df


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
    df['UnoError'] = df['Revenue'] - df['SingleExpo']
    df['UnoMFE'] = (df['UnoError']).mean()
    df['UnoMAD'] = np.fabs(df['UnoError']).mean()
    df['UnoMSE'] = np.sqrt(np.square(df['UnoError']).mean())
    df['UnoTS'] = np.sum(df['UnoError'])/df['UnoMAD']

    #print Alpha, df.UnoMAD[0]

    if test == 0:
        return df.UnoMAD[0]
    else: return df


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

    # Double Exponential Smoothing
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
    df['DosError'] = df['Revenue'] - df['DoubleExpo']
    df['DosMFE'] = (df['DosError']).mean()
    df['DosMAD'] = np.fabs(df['DosError']).mean()
    df['DosMSE'] = np.sqrt(np.square(df['DosError']).mean())
    df['DosTS'] = np.sum(df['DosError'])/df['DosMAD']

    #print a,b, df.DosMAD[0]

    if test == 0:
        return df.DosMAD[0]
    else: return df

def TripleExponentialSmoothing(Input,N,Alpha,Beta,Gamma,Seasons,test=0):

    # NOTE: Any multiplication done by 1.0 is to prevent numbers from getting rounded to int
    Num = N
    a = Alpha
    b = Beta
    c = Gamma
    s = Seasons

    # Create data frame
    df = DataFrame(Input, columns=['Revenue'])

    # Add Cummulative sums
    df['CummSum'] = df['Revenue'].cumsum()

    # Initial values for L
    '''  L = average of the first period (s)
           = (x1+x2+x3+...+xs) / s

             **start calculating L at time s
    '''
    df['L'] = df['Revenue'][:s].mean()
    df['L'][:s-1] = None #erase all values before period s

    # Initial values for b
    '''     b = (current value - first value) / ( period(s) - 1 )

             **start calculating b at time s
    '''
    df['b'] = 1.0*(df['Revenue'][s-1] - df['Revenue'][0]) / (s - 1)
    df['b'][:s-1] = None #erase all values before period s
   
    # Add initial seasonality for period s
    '''     s = (current value) / (average of the first period(s) )

             **only calculate for the first period s
    '''
    df['s'] = 1.0*df['Revenue'][:s-1]/df['Revenue'][:s].mean()

    # Initial value at time s-1
    # this is exactly the row after the previous "df['s'] =" statement 
    df['s'][s-1] = 1.0*df['Revenue'][s-1]/df['Revenue'][:s].mean()
    
    # Initial forecast = actual
    '''     It does not matter what number you set the initial forecast,
            we only do this to create the column
    '''
    df['TripleExpo'] = df['Revenue'][0]*1.0
    df['TripleExpo'][:s] = None #erase all values before and including period s


    # Triple Exponential Smoothing
    for i in range(Num):

        # We start at the end of period s
        if (i >= s):

            # Get the previous L and b
            LPrev = df['L'][i-1]
            bPrev = df['b'][i-1]
            #print LPrev, bPrev

            '''
                Eq1. L1 = alpha * (y1 /	S0) + (1 - alpha) * (L0 + b0)
                Eq2. b1 = beta * (L1 - L0) + (1 - beta) * b0
                Eq3. S1 = Gamma * (y1 / L1) + (1 - Gamma) * S0
                Eq4. F(1+m) = L1 + (b1 * S0)
            '''
            df['L'][i] = a * (df['Revenue'][i] / df['s'][i-s]) + (1 - a) * (LPrev + bPrev)
            df['b'][i] = b * (df['L'][i] - LPrev) + (1 - b) * bPrev
            df['s'][i] = c * (df['Revenue'][i] / df['L'][i]) + (1 - c) * df['s'][i-s]
            #print  df['L'][i], df['b'][i], df['s'][i]

            # forecast for period i
            df['TripleExpo'][i] = (df['L'][i-1] + df['b'][i-1]) * df['s'][i-s]
            #print df['TripleExpo'][i]


    # Track Errors
    df['TresError'] = df['Revenue'] - df['TripleExpo']
    df['TresMFE'] = (df['TresError']).mean()
    df['TresMAD'] = np.fabs(df['TresError']).mean()
    df['TresMSE'] = np.sqrt(np.square(df['TresError']).mean())
    df['TresTS'] = np.sum(df['TresError'])/df['TresMAD']

    #print a,b, df.TresMAD[0]

    if test == 0:
        return df.TresMAD[0]
    else: return df

    
#----------------------------------------------------
#-------- Input ------------
#----------------------------------------------------
    
# data set
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
#-------- Ghetto Solver ------------
#----------------------------------------------------

# Calculate the maximum number of iterations allowed (max = 10)
MaxIter = [10, len(data)/2]
#print MaxIter, min(MaxIter)

# Create array to hold N, f(N)
sol = []

# populate array
for i in range(min(MaxIter)):
    if i>1:
        sol.append([i,MovingAverage(data,i)])

#print sol
# Sort array on the f(N) column, ascending
# this will be the optimal solution
sol = sorted(sol, key=lambda x: x[1])

# Optimal solution = sol[0][0] = 1st value in 1st array   
MAresult = MovingAverage(data,sol[0][0],1)

#----------------------------------------------------
#-------- Single Exponential Solver ------------
#----------------------------------------------------

## Objective Function
Singlefun = lambda x: SingleExponentialSmoothing(data,len(data),x[0])

## Contraints
Singlecons = ({'type': 'ineq', 'fun': lambda x:  x[0] - 0.100}, # x - 0.1 >= 0
        {'type': 'ineq', 'fun': lambda x:  0.900 - x[0]}) # 0.9-x>=0


## Bounds (note sure what this is yet)
Singlebnds = (None,None)

## Solver
Singleres = minimize(Singlefun, 0.500, method='SLSQP', bounds=Singlebnds, constraints=Singlecons)

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
Singleresult = SingleExponentialSmoothing(data,len(data),Singleres.x,1)

#----------------------------------------------------
#-------- Double Exponential Solver ------------
#----------------------------------------------------

## Objective Function
Doublefun = lambda x: DoubleExponentialSmoothing(data,len(data),x[0],x[1])

## Contraints
Doublecons = ({'type': 'ineq', 'fun': lambda x:  x[0] - 0.01}, # x - 0.1 >= 0
        {'type': 'ineq', 'fun': lambda x:  0.99 - x[0]}, # 0.9-x>=0
        {'type': 'ineq', 'fun': lambda x:  x[1] - 0.01}, # x - 0.1 >= 0
        {'type': 'ineq', 'fun': lambda x:  0.99 - x[1]}) # 0.9-x>=0

## Bounds (note sure what this is yet)
Doublebnds = (None,None)

## Solver
Doubleres = minimize(Doublefun, (0.5,0.5), method='SLSQP', bounds=Doublebnds, constraints=Doublecons)

# print final results
Doubleresult = DoubleExponentialSmoothing(data,len(data),Doubleres.x[0],Doubleres.x[1],1)



#----------------------------------------------------
#-------- Triple Exponential Solver ------------
#----------------------------------------------------

## Objective Function
Triplefun = lambda x: TripleExponentialSmoothing(data,len(data),x[0],x[1],x[2],12)

## Contraints
Triplecons = ({'type': 'ineq', 'fun': lambda x:  x[0] - 0.01}, # x - 0.1 >= 0
        {'type': 'ineq', 'fun': lambda x:  0.99 - x[0]}, # 0.9-x>=0
        {'type': 'ineq', 'fun': lambda x:  x[1] - 0.01}, # x - 0.1 >= 0
        {'type': 'ineq', 'fun': lambda x:  0.99 - x[1]}, # 0.9-x>=0
        {'type': 'ineq', 'fun': lambda x:  x[2] - 0.01}, # x - 0.1 >= 0
        {'type': 'ineq', 'fun': lambda x:  0.99 - x[2]}) # 0.9-x>=0

## Bounds (note sure what this is yet)
Triplebnds = (None,None)

## Solver
Tripleres = minimize(Triplefun, (0.5,0.5,0.5), method='SLSQP', bounds=Triplebnds, constraints=Triplecons)

# print final results
Tripleresult = TripleExponentialSmoothing(data,len(data),Tripleres.x[0],Tripleres.x[1],Tripleres.x[2],12,1)


#----------------------------------------------------
#-------- Merge Results ------------
#----------------------------------------------------

pieces = [MAresult,
          Singleresult[['SingleExpo', 'UnoError', 'UnoMFE', 'UnoMAD', 'UnoMSE', 'UnoTS']],
          Doubleresult[['L', 'b', 'DoubleExpo', 'DosError', 'DosMFE', 'DosMAD', 'DosMSE', 'DosTS']],
          Tripleresult[['L', 'b', 's', 'TripleExpo', 'TresError', 'TresMFE', 'TresMAD', 'TresMSE', 'TresTS']]]
bigdata = concat(pieces,axis=1)


#print bigdata
print bigdata.to_string() #if data is supressed

