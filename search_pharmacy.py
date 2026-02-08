import sys
from io import BytesIO
import requests
from PIL import Image
import geocoder


def main():
    if len(sys.argv) < 2:
        return

    address = " ".join(sys.argv[1:])

    toponym = geocoder.geocode(address)
    if not toponym:
        print("Адрес не найден")
        return

    address_lon, address_lat = geocoder.get_coordinates(address)
    address_ll = f"{address_lon},{address_lat}"

    search_api = "https://search-maps.yandex.ru/v1/"
    search_params = {
        "apikey": "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3",
        "text": "аптека",
        "lang": "ru_RU",
        "ll": address_ll,
        "type": "biz",
        "results": 1
    }

    resp = requests.get(search_api, params=search_params)
    if not resp or not resp.json().get("features"):
        print("Аптека не найдена")
        return

    pharmacy = resp.json()["features"][0]
    ph_lon, ph_lat = pharmacy["geometry"]["coordinates"]
    pharmacy_ll = f"{ph_lon},{ph_lat}"

    distance = geocoder.calculate_distance(
        address_lon, address_lat, ph_lon, ph_lat)
    distance_str = f"{distance:.0f} м" if distance < 1000 else f"{distance/1000:.1f} км"

    props = pharmacy["properties"]["CompanyMetaData"]
    print(f"\n{'═'*50}")
    print(f"АДРЕС: {address}")
    print(f"АПТЕКА: {props.get('name', 'Неизвестно')}")
    print(f"АДРЕС АПТЕКИ: {props.get('address', 'Не указан')}")
    print(f"РАБОТАЕТ: {props.get('Hours', {}).get('text', 'Не указано')}")
    print(f"РАССТОЯНИЕ: {distance_str}")
    print(f"{'═'*50}\n")

    center_lon = (address_lon + ph_lon) / 2
    center_lat = (address_lat + ph_lat) / 2
    delta_lon = abs(address_lon - ph_lon) * 1.5
    delta_lat = abs(address_lat - ph_lat) * 1.5

    map_params = {
        "ll": f"{center_lon},{center_lat}",
        "spn": f"{delta_lon},{delta_lat}",
        "apikey": "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13",
        "l": "map",
        "pt": f"{address_ll},pm2al~{pharmacy_ll},pm2bl"
    }

    resp = requests.get(
        "https://static-maps.yandex.ru/1.x/", params=map_params)
    if resp:
        Image.open(BytesIO(resp.content)).show()
    else:
        print("Ошибка загрузки карты")


if __name__ == "__main__":
    main()
