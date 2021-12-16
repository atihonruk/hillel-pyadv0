from rest_framework import serializers

from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    # custom_field = serializers.SerializerMethodField()
    #  other_field()
    
    class Meta:
        model = Todo
        fields = ['title', 'description', 'created_by']

    # def get_custom_field(self):
        # logic
    #    return 'Hello'

    # def get_other_field()
