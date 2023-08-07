from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from habit.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    # Сериализатор для привычек с проверкой на приятную или полузкую привычку. В случае с приятной нет вознаграждения.
    user = serializers.CurrentUserDefault()

    def validate(self, attrs):
        try:
            attrs['good_habit_sign']
        except KeyError:
            attrs['good_habit_sign'] = False
        try:
            attrs['related_habit']
        except KeyError:
            attrs['related_habit'] = None
        try:
            attrs['reward']
        except KeyError:
            attrs['reward'] = None
            print(attrs)
        print(attrs)
        if attrs['good_habit_sign'] is True and (
                isinstance(attrs['related_habit'], type(None)) is False or isinstance(attrs['reward'],
                                                                                      type(None)) is False):
            raise ValidationError(['У приятной привычки не может быть вознаграждения или связанной привычки.'])
        return attrs

    class Meta:
        model = Habit
        fields = '__all__'
