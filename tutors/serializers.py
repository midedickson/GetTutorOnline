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


class ExpertiseSerializer(serializers.ModelSerializer):
    display_name = serializers.SerializerMethodField()

    class Meta:
        model = Expertise
        fields = ('display_name', )

    def get_display_name(self, obj):
        return obj.__str__()


class TutoringPlanSerializer(serializers.ModelSerializer):
    tutor = TutorSerializer(many=False, read_only=True)
    major_expertise = serializers.SerializerMethodField(read_only=True)
    minor1_expertise = serializers.SerializerMethodField(read_only=True)
    minor2_expertise = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = TutoringPlan
        fields = '__all__'

    def get_major_expertise(self, obj):
        return ExpertiseSerializer(obj.major, many=False).data

    def get_minor1_expertise(self, obj):
        return ExpertiseSerializer(obj.minor1, many=False).data


    def get_minor2_expertise(self, obj):
        return ExpertiseSerializer(obj.minor2, many=False).data
