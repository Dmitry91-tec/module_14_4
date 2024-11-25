from aiogram import Bot, Dispatcher, executor, types            #Импортируем сущность бота, диспетчера, «executor», типы
from aiogram.contrib.fsm_storage.memory import MemoryStorage    #блока работы с памятью
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton   #lля работы с инлайн-клавиатурами
import asyncio
import crud_functions

api = ""
bot = Bot(token = api)                                                #Дальше понадобится api ключ, который мы получили в «BotFather». Так же переменная бота, она будет хранить объект бота, «token» будет равен вписанному ключу
dp = Dispatcher(bot, storage = MemoryStorage())                       #Понадобится «Dispatcher», который будет объектом «Dispatcher», у него будет наш бот в качестве аргументов. В качестве «Storage» будет «MemoryStorage»

kb = ReplyKeyboardMarkup(resize_keyboard=True)                        #инициализируем клавиатуру
button_1 = KeyboardButton(text = "Рассчитать")
button_2 = KeyboardButton(text = 'Информация')
button_3 = KeyboardButton(text = 'Купить')
kb.row(button_1)                                                      #добавим кнопки в клавиатуру
kb.row(button_2)
kb.row(button_3)

kb_in = InlineKeyboardMarkup()
button_in_1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button_in_2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb_in.add(button_in_1)
kb_in.add(button_in_2)

catalog_kb = InlineKeyboardMarkup()
button_cat_1 = InlineKeyboardButton(text="Product1", callback_data="Цена: 100")
button_cat_2 = InlineKeyboardButton(text="Product2", callback_data="Цена: 200")
button_cat_3 = InlineKeyboardButton(text="Product3", callback_data="Цена: 300")
button_cat_4 = InlineKeyboardButton(text="Product4", callback_data="Цена: 400")
catalog_kb.add(button_cat_1)
catalog_kb.add(button_cat_2)
catalog_kb.add(button_cat_3)
catalog_kb.add(button_cat_4)


@dp.message_handler(text = 'Купить')
async def get_all_products(message):
    await message.answer('Что вас интересует?', reply_markup=catalog_kb)
    with open("files/photo_2024-11-24_16-35-53.jpg","rb") as img1:
        await message.answer_photo(img1,f"Название: {crud_functions.title1}, Описание: {crud_functions.description1}, Цена: {crud_functions.price1}")
    with open("files/photo_2024-11-24_16-36-39.jpg","rb") as img2:
        await message.answer_photo(img2,f"Название: {crud_functions.title2}, Описание: {crud_functions.description2}, Цена: {crud_functions.price2}")
    with open("files/photo_2024-11-24_16-37-20.jpg", "rb") as img3:
        await message.answer_photo(img3, f"Название: {crud_functions.title3}, Описание: {crud_functions.description3}, Цена: {crud_functions.price3}")
    with open("files/photo_2024-11-24_16-38-01.jpg", "rb") as img4:
        await message.answer_photo(img4, f"Название: {crud_functions.title4}, Описание: {crud_functions.description4}, Цена: {crud_functions.price4}")


@dp.callback_query_handler(text = 'Цена: 100')
async def buy_100(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()

@dp.callback_query_handler(text = 'Цена: 200')
async def buy_200(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()

@dp.callback_query_handler(text = 'Цена: 300')
async def buy_300(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()

@dp.callback_query_handler(text = 'Цена: 400')
async def buy_400(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()

@dp.message_handler(text = 'Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup = kb_in)

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью.", reply_markup = kb)   #позволяет отображать клавиатуру

@dp.callback_query_handler(text = 'formulas')
async def get_formulas(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.callback_query_handler(text = 'calories')
async def set_age(call):
    await call.message.answer("Введите свой возраст:")               #ожидание получения сообщения от пользователя
    await call.answer()
    await UserState.age.set()                                   #для установки состояния и записи адреса


@dp.message_handler(state=UserState.age)                       #обработано не обычным хендлером, а хендлером состояния «@dp.message_handler()».
async def set_growth(message, state):                          #когда хендлер сработает, вы получите два объекта: «message» и «state», который представляет текущее состояние пользователя
    await state.update_data(first=message.text)                #позволяет обновить данные, связанные с текущим состоянием пользователя
    data = await state.get_data()                              #метод позволяет вернуть все данные, связанные с текущим состоянием пользователя
    await message.answer(f'Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)                   # обработано не обычным хендлером, а хендлером состояния «@dp.message_handler()».
async def set_weight(message,state):                          # когда хендлер сработает, вы получите два объекта: «message» и «state», который представляет текущее состояние пользователя
    await state.update_data(second=message.text)              # позволяет обновить данные, связанные с текущим состоянием пользователя
    data = await state.get_data()                             # метод позволяет вернуть все данные, связанные с текущим состоянием пользователя
    await message.answer(f'Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)                  # обработано не обычным хендлером, а хендлером состояния «@dp.message_handler()».
async def send_calories(message,state):                      # когда хендлер сработает, вы получите два объекта: «message» и «state», который представляет текущее состояние пользователя
    await state.update_data(third=message.text)              # позволяет обновить данные, связанные с текущим состоянием пользователя
    data = await state.get_data()                            # метод позволяет вернуть все данные, связанные с текущим состоянием пользователя
    result=round(10*int(data['second']) + 6.25*int(data['third'])-5*int(data['first']) + 5)
    await message.answer(f'Ваша норма каллорий {result}')
    await UserState.weight.set()
    await state.finish()                                                   #машина состояний завершила работу, ее необходимо закрыть с помощью метода



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)          #Запускаем «executor», у которого есть функция «start_polling». Объясняем, через кого ему запускаться