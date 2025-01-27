from tortoise import Tortoise, fields
from tortoise.models import Model
from enum import Enum
from uuid import uuid4
from tortoise.validators import MinValueValidator, MaxValueValidator

class Users(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=255, unique=True)
    email = fields.CharField(max_length=255, unique=True)

class Recipes(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255, null=False)
    description = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    related_user = fields.ForeignKeyField("models.Users", related_name="recipes")

class Ingredients_Recipes(Model):
    id = fields.IntField(pk=True)
    amount = fields.FloatField(null=False)
    unit = fields.CharField(max_length=255, null=False)
    related_recipe = fields.ForeignKeyField("models.Recipes", related_name="ingredients")
    related_ingredient = fields.ForeignKeyField("models.Ingredients", related_name="recipes")

    class Meta:
        unique_together = ("related_recipe", "related_ingredient")

class Ingredients(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, null=False)
    calories = fields.FloatField(null=False)
    fat = fields.FloatField(null=False)
    carbs = fields.FloatField(null=False)
    protein = fields.FloatField(null=False)
    related_user = fields.ForeignKeyField("models.Users", related_name="ingredients")

    class Meta:
        unique_together = ("name", "related_user")
    
class Steps(Model):
    id = fields.IntField(pk=True)
    step_number = fields.IntField(null=False)
    instruction = fields.TextField(null=False)
    related_recipe = fields.ForeignKeyField("models.Recipes", related_name="steps")

    class Meta:
        unique_together = ("related_recipe", "step_number")


class Stars(Model):
    id = fields.IntField(pk=True)
    rating = fields.IntField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    related_user = fields.ForeignKeyField("models.Users", related_name="stars")
    related_recipe = fields.ForeignKeyField("models.Recipes", related_name="stars")

    class Meta:
        unique_together = ("related_user", "related_recipe")