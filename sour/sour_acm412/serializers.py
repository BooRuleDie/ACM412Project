from rest_framework import serializers
from .models import Topics

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topics
        fields = ['id', 'title', 'origin_comment']

class SearchTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topics
        fields = ['id', 'title']
