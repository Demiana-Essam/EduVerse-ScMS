import pyrebase


class dataBase():
    def __init__(self):
        self.firebaseConfig = {
            "apiKey": "AIzaSyAQG_KmhFcIzDT90Oj9i9uaKNCE1kM-TqQ",
            "authDomain": "fir-course-eb838.firebaseapp.com",
            "projectId": "fir-course-eb838",
            "storageBucket": "fir-course-eb838.appspot.com",
            "messagingSenderId": "513264369969",
            "appId": "1:513264369969:web:0d0a3123d5e4eb572ab010",
            "databaseURL": "https://fir-course-eb838-default-rtdb.europe-west1.firebasedatabase.app/"
        }
        self.start_Firebase_Connection()

    def start_Firebase_Connection(self):
        self.firebase = pyrebase.initialize_app(self.firebaseConfig)
        self.auth = self.firebase.auth()
        self.db = self.firebase.database()

    def getUser(self, email):
        user = self.db.child("USERS").order_by_child("Email").equal_to(email).get()

        for row in user.each():
            if int(row.val()['ROLE']) == 4:
                # print(row.key())
                var = self.db.child("Students").child(row.key()).get()
            elif int(row.val()['ROLE']) == 3:
                var = self.db.child("Teachers").child(row.key()).get()
            elif int(row.val()['ROLE']) == 5:
                continue
            else:
                var = self.db.child("Managers").child(row.key()).get()
            break
        return var.val(), int(row.val()['ROLE'])

    def addUser(self, id, role, user):
        if role == 1:
            table = 'Managers'
        elif role == 2:
            table = 'Managers'
        elif role == 3:
            table = 'Teachers'
        elif role == 4:
            table = 'Students'
        else:
            table = 'Students_Affair'

        self.db.child(table).child(id).set(user)
        self.auth.create_user_with_email_and_password(user['Email'], user['Password'])
        self.db.child('USERS').child(id).set({'Email': user['Email'], 'ROLE': role})

    def isID_exist(self, id):
        res = self.db.child("USERS").child(id).get()
        if res.val() != None:
            return True
        else:
            return False


    def getUserName_ByEmail(self, email):
        user = self.db.child("USERS").order_by_child("Email").equal_to(email).get()
        for row in user.each():
            if int(row.val()['ROLE']) == 4:
                var = self.db.child("Students").child(row.key()).get()
            elif int(row.val()['ROLE']) == 3:
                var = self.db.child("Teachers").child(row.key()).get()
            elif int(row.val()['ROLE']) == 5:
                continue
            else:
                var = self.db.child("Managers").child(row.key()).get()
            break

        return var.val()['Name']

    def getUserByID(self, faceImageID):
        user = self.db.child("USERS").child(faceImageID).get()

        if int(user.val()['ROLE']) == 4:
            var = self.db.child("Students").child(user.key()).get()
        elif int(user.val()['ROLE']) == 3:
            var = self.db.child("Teachers").child(user.key()).get()
        elif int(user.val()['ROLE']) == 5:
            pass
        else:
            var = self.db.child("Managers").child(user.key()).get()

        return var.val()

    def mapRole(self, role):
        r = self.db.child("ROLES").child(role).get()
        return r.val()['ROLE']

    def getCourseName(self, courseID):
        subject = self.db.child('Subjects').child(courseID).get()
        return subject.val()['SubjectName']

    def getSystem_Statistics(self):
        users = self.db.child("USERS").get()
        numUsers = len(users.val())
        Students = self.db.child("Students").get()
        numStudents = len(Students.val())
        return numUsers, numStudents

    def login(self, email, password):
        try:
            self.auth.sign_in_with_email_and_password(str(email), str(password))
            return True
        except:
            return False

    def createUserAccount(self, email, password):
        try:
            self.auth.create_user_with_email_and_password(str(email), str(password))
            print("Account Created Successfully")
            return True
        except:
            print("Account already exists")
            return False
