# Generated by Django 5.0.3 on 2024-05-13 08:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("recipe", "0002_alter_recipe_serving"),
    ]

    operations = [
        migrations.RenameField(
            model_name="recipeingredientrelation",
            old_name="ingredient_id",
            new_name="ingredient",
        ),
        migrations.RenameField(
            model_name="recipeingredientrelation",
            old_name="recipe_id",
            new_name="recipe",
        ),
    ]
