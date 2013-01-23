from sqlalchemy import *
from pandas import *

#----------------------------------------------------
#-------- Write to SQL ------------
#----------------------------------------------------

# DB Parameters
ServerName = "devdb4\sql4"
Database = "BizIntel"
TableName = "#TableCheckTest"

# pyobdc must be installed
engine = create_engine('mssql+pyodbc://' + ServerName + '/' + Database)
conn = engine.connect()

# Required for querying tables
metadata = MetaData(conn)

## Create table
    # To create a temp table just add a "#" to the table name
    # To create a global table just add a "##" to the table name
tbl = Table(TableName, metadata,
    Column('DateAdded', DateTime),
    Column('Revenue', Integer)
)

# This actually creates a table in the sql database
# checkfirst=True >> create if table does not exist
tbl.create(checkfirst=True)

# Create data to insert into table
# Create a dataframe with dates as your index
data = [1,2,3,4,5,6,7,8,9,10]
idx = date_range('1/1/2012', periods=10, freq='MS')
df = DataFrame(data, index=idx, columns=['Revenue'])

# Remove the index if you want to include it in the insert
df = df.reset_index()
#print df

# Iterate through each of the columns and insert into table
for x in df.iterrows():
    #print list(x[1])
    sql = tbl.insert(list(x[1]))
    conn.execute(sql)

# select all form table
sql = tbl.select()
result = conn.execute(sql)
for row in result:
    print 'Write to SQL', row

#----------------------------------------------------
#-------- Read from SQL ------------
#----------------------------------------------------

## Syntax to query an existing table
##tbl = Table(TableName, metadata, autoload=True, schema="dbo")
##tbl.create(checkfirst=True)

# select all where 
sql = select(tbl.c.DateAdded == '1/1/2012')

# select specific columns
sql = select([tbl.c.DateAdded, tbl.c.Revenue])

# select top N
sql = select([tbl.c.DateAdded, tbl.c.Revenue],limit=5)

# select specific column and a where clause
sql = select([tbl.c.Revenue], tbl.c.Revenue == 1)

# and, or, not, in
sql = select([tbl], and_(tbl.c.Revenue < 4, tbl.c.Revenue != 1))
sql = select([tbl], or_(tbl.c.Revenue < 4, tbl.c.Revenue != 1))
sql = select([tbl], not_(tbl.c.Revenue > 4))
sql = select([tbl], tbl.c.Revenue.in_( (1,4) ))

# like, between
sql = select([tbl], tbl.c.Revenue.startswith('M'))
sql = select([tbl], tbl.c.Revenue.like('%a%'))
sql = select([tbl], tbl.c.Revenue.endswith('n'))
sql = select([tbl], tbl.c.Revenue.between(1,10),limit=10)

# run sql code
result = conn.execute(sql)

# Insert to a dataframe
df2 = DataFrame(data=list(result), columns=result.keys())

# Convert data types 
df2.DateAdded = df2.DateAdded.astype('datetime64')
df2.Revenue = df2.Revenue.astype('int')
print ' '
print 'Data Types'
print df2.dtypes

# Set index to dataframe
df2 = df2.set_index('DateAdded')
print ' '
print 'Read from SQL', df2
#print df2.head().to_string()

# Close connection
conn.close()















