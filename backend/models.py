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

class Ingredients(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, null=False)
    amount = fields.FloatField(null=False)
    unit = fields.CharField(max_length=255, null=False)
    related_recipe = fields.ForeignKeyField("models.Recipes", related_name="ingredients")

class Steps(Model):
    id = fields.IntField(pk=True)
    step_number = fields.IntField(null=False)
    instruction = fields.TextField(null=False)
    related_recipe = fields.ForeignKeyField("models.Recipes", related_name="steps")
