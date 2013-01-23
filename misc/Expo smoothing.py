'''
simple exponential smoothing
go back to last N values
y_t = a * y_t + a * (1-a)^1 * y_t-1 + a * (1-a)^2 * y_t-2 + ... + a*(1-a)^n * y_t-n
'''
from random import random,randint
from pandas import *

def gen_weights(a,N):
    ws = list()
    for i in range(N):
        w = a * ((1-a)**i)
        ws.append(w)
    return ws

def weighted(data,ws):
    wt = list()
    for i,x in enumerate(data):
        wt.append(x*ws[i])
    return wt

def SingleExponentialSmoothing(Input,N,Alpha):

    Num = N
    a = Alpha
    ws = gen_weights(a,Num)
    data = Input
    weighted_data = weighted(data,ws)

    print 'weights: ',ws
    print 'weighted data: ',weighted_data
    print 'weighted avg: ',sum(weighted_data)
    return sum(weighted_data)

y = [randint(0,100) for r in xrange(10)]
print 'data: ',y


SingleExponentialSmoothing(y,len(y),0.5)

# Create data frame
df = DataFrame(y, columns=['Revenue'])

# Add columns
df['CummSum'] = df['Revenue'].cumsum()
df['SingleExpo'] = ewma(df['Revenue'], span=2)
df['Error'] = df['Revenue'] - df['SingleExpo']
df['MFE'] = (df['Error']).mean()
df['MAD'] = np.fabs(df['Error']).mean()
df['MSE'] = np.sqrt(np.square(df['Error']).mean())
df['TS'] = np.sum(df['Error'])/df['MAD']

#print df
print df.to_string() #if data is supressed


