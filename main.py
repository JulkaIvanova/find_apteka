import requests
from io import BytesIO
from PIL import Image
from geopy.distance import geodesic



search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
# address_ll = "65.353587,55.447509"
address_ll = "37.588392,55.704036"
search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": address_ll,
    "type": "biz"
}
response = requests.get(search_api_server, params=search_params)
json_response = response.json()


organization = json_response["features"][0]
org_name = organization["properties"]["CompanyMetaData"]["name"]
org_address = organization["properties"]["CompanyMetaData"]["address"]
org_hours = organization["properties"]["CompanyMetaData"]["Hours"]["text"]
point = organization["geometry"]["coordinates"]
org_point = f"{point[0]},{point[1]}"
distance = geodesic((float(address_ll.split(',')[1]), float(address_ll.split(',')[0])),
                    (float(org_point.split(',')[1]), float(org_point.split(',')[0]))).meters
snippet = f"""
Название аптеки: {org_name}
Адрес аптеки: {org_address}
Время работы: {org_hours}
Расстояние до аптеки: {distance:.2f} метров
"""

print(snippet)
json_response = response.json()
apikey = "37db8bb4-5347-4a85-a54f-a594f7c123ea"
map_params = {
    "ll": address_ll,
    "apikey": apikey,
    "pt": f"{org_point},pm2rdm~{address_ll},pm2gnm",
}

map_api_server = "https://static-maps.yandex.ru/v1"
response = requests.get(map_api_server, params=map_params)
im = BytesIO(response.content)
opened_image = Image.open(im)
opened_image.show()
