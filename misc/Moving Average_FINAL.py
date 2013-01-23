from pandas import *


## Moving Average
def MovingAverage(Input,N):

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

    return df
    
    
# data set
data = [1,2,3,4,5,5,5,5,5,5,5,5,5,5,5]
result = MovingAverage(data,2)

print result
#print result.to_string() #if data is supressed


