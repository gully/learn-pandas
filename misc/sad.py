
##MaxRetries 
## Specifies the number of times a report server will retry a delivery if the first
## attempt does not succeed. The default value is 3.
## 
##SecondsBeforeRetry 
## Specifies the interval of time (in seconds) between each retry
## attempt. The default value is 900.
 




import pyodbc

UserName = 'INFINITEENERGY\bizintelreports' #'INFINITEENERGY\hdrojas'
PassWord = 'GatorGreen1'

#cnxn = pyodbc.connect('DRIVER={SQL Server Native Client 10.0};SERVER=devdb4\sql4;DATABASE=BizIntel;UID=' + UserName + ';PWD='+ PassWord + ';')
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=devdb4\sql4;DATABASE=BizIntel;Trusted_Connection=yes')
cursor = cnxn.cursor()

##== For select statements ==##
#cursor.execute("select top 10 * FROM ReportServer.dbo.ExecutionLog")
#row = cursor.fetchall()

##== For stored procedures ==##
## Make sure to add the following line to the begining of your stored proc "SET NOCOUNT ON;"
## Without this you will get an error
args = (2,1)
cursor.execute("{call dbo.SSRS_Summary(?, ?)}", args)
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
print row[0][0]
