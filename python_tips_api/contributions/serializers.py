from rest_framework import serializers
from django.core.exceptions import ValidationError
from . models import Tips
from django.conf import settings

ACTIONS = settings.ACTIONS

class CreateTipSerializer(serializers.ModelSerializer):
    """
    FORM FOR USER INPUTTING TIPS BASED OFF ON THE MODEL
    FIELDS STATED
    """

    class Meta:
        model= Tips
        exclude = ['user', 'created_at']

    def validate(self, data):
        """
        VALIDATES EACH DATA PASSING THROUGH THE FORM BEFORE SAVING
        TO THE DATABASE TO AVIOD DUPLICATION ON SIMILARITIES WITH
        PREVIOUS TIPS
        """
        qs = Tips.objects.filter(tips_icontains = data['tips']):
        if qs.exists():
            raise serializers.ValidationError("This tips match a tips in the database")
        return data

    def create(self, validated_data):
        return Tips.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.tips = validated_data.get('tips', instance.tips)
        instance.twitter_id = validated_data.get('twitter_id', instance.twitter_id)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance


class TipsSerializer(serializers.NodelSerializer):
    """
    RENDERS DATA ACCORDING TO THE FIELDS SET ALLOWES IN THE 
    FIELD OPTION
    """
    likes = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Tips
        fields = "__all__"

    
    def get_likes(self, obj):
        return obj.likes.count()
class ActionTipsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()

    def validate_action(self, value):
        value = value.lower().strip()
        if not value in ACTIONS:
            raise serializers.ValidationError(status=400)
        return value
