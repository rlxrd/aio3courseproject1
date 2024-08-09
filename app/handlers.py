from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from app import keyboards as kb
from app.database import requests as rq

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


class Reg(StatesGroup):
    name = State()
    number = State()
    location = State()

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer('Привет! Добро пожаловать в магазин',
                         reply_markup=kb.main)


@router.message(F.text == 'Каталог')
async def catalog(message: Message):
    await message.answer('Выберите категорию', reply_markup=await kb.catalog())


@router.message(F.text == 'Моя корзина')
async def catalog(message: Message):
    my_items = await rq.get_my_basket(message.from_user.id)
    items_data = {}
    all_price = 0
    for myitem in my_items:
        item = await rq.get_item(myitem.item)
        all_price += float(item.price)
        if item.name in items_data:
            items_data[item.name] = [items_data[item.name][0] + 1, items_data[item.name][1]]
        else:
            items_data[item.name] = [1, float(item.price)]

    result = []
    
    for name, cnt_price in items_data.items():
        result.append(f'{name} - {cnt_price[0]} x {cnt_price[1]} = {cnt_price[0] * cnt_price[1]}')


    result.append(f'\nResult: {all_price}' if all_price != 0 else 'корзина пуста')
    await message.answer('\n'.join(result), reply_markup=await kb.basket_buttons19() if all_price != 0 else await kb.basket_buttons20())


@router.message(F.text == 'Мои заказы')
async def catalog(message: Message):
    await message.answer('Заказы:', reply_markup=await kb.catalog4(message.from_user.id))


@router.message(F.text == 'Контакты')
async def catalog(message: Message):
    await message.answer('Контакты:', reply_markup=await kb.contacts())


@router.callback_query(F.data.startswith('sdhfgsdghsdkjg_'))
async def asdasfxcxcv(callback: CallbackQuery):
    await callback.answer('Назад')
    await callback.message.answer(text='Привет! Добро пожаловать в магазин',
                         reply_markup=kb.main)


@router.callback_query(F.data == 'categories')
async def catalog(callback: CallbackQuery):
    await callback.answer('Категории')
    await callback.message.edit_text('Выберите бренд товара')
    await callback.message.edit_reply_markup(reply_markup=await kb.catalog())


@router.callback_query(F.data == ('back_reply'))
async def category_items(callback: CallbackQuery):
    await callback.answer('Назад')
    await callback.message.edit_text('Назад')
    await callback.message.answer('Привет! Добро пожаловать в магазин',
                         reply_markup=kb.main)



@router.callback_query(F.data.startswith('category_'))
async def category_items(callback: CallbackQuery):
    await callback.answer('Вы выбрали категорию')
    await callback.message.edit_text('Выберите товар')
    await callback.message.edit_reply_markup(reply_markup=await kb.items(callback.data.split('_')[1]))


@router.callback_query(F.data == ('back_catalog'))
async def category_items(callback: CallbackQuery):
    await callback.answer('Назад')
    await callback.message.edit_text('Выберите бренд товара')
    await callback.message.edit_reply_markup(reply_markup=await kb.catalog())
    

    



@router.callback_query(F.data.startswith('item_'))
async def item_card(callback: CallbackQuery):
    await callback.answer('Вы выбрали товар')
    item = await rq.get_item(callback.data.split('_')[1])
    items_basket = await rq.get_items_basket(callback.from_user.id, item.id)

    result = []
    result.append(f'Id товара: {item.id}\n')
    result.append(f'Название: {item.name}\n')
    result.append(f'Описание: {item.description}\n')
    result.append(f'Цена: {item.price} руб\n')
    result.append(f'В корзине у вас: {len(items_basket.all())} шт.\n')
    item_basket_all = await rq.get_item_basket_all(item.id)
    result.append(f'В корзине у: {len(item_basket_all)} шт. пользователей\n')
    item_order = await rq.get_item_order_all(item.id)
    result.append(f'Заказали: {len(item_order)} шт.')

    await callback.message.answer_photo(item.photo_id, reply_markup=await kb.item_buttons(callback.data.split('_')[1], callback.data.split('_')[2]), caption=''.join(result))


