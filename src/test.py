import sqlite3
from sqlite3 import Error
from zxcvbn import zxcvbn
import math

results = zxcvbn('JohnSmith123')

print(math.log2(results["guesses"]))


# try:
#     con = sqlite3.connect("db_file.db")
#
#     cursor = con.cursor()
#
#     table = '''
#             CREATE TABLE IF NOT EXISTS test (
#             username CHAR(20) NOT NULL,
#             password CHAR(1000)
#     )'''
#
#     table2 = '''
#             CREATE TABLE IF NOT EXISTS test2 (
#             username CHAR(20) NOT NULL,
#             password CHAR(1000)
#     )'''
#     cursor.execute(table)
#     cursor.execute(table2)
#
#     cursor.execute("INSERT INTO test VALUES(?,?)", ("lol", "password123"))
#
#     cursor.execute("INSERT INTO test2 VALUES(?,?)", ("loleeee", "password123sasasa"))
#
#     print("Saved database")
#     cursor.execute('''SELECT * FROM test''')
#     result = cursor.fetchall()
#     print(result)
#
#     cursor.execute('''SELECT * FROM test2''')
#     result = cursor.fetchall()
#     print(result)
#
#     con.commit()
#
#     try:
#         conn = sqlite3.connect(':memory:')
#         query = "".join(line for line in con.iterdump())
#         conn.executescript(query)
#         print("Inside memory database")
#         cursor.execute('''SELECT * FROM test''')
#         result = cursor.fetchall()
#         print(result)
#
#         cursor.execute('''SELECT * FROM test2''')
#         result = cursor.fetchall()
#         print(result)
#     except Error as e:
#         print(e)
#     finally:
#         if conn:
#             conn.close()
#
#     # cursor = con.cursor()
#     print(sqlite3.version)
# except Error as e:
#     print(e)
# finally:
#     if conn:
#         conn.close()