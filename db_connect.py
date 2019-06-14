import pymysql
import json

# Open json file
file = open('uff_api.json', 'r')
file = json.load(file)

# Open database connection
db = pymysql.connect("localhost", "root", "", "uffinder")

# prepare a cursor object using cursor() method
cursor = db.cursor()

for dept in file:
    lectures = dept['disciplinas']
    for lect in lectures:
        # Prepare SQL query to INSERT a record into the database.
        query_1 = """
            INSERT INTO DISCIPLINES(cod, name)
            VALUES (%s, %s)
            """

        try:
            # Execute the SQL command
            cursor.execute(query_1, (lect['codigo'], lect['nome']))
            # Commit your changes in the database
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()

        query_2 = """
            INSERT INTO CLASSES(num, idDisc)
            VALUES (%s,
                (
                SELECT id from DISCIPLINES
                WHERE cod = %s
                )
            )
            """

        try:
            # Execute the SQL command
            cursor.execute(query_2, (lect['turma'], lect['codigo']))
            # Commit your changes in the database
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()

        # disconnect from server
db.close()
