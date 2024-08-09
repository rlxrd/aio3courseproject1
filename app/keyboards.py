from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from app.database.requests import get_categories, get_items, get_orders, get_item, get_order_items

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Каталог')],
                                     [KeyboardButton(text='Моя корзина')],
                                     [KeyboardButton(text='Мои заказы')],
                                     [KeyboardButton(text='Контакты')]],
                                     resize_keyboard=True,
                                     one_time_keyboard=True,
                                     input_field_placeholder='Выберите действие...'
                                     ) 



async def item_buttons(item_id, category_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Моя корзина', callback_data=f'mybasket_{item_id}_{category_id}')],
        [InlineKeyboardButton(text='Мои заказы', callback_data=f'agag111fsrgaefawdwad_{item_id}_{category_id}')],
        [InlineKeyboardButton(text='-1', callback_data=f'basketminus_{item_id}_{category_id}'),
         InlineKeyboardButton(text='+1', callback_data=f'basketplus_{item_id}_{category_id}')],
        [InlineKeyboardButton(text='Назад', callback_data=f'back_items_{item_id}_{category_id}')]])
    return keyboard

async def contacts():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='admin: @pfjaoighsoigbot', url='https://t.me/PIsyapopka223')],
        [InlineKeyboardButton(text='Назад', callback_data=f'sdhfgsdghsdkjg_')]])
    return keyboard

async def basket_buttons(item_id, category_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Оформить заказ', callback_data=f'checkout_order_{item_id}')],
                                                     [InlineKeyboardButton(text='Удалить все', callback_data=f'delete_basket_')],
        [InlineKeyboardButton(text='Назад', callback_data=f'back_buttons_{item_id}_{category_id}')]])
    return keyboard


async def basket_buttons19():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Оформить заказ', callback_data=f'xcvkbhxckljb')],
                                                     [InlineKeyboardButton(text='Удалить все', callback_data=f'delete_basket_')],
        [InlineKeyboardButton(text='Назад', callback_data=f'xkchjvlzkhxlvnvnvbn')]])
    return keyboard

async def basket_buttons20():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Назад', callback_data=f'xkchjvlzkhxlvnvnvbn')]])
    return keyboard


async def basket_buttons2(item_id, category_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Назад', callback_data=f'back_buttons_{item_id}_{category_id}')]])
    return keyboard


async def basket_buttons3():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Категории', callback_data=f'categories')]])
    return keyboard



async def basket_buttons5():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Enter name', callback_data=f'enter_name')],
                                                     [InlineKeyboardButton(text='Enter number', callback_data=f'enter_number')],
                                                     [InlineKeyboardButton(text='Enter location', callback_data=f'enter_location')],
                                                     [InlineKeyboardButton(text='Confirm', callback_data=f'confirm')],
        [InlineKeyboardButton(text='Отмена', callback_data=f'zz11wdback_asdavvv')]])
    return keyboard


async def basket_buttons32():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Enter photo', callback_data=f'vbcvkjbhcvhkbj_')],
                                                     [InlineKeyboardButton(text='Enter description', callback_data=f'lclbhcjlkbhcjvkb_')],
                                                     [InlineKeyboardButton(text='Send', callback_data=f'xcklbxclkblxcjvblk_')],
        [InlineKeyboardButton(text='Назад', callback_data=f'c12312sdfjzklf')]])
    return keyboard

async def basket_buttons6():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='categories', callback_data=f'admin_categories')],
                                                     [InlineKeyboardButton(text='items', callback_data=f'admin_items')],
                                                     [InlineKeyboardButton(text='рассылка', callback_data=f'sdgjdklfgjldskfgl_')],
        [InlineKeyboardButton(text='Назад', callback_data=f'afjasfhasjkfhkasj_')]])
    return keyboard


async def basket_buttons7(category_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='delete', callback_data=f'afawfawfasdgsdg_{category_id}')],
                                                     [InlineKeyboardButton(text='edit', callback_data=f'asdfgsgs_{category_id}')],
        [InlineKeyboardButton(text='back', callback_data=f'fffasfasf')]])
    return keyboard


async def basket_buttons8(category_id, item_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='delete', callback_data=f'hdmfklhghlk_{category_id}_{item_id}')],
                                                     [InlineKeyboardButton(text='edit', callback_data=f'awwaaw13123_{item_id}_{category_id}')],
        [InlineKeyboardButton(text='back', callback_data=f'asfawasdasda1111_{category_id}')]])
    return keyboard


async def basket_buttons9(category_id, item_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='back', callback_data=f'adahfa12312415_{item_id}_{category_id}')],
                                                     [InlineKeyboardButton(text='edit name', callback_data=f'2222w123123_{item_id}_{category_id}')],
                                                     [InlineKeyboardButton(text='edit description', callback_data=f'1111asfgaethdthfg_{item_id}_{category_id}')],
                                                     [InlineKeyboardButton(text='edit price', callback_data=f'222223saas212gdflkgjdlfkg_{item_id}_{category_id}')],
                                                     [InlineKeyboardButton(text='edit photo', callback_data=f'1z234saasdf_{item_id}_{category_id}')]])
    return keyboard


async def sdfgsdfggw(item_id, category_id, order_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='delete', callback_data=f'1233agefasef_{item_id}_{category_id}_{order_id}')],
                                                     [InlineKeyboardButton(text='back', callback_data=f'2sssz222w123123_{item_id}_{category_id}')]])
    return keyboard


