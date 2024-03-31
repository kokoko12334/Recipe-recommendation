from rest_framework import serializers
from user.models import CustomUser,Likes
from recipe.models import Recipe

class CustomUserSchema(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id","username","email","like","date_joined","date_of_birth","phone")
        depth = 1
        
class CustomUserDetailSchema(CustomUserSchema):
    class Meta(CustomUserSchema.Meta):
        excludes = ("password",)

class CustomUserRequestSchema(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id","username","first_name","last_name","email","password", "date_of_birth","phone")
        # extra_kwargs = {
        #     'password': {'write_only': True}  # 패스워드 필드를 write_only로 설정하여 응답에 포함되지 않도록 함
        # }

    def create(self, validated_data):
        # 사용자 생성 시 패스워드 해시 적용
        user = CustomUser.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            date_of_birth=validated_data['date_of_birth'],
            phone=validated_data['phone']
        )
        user.set_password(validated_data['password'])  # 패스워드 해시
        user.save()
        return user

    def update(self, instance, validated_data):
        # 패스워드가 제공된 경우 해시 적용
        password = validated_data.pop('password', None)
        if password is not None:
            instance.set_password(password)
        
        # 나머지 필드 업데이트
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class LikesSerializer(serializers.ModelSerializer):
    user = CustomUserDetailSchema()
    recipe = Recipe()

    class Meta:
        model = Likes
        fields = "__all__"
        

