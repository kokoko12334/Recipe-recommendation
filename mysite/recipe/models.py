from django.db import models
#rcp_no,name,ingre,image_url,ck_mth,ck_knd,serving,url
class Recipe(models.Model):
    recipe_name = models.CharField(max_length=200,null=False )
    preprocessed_ingredients = models.ManyToManyField(to="Ingredient", through="RecipeIngredientRelation")
    url = models.URLField(max_length=200,null=False)
    serving = models.CharField(max_length=50,null=False )
    cnt = models.IntegerField()
    image_url = models.URLField(max_length=200)

    class Meta:
        db_table = "recipe"
        db_table_comment = "레시피 목록"
        
    def __str__(self): 
        return f'Recipe object ({self.recipe_name})'

class Ingredient(models.Model):
    ingredient = models.CharField(max_length=50,null=False)

    class Meta:
        db_table = "ingredient"
        db_table_comment = "전처리된 재료들"

class RecipeIngredientRelation(models.Model):
    recipe = models.ForeignKey(to="Recipe", on_delete=models.CASCADE)
    ingredient = models.ForeignKey(to="Ingredient", on_delete=models.CASCADE)

    class Meta:
        db_table = "recipe_ingredient_set"

