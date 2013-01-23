from xlwt import *
from pandas import *
import numpy as np

# Create a dataframe with dates as your index
data = [1,2,3,4,5,6,7,8,9,10]
idx = date_range('1/1/2012', periods=10, freq='MS')
df = DataFrame(data, index=idx, columns=['Revenue'])


# Create a workbook
wb = Workbook()

# Add a sheet/tab
ws0 = wb.add_sheet('Picture_Test')
ws1 = wb.add_sheet('DataFrame_Test')

# Write text to cell at location (0,1)
ws0.write(0, 1, "Moving Average")

# Write dataframe
date_xf = easyxf(num_format_str='DD/MM/YYYY') # sets date format in Excel
num_xf = easyxf(num_format_str='#0.000000') # sets date format in Excel
for i, (date, row) in enumerate(df.T.iteritems()):
    print i, date, row[0],type(row[0]).__name__
    if type(date).__name__ == 'Timestamp':
        ws1.write(i,0,date,date_xf)
    elif type(date).__name__ == 'str':
        ws1.write(i,0,date)
    else:
        ws1.write(i,0,date.astype(np.float),num_xf)
    if type(row[0]).__name__ == 'Timestamp':
        ws1.write(i,1,row[0].astype(np.float),date_xf)
    elif type(row[0]).__name__ == 'str':
        ws1.write(i,1,row[0].astype(np.float))
    else:
        ws1.write(i,1,row[0].astype(np.float),num_xf)


# Add picture at location (2,1)
# Note: Only accepts bmp files
# i.e. ws0.insert_bitmap('C:\Users\username\Desktop/test.bmp', 2, 1)
ws0.insert_bitmap('test.bmp', 2, 1)

# Write excel file
# Note: This will overwrite any other files with the same name
wb.save('hello.xls')




