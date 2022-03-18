from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from models import *
from auth import get_hashed_password

#signals
from tortoise.signals import post_save
from tortoise import BaseDBAsyncClient
from typing import Type, List, Optional

app = FastAPI()

@post_save(Account)
async def create_vendor(
    sender: "Type[Account]",
    instance: Account,
    created: bool,
    using_db: "Optional[BaseDBAsyncClient]",
    update_fields: List[str]
) -> None:
    if created:
        vendor_obj = await Vendor.create(
            name=instance.username, owner=instance
        )
        await vendor_pydantic.from_tortoise_orm(vendor_obj)
        #send email

@app.get('/')
async def index():
    return {"Message": "Hello World"}

@app.post('/')
async def user_registration(account: account_pydanticIn):
    account_info = account.dict()
    account_info['password'] = get_hashed_password(account_info['password'])
    account_obj = await Account.create(**account_info)
    new_account = await account_pydantic.from_tortoise_orm(account_obj)
    return {
        "status": "ok",
        "data": f"Hello {new_account.username}, thanks for choosing our services. Please check your email inbox and click on the link to confirm your registration"
    }

register_tortoise(
    app,
    db_url="sqlite://database.sqlite3",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True
)