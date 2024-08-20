from django.contrib.auth import get_user_model
from django.db.models import Avg, Count, Sum
from rest_framework import serializers

from courses.models import Course, Group, Lesson
from users.models import Subscription

User = get_user_model()


class LessonSerializer(serializers.ModelSerializer):
    """Список уроков."""

    course = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Lesson
        fields = (
            'title',
            'link',
            'course'
        )


class CreateLessonSerializer(serializers.ModelSerializer):
    """Создание уроков."""

    class Meta:
        model = Lesson
        fields = (
            'title',
            'link',
            'course'
        )


class StudentSerializer(serializers.ModelSerializer):
    """Студенты курса."""

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
        )


class GroupSerializer(serializers.ModelSerializer):
    """Список групп."""

    # TODO Доп. задание

    class Meta:
        model = Group


class CreateGroupSerializer(serializers.ModelSerializer):
    """Создание групп."""

    class Meta:
        model = Group
        fields = (
            'title',
            'course',
        )


class MiniLessonSerializer(serializers.ModelSerializer):
    """Список названий уроков для списка курсов."""

    class Meta:
        model = Lesson
        fields = (
            'title',
        )


class CourseSerializer(serializers.ModelSerializer):
    """Список курсов."""

    lessons = MiniLessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField(read_only=True)
    students_count = serializers.SerializerMethodField(read_only=True)
    groups_filled_percent = serializers.SerializerMethodField(read_only=True)
    demand_course_percent = serializers.SerializerMethodField(read_only=True)

    def get_lessons_count(self, obj):
        """Количество уроков в курсе."""
        # TODO Доп. задание
        return obj.lessons.count()

    def get_students_count(self, obj):
        """Общее количество студентов на курсе."""
        # TODO Доп. задание
        return Group.objects.filter(course=obj).count()

    def get_groups_filled_percent(self, obj):
        """Процент заполнения групп, если в группе максимум 30 чел.."""
        # TODO Доп. задание
        groups = Group.objects.filter(course=obj)

        total_students = groups.aggregate(total_students=Count('student'))['total_students'] or 0
        max_students = groups.count() * 30

        return (total_students / max_students) * 100

    def get_demand_course_percent(self, obj):
        """Процент приобретения курса."""
        # TODO Доп. задание
        users = User.objects.count()

        if users == 0:
            return 0

        subscriptions = Subscription.objects.filter(course=obj).count()
        return (subscriptions / users) * 100


    class Meta:
        model = Course
        fields = (
            'id',
            'author',
            'title',
            'start_date',
            'price',
            'lessons_count',
            'lessons',
            'demand_course_percent',
            'students_count',
            'groups_filled_percent',
        )


class CreateCourseSerializer(serializers.ModelSerializer):
    """Создание курсов."""

    class Meta:
        model = Course
