import numpy as np
from pandas import *



## Moving Average
def MovingAverage(Input,N):
    WINDOW = N
    weightings = np.repeat(1.0, WINDOW) / WINDOW
    return np.convolve(Input, weightings)[WINDOW-1:-(WINDOW-1)]
    

data = [1,2,3,4,5,5,5,5,5,5,5,5,5,5,5]
#print MovingAverage(data,2)


# Create data frame
df = DataFrame(data, columns=['Revenue'])

# Add columns
df['CummSum'] = df['Revenue'].cumsum()
df['Mavg'] = rolling_mean(df['Revenue'], 2)
df['Error'] = df['Revenue'] - df['Mavg']
df['MFE'] = (df['Error']).mean()
df['MAD'] = np.fabs(df['Error']).mean()
df['MSE'] = np.sqrt(np.square(df['Error']).mean())
df['TS'] = np.sum(df['Error'])/df['MAD']

print df
#print df.to_string() #if data is supressed