@router.callback_query(F.data.startswith('back_items_'))
async def item_card(callback: CallbackQuery):
    await callback.answer('Назад')

    await callback.message.answer(reply_markup=await kb.items(callback.data.split('_')[-1]), text='Выберите товар')





@router.callback_query(F.data.startswith('basketplus_'))
async def item_basket(callback: CallbackQuery):
    await callback.answer('Товар добавлен в корзину!')
    await rq.set_item_basket(callback.from_user.id, callback.data.split('_')[1])

    item = await rq.get_item(callback.data.split('_')[1])
    items_basket = await rq.get_items_basket(callback.from_user.id, item.id)

    result = []
    result.append(f'Id товара: {item.id}\n')
    result.append(f'Название: {item.name}\n')
    result.append(f'Описание: {item.description}\n')
    result.append(f'Цена: {item.price} руб\n')
    result.append(f'В корзине: {len(items_basket.all())} шт.\n')
    item_basket_all = await rq.get_item_basket_all(item.id)
    result.append(f'В корзине у: {len(item_basket_all)} шт. пользователей\n')
    item_order = await rq.get_item_order_all(item.id)
    result.append(f'Заказали: {len(item_order)} шт.')

    await callback.message.answer_photo(item.photo_id, reply_markup=await kb.item_buttons(callback.data.split('_')[1], callback.data.split('_')[2]), caption=''.join(result))


@router.callback_query(F.data.startswith('basketminus_'))
async def item_basket(callback: CallbackQuery):
    item = await rq.get_item(callback.data.split('_')[1])
    basket_item = await rq.get_item_basket(callback.from_user.id, item.id)

    if basket_item:
        await callback.answer('Товар удален из корзины!')
        await rq.delete_item_basket(callback.from_user.id, item.id)

        item = await rq.get_item(callback.data.split('_')[1])
        items_basket = await rq.get_items_basket(callback.from_user.id, item.id)

        result = []
        result.append(f'Id товара: {item.id}\n')
        result.append(f'Название: {item.name}\n')
        result.append(f'Описание: {item.description}\n')
        result.append(f'Цена: {item.price} руб\n')
        result.append(f'В корзине: {len(items_basket.all())} шт.\n')
        item_basket_all = await rq.get_item_basket_all(item.id)
        result.append(f'В корзине у: {len(item_basket_all)} шт. пользователей\n')
        item_order = await rq.get_item_order_all(item.id)
        result.append(f'Заказали: {len(item_order)} шт.')

        await callback.message.answer_photo(item.photo_id, reply_markup=await kb.item_buttons(callback.data.split('_')[1], callback.data.split('_')[2]), caption=''.join(result))

    else:
        await callback.answer('Товара нету в корзине!')


@router.callback_query(F.data.startswith('mybasket_'))
async def item_basket(callback: CallbackQuery):
    await callback.answer('Корзина')
    my_items = await rq.get_my_basket(callback.from_user.id)
    items_data = {}
    all_price = 0
    for myitem in my_items:
        item = await rq.get_item(myitem.item)
        all_price += float(item.price)
        if item.name in items_data:
            items_data[item.name] = [items_data[item.name][0] + 1, items_data[item.name][1]]
        else:
            items_data[item.name] = [1, float(item.price)]

    result = []
    
    for name, cnt_price in items_data.items():
        result.append(f'{name} - {cnt_price[0]} x {cnt_price[1]} = {cnt_price[0] * cnt_price[1]}')

    if len(result) == 0:
        result.append('Корзина пуста')
        await callback.message.answer(reply_markup=await kb.basket_buttons2(callback.data.split('_')[1], callback.data.split('_')[2]), text='\n'.join(result))
    else:
        result.append(f'\nResult: {all_price}')
        await callback.message.answer('\n'.join(result), reply_markup=await kb.basket_buttons(callback.data.split('_')[1], callback.data.split('_')[2]))


