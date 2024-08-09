from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command, Filter

from app import keyboards as kb
from app.database import requests as rq


from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


class Reklama(StatesGroup):
    photo_id = State()
    description = State()


class AddCategory(StatesGroup):
    name = State()

class EditCategory(StatesGroup):
    name = State()
    category_id = State()

class Additem(StatesGroup):
    name = State()
    description = State()
    price = State()
    category_id = State()
    item_id = State()
    photo_id = State()

class EditItem(StatesGroup):
    name = State()
    description = State()
    price = State()
    category_id = State()
    item_id = State()
    photo_id = State()

admin = Router()

class Admin(Filter):
    def __init__(self):
        self.admins = [7015270939]

    async def __call__(self, message: Message):
        return message.from_user.id in self.admins
    

@admin.message(Admin(), Command('admin'))
async def cmd_start(message: Message):
    await message.answer('Добро пожаловать в бот, администратор!', reply_markup=await kb.basket_buttons6())


@admin.callback_query(Admin(), F.data == 'admin_categories')
async def catalog(callback: CallbackQuery):
    await callback.answer('Категории')
    await callback.message.edit_text('Выберите  товара')
    await callback.message.edit_reply_markup(reply_markup=await kb.catalog_admin())

    
@admin.callback_query(Admin(), F.data == 'admin_back_reply')
async def catalog(callback: CallbackQuery):
    await callback.answer('Назад')
    await callback.message.edit_text('Назад')
    await callback.message.answer('Добро пожаловать в бот, администратор!', reply_markup=await kb.basket_buttons6())


@admin.callback_query(Admin(), F.data == 'afjasfhasjkfhkasj_')
async def catalog(callback: CallbackQuery):
    await callback.answer('Назад')
    await callback.message.answer('Привет! Добро пожаловать в магазин',
                         reply_markup=kb.main)



@admin.callback_query(Admin(), F.data == 'admin_add_category')
async def catalog(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Add')
    await callback.message.edit_text('enter category name:')
    await state.set_state(AddCategory.name)


@admin.message(Admin(), AddCategory.name)
async def catalog(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    name = data['name']
    await state.clear()

    await rq.add_category(name)

    await message.answer('Выберите товара', reply_markup=await kb.catalog_admin())


@admin.callback_query(Admin(), F.data.startswith('admin_category_'))
async def catalog(callback: CallbackQuery):
    category_id = callback.data.split('_')[-2]
    category_name = callback.data.split('_')[-1]

    await callback.message.edit_text(f'{category_name}')
    await callback.message.edit_reply_markup(reply_markup=await kb.basket_buttons7(category_id))


@admin.callback_query(Admin(), F.data == 'fffasfasf')
async def catalog(callback: CallbackQuery):
    await callback.answer('Назад')
    await callback.message.edit_text('Выберите товара')
    await callback.message.edit_reply_markup(reply_markup=await kb.catalog_admin())


@admin.callback_query(Admin(), F.data.startswith('afawfawfasdgsdg_'))
async def catalog(callback: CallbackQuery):
    category_id = callback.data.split('_')[-1]
    await callback.answer('deleted')
    await rq.delete_category(category_id)
    await callback.message.edit_text('Выберите товара')
    await callback.message.edit_reply_markup(reply_markup=await kb.catalog_admin())


@admin.callback_query(Admin(), F.data.startswith('asdfgsgs_'))
async def catalog(callback: CallbackQuery, state: FSMContext):
    category_id = callback.data.split('_')[-1]

    await callback.message.edit_text('new name:')

    await state.update_data(category_id=category_id)
    await state.set_state(EditCategory.name)


@admin.message(Admin(), EditCategory.name)
async def catalog(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    name = data['name']
    category_id = data['category_id']
    await state.clear()

    await rq.edit_category(category_id, name)

    await message.answer(f'{name}', reply_markup=await kb.basket_buttons7(category_id))


@admin.callback_query(Admin(), F.data == ('asdasfawf'))
async def category_items(callback: CallbackQuery):
    await callback.answer('Назад')
    await callback.message.edit_text('Назад')
    await callback.message.answer('Привет! Добро пожаловать в магазин',
                         reply_markup=kb.main)
    

@admin.callback_query(Admin(), F.data == ('admin_items'))
async def category_items(callback: CallbackQuery):
    await callback.message.edit_text('choose category')
    await callback.message.edit_reply_markup(reply_markup=await kb.catalog2())



@admin.callback_query(Admin(), F.data.startswith('gisjdgoshdugi_'))
async def category_items(callback: CallbackQuery):
    category_id = callback.data.split('_')[-1]
    await callback.message.edit_text('choose item')
    await callback.message.edit_reply_markup(reply_markup=await kb.items2(category_id))



@admin.callback_query(Admin(), F.data == ('sdlfgjkdflkgjslkdg'))
async def category_items(callback: CallbackQuery):
    await callback.answer('Назад')
    await callback.message.edit_text('choose category')
    await callback.message.edit_reply_markup(reply_markup=await kb.catalog2())


@admin.callback_query(Admin(), F.data.startswith('safafawf2121_'))
async def category_items(callback: CallbackQuery, state: FSMContext):
    category_id = callback.data.split('_')[-1]
    await state.update_data(category_id=category_id)

    await callback.message.edit_text('enter name item')
    await state.set_state(Additem.name)

@admin.message(Admin(), Additem.name)
async def category_items(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    await message.answer('enter description')
    await state.set_state(Additem.description)


@admin.message(Admin(), Additem.description)
async def category_items(message: Message, state: FSMContext):
    await state.update_data(description=message.text)

    await message.answer('enter price')
    await state.set_state(Additem.price)


@admin.message(Admin(), Additem.price)
async def category_items(message: Message, state: FSMContext):
    await state.update_data(price=message.text)

    await message.answer('enter photo')
    await state.set_state(Additem.photo_id)


@admin.message(Admin(), Additem.photo_id)
async def category_items(message: Message, state: FSMContext):
    await state.update_data(photo_id=message.photo[-1].file_id)

    data = await state.get_data()
    await state.clear()

    await rq.add_item(data['category_id'], data['name'], data['description'], data['price'], data['photo_id'])

    await message.answer('choose item', reply_markup=await kb.items2(data['category_id']))


@admin.callback_query(Admin(), F.data.startswith('41412413wdasd_'))
async def category_items(callback: CallbackQuery):
    item_id = callback.data.split('_')[-2]
    category_id = callback.data.split('_')[-1]

    item = await rq.get_item(item_id)

    await callback.message.answer_photo(item.photo_id, reply_markup=await kb.basket_buttons8(category_id, item_id), caption=f'id: {item.id}\nname: {item.name}\ndescription: {item.description}\nprice: {item.price}')

@admin.callback_query(Admin(), F.data.startswith('asfawasdasda1111_'))
async def category_items(callback: CallbackQuery):
    category_id = callback.data.split('_')[-1]

    await callback.message.answer(f'choose item', reply_markup=await kb.items2(category_id))


@admin.callback_query(Admin(), F.data.startswith('hdmfklhghlk_'))
async def category_items(callback: CallbackQuery):
    item_id = callback.data.split('_')[-1]
    category_id = callback.data.split('_')[-2]

    await rq.delete_item(item_id)

    await callback.message.answer(f'choose item', reply_markup=await kb.items2(category_id))


@admin.callback_query(Admin(), F.data.startswith('awwaaw13123_'))
async def category_items(callback: CallbackQuery):
    item_id = callback.data.split('_')[-2]
    category_id = callback.data.split('_')[-1]

    item = await rq.get_item(item_id)

    await callback.message.answer_photo(item.photo_id, reply_markup=await kb.basket_buttons9(category_id, item_id), caption=f'id:{item.id}\nname: {item.name}\ndescription: {item.description}\nprice: {item.price}')



@admin.callback_query(Admin(), F.data.startswith('adahfa12312415_'))
async def category_items(callback: CallbackQuery):
    item_id = callback.data.split('_')[-2]
    category_id = callback.data.split('_')[-1]

    item = await rq.get_item(item_id)

    await callback.message.answer_photo(item.photo_id, reply_markup=await kb.basket_buttons8(category_id, item_id), caption=f'id:{item.id}\nname: {item.name}\ndescription: {item.description}\nprice: {item.price}')


@admin.callback_query(Admin(), F.data.startswith('2222w123123_'))
async def category_items(callback: CallbackQuery, state: FSMContext):
    item_id = callback.data.split('_')[-2]
    category_id = callback.data.split('_')[-1]

    await state.update_data(category_id=category_id)
    await state.update_data(item_id=item_id)
    await state.set_state(EditItem.name)

    await callback.message.answer('enter name')

@admin.message(Admin(), EditItem.name)
async def category_items(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    await state.clear()

    category_id = data['category_id']
    item_id = data['item_id']
    name = data['name']

    await rq.update_item_name(item_id, name)

    item = await rq.get_item(item_id)

    await message.answer_photo(item.photo_id, reply_markup=await kb.basket_buttons9(category_id, item_id), caption=f'id:{item.id}\nname: {item.name}\ndescription: {item.description}\nprice: {item.price}')



@admin.callback_query(Admin(), F.data.startswith('1111asfgaethdthfg_'))
async def category_items(callback: CallbackQuery, state: FSMContext):
    item_id = callback.data.split('_')[-2]
    category_id = callback.data.split('_')[-1]

    await state.update_data(category_id=category_id)
    await state.update_data(item_id=item_id)
    await state.set_state(EditItem.description)

    await callback.message.answer('enter description')

@admin.message(Admin(), EditItem.description)
async def category_items(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    data = await state.get_data()
    await state.clear()

    category_id = data['category_id']
    item_id = data['item_id']
    description = data['description']

    await rq.update_item_description(item_id, description)

    item = await rq.get_item(item_id)

    await message.answer_photo(item.photo_id, reply_markup=await kb.basket_buttons9(category_id, item_id), caption=f'id:{item.id}\nname: {item.name}\ndescription: {item.description}\nprice: {item.price}')


@admin.callback_query(Admin(), F.data.startswith('222223saas212gdflkgjdlfkg_'))
async def category_items(callback: CallbackQuery, state: FSMContext):
    item_id = callback.data.split('_')[-2]
    category_id = callback.data.split('_')[-1]

    await state.update_data(category_id=category_id)
    await state.update_data(item_id=item_id)
    await state.set_state(EditItem.price)

    await callback.message.answer('enter price')

@admin.message(Admin(), EditItem.price)
async def category_items(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    data = await state.get_data()
    await state.clear()

    category_id = data['category_id']
    item_id = data['item_id']
    price = data['price']

    await rq.update_item_price(item_id, price)

    item = await rq.get_item(item_id)

    await message.answer_photo(item.photo_id, reply_markup=await kb.basket_buttons9(category_id, item_id), caption=f'id:{item.id}\nname: {item.name}\ndescription: {item.description}\nprice: {item.price}')



@admin.callback_query(Admin(), F.data.startswith('1z234saasdf_'))
async def category_items(callback: CallbackQuery, state: FSMContext):
    item_id = callback.data.split('_')[-2]
    category_id = callback.data.split('_')[-1]

    await state.update_data(category_id=category_id)
    await state.update_data(item_id=item_id)
    await state.set_state(EditItem.photo_id)

    await callback.message.answer('enter photo')

@admin.message(Admin(), EditItem.photo_id)
async def category_items(message: Message, state: FSMContext):
    await state.update_data(photo_id=message.photo[-1].file_id)
    data = await state.get_data()
    await state.clear()

    category_id = data['category_id']
    item_id = data['item_id']
    photo_id = data['photo_id']

    await rq.update_item_photo_id(item_id, photo_id)

    item = await rq.get_item(item_id)

    await message.answer_photo(item.photo_id, reply_markup=await kb.basket_buttons9(category_id, item_id), caption=f'id:{item.id}\nname: {item.name}\ndescription: {item.description}\nprice: {item.price}')



@admin.callback_query(Admin(), F.data.startswith('sdgjdklfgjldskfgl_'))
async def category_items(callback: CallbackQuery, state: FSMContext):
    await callback.answer('рассылка')
    data = await state.get_data()

    photo_id = data.get('photo_id', None)
    description = data.get('description', None)

    if photo_id:
        await callback.message.answer_photo(photo_id, caption=description if description else 'no description provided', reply_markup=await kb.basket_buttons32())
    else:
        await callback.message.answer(text=description if description else 'no description provided', reply_markup=await kb.basket_buttons32())


@admin.callback_query(Admin(), F.data.startswith('c12312sdfjzklf'))
async def cmd_start(callback: CallbackQuery):
    await callback.answer('Отмена')
    await callback.message.answer('Добро пожаловать в бот, администратор!', reply_markup=await kb.basket_buttons6())



@admin.callback_query(Admin(), F.data.startswith('vbcvkjbhcvhkbj_'))
async def category_items(callback: CallbackQuery, state: FSMContext):
    await callback.answer('фото')
        
    await state.set_state(Reklama.photo_id)

    await callback.message.answer('enter photo')
    

@admin.message(Admin(), Reklama.photo_id)
async def category_items(message: Message, state: FSMContext):
    await state.update_data(photo_id=message.photo[-1].file_id)
    data = await state.get_data()

    photo_id = data.get('photo_id', None)
    description = data.get('description', None)

    if photo_id:
        await message.answer_photo(photo_id, caption=description if description else 'no description provided', reply_markup=await kb.basket_buttons32())
    else:
        await message.answer(text=description if description else 'no description provided', reply_markup=await kb.basket_buttons32())

    

@admin.callback_query(Admin(), F.data.startswith('lclbhcjlkbhcjvkb_'))
async def category_items(callback: CallbackQuery, state: FSMContext):
    await callback.answer('описание')
        
    await state.set_state(Reklama.description)

    await callback.message.answer('enter description')


@admin.message(Admin(), Reklama.description)
async def category_items(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    data = await state.get_data()

    photo_id = data.get('photo_id', None)
    description = data.get('description', None)

    if photo_id:
        await message.answer_photo(photo_id, caption=description if description else 'no description provided', reply_markup=await kb.basket_buttons32())
    else:
        await message.answer(text=description if description else 'no description provided', reply_markup=await kb.basket_buttons32())



@admin.callback_query(Admin(), F.data.startswith('xcklbxclkblxcjvblk_'))
async def category_items(callback: CallbackQuery, state: FSMContext):
    await callback.answer('отправка')

    data = await state.get_data()

    photo_id = data.get('photo_id', None)
    description = data.get('description', None)

    if photo_id and description:
        users = await rq.all_users()
        for user in users:
            await callback.message.bot.send_photo(chat_id=user.tg_id, photo=photo_id, caption=description)
            await callback.answer(f'отправлено user: {user.tg_id}')
        await callback.message.answer('Добро пожаловать в бот, администратор!', reply_markup=await kb.basket_buttons6())
    else:
        await callback.answer('no photo or description provided', show_alert=True)