from werkzeug.security import generate_password_hash

class CreateAccount:

    def check_user(db, user):
        cursor = db.connection.cursor()
        cursor.execute(f"""SELECT username 
                       FROM patients
                       WHERE (username = '{user}')""")
        data = cursor.fetchall()

        try:
            result = data[0]
        except:
            result = False

        return result
    


    def create_account(db, user, name, date, room, password):
        generate_password = generate_password_hash(password)

        cursor = db.connection.cursor()
        cursor.execute(f"""INSERT INTO patients (id, username, pt_name, birthday, room, pt_password)
                    VALUES ({0}, '{user}','{name}','{date}',{room},'{generate_password}')""")
        db.connection.commit()

        return "Account successfully created! Please go to log in. Thank you!"