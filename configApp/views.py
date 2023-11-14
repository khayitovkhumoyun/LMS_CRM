import random
from django.core.cache import cache
from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from django.contrib.auth.hashers import make_password
from rest_framework.viewsets import ModelViewSet


class PhoneSendOTP(APIView):
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        print(phone_number)
        if phone_number:
            phone = str(phone_number)
            user = User.objects.filter(phone__iexact=phone)
            if user.exists():
                return Response({
                    'status': False,
                    'detail': 'phone number already exist'
                })
            else:
                key = send_otp(phone)

                if key:
                    # Store the verification code and phone number in cache for 5 minutes
                    cache.set(phone_number, key, 600)

                    return Response({"message": "SMS sent successfully"}, status=status.HTTP_200_OK)

                return Response({"message": "Failed to send SMS"}, status=status.HTTP_400_BAD_REQUEST)


def send_otp(phone):
    if phone:
        key = 1212
        print(key)
        return key
    else:
        return False


class VerifySms(APIView):
    pagination_class = PageNumberPagination

    def post(self, request):
        serializer = VerifySMSSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            verification_code = serializer.validated_data['verification_code']
            cached_code = str(cache.get(phone_number))
            if verification_code == str(cached_code):
                return Response({
                    'status': True,
                    'detail': 'OTP matched. please proceed for registration'
                })
            else:
                return Response({
                    'status': False,
                    'detail': 'otp INCOORECT'
                })
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterUserApi(APIView):
    pagination_class = PageNumberPagination
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            password = serializer.validated_data.get('password')
            serializer.validated_data['password'] = make_password(password)
            serializer.save()
            return Response({
                'status': True,
                'datail': 'Account create'
            })

    def get(self, request):
        users = User.objects.all().order_by('-id')
        serializer = UserSerializer(users, many=True)
        return Response(data=serializer.data)


