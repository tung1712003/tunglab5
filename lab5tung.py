import requests
import json
from tabulate import tabulate
import datetime
from tkinter import Tk, Label, Button
from PIL import Image, ImageTk
import io

# Задание 1
def get_weather(city_name):
    api_key = '590260f28e26ef37fbb58452bd15161c'
    response = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=5&appid={api_key}")
    data = response.json()
    lat = data[0]['lat']
    lon = data[0]['lon']
    r_city = requests.get(f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}")
    data_city = r_city.json()
    weather = f"{data_city['list'][0]['weather'][0]['main']}, {data_city['list'][0]['weather'][0]['description']}"
    humidity = data_city['list'][0]['main']['humidity']
    pressure = data_city['list'][0]['main']['pressure']
    return city_name, weather, humidity, pressure


info_tuple = get_weather('Kursk')
print(f"2. Информация о погоде в {info_tuple[0]}\nОписание погоды: {info_tuple[1]}\nВлажность: {info_tuple[2]}\n"
      f"Давление: {info_tuple[3]}\n")


# Задание 2
def json_parse(url):
    r = requests.get(url)
    data = json.loads(r.text)

    datetime_str = data['Date']
    datetime_obj = datetime.datetime.fromisoformat(datetime_str)
    date = datetime_obj.date()

    len_currencies = len(data['Valute'])

    info_headers = ['валюта', 'название валюты', 'текущий курс обмена валюты', 'прошлый курс обмена валюты']
    info = []
    for currency in data['Valute']:
        info.append([currency, data['Valute'][currency]['Name'], data['Valute'][currency]['Value'], data['Valute'][currency]['Previous']])

    return info, info_headers, date, len_currencies

total_info = json_parse("https://www.cbr-xml-daily.ru/daily_json.js")
print(f"\n2. Информация, полученная из API обменного курса cbr.ru\nдата: {total_info[2]}\nколичество считаемой валюты: {total_info[3]}"
      f"\n{tabulate(total_info[0], headers=total_info[1])}")

# Допзадание
def fox_display():
    window = Tk()
    window.title("Random Fox Generator")
    window.geometry('800x600')

    def get_random_fox():
        response = requests.get('https://randomfox.ca/floof/')
        fox_data = response.json()
        return fox_data['image']

    def load_fox_image(url):
        img_data = requests.get(url).content
        img = Image.open(io.BytesIO(img_data))
        photo = ImageTk.PhotoImage(img)
        return photo

    def update_fox_image():
        new_fox_url = get_random_fox()
        new_fox_image = load_fox_image(new_fox_url)
        fox_label.configure(image=new_fox_image)
        fox_label.image = new_fox_image  

    fox_url = get_random_fox()
    fox_image = load_fox_image(fox_url)

    fox_label = Label(window, image=fox_image)
    fox_label.place(x=0, y=0)

    b = Button(window, text="Изменить изображение", font=("Arial", 15), command=update_fox_image)
    b.grid(row=5, column=3)

    window.mainloop()

fox_display()