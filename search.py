import sys
from io import BytesIO
import requests
from PIL import Image
import geocoder

STATIC_API_KEY = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"


def main():
    if len(sys.argv) < 2:
        return

    address = " ".join(sys.argv[1:])

    ll, spn = geocoder.get_ll_span(address)

    if not ll:
        print("Адрес не найден")
        return

    lon, lat = geocoder.get_coordinates(address)

    map_params = {
        "ll": ll,
        "spn": spn,
        "apikey": STATIC_API_KEY,
        "l": "map",
        "pt": f"{lon},{lat},pm2dgl"
    }

    response = requests.get(
        "https://static-maps.yandex.ru/1.x/", params=map_params)

    if response:
        Image.open(BytesIO(response.content)).show()
    else:
        print("Ошибка")


if __name__ == "__main__":
    main()
