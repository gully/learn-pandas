from sqlalchemy import *
from datetime import datetime, date, time
from pandas import *
from scipy.optimize import minimize
import numpy as np
from xlwt import *
import matplotlib.pyplot as plt
from PIL import Image
import os

#----------------------------------------------------
#-------- SQL Section ------------
#----------------------------------------------------

# Parameters
ServerName = "devdb4\sql4"
Database = "BizIntel"
StartDate = date(2011, 1, 1)
EndDate = date(2012, 10, 31)

# Make sure pyobdc is installed
engine = create_engine('mssql+pyodbc://' + ServerName + '/' + Database)
conn = engine.connect()

# Required for querying tables
metadata = MetaData(conn)

# Tables to query
TableName = "RPT_GA_AccountingSummary"

# Table to query
tbl = Table(TableName, metadata, autoload=True, schema="dbo")

# select Market, BillDate, Revenue WHERE BillDate>= StartDate and BillDate < EndDate
sql = select([literal("GA").label("Market"),tbl.c.BillDate,tbl.c.Revenue], and_(tbl.c.BillDate >= StartDate,tbl.c.BillDate < EndDate))
result = conn.execute(sql)

dataDF = DataFrame(data=list(result))#result.fetchall())
dataDF.columns = result.keys()
dataDF = dataDF.set_index('BillDate', drop=True)
dataDF['Revenue'] = -1*dataDF['Revenue'].astype(np.float64)
#dataDF = dataDF.ix[:10]
#print dataDF.head()

Monthly = dataDF.resample('MS', how={'Market': 'first', 'Revenue': 'sum'}, closed='left', label='left')
#print Monthly.head()

# Close connection
conn.close()


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
data = []
data = list(Monthly['Revenue'])
#print data


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

bigdata = bigdata.set_index(Monthly.index)

#print bigdata
#print bigdata.to_string() #if data is supressed

#----------------------------------------------------
#-------- Create Plots ------------
#----------------------------------------------------

# Convert png to bmp
def ConvertImg(file_in,file_out):
    img = Image.open(file_in)

    #print len(img.split())  # test
    if len(img.split()) == 4:
        # prevent IOError: cannot write mode RGBA as BMP
        r, g, b, a = img.split()
        img = Image.merge("RGB", (r, g, b))
        img.save(file_out)
    else:
        img.save(file_out)

plot1 = bigdata[['Revenue','Mavg']].plot()
plt.savefig('MApng.png')
ConvertImg('MApng.png', 'MA.bmp')

plot2 = bigdata[['Revenue','SingleExpo']].plot()
plt.savefig('Singlepng.png')
ConvertImg('Singlepng.png', 'Single.bmp')

plot3 = bigdata[['Revenue','DoubleExpo']].plot()
plt.savefig('Doublepng.png')
ConvertImg('Doublepng.png', 'Double.bmp')

plot3 = bigdata[['Revenue','TripleExpo']].plot()
plt.savefig('Triplepng.png')
ConvertImg('Triplepng.png', 'Triple.bmp')

# Delete temp files
os.remove('MApng.png')
os.remove('Singlepng.png')
os.remove('Doublepng.png')
os.remove('Triplepng.png')

#----------------------------------------------------
#-------- Excel Output ------------
#----------------------------------------------------

# Get today's date
CurrentTime = datetime.now()
CurrentTime = CurrentTime.strftime("%Y-%m-%d_%H-%M-%S")

# Create a workbook
wb = Workbook()

# Add a sheet/tab
ws = wb.add_sheet('Forecast Summary')
ws0 = wb.add_sheet('MovingAverage')
ws1 = wb.add_sheet('Single')
ws2 = wb.add_sheet('Double')
ws3 = wb.add_sheet('Triple')

# Formatting
bold_xf = easyxf('font: bold on')
num_xf = easyxf(num_format_str='$#,##0.00') # sets currency format in Excel

# Write text to cell
for i, col in enumerate(bigdata[['Mavg','SingleExpo','DoubleExpo','TripleExpo']].columns):
    #print i, col
    ws.write(0, i, col, bold_xf)

forecasts = bigdata[['Mavg','SingleExpo','DoubleExpo','TripleExpo']].ix[-1].T.iteritems()
for i, (a,b) in enumerate(forecasts):
    #print i, a,b
    ws.write(1, i, b, num_xf)


# Add picture at location (2,1)
# Note: Only accepts bmp files
# i.e. ws0.insert_bitmap('C:\Users\username\Desktop/test.bmp', 2, 1)
ws0.insert_bitmap('MA.bmp', 2, 1)
ws1.insert_bitmap('Single.bmp', 2, 1)
ws2.insert_bitmap('Double.bmp', 2, 1)
ws3.insert_bitmap('Triple.bmp', 2, 1)

# Write excel file
# Note: This will overwrite any other files with the same name
wb.save('hello.xls')

# Delete temp files
os.remove('MA.bmp')
os.remove('Single.bmp')
os.remove('Double.bmp')
os.remove('Triple.bmp')
