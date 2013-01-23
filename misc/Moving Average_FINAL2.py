from pandas import *

#----------------------------------------------------
#-------- Create Function ------------
#----------------------------------------------------

## Moving Average
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

    if test == 0:
        return df.MAD[0]
    else: return df
    
#----------------------------------------------------
#-------- Input ------------
#----------------------------------------------------
    
# data set
data = [1,2,3,4,5,5,5,5,5,5,5,5,5,5,5]


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
result = MovingAverage(data,sol[0][0],1)

#print result
print result.to_string() #if data is supressed
