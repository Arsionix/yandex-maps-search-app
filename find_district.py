import sys
import geocoder


def main():
    if len(sys.argv) < 2:
        return

    address = " ".join(sys.argv[1:])
    print(f"Ищу район для адреса: {address}")

    lon, lat = geocoder.get_coordinates(address)
    if not lon:
        print("Не нашел такой адрес :(")
        return

    district = geocoder.get_nearest_object((lon, lat), "district")

    if not district:
        print("Не нашел район")
        return

    print(f"\nАдрес находится в районе: {district}")


if __name__ == "__main__":
    main()
