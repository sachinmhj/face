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

# take attendance
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

    attendance_taken = False    # Add variable to keep track of attendance taken or not
    while True:
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

            if compar[bestIndex]:
                if not attendance_taken:  # Check if attendance has not been taken for this student
                    naam = AllImaze[int(bestIndex)]
                    img = fram
                    text = f"{naam} Attendance Taken"
                    org = (200, 200)
                    fontface = cv2.FONT_HERSHEY_DUPLEX
                    fontscale = 1.0
                    color = (125, 246, 55)
                    fm = cv2.putText(img, text, org, fontface, fontscale, color)
                    cv2.imshow("camra", fm)

                    nem = naam.id
                    now = datetime.now()
                    dt_string = now.strftime("%Y-%m-%d")
                    dt_time = now.strftime("%H:%M:%S")

                    # attendace save in database
                    SavAttendanceInDb = Attendance(date=dt_string, time=dt_time, status="present", student_id=nem)
                    SavAttendanceInDb.save()
                    attendance_taken = True  # Set True, so that attendance is not taken again for this student

            else:
                text = "Detecting Face..."
                cv2.imshow("camra", fram)

        if cv2.waitKey(10) == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    return render(request, "uzer/attend.html")

# def atendance(request):
#     cap = cv2.VideoCapture(0)

#     AllImaze = customuser.objects.filter(Role="student")
#     # print(AllImaze)
#     dbImazeList = [a.Imege for a in AllImaze]
#     # print(dbImazeList)
#     loaddbImazeList = [face_recognition.load_image_file(i) for i in dbImazeList]
#     # print(loaddbImazeList)
#     encodloaddbImageList = [face_recognition.face_encodings(i)[0] for i in loaddbImazeList]
#     # print(type(encodloaddbImageList[0]))

#     # Initialize variables for attendance tracking
#     attendance_taken = []

#     while True:
#         bol, fram = cap.read()
#         # print(bol)
#         # print(fram)
#         locatefram = face_recognition.face_locations(fram)
#         encodfram = face_recognition.face_encodings(fram, locatefram)
#         # print(encodfram)
#         for data in encodfram:
#             compar = face_recognition.compare_faces(encodloaddbImageList, data)
#             # print(compar)
#             distanc = face_recognition.face_distance(encodloaddbImageList, data)
#             bestIndex = numpy.argmin(distanc)
#             # print(bestIndex)

#             # attendance_interval = timedelta(minutes=30)  # Set the desired attendance interval (e.g., 30 minutes)
            
#             naam = AllImaze[int(bestIndex)]
#             print(naam)
#             img = fram
#             text = f"{naam} Attendance Taken"
#             org = (200, 200)
#             fontface = cv2.FONT_HERSHEY_DUPLEX
#             fontscale = 1.0
#             color = (125, 246, 55)

#             if compar[bestIndex]:
#                 fm = cv2.putText(img, text, org, fontface, fontscale, color)
#                 cv2.imshow("camra", fm)

#                 if naam.id not in attendance_taken:
#                     nem = naam.id
#                     now = datetime.now()
#                     dt_string = now.strftime("%Y-%m-%d")
#                     dt_time = now.strftime("%H:%M:%S")

#                     # attendace save in database
#                     SavAttendanceInDb = Attendance(date=dt_string, time=dt_time, status="present", student_id=nem)
#                     SavAttendanceInDb.save()
#                     attendance_taken.append(nem)
#                     # print(attendance_taken)
                    
#             else:
#                 text = "Detecting Face..."
#                 color = (125, 200, 0)
#                 fms = cv2.putText(img, text, org, fontface, fontscale, color)
#                 cv2.imshow("camra", fms)

#         if cv2.waitKey(10) == ord("q"):
#             break

#     cap.release()
#     cv2.destroyAllWindows()
#     return render(request, "uzer/attend.html")

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