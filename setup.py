import sqlite3
import config

connection = sqlite3.connect(config.SQLITE3_DB_FILE_NAME)

cursor = connection.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS policies
              (id TEXT, policy TEXT, data TEXT, input TEXT)''')

connection.commit()

connection.close()