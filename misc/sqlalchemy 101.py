from sqlalchemy import *

# DB Parameters
ServerName = "devdb4\sql4"
Database = "BizIntel"

# Make sure pyobdc is installed
engine = create_engine('mssql+pyodbc://' + ServerName + '/' + Database)
conn = engine.connect()

# Required for querying tables
metadata = MetaData(conn)

# Table to query
tbl = Table("TableCheck", metadata, autoload=True, schema="dbo")


# select all where 
sql = select(tbl.c.ColumnName == 'operator_id_netsent')

# select specific columns
sql = select([tbl.c.DB, tbl.c.DataType, tbl.c.MaxLength])

# select top N
sql = select([tbl.c.DB, tbl.c.DataType, tbl.c.MaxLength],limit=10)

# select specific column and a where clause
sql = select([tbl.c.DB], tbl.c.ColumnName == 'operator_id_netsent')

# and, or, not, in
sql = select([tbl], and_(tbl.c.MaxLength < 4, tbl.c.MaxLength != 1))
sql = select([tbl], or_(tbl.c.MaxLength < 4, tbl.c.MaxLength != 1))
sql = select([tbl], not_(tbl.c.MaxLength > 4))
sql = select([tbl], tbl.c.MaxLength.in_( (1,4) ))

# like, between
sql = select([tbl], tbl.c.TableName.startswith('M'))
sql = select([tbl], tbl.c.TableName.like('%a%'))
sql = select([tbl], tbl.c.TableName.endswith('n'))
sql = select([tbl], tbl.c.MaxLength.between(30,39),limit=10)


result = conn.execute(sql)
for row in result:
    print row

# Close connection
conn.close()