@router.callback_query(F.data.startswith('back_buttons_'))
async def item_card(callback: CallbackQuery):
    await callback.answer('Назад')

    item = await rq.get_item(callback.data.split('_')[-2])
    items_basket = await rq.get_items_basket(callback.from_user.id, item.id)

    result = []
    result.append(f'Id товара: {item.id}\n')
    result.append(f'Название: {item.name}\n')
    result.append(f'Описание: {item.description}\n')
    result.append(f'Цена: {item.price} руб\n')
    result.append(f'В корзине: {len(items_basket.all())} шт.\n')
    item_basket_all = await rq.get_item_basket_all(item.id)
    result.append(f'В корзине у: {len(item_basket_all)} шт. пользователей\n')
    item_order = await rq.get_item_order_all(item.id)
    result.append(f'Заказали: {len(item_order)} шт.\n')

    await callback.message.answer_photo(item.photo_id,reply_markup=await kb.item_buttons(callback.data.split('_')[-2], callback.data.split('_')[-1]), caption=''.join(result))



@router.callback_query(F.data.startswith('delete_basket_'))
async def delete_basket(callback: CallbackQuery):
    await rq.delete_my_basket(callback.from_user.id)
    await callback.answer('Корзина удалена')
    my_items = await rq.get_my_basket(callback.from_user.id)
    items_data = {}
    all_price = 0
    for myitem in my_items:
        item = await rq.get_item(myitem.item)
        all_price += float(item.price)
        if item.name in items_data:
            items_data[item.name] = [items_data[item.name][0] + 1, items_data[item.name][1]]
        else:
            items_data[item.name] = [1, float(item.price)]

    result = []
    
    for name, cnt_price in items_data.items():
        result.append(f'{name} - {cnt_price[0]} x {cnt_price[1]} = {cnt_price[0] * cnt_price[1]}')

    if len(result) == 0:
        result.append('Выберите бренд товара')
    else:
        result.append(f'\nResult: {all_price}')

    await callback.message.edit_text('\n'.join(result))

    await callback.message.edit_reply_markup(reply_markup=await kb.catalog())