class ChangePasswordView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def patch(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(instance=self.request.user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepartmentsApiView(ModelViewSet):
    queryset = Departments.objects.all().order_by('-id')
    serializer_class = DepartmentsSerializer
    pagination_class = PageNumberPagination


class CourseApiView(ModelViewSet):
    queryset = Course.objects.all().order_by('-id')
    serializer_class = CourseSerializer
    pagination_class = PageNumberPagination


class TeacherApiView(APIView):
    def post(self, request):
        serializer = WorkerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user_id = serializer.validated_data.get('user')
            user = User.objects.get(phone=user_id)
            user.is_teacher = 1
            user.save()
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        pagination_class = PageNumberPagination
        teacher = Worker.objects.filter(user__is_teacher=True).order_by('-id')
        serializer = WorkerSerializer(instance=teacher, many=True)
        return Response(data=serializer.data)


class WorkerApiView(APIView):
    pagination_class = PageNumberPagination

    def post(self, request):
        serializer = WorkerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user_id = serializer.validated_data.get('user')
            user = User.objects.get(phone=user_id)
            user.is_staff = True
            user.save()
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):

        worker = Worker.objects.filter(user__is_staff=True).order_by('-id')
        serializer = WorkerSerializer(worker, many=True)
        return Response(data=serializer.data)


class WorkerApiViewId(APIView):
    def get(self, request, pk):
        try:
            worker = Worker.objects.get(pk=pk)
            serializer = WorkerSerializer(worker)
            return Response(data=serializer.data)
        except Exception as e:
            return Response(data={'error': e})

    def put(self, request, pk):
        try:
            teacher = Worker.objects.get(id=pk)
            serializer = WorkerSerializer(teacher, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(data=serializer.data)
        except Exception as e:
            return Response(data={'error': e})

    def patch(self, request, pk):
        try:
            teacher = Worker.objects.get(pk=pk)
            serializer = WorkerSerializer(teacher, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(data=serializer.data)
        except Exception as e:
            return Response(data={'error': e})


class WorkerApiView(APIView):
    pagination_class = PageNumberPagination

    def post(self, request):
        serializer = WorkerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user_id = serializer.validated_data.get('user')
            user = User.objects.get(phone=user_id)
            user.is_staff = True
            user.save()
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        worker = Worker.objects.filter(user__is_staff=True).order_by('-id')
        serializer = WorkerSerializer(worker, many=True)
        return Response(data=serializer.data)


class RoomAPIView(ModelViewSet):
    queryset = Rooms.objects.all().order_by('-id')
    serializer_class = RoomSerializer
    pagination_class = PageNumberPagination


class DayAPIView(ModelViewSet):
    queryset = Day.objects.all().order_by('-id')
    serializer_class = DaySerializer
    pagination_class = PageNumberPagination


class WorkerApiView(APIView):
    pagination_class = PageNumberPagination

    def post(self, request):
        serializer = WorkerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user_id = serializer.validated_data.get('user')
            user = User.objects.get(phone=user_id)
            user.is_staff = True
            user.save()
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        worker = Worker.objects.filter(user__is_staff=True).order_by('-id')
        serializer = WorkerSerializer(worker, many=True)
        return Response(data=serializer.data)


class StudentApiView(APIView):
    pagination_class = PageNumberPagination

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user_id = serializer.validated_data.get('user')
            user = User.objects.get(phone=user_id)
            user.is_student = True
            user.save()
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        student = Student.objects.filter(user__is_student=True).order_by('-id')
        group = Group.objects.all().order_by('-id')
        course = Course.objects.all().order_by('-id')
        serializer_student = StudentSerializer(student, many=True)
        serializer_group = GroupSerializer(group, many=True)
        serializer_course = CourseSerializer(course, many=True)
        data = {
            "students": serializer_student.data,
            "groups": serializer_group.data,
            "courses": serializer_course.data
        }
        return Response(data=data)


class StudentApiViewId(APIView):
    def get(self, request, pk):
        try:
            student = Student.objects.get(pk=pk)
            serializer = StudentSerializer(student)
            return Response(data=serializer.data)
        except Exception as e:
            return Response(data={'error': e})

    def put(self, request, pk):
        try:
            student = Student.objects.get(id=pk)
            serializer = StudentSerializer(student, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(data=serializer.data)
        except Exception as e:
            return Response(data={'error': e})

    def patch(self, request, pk):
        try:
            student = Student.objects.get(pk=pk)
            serializer = StudentSerializer(student, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(data=serializer.data)
        except Exception as e:
            return Response(data={'error': e})


# group uchun crud
class GroupApiView(ModelViewSet):
    pagination_class = PageNumberPagination
    queryset = Group.objects.all().order_by('-id')
    serializer_class = GroupSerializer


# groupning get method , frontend shuni Apini ishladadi
class GroupApi(APIView):
    pagination_class = PageNumberPagination

    def get(self, request):
        teachers = Worker.objects.filter(user__is_teacher=True).order_by('-id')
        courses = Course.objects.all().order_by('-id')
        tables = Table.objects.all().order_by('-id')
        serializer_teachers = WorkerSerializer(teachers, many=True)
        serializer_courses = CourseSerializer(courses, many=True)
        serializer_table = TableSerializer(tables, many=True)

        datas = {
            "teachers": serializer_teachers.data,
            "courses": serializer_courses.data,
            "tables": serializer_table.data
        }

        return Response(data=datas)


class TableTypeApi(ModelViewSet):
    pagination_class = PageNumberPagination
    queryset = TableType.objects.all().order_by('-id')
    serializer_class = TableTypeSerializer


class TableApi(ModelViewSet):
    pagination_class = PageNumberPagination
    queryset = Table.objects.all().order_by('-id')
    serializer_class = TableSerializer


class TopicsApi(ModelViewSet):
    queryset = Topics.objects.all().order_by('-id')
    serializer_class = TopicsSerializer
    pagination_class = PageNumberPagination


class GroupHomeWorkApi(ModelViewSet):
    pagination_class = PageNumberPagination
    queryset = GroupHomeWork.objects.all().order_by('-id')
    serializer_class = GroupHomeWorkSerializer


class HomeWorkApi(ModelViewSet):
    queryset = HomeWork.objects.all().order_by('-id')
    serializer_class = HomeWorkSerializer
    pagination_class = PageNumberPagination


class AttendanceLevelApi(ModelViewSet):
    queryset = AttendanceLevel.objects.all().order_by('-id')
    serializer_class = AttendanceLevelSerializer
    pagination_class = PageNumberPagination
