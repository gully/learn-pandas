from pandas import *


def DoubleExponentialSmoothing(Input,N,Alpha,Beta,Gamma,Seasons):

    Num = N
    a = Alpha
    b = Beta
    c = Gamma
    s = Seasons

    # Create data frame
    df = DataFrame(Input, columns=['Revenue'])

    # Add Cummulative sums
    df['CummSum'] = df['Revenue'].cumsum()

    # Initial vallues for L and b
    df['L'] = df['Revenue'].mean()
    df['b'] = (df['Revenue'][1*s] - df['Revenue'][0]) / s

    # Add seasonality column
    df['season'] = 1.0*df['Revenue']/df['Revenue'].mean()

    # Initial vallues for s
    df['s'] = df['season'][(1*s)]

    # Initial forecast = actual
    # we multiply by 1.0 to prevent numbers getting rounded to int
    df['DoubleExpo'] = df['Revenue'][0]*1.0


    # Single Exponential Smoothing
    for i in range(Num):

        # We skip the first one since its a guess
        if (i > s):

            # Get the previous L and b
            LPrev = df['L'][i-1]
            bPrev = df['b'][i-1]
            #print LPrev, bPrev

            df['L'][i] = a * (df['Revenue'][i] / df['season'][i-1]) + (1 - a) * (LPrev + bPrev)
            df['b'][i] = b * (df['L'][i] - LPrev) + (1 - b) * bPrev
            df['s'] = c * (df['Revenue'][i] / df['L'][i]) + (1 - c) * df['s'][i-1]

            # We skip the first two
            if (i > 1):
                # forecast for period i
                df['DoubleExpo'][i] = (df['L'][i-1] + df['b'][i-1]) * df['s'][i-1]
                #print df['DoubleExpo'][i]


    # Track Errors
    df['Error'] = df['Revenue'] - df['DoubleExpo']
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
166
] 
#[randint(0,100) for r in xrange(10)]
print 'data: ',y


result = DoubleExponentialSmoothing(y,len(y),0.5, 0.5, 0.5, 12)
#print result
print result.to_string() #if data is supressed
