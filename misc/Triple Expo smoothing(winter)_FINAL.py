from pandas import *


def TripleExponentialSmoothing(Input,N,Alpha,Beta,Gamma,Seasons):

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


    # Single Exponential Smoothing
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
    df['Error'] = df['Revenue'] - df['TripleExpo']
    df['MFE'] = (df['Error']).mean()
    df['MAD'] = np.fabs(df['Error']).mean()
    df['MSE'] = np.sqrt(np.square(df['Error']).mean())
    df['TS'] = np.sum(df['Error'])/df['MAD']

    return df


# Data set
y = [112,
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
#[randint(0,100) for r in xrange(10)]
print 'data: ',y


result = TripleExponentialSmoothing(y,len(y),0.5, 0.5, 0.5, 12)
#print result
print result.to_string() #if data is supressed
