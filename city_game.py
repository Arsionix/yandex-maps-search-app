import requests
import random
from io import BytesIO
from PIL import Image
import geocoder

cities = ["Москва", "СПб", "Казань", "Сочи", "Екатеринбург"]


def get_part(city):
    ll, spn = geocoder.get_ll_span(city)
    if not ll:
        return None

    lon, lat = map(float, ll.split(","))
    w, h = map(float, spn.split(","))

    lon += random.uniform(-w/2, w/2)
    lat += random.uniform(-h/2, h/2)

    spn = f"{w/7},{h/7}"

    params = {
        "ll": f"{lon},{lat}",
        "spn": spn,
        "apikey": "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13",
        "l": "map"
    }

    r = requests.get("https://static-maps.yandex.ru/1.x/", params=params)
    return r.content if r else None


random.shuffle(cities)

for city in cities:
    print(f"\nГород: ???")

    img_data = get_part(city)
    if img_data:
        Image.open(BytesIO(img_data)).show()

    ans = input("Что за город? ")

    if ans.lower() == city.lower():
        print("Да!")
    else:
        print(f"Нет, это {city}")

    if input("Еще? (д/н): ").lower() != 'д':
        break

print("\nКонец игры!")