@router.callback_query(F.data.startswith('checkout_order'))
async def delete_basket(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Оформление зааза')

    data = await state.get_data()

    my_items = await rq.get_my_basket(callback.from_user.id)
    items_data = {}
    all_price = 0
    for myitem in my_items:
        item = await rq.get_item(myitem.item)
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

    result.append(f'Name: {data.get("name", "x")}')
    result.append(f'Number: {data.get("number", "x")}')
    result.append(f'Location: {data.get("location", "x")}')

    await callback.message.edit_text('\n'.join(result))
    await callback.message.edit_reply_markup(reply_markup=await kb.basket_buttons5())


@router.callback_query(F.data.startswith('enter_name'))
async def delete_basket(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Введите имя')
    await state.set_state(Reg.name)
    await callback.message.edit_text('Enter name:')

@router.message(Reg.name)
async def reg_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()

    my_items = await rq.get_my_basket(message.from_user.id)

    items_data = {}
    all_price = 0
    for myitem in my_items:
        item = await rq.get_item(myitem.item)
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

    result.append(f'Name: {data.get("name", "x")}')
    result.append(f'Number: {data.get("number", "x")}')
    result.append(f'Location: {data.get("location", "x")}')


    await message.answer('\n'.join(result), reply_markup=await kb.basket_buttons5())


@router.callback_query(F.data.startswith('enter_number'))
async def delete_basket(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Введите telephone')
    await state.set_state(Reg.number)
    await callback.message.edit_text('Enter phone:')

@router.message(Reg.number)
async def reg_name(message: Message, state: FSMContext):
    await state.update_data(number=message.text)
    data = await state.get_data()

    my_items = await rq.get_my_basket(message.from_user.id)

    items_data = {}
    all_price = 0
    for myitem in my_items:
        item = await rq.get_item(myitem.item)
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

    result.append(f'Name: {data.get("name", "x")}')
    result.append(f'Number: {data.get("number", "x")}')
    result.append(f'Location: {data.get("location", "x")}')


    await message.answer('\n'.join(result), reply_markup=await kb.basket_buttons5())


@router.callback_query(F.data.startswith('enter_location'))
async def delete_basket(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Введите lcation')
    await state.set_state(Reg.location)
    await callback.message.edit_text('Enter address:')

@router.message(Reg.location)
async def reg_name(message: Message, state: FSMContext):
    await state.update_data(location=message.text)
    data = await state.get_data()

    my_items = await rq.get_my_basket(message.from_user.id)

    items_data = {}
    all_price = 0
    for myitem in my_items:
        item = await rq.get_item(myitem.item)
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

    result.append(f'Name: {data.get("name", "x")}')
    result.append(f'Number: {data.get("number", "x")}')
    result.append(f'Location: {data.get("location", "x")}')


    await message.answer('\n'.join(result), reply_markup=await kb.basket_buttons5())



@router.callback_query(F.data.startswith('confirm'))
async def delete_basket(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    await rq.set_order(callback.from_user.id, data)

    await rq.delete_my_basket(callback.from_user.id)


    await callback.answer('спасибо за покупку!', show_alert=True)

    await callback.message.edit_text('Выберите категорию')
    await callback.message.edit_reply_markup(reply_markup=await kb.catalog())
    

@router.callback_query(F.data.startswith('zz11wdback_asdavvv'))
async def delete_basket(callback: CallbackQuery):
    await callback.answer('Назад')
    await callback.message.edit_text('Выберите категорию')
    await callback.message.edit_reply_markup(reply_markup=await kb.catalog())



@router.callback_query(F.data.startswith('agag111fsrgaefawdwad_'))
async def delete_basket(callback: CallbackQuery):
    await callback.answer('Заказы')

    item_id = callback.data.split('_')[-2]
    category_id = callback.data.split('_')[-1]

    await callback.message.answer('Заказы:', reply_markup=await kb.catalog3(callback.from_user.id, item_id, category_id))

@router.callback_query(F.data.startswith('oihfjhfkhlgw_'))
async def delete_basket(callback: CallbackQuery):

    await callback.answer('Назад')
    item = await rq.get_item(callback.data.split('_')[1])
    items_basket = await rq.get_items_basket(callback.from_user.id, item.id)

    result = []
    result.append(f'Id товара: {item.id}\n')
    result.append(f'Название: {item.name}\n')
    result.append(f'Описание: {item.description}\n')
    result.append(f'Цена: {item.price} руб\n')
    result.append(f'В корзине: {len(items_basket.all())} шт.\n')
    item_basket_all = await rq.get_item_basket_all(item.id)
    result.append(f'В корзине у: {len(item_basket_all)} шт. пользователей\n')
    item_order = await rq.get_item_order_all(item.id)
    result.append(f'Заказали: {len(item_order)} шт.')

    await callback.message.answer_photo(item.photo_id, reply_markup=await kb.item_buttons(callback.data.split('_')[1], callback.data.split('_')[2]), caption=''.join(result))


@router.callback_query(F.data.startswith('asdfgeaesgaeeg_'))
async def delete_basket(callback: CallbackQuery):
    item_id = callback.data.split('_')[1]
    category_id = callback.data.split('_')[2]

    order_id = callback.data.split('_')[3]
    order = await rq.get_order(order_id)

    order_items = await rq.get_order_items(order.id)

    my_items = order_items
    items_data = {}
    all_price = 0
    for myitem in my_items:
        item = await rq.get_item(myitem.item)
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

    await callback.message.edit_text(text='\n'.join(result))
    await callback.message.edit_reply_markup(reply_markup=await kb.sdfgsdfggw(item_id, category_id, order_id))


@router.callback_query(F.data.startswith('2sssz222w123123_'))
async def delete_basket(callback: CallbackQuery):
    
    await callback.answer('назад')

    item_id = callback.data.split('_')[-2]
    category_id = callback.data.split('_')[-1]

    await callback.message.edit_text('Заказы:')
    await callback.message.edit_reply_markup(reply_markup=await kb.catalog3(callback.from_user.id, item_id, category_id))



@router.callback_query(F.data.startswith('1233agefasef_'))
async def delete_basket(callback: CallbackQuery):
    
    await callback.answer('deleted')

    item_id = callback.data.split('_')[1]
    category_id = callback.data.split('_')[2]
    order_id = callback.data.split('_')[3]

    await rq.delete_order(order_id)

    await callback.message.edit_text('Заказы:')
    await callback.message.edit_reply_markup(reply_markup=await kb.catalog3(callback.from_user.id, item_id, category_id))


@router.callback_query(F.data.startswith('sdfiogusduiofhygui_'))
async def dfgjsdlkfgjkls(callback: CallbackQuery):
    await callback.answer('Корзина')
    my_items = await rq.get_my_basket(callback.from_user.id)
    items_data = {}
    all_price = 0
    for myitem in my_items:
        item = await rq.get_item(myitem.item)
        all_price += float(item.price)
        if item.name in items_data:
            items_data[item.name] = [items_data[item.name][0] + 1, items_data[item.name][1]]
        else:
            items_data[item.name] = [1, float(item.price)]

    result = []
    
    for name, cnt_price in items_data.items():
        result.append(f'{name} - {cnt_price[0]} x {cnt_price[1]} = {cnt_price[0] * cnt_price[1]}')


    result.append(f'\nResult: {all_price}' if all_price != 0 else 'корзина пуста')
    await callback.message.edit_text('\n'.join(result))

    await callback.message.edit_reply_markup(reply_markup=await kb.basket_buttons19() if all_price != 0 else await kb.basket_buttons20())



@router.callback_query(F.data.startswith('xkchjvlzkhxlvnvnvbn'))
async def dfgjsdlkfgjkls(callback: CallbackQuery):
    await callback.answer('back')
    await callback.message.edit_text('Выберите категорию')
    await callback.message.edit_reply_markup(reply_markup=await kb.catalog())



@router.callback_query(F.data.startswith('xcvkbhxckljb'))
async def delete_basket(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Оформление зааза')

    data = await state.get_data()

    my_items = await rq.get_my_basket(callback.from_user.id)
    items_data = {}
    all_price = 0
    for myitem in my_items:
        item = await rq.get_item(myitem.item)
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

    result.append(f'Name: {data.get("name", "x")}')
    result.append(f'Number: {data.get("number", "x")}')
    result.append(f'Location: {data.get("location", "x")}')

    await callback.message.edit_text('\n'.join(result))
    await callback.message.edit_reply_markup(reply_markup=await kb.basket_buttons5())



@router.callback_query(F.data.startswith('khvxcjkhvbxckjvb_'))
async def delete_basket(callback: CallbackQuery):
    await callback.answer('Заказы')


    await callback.message.edit_text('Заказы:')
    await callback.message.edit_reply_markup(reply_markup=await kb.catalog4(callback.from_user.id))
    


@router.callback_query(F.data.startswith('xv1111bxcvbxcvbxcvb_'))
async def delete_basket(callback: CallbackQuery):
    await callback.answer('Назад')


    await callback.message.edit_text('Выберите категорию')
    await callback.message.edit_reply_markup(reply_markup=await kb.catalog())



@router.callback_query(F.data.startswith('zxcfjghdkfjg_'))
async def delete_basket(callback: CallbackQuery):
    order_id = callback.data.split('_')[-1]
    order = await rq.get_order(order_id)

    order_items = await rq.get_order_items(order.id)

    my_items = order_items
    items_data = {}
    all_price = 0
    for myitem in my_items:
        item = await rq.get_item(myitem.item)
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

    await callback.message.edit_text(text='\n'.join(result))
    await callback.message.edit_reply_markup(reply_markup=await kb.xvxcvxcfasd213(order_id))


@router.callback_query(F.data.startswith('kgjdklgjdl_'))
async def delete_basket(callback: CallbackQuery):
    await callback.answer('Заказы')


    await callback.message.edit_text('Заказы:')
    await callback.message.edit_reply_markup(reply_markup=await kb.catalog4(callback.from_user.id))



@router.callback_query(F.data.startswith('xcvjxclkvlkxcjv_'))
async def delete_basket(callback: CallbackQuery):
    
    await callback.answer('deleted')

    order_id = callback.data.split('_')[-1]

    await rq.delete_order(order_id)

    await callback.message.edit_text('Заказы:')
    await callback.message.edit_reply_markup(reply_markup=await kb.catalog4(callback.from_user.id))