# Generated by Django 5.0.3 on 2024-05-13 08:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Ingredient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("ingredient", models.CharField(max_length=50)),
            ],
            options={"db_table": "ingredient", "db_table_comment": "전처리된 재료들",},
        ),
        migrations.CreateModel(
            name="Recipe",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("recipe_name", models.CharField(max_length=200)),
                ("url", models.URLField()),
                ("serving", models.IntegerField()),
                ("cnt", models.IntegerField()),
                ("image_url", models.URLField()),
            ],
            options={"db_table": "recipe", "db_table_comment": "레시피 목록",},
        ),
        migrations.CreateModel(
            name="RecipeIngredientRelation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "ingredient_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="recipe.ingredient",
                    ),
                ),
                (
                    "recipe_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="recipe.recipe"
                    ),
                ),
            ],
            options={"db_table": "recipe_ingredient_set",},
        ),
        migrations.AddField(
            model_name="recipe",
            name="preprocessed_ingredients",
            field=models.ManyToManyField(
                through="recipe.RecipeIngredientRelation", to="recipe.ingredient"
            ),
        ),
    ]
