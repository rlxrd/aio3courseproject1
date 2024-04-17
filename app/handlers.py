from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from app import keyboards as kb
from app.database import requests as rq

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer('Привет! Добро пожаловать в магазин Sneakers Shop',
                         reply_markup=kb.main)


@router.message(F.text == 'Каталог')
async def catalog(message: Message):
    await message.answer('Выберите бренд товара', reply_markup=await kb.catalog())


@router.callback_query(F.data.startswith('category_'))
async def category_items(callback: CallbackQuery):
    await callback.answer('Вы выбрали категорию')
    await callback.message.answer('Выберите товар', reply_markup=await kb.items(callback.data.split('_')[1]))


@router.callback_query(F.data.startswith('item_'))
async def item_card(callback: CallbackQuery):
    item = await rq.get_item(callback.data.split('_')[1])
    await callback.answer('Вы выбрали товар')
    await callback.message.answer(f'Название: {item.name}\nОписание: {item.description}\nЦена: {item.price} руб',
                                  reply_markup=await kb.item_buttons(callback.data.split('_')[1]))


@router.callback_query(F.data.startswith('basket_'))
async def item_basket(callback: CallbackQuery):
    await rq.set_item_basket(callback.from_user.id, callback.data.split('_')[1])
    await callback.answer('Товар добавлен в корзину!')
    await callback.message.edit_reply_markup(reply_markup=await kb.item_buttons_second(callback.data.split('_')[1]))


@router.callback_query(F.data.startswith('basketplus_'))
async def item_basket(callback: CallbackQuery):
    await rq.set_item_basket(callback.from_user.id, callback.data.split('_')[1])
    await callback.answer('Товар добавлен в корзину!')


@router.message(F.text == 'Корзина')
async def mybasket(message: Message):
    my_items = await rq.get_my_basket(message.from_user.id)
    items_data = {}
    for myitem in my_items:
        item = await rq.get_item(myitem.item)
        if item.name in items_data:
            items_data[item.name] += int(item.price)
        else:
            items_data[item.name] = int(item.price)
    
    items = []
    for name, price in items_data.items():
        items.append(f"{name}: {price}")
    
    items.append(f"\nОбщая сумма: {sum(items_data.values())}")
    await message.answer('\n'.join(items))
