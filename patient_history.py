class PatientHistory:

    def patient_history(self, db, a, b):
    
        cursor = db.connection.cursor()
        cursor.execute(f"SELECT reason, appt_date, appt_hour, room, if(timestamp(appt_date, appt_hour) < now(), 'Concluido', 'Pendiente') as stat FROM medical_appointment WHERE (id = {a} and room = {b})")
        data = cursor.fetchall()

        return data