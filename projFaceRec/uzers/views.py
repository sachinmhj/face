from django.shortcuts import render
from sineup.models import customuser
from .models import Attendance

# for face_recognition required imports
import cv2
import face_recognition
import numpy
from datetime import datetime
# Create your views here.

# user home page
def profile(request):
    naam = request.user.username
    idy = request.user.id
    rol = request.user.Role
    pm = {"nam":naam,"idy":idy,"rol":rol}
    return render(request,"uzer/profile.html",pm)

# user info
def details(request):
    nem = request.user.username
    fname = request.user.first_name
    lname = request.user.last_name
    emel = request.user.email
    rol = request.user.Role
    pic = request.user.Imege
    pm = {"name":nem,"fname":fname,"lname":lname,"email":emel,"role":rol,"imag":pic}
    return render(request,"uzer/userDetails.html",pm)

def atendance(request):
    cap = cv2.VideoCapture(0)

    AllImaze = customuser.objects.filter(Role="student")
    # print(AllImaze)
    dbImazeList = [a.Imege for a in AllImaze]
    # print(dbImazeList)
    loaddbImazeList = [face_recognition.load_image_file(i) for i in dbImazeList]
    # print(loaddbImazeList)
    encodloaddbImageList = [face_recognition.face_encodings(i)[0] for i in loaddbImazeList]
    # print(type(encodloaddbImageList[0]))
    
    while True:
        currentTime = datetime.now()
        cTim = currentTime.strftime("%Y-%m-%d")
        # print("current time is",cTim)
        # print(type(cTim))
        bol, fram = cap.read()
        # print(bol)
        # print(fram)
        locatefram = face_recognition.face_locations(fram)
        encodfram = face_recognition.face_encodings(fram, locatefram)
        # print(encodfram)
        for data in encodfram:
            compar = face_recognition.compare_faces(encodloaddbImageList, data)
            # print(compar)
            distanc = face_recognition.face_distance(encodloaddbImageList, data)
            bestIndex = numpy.argmin(distanc)
            # print(bestIndex)

            # attendance_interval = timedelta(minutes=30)  # Set the desired attendance interval (e.g., 30 minutes)
            
            naam = AllImaze[int(bestIndex)]
            # print(naam)
            # print(type((naam)))
            # print(type(str(Attendance.objects.get(student=naam.id).date)))
            # print(str(Attendance.objects.get(student=naam.id).date))
            img = fram
            text = f"{naam} Attendance Taken"
            org = (200, 200)
            fontface = cv2.FONT_HERSHEY_DUPLEX
            fontscale = 1.0
            color = (125, 246, 55)
            # print(Attendance.objects.filter(student=naam.id)[0].date)

            if compar[bestIndex]:
                fm = cv2.putText(img, text, org, fontface, fontscale, color)
                cv2.imshow("camra", fm)

                # print(str(Attendance.objects.filter(student=naam.id)[0].date))
                # print(daat)
                firstAtend = Attendance.objects.filter(student=naam.id)
                print(firstAtend)
                studentAttendDate = [str(Attendance.objects.filter(student=naam.id)[i].date) for i in range(len(firstAtend))]
                print(studentAttendDate)
                # print(type(studentAttendDate))
                # if cTim not in daat:
                if not firstAtend.exists():
                    print("didn't existed")
                    nem = naam.id
                    now = datetime.now()
                    dt_string = now.strftime("%Y-%m-%d")
                    dt_time = now.strftime("%H:%M:%S")

                    # attendace save in database
                    SavAttendanceInDb = Attendance(date=dt_string, time=dt_time, status="present", student_id=nem)
                    SavAttendanceInDb.save()
                elif(cTim not in studentAttendDate):
                    print("time not existed")
                    nem = naam.id
                    now = datetime.now()
                    dt_string = now.strftime("%Y-%m-%d")
                    dt_time = now.strftime("%H:%M:%S")

                    # attendace save in database
                    SavAttendanceInDb = Attendance(date=dt_string, time=dt_time, status="present", student_id=nem)
                    SavAttendanceInDb.save()
                else:
                    pass
                    
            else:
                text = "Detecting Face..."
                color = (125, 200, 0)
                fms = cv2.putText(img, text, org, fontface, fontscale, color)
                cv2.imshow("camra", fms)

        if cv2.waitKey(10) == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    return render(request, "uzer/attend.html")

# attendance data
def attendData(request):
    rol = request.user.Role

    usr_id = request.user.id
    at = Attendance.objects.filter(student_id = usr_id)
    atAll = Attendance.objects.all()
    pm = {"attend": at,"rol":rol,"atall":atAll}
    # print(at)
    # print(atAll)
    return render(request,"uzer/attendData.html",pm)