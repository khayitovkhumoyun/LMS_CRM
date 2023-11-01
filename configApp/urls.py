from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'course', CourseApiView)
router.register(r'department', DepartmentsApiView)
router.register(r'room', RoomAPIView)
router.register(r'day', DayAPIView)
router.register(r'course', CourseApiView)

router.register(r'group', GroupApiView)
# dard javvali turi
router.register(r'tableType', TableTypeApi)
# dars jadvali
router.register(r'table', TableApi)
# guruhga vazifa biriktirish
router.register(r'groupHome', GroupHomeWorkApi)
# Mavzular
router.register(r'topic', TopicsApi)
# uyga fazifa
router.register(r'homeWork', HomeWorkApi)
#yuqlama
router.register(r'attendanceLevel', AttendanceLevelApi)
urlpatterns = [
    path('', include(router.urls)),
    path('register_user/', RegisterUserApi.as_view()),
    path('refresh_password/', ChangePasswordView.as_view()),
    path('sentOTP/', PhoneSendOTP.as_view()),
    path('sentOTP_and_phone/', VerifySms.as_view()),
    path('add_teacher/', TeacherApiView.as_view()),
    path('add_worker/', WorkerApiView.as_view()),
    path('workerId/<int:pk>/', WorkerApiViewId.as_view()),
    path('student/', StudentApiView.as_view()),
    path('student/<int:pk>/', StudentApiViewId.as_view()),
    # path('topicNumber/', TopicsApi.as_view()),

]
