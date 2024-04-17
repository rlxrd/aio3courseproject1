from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from app.database.requests import get_categories, get_items

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Каталог')],
                                     [KeyboardButton(text='Корзина')],
                                     [KeyboardButton(text='Поиск товара')],
                                     [KeyboardButton(text='Контакты')]])

async def item_buttons(item_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='В корзину', callback_data=f'basket_{item_id}')],
                                                     [InlineKeyboardButton(text='Назад', callback_data='back')]])
    return keyboard


async def item_buttons_second(item_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Моя корзина', callback_data='mybasket'),
                                                      InlineKeyboardButton(text='+1', callback_data=f'basketplus_{item_id}')],
                                                     [InlineKeyboardButton(text='Назад', callback_data='back')]])
    return keyboard


async def catalog():
    all_categories = await get_categories()
    keyboard = InlineKeyboardBuilder()

    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name, callback_data=f'category_{category.id}'))
    
    return keyboard.adjust(2).as_markup()


async def items(category_id):
    all_items = await get_items(category_id)
    keyboard = InlineKeyboardBuilder()
    
    for item in all_items:
        keyboard.add(InlineKeyboardButton(text=item.name, callback_data=f'item_{item.id}'))
        
    return keyboard.adjust(2).as_markup()
