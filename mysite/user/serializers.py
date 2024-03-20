from rest_framework import serializers
from user.models import CustomUser,Likes
from recipe.models import Recipe

class CustomUserSchema(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id","username","email","like","date_joined","date_of_birth","phone")
        depth = 2
        
class CustomUserDetailSchema(CustomUserSchema):
    class Meta(CustomUserSchema.Meta):
        excludes = ("password",)

class CustomUserRequestSchema(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id","username","first_name","last_name","email","password", "date_of_birth","phone")

class LikesSerializer(serializers.ModelSerializer):
    user = CustomUserDetailSchema()
    recipe = Recipe()

    class Meta:
        model = Likes
        fields = "__all__"
        

