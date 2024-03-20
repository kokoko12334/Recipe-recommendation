from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

class CustomUser(AbstractUser):
    email = models.EmailField(verbose_name=("email address"), unique = True, blank=False)
    date_of_birth = models.DateField(verbose_name=('Date_of_birth'), null = False)
    phone = PhoneNumberField(verbose_name=('Phone'), unique = True, null = False, blank = False) 
    like = models.ManyToManyField(to="recipe.Recipe", through="Likes")

    USERNAME_FIELD = 'email'  # 인증기반시 필요한거
    REQUIRED_FIELDS = ['phone', 'date_of_birth' ] # 회원가입시 필수 입력 사항
    
    class Meta:
        db_table = "user"
        db_table_comment = "회원가입 유저들"
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ['date_joined'] # 필드명 기준으로

    def __str__(self):
        return f'username: ({self.username})'
    

class Likes(models.Model):
    user_id = models.ForeignKey(to="CustomUser",on_delete=models.CASCADE)
    recipe_id = models.ForeignKey(to="recipe.Recipe", on_delete=models.CASCADE) #타 앱사용시 앞에 app.model

    class Meta:
        db_table = "likes"
        db_table_comment = "유저들 좋아요목록"