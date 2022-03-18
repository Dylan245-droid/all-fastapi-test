from email.policy import default
from enum import unique
import pydantic
from tortoise import Model, fields
from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

class Account(Model):
    id = fields.IntField(pk= True, index= True)
    username = fields.CharField(max_length= 20, null= False, unique= True)
    email = fields.CharField(max_length= 200, null= False, unique= True)
    password = fields.CharField(max_length=100, null= False)
    is_verified = fields.BooleanField(default= False)
    date_joined = fields.DatetimeField(auto_now_add= True)

class Vendor(Model):
    id = fields.IntField(pk= True, index= True)
    name = fields.CharField(max_length=100, null= False, unique= True)
    type = fields.CharField(max_length=100, null= True, default="Raison Sociale")
    city = fields.CharField(max_length= 100, null= False, default= "Unspecified")
    region = fields.CharField(max_length= 100, null= False, default= "Unspecified")
    logo = fields.CharField(max_length=200, null=True, default="default.jpg")
    owner = fields.ForeignKeyField('models.Account', related_name="vendor")


account_pydantic = pydantic_model_creator(Account, name="Account", exclude=("is_verified", ))
account_pydanticIn = pydantic_model_creator(Account, name="AccountIn", exclude_readonly=True, exclude=("is_verified", "date_joined"))
account_pydanticOut = pydantic_model_creator(Account, name="AccountOut", exclude=("password", ))

vendor_pydantic = pydantic_model_creator(Vendor, name="Vendor", exclude=("is_verified", ))
vendor_pydanticIn = pydantic_model_creator(Vendor, name="VendorIn", exclude_readonly=True)