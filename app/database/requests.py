from app.database.models import User, Category, Item, Basket, async_session, Order, OrderItem
from sqlalchemy import select, update, distinct


async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def get_categories():
    async with async_session() as session:
        return await session.scalars(select(Category))
    

async def get_item_basket_all(item_id):
    async with async_session() as session:
        result = await session.scalars(
            select(Basket).where(Basket.item == item_id).distinct(Basket.item)
        )
        results = []
        for item in result.all():
            results.append((item.user, item.item))

        return set(results)
    

async def get_item_order_all(item_id):
    async with async_session() as session:
        result = await session.scalars(
            select(OrderItem).where(OrderItem.item == item_id)
        )

        return set(result.all())
    

async def all_users():
    async with async_session() as session:
        result = await session.scalars(
            select(User)
        )

        return result.all()
    
async def edit_category(category_id, name):
    async with async_session() as session:
        await session.execute(update(Category).where(Category.id == category_id).values(name=name))
        await session.commit()
        


async def delete_category(category_id):
    async with async_session() as session:
        category = await session.scalar(select(Category).where(Category.id == category_id))
        await session.delete(category)
        await session.commit()


async def get_items(category_id):
    async with async_session() as session:
        return await session.scalars(select(Item).where(Item.category == category_id))


async def get_item(item_id):
    async with async_session() as session:
        item = await session.scalar(select(Item).where(Item.id == item_id))
        return item


async def set_item_basket(tg_id, item_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        session.add(Basket(user=user.id, item=item_id))
        await session.commit()


async def get_item_basket(tg_id, item_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        basket = await session.scalar(select(Basket).where(Basket.user == user.id, Basket.item == item_id))
        return basket
    

async def get_items_basket(tg_id, item_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        basket = await session.scalars(select(Basket).where(Basket.user == user.id, Basket.item == item_id))
        return basket
    

async def delete_item_basket(tg_id, item_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        basket = await session.scalar(select(Basket).where(Basket.user == user.id, Basket.item == item_id))
        await session.delete(basket)
        await session.commit()


async def get_my_basket(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        basket_items = await session.scalars(select(Basket).where(Basket.user == user.id))
        return basket_items


async def delete_my_basket(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        basket_items = await session.scalars(select(Basket).where(Basket.user == user.id))
        for item in basket_items:
            await session.delete(item)
        
        await session.commit()


async def delete_order(order_id):
    async with async_session() as session:
        order = await session.scalar(select(Order).where(Order.id == order_id))
        await session.delete(order)
        items = await get_order_items(order_id)
        for item in items:
            await session.delete(item)
        await session.commit()


async def get_order(order_id):
    async with async_session() as session:
        return await session.scalar(select(Order).where(Order.id == order_id))
    

async def add_category(name):
    async with async_session() as session:
        session.add(Category(name=name))
        await session.commit()


async def add_item(category_id, name, description, price, photo_id):
    async with async_session() as session:
        session.add(Item(category=category_id, name=name, description=description, price=price, photo_id=photo_id))
        await session.commit()


async def delete_item(item_id):
    async with async_session() as session:
        item = await session.scalar(select(Item).where(Item.id == item_id))
        await session.delete(item)
        await session.commit()


async def update_item_name(item_id, name):
    async with async_session() as session:
        await session.execute(update(Item).where(Item.id == item_id).values(name=name))
        await session.commit()


async def update_item_description(item_id, description):
    async with async_session() as session:
        await session.execute(update(Item).where(Item.id == item_id).values(description=description))
        await session.commit()


async def update_item_price(item_id, price):
    async with async_session() as session:
        await session.execute(update(Item).where(Item.id == item_id).values(price=price))
        await session.commit()


async def update_item_photo_id(item_id, photo_id):
    async with async_session() as session:
        await session.execute(update(Item).where(Item.id == item_id).values(photo_id=photo_id))
        await session.commit()

async def set_order_items(tg_id, order_id, basket):
    async with async_session() as session:
        for item in basket:
            session.add(OrderItem(order=order_id, item=item.id))
        await session.commit()


async def set_order(tg_id, data):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        order = Order(user=user.id, name=data['name'], number=data['number'], location=data['location'])
        session.add(order)

        await session.flush()

        basket = await get_my_basket(tg_id)

        for item in basket:
            session.add(OrderItem(order=order.id, item=item.item))

        await session.commit()


async def get_orders(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        orders = await session.scalars(select(Order).where(Order.user == user.id))
        return orders
    
async def get_order_items(order_id):
    async with async_session() as session:
        return await session.scalars(select(OrderItem).where(OrderItem.order == order_id))