async def xvxcvxcfasd213(order_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='delete', callback_data=f'xcvjxclkvlkxcjv_{order_id}')],
                                                     [InlineKeyboardButton(text='back', callback_data=f'kgjdklgjdl_')]])
    return keyboard

async def catalog3(tg_id, item_id, category_id):
    orders = await get_orders(tg_id)
    keyboard = InlineKeyboardBuilder()
    for order in orders:
        order_items = await get_order_items(order.id)

        my_items = order_items

        items_data = {}
        all_price = 0
        for myitem in my_items:
            item = await get_item(myitem.item)
            all_price += float(item.price)
            if item.name in items_data:
                items_data[item.name] = [items_data[item.name][0] + 1, items_data[item.name][1]]
            else:
                items_data[item.name] = [1, float(item.price)]

        result = []
        
        for name, cnt_price in items_data.items():
            result.append(f'{name} - {cnt_price[0]} x {cnt_price[1]} = {cnt_price[0] * cnt_price[1]}')

        result.append(f'\nResult: {all_price}')
        result.append(f'\nInformation:\n')

        result.append(f'Name: {order.name}')
        result.append(f'Number: {order.number}')
        result.append(f'Location: {order.location}')

        keyboard.add(InlineKeyboardButton(text='\n'.join(result), callback_data=f'asdfgeaesgaeeg_{item_id}_{category_id}_{order.id}'))
    
    keyboard = keyboard.adjust(1).as_markup()
    keyboard = keyboard.inline_keyboard
    keyboard.append([InlineKeyboardButton(text='Назад', callback_data=f'oihfjhfkhlgw_{item_id}_{category_id}')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return keyboard


async def catalog4(tg_id):
    orders = await get_orders(tg_id)
    keyboard = InlineKeyboardBuilder()
    for order in orders:
        order_items = await get_order_items(order.id)

        my_items = order_items

        items_data = {}
        all_price = 0
        for myitem in my_items:
            item = await get_item(myitem.item)
            all_price += float(item.price)
            if item.name in items_data:
                items_data[item.name] = [items_data[item.name][0] + 1, items_data[item.name][1]]
            else:
                items_data[item.name] = [1, float(item.price)]

        result = []
        
        for name, cnt_price in items_data.items():
            result.append(f'{name} - {cnt_price[0]} x {cnt_price[1]} = {cnt_price[0] * cnt_price[1]}')

        result.append(f'\nResult: {all_price}')
        result.append(f'\nInformation:\n')

        result.append(f'Name: {order.name}')
        result.append(f'Number: {order.number}')
        result.append(f'Location: {order.location}')

        keyboard.add(InlineKeyboardButton(text='\n'.join(result), callback_data=f'zxcfjghdkfjg_{order.id}'))
    
    keyboard = keyboard.adjust(1).as_markup()
    keyboard = keyboard.inline_keyboard
    keyboard.append([InlineKeyboardButton(text='Назад', callback_data=f'xv1111bxcvbxcvbxcvb_')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return keyboard


async def catalog():
    all_categories = await get_categories()

    keyboard = InlineKeyboardBuilder()

    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name, callback_data=f'category_{category.id}'))

    keyboard = keyboard.adjust(2).as_markup()
    keyboard = keyboard.inline_keyboard
    keyboard.append([InlineKeyboardButton(text='Моя корзина', callback_data='sdfiogusduiofhygui_')])
    keyboard.append([InlineKeyboardButton(text='Мои заказы', callback_data='khvxcjkhvbxckjvb_')])
    keyboard.append([InlineKeyboardButton(text='Назад', callback_data='back_reply')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return keyboard


async def catalog2():
    all_categories = await get_categories()

    keyboard = InlineKeyboardBuilder()

    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name, callback_data=f'gisjdgoshdugi_{category.id}'))

    keyboard = keyboard.adjust(2).as_markup()
    keyboard = keyboard.inline_keyboard
    keyboard.append([InlineKeyboardButton(text='Назад', callback_data='admin_back_reply')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return keyboard


async def catalog_admin():
    all_categories = await get_categories()

    keyboard = InlineKeyboardBuilder()

    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name, callback_data=f'admin_category_{category.id}_{category.name}'))

    keyboard = keyboard.adjust(2).as_markup()
    keyboard = keyboard.inline_keyboard
    keyboard.append([InlineKeyboardButton(text='Add', callback_data='admin_add_category')])
    keyboard.append([InlineKeyboardButton(text='Назад', callback_data='admin_back_reply')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return keyboard


async def items(category_id):
    all_items = await get_items(category_id)
    keyboard = InlineKeyboardBuilder()
    
    for item in all_items:
        keyboard.add(InlineKeyboardButton(text=item.name, callback_data=f'item_{item.id}_{category_id}'))
        
    keyboard = keyboard.adjust(2).as_markup()
    keyboard = keyboard.inline_keyboard
    keyboard.append([InlineKeyboardButton(text='Назад', callback_data='back_catalog')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return keyboard


async def items2(category_id):
    all_items = await get_items(category_id)
    keyboard = InlineKeyboardBuilder()
    
    for item in all_items:
        keyboard.add(InlineKeyboardButton(text=item.name, callback_data=f'41412413wdasd_{item.id}_{category_id}'))
        
    keyboard = keyboard.adjust(2).as_markup()
    keyboard = keyboard.inline_keyboard
    keyboard.append([InlineKeyboardButton(text='Add item', callback_data=f'safafawf2121_{category_id}')])
    keyboard.append([InlineKeyboardButton(text='Назад', callback_data='sdlfgjkdflkgjslkdg')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return keyboard

