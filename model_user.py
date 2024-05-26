from user import User

class ModelUser:
    @classmethod
    def login(self, db, user):
        cursor = db.connection.cursor()
        cursor.execute("SELECT * FROM patients WHERE (username = '{}')".format(user.username))
        data = cursor.fetchall()
        
        data_info = data[0]

        if data != None:
            user = User(data_info[0], data_info[1], 
                        data_info[2], data_info[3], 
                        data_info[4], User.check_password(data_info[5], user.password))
            return user
        else:
            return None
        
    @classmethod
    def get_by_id(self, db, id):
        cursor = db.connection.cursor()
        cursor.execute("SELECT * FROM patients WHERE (id = '{}')".format(id))
        data = cursor.fetchall()
        
        data_info = data[0]

        if data != None:
            logged_user = User(data_info[0], data_info[1], 
                               data_info[2], data_info[3],
                               data_info[4], None)
            return logged_user
        else:
            return None