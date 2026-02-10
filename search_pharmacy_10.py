import sys
import requests
from io import BytesIO
from PIL import Image
import geocoder

GREEN = "pm2gnl"
BLUE = "pm2bll"
GRAY = "pm2grl"


def get_color(apteka):
    hours = apteka.get("Hours")
    if not hours:
        return GRAY

    text = hours.get("text", "").lower()
    if "круглосуточно" in text or "24" in text:
        return GREEN
    return BLUE


def main():
    if len(sys.argv) < 2:
        return

    my_address = " ".join(sys.argv[1:])
    print(f"Ищу аптеки рядом с: {my_address}")

    my_lon, my_lat = geocoder.get_coordinates(my_address)
    if not my_lon:
        print("Не нашел такой адрес")
        return

    url = "https://search-maps.yandex.ru/v1/"
    params = {
        "apikey": "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3",
        "text": "аптека",
        "lang": "ru_RU",
        "ll": f"{my_lon},{my_lat}",
        "type": "biz",
        "results": 10
    }

    r = requests.get(url, params=params)
    if not r or not r.json().get("features"):
        print("Не нашел аптек")
        return

    aptekas = r.json()["features"]
    print(f"\nНашел {len(aptekas)} аптек:")

    points = [f"{my_lon},{my_lat},pm2rdl"]

    for apt in aptekas:
        coords = apt["geometry"]["coordinates"]
        lon, lat = coords[0], coords[1]

        info = apt["properties"]["CompanyMetaData"]
        name = info.get("name", "Аптека")

        color = get_color(info)
        if color == GREEN:
            status = "круглосуточно"
        elif color == BLUE:
            status = "не круглосуточно"
        else:
            status = "неизвестно"

        print(f"- {name} ({status})")
        points.append(f"{lon},{lat},{color}")

    all_lons = [my_lon]
    all_lats = [my_lat]
    for apt in aptekas:
        coords = apt["geometry"]["coordinates"]
        all_lons.append(coords[0])
        all_lats.append(coords[1])

    center_lon = (min(all_lons) + max(all_lons)) / 2
    center_lat = (min(all_lats) + max(all_lats)) / 2
    delta = max(max(all_lons)-min(all_lons), max(all_lats)-min(all_lats)) * 1.3

    map_params = {
        "ll": f"{center_lon},{center_lat}",
        "spn": f"{delta},{delta}",
        "apikey": "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13",
        "l": "map",
        "pt": "~".join(points)
    }

    r = requests.get("https://static-maps.yandex.ru/1.x/", params=map_params)
    if r:
        img = Image.open(BytesIO(r.content))
        img.show()
    else:
        print("Ошибка с картой")


if __name__ == "__main__":
    main()
