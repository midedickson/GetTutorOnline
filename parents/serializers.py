from rest_framework import serializers
from .models import TutorRequest, ParentProfile
from accounts.serializers import UserSerilizer
from tutors.models import TutoringPlan, Expertise


class StringSerializer(serializers.StringRelatedField):
    def to_internal_value(self, value):
        return value


class ParentSerializer(serializers.ModelSerializer):
    user = UserSerilizer(many=False, read_only=True)

    class Meta:
        model = ParentProfile
        fields = '__all__'


class TutorRequestSerializer(serializers.ModelSerializer):
    requested_tutorplan = serializers.PrimaryKeyRelatedField(
        many=False, queryset=TutoringPlan.objects.all())
    subjects_requested = StringSerializer(many=True)
    requested_tutor = serializers.SerializerMethodField()
    amount_payable = serializers.SerializerMethodField()

    class Meta:
        model = TutorRequest
        fields = '__all__'

    def get_requested_tutor(self, obj):
        from tutors.serializers import TutorSerializer
        return TutorSerializer(obj.get_tutor, many=False).data

    def get_amount_payable(self, obj):
        return obj.get_total_price


""" class SpecialRequestSerializer(serializers.ModelSerializer):
    requested_by = StringSerializer(many=False)
    subjects_needed = StringSerializer(many=True)

    class Meta:
        model = SpecialRequest
        fields = '__all__'


class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        models = Child
        fields = '__all__'
 """
