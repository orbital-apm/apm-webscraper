import psycopg2

con = psycopg2.connect(...)
cursor = con.cursor()

with open('json_template') as file:
    data = file.read()

query_sql = """
insert into table1 select * from
json_populate_record(NULL::table1, %s);
"""

cursor.execute(query_sql, (data,))
con.commit()
cursor.execute('select * from table1')
print(cursor.fetchall())