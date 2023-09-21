from django.urls import path
from . import views
urlpatterns = [
    path("",views.profile,name="uprof"),
    path("myDetails/",views.details,name="det"),
    # for attendance
    path("Attendance/",views.atendance,name="atnd"),
    path("AttendanceData/",views.attendData,name="atndata"),
]
