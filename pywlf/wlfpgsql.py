import psycopg2


def execute_pgsql(sql):
    conn = psycopg2.connect(host='192.168.19.41',
                            user='root',
                            password='ylkj@123',
                            database='zhfq_gw',
                            port='5432')
    cursor = conn.cursor()
    cursor.execute(sql)
    sqlResult = cursor.fetchall()
    cursor.close()
    conn.close()
    return sqlResult