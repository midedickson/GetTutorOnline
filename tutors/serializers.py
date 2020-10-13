from rest_framework import serializers
from .models import (
    Tutor,
    TutoringPlan,
    Expertise
)
# from parents.serializers import ParentSerializer
from parents.serializers import ParentSerializer


class StringSerializer(serializers.StringRelatedField):
    def to_internal_value(self, value):
        return value


class TutorSerializer(serializers.ModelSerializer):
    profile = ParentSerializer(many=False, read_only=True)

    class Meta:
        model = Tutor
        fields = '__all__'


class TutoringPlanSerializer(serializers.ModelSerializer):
    tutor = TutorSerializer(many=False, read_only=True)
    major = StringSerializer(many=False)
    minor1 = StringSerializer(many=False)
    minor2 = StringSerializer(many=False)

    class Meta:
        model = TutoringPlan
        fields = '__all__'


class ExpertiseSerializer(serializers.ModelSerializer):
    display_name = serializers.SerializerMethodField()

    class Meta:
        model = Expertise
        fields = '__all__'

    def get_display_name(self, obj):
        return obj.__str__()
