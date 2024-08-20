from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.permissions import IsStudentOrIsAdmin, ReadOnlyOrIsAdmin
from api.v1.serializers.course_serializer import (CourseSerializer,
                                                  CreateCourseSerializer,
                                                  CreateGroupSerializer,
                                                  CreateLessonSerializer,
                                                  GroupSerializer,
                                                  LessonSerializer)
from api.v1.serializers.user_serializer import SubscriptionSerializer
from courses.models import Course, Group
from users.models import Subscription

from users.models import Balance


class LessonViewSet(viewsets.ModelViewSet):
    """Уроки."""

    permission_classes = (IsStudentOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return LessonSerializer
        return CreateLessonSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.lessons.all()


class GroupViewSet(viewsets.ModelViewSet):
    """Группы."""

    permission_classes = (permissions.IsAdminUser,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GroupSerializer
        return CreateGroupSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.groups.all()


class CourseViewSet(viewsets.ModelViewSet):
    """Курсы """

    queryset = Course.objects.all()
    permission_classes = (ReadOnlyOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CourseSerializer
        return CreateCourseSerializer

    @action(
        methods=['post'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def pay(self, request, pk):
        """Покупка доступа к курсу (подписка на курс)."""

        # TODO
        course = get_object_or_404(Course, pk=pk)
        balance = get_object_or_404(Balance, user=request.user)

        if balance.balance > course.price:
            balance.balance -= course.price
            balance.save()

            subscription, created = Subscription.objects.get_or_create(user=request.user, course=course)

            if created:
                group = Group.objects.filter(course=course).annotate(student_count=Count('student')).order_by(
                    'student_count').first()
                if group:
                    group.students.add(request.user)
                    group.save()

                    serializer = SubscriptionSerializer(subscription)

                    return Response(
                        {'Успешно добавлено в группу',
                        serializer.data},
                        status=status.HTTP_201_CREATED
                    )
                else:
                    return Response({'Нет свободных групп'},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'Уже есть подписка на этот курс'},
                                status=status.HTTP_200_OK)
        else:
            return Response({'У вас недостаточно средств'}, status=status.HTTP_400_BAD_REQUEST)