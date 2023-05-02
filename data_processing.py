import pymysql
from sqlalchemy import text
from datetime import datetime, time
from collections import defaultdict
from app import app, db


class DataProcessing:
    def __init__(self, current_user_id):
        # Attribute
        self.current_user_id = current_user_id
        self.opening_hours = None
        self.laden_oeffnet = None
        self.laden_schliesst = None
        self.user_availability = None
        self.binary_availability = None


    def run(self):
        """ Die einzelnen Methoden werden in der Reihe nach ausgeführt """
        self.get_availability()
        # Ausgabe user_availability
        print(f"User Availability: {self.user_availability}")
        #self.get_opening_hours()
        self.binaere_liste()
        print(f"Binary Availability: {self.binary_availability}")



    def get_availability(self):
        """ In dieser Funktion wird user_id, date, start_time, end_time aus der Availability Entität gezogen
            und in einer Liste gespeichert. Key ist user_id """

        print(f"Admin mit der User_id: {self.current_user_id} hat den Solve Button gedrückt.")

        with app.app_context():
            start_date = "2023-05-15"
            end_date = "2023-05-21"
            
            sql = text("""
                SELECT a.user_id, a.date, a.start_time, a.end_time
                FROM availability a
                WHERE a.user_id = :current_user_id
                AND a.date BETWEEN :start_date AND :end_date
            """)
            # execute = rohe Mysql Abfrage.
            result = db.session.execute(sql, {"current_user_id": self.current_user_id, "start_date": start_date, "end_date": end_date})
            # fetchall = alle Zeilen der Datenbank werden abgerufen und in einem Tupel gespeichert
            times = result.fetchall()

            # Dictionarie erstellen mit user_id als Key:
            user_availability = defaultdict(list)
            for user_id, date, start_time, end_time in times:
                user_availability[user_id].append((date, start_time, end_time))

            self.user_availability = user_availability



    def time_to_int_1(self, t):
        """ Die eingegebene Uhrzeit (hour, minute, second) wird in Stunden umgerechnet """
        return int((t.hour * 3600 + t.minute * 60 + t.second) / 3600)



    def time_to_int_2(self, t):
        """ Die eingegebene Uhrzeit (second) wird in Stunden umgerechnet """
        return int(t.seconds / 3600)




    def get_opening_hours(self): 
        """ In dieser Funktion werden die Öffnungszeiten der jeweiligen Company aus der Datenbank gezogen. """
        with app.app_context():
            sql = text("""
                SELECT company_id
                FROM user
                WHERE id = :current_user_id
            """)
            result = db.session.execute(sql, {"current_user_id": self.current_user_id})
            company_id = result.fetchone()[0]

            # Zuerst müssen die relationsships korrekt erstellt werden!

            sql = text("""
                SELECT weekday, start_time, end_time
                FROM opening_hours
                WHERE company_id = :company_id
            """)
            result = db.session.execute(sql, {"company_id": company_id})
            times = result.fetchall()


        for weekday, start_time, end_time in times:
            if not self.laden_oeffnet or start_time < self.laden_oeffnet:
                self.laden_oeffnet = start_time
            if not self.laden_schliesst or end_time > self.laden_schliesst:
                self.laden_schliesst = end_time

        if self.laden_oeffnet and self.laden_schliesst:
            self.opening_hours = (self.laden_schliesst.hour * 60 + self.laden_schliesst.minute) - (self.laden_oeffnet.hour * 60 + self.laden_oeffnet.minute)





    def binaere_liste(self):
        """ In dieser Funktion werden die zuvor erstellen user_availabilities in binäre Listen umgewandelt. """
        # Testwerte für Ladenöffnungszeiten!!
        self.laden_oeffnet = time(hour=6)
        self.laden_schliesst = time(hour=17)
        self.opening_hours = (self.laden_schliesst.hour * 60 + self.laden_schliesst.minute) - (self.laden_oeffnet.hour * 60 + self.laden_oeffnet.minute)


        # Generiert automatisch einen Standartwert für nicht vorhandene Schlüssel.
        binary_availability = defaultdict(list)

        for user_id, availabilities in self.user_availability.items():
            for date, start_time, end_time in availabilities:
                # Anzahl der Stunden Berechnen, in denen der Laden geöffnet ist
                num_hours = self.opening_hours // 60

                # Liste erstellen von Nullen mit der Länge der Anzahl der Stunden, in denen der Laden geöffnet ist
                binary_list = [0] * num_hours

                # Werte werden auf 1 gesetzt, wenn der MA Arbeiten kann.
                start_hour = self.time_to_int_2(start_time) - self.time_to_int_1(self.laden_oeffnet)
                end_hour = self.time_to_int_2(end_time) - self.time_to_int_1(self.laden_oeffnet)
                for i in range(start_hour, end_hour):
                    binary_list[i] = 1

                binary_availability[user_id].append((date, binary_list))

        self.binary_availability = binary_availability

