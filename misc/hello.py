
##MaxRetries 
## Specifies the number of times a report server will retry a delivery if the first
## attempt does not succeed. The default value is 3.
## 
##SecondsBeforeRetry 
## Specifies the interval of time (in seconds) between each retry
## attempt. The default value is 900.
 




import pyodbc

cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=devdb4\sql4;DATABASE=BizIntel;Trusted_Connection=yes')
cursor = cnxn.cursor()

# Open file
f = open('sql.txt', 'r')
#print f.read()

##== For select statements ==##
cursor.execute(f.read())
row = cursor.fetchall()

##== Loop through all records, one at a time ==##
##for x in range(0, len(row)):
##    for y in range(0, len(row[x])):
##        print row[x][y]

##== Loop through all records, one row at a time ==##
##for x in range(0, len(row)):
##    print row[x]

##== Print first row ==##
##print row[0]

##== Print first value in first column ==##
##print row[0][0]

print row
