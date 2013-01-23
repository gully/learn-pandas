from pandas import *



def SingleExponentialSmoothing(Input,N,Alpha):

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

    return df


# Data set
y = [200,215,210,220,230,220,235,215,220,210] 
#[randint(0,100) for r in xrange(10)]
print 'data: ',y


result = SingleExponentialSmoothing(y,len(y),0.70)
#print result
print result.to_string() #if data is supressed
