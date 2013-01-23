from xlwt import *

# Create a workbook
wb = Workbook()

# Add a sheet/tab
ws0 = wb.add_sheet('Picture_Test')

# Write text to cell at location (0,1)
ws0.write(0, 1, "Moving Average")

# Add picture at location (2,1)
# Note: Only accepts bmp files
# i.e. ws0.insert_bitmap('C:\Users\username\Desktop/test.bmp', 2, 1)
ws0.insert_bitmap('test.bmp', 2, 1)

# Write excel file
# Note: This will overwrite any other files with the same name
wb.save('hello.xls')




