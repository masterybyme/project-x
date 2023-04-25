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

    def run(self):
        """ Die einzelnen Methoden werden in der Reihe nach ausgeführt """
        #self.get_availability()
        #self.get_opening_hours()
        #self.binaere_liste()

    def get_availability(self):
        """ In dieser Funktion wird date, start_time, end_time aus der Availability Entität gezogen
            und in einer Liste gespeichert. Key ist current_user_id """

        print(f"Admin mit der User_id: {self.current_user_id} hat den Solve Button gedrückt.")

        with app.app_context():
            # Kann erst ausgeführt werden, wenn die relationships gemacht sind
            sql = text("""
                SELECT a.date, a.start_time, a.end_time, ua.user_id
                FROM availability a
                JOIN UserAvailability ua ON a.id = ua.availability_id
                WHERE ua.user_id = :current_user_id 
            """)
            # execute = rohe Mysql Abfrage.
            result = db.session.execute(sql, {"current_user_id": self.current_user_id})
            # fetchall = alle Zeilen der Datenbank werden abgerufen und in einem Tupel gespeichert
            times = result.fetchall()

            filtered_list = [
                (datetime.date(2023, 4, 10), datetime.timedelta(seconds=25200), datetime.timedelta(seconds=43200), 1),
                (datetime.date(2023, 4, 11), datetime.timedelta(seconds=25200), datetime.timedelta(seconds=43200), 1),
                (datetime.date(2023, 4, 12), datetime.timedelta(seconds=32400), datetime.timedelta(seconds=50400), 1),
                (datetime.date(2023, 4, 13), datetime.timedelta(0), datetime.timedelta(0), 1),
                (datetime.date(2023, 4, 14), datetime.timedelta(0), datetime.timedelta(0), 1),
                (datetime.date(2023, 4, 15), datetime.timedelta(0), datetime.timedelta(0), 1),
                (datetime.date(2023, 4, 16), datetime.timedelta(0), datetime.timedelta(0), 1),
                (datetime.date(2023, 4, 10), datetime.timedelta(seconds=28800), datetime.timedelta(seconds=50400), 2),
                (datetime.date(2023, 4, 11), datetime.timedelta(seconds=25200), datetime.timedelta(seconds=57600), 2),
                (datetime.date(2023, 4, 12), datetime.timedelta(seconds=32400), datetime.timedelta(seconds=39600), 2),
                (datetime.date(2023, 4, 13), datetime.timedelta(seconds=36000), datetime.timedelta(seconds=43200), 2),
                (datetime.date(2023, 4, 14), datetime.timedelta(seconds=32400), datetime.timedelta(seconds=57600), 2),
                (datetime.date(2023, 4, 15), datetime.timedelta(seconds=28800), datetime.timedelta(seconds=39600), 2),
                (datetime.date(2023, 4, 16), datetime.timedelta(0), datetime.timedelta(0), 2)]
            print(filtered_list[0][0])
            print(filtered_list[0][1])
            print(filtered_list[0][2])
            print(filtered_list[0][3])

            # Dictionarie erstellen mit user_id als Key:
            user_availability = defaultdict(list)
            for date, start_time, end_time, user_id in times:
                user_availability[user_id].append((date, start_time, end_time))

            return user_availability

    def time_to_int_1(self, t):
        """ Die eingegebene Uhrzeit (hour, minute, second) wird in Stunden umgerechnet """
        return int((t.hour * 3600 + t.minute * 60 + t.second) / 3600)

    def time_to_int_2(self, t):
        """ Die eingegebene Uhrzeit (second) wird in Stunden umgerechnet """
        return int(t.seconds / 3600)

    def get_opening_hours(self):
        with app.app_context():
            # Auch hier muss die user_id übereinstimmen!
            sql = text("SELECT weekday, start_time, end_time FROM opening_hours")
            # execute = rohe Mysql Abfrage.
            result = db.session.execute(sql, {"current_user_id": self.current_user_id})
            # fetchall = alle Zeilen der Datenbank werden abgerufen und in einem Tupel gespeichert
            times = result.fetchall()
        print("Ausgabe der Öffnungszeiten: ", times)

        # Die nachfolgenden 2 Variablen sind sobald get_opening_hours funktioniert nicht mehr nötig
        laden_oeffnet = time(hour=5, minute=0)
        laden_schliesst = time(hour=18, minute=0)
        opening_hours = self.time_to_int_1(laden_schliesst) - self.time_to_int_1(laden_oeffnet)

        self.opening_hours = opening_hours
        self.laden_oeffnet = laden_oeffnet
        self.laden_schliesst = laden_schliesst

    def binaere_liste(self):

        uhrzeit1 = filtered_list[0][1]
        uhrzeit2 = filtered_list[0][2]

        # ----------------------------------------------------------------------------------------------------------------------

        for outer_index, outside in enumerate(filtered_list):
            for inner_index, inside in enumerate(outside):
                if inside == 1:
                    print("Position: (", outer_index, ",", inner_index, ")")


        ma_1 = [0] * opening_hours

        for i in range(time_to_int_2(uhrzeit1) - time_to_int_1(laden_oeffnet),
                       time_to_int_2(uhrzeit2) - time_to_int_1(laden_oeffnet)):
            ma_1[i] = 1
        return ma_1
