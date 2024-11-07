import requests
import psycopg2
from decouple import config

DATABASE_NAME = config('DATABASE_NAME')
HOST_NAME = config('HOST_NAME')
USER = config('USER')
PASSWORD = config('PASSWORD')
PORT = config('PORT')

def connect_to_db():
    conn = psycopg2.connect(database=DATABASE_NAME,
                            host=HOST_NAME,
                            user=USER,
                            password=PASSWORD,
                            port=PORT)

    curse = conn.cursor()

    creat_table = '''CREATE TABLE IF NOT EXISTS car(
        name VARCHAR(255) NOT NULL,
        year INTEGER NOT NULL,
        mileage BIGINT NOT NULL,
        transmission VARCHAR(255) NOT NULL,
        fuel VARCHAR(255) NOT NULL,
        body_status VARCHAR(255) NOT NULL,
        price BIGINT NOT NULL
        );'''

    try:
        curse.execute(creat_table)
        status = True
        print("Table Created")
        conn.commit()
        return status, conn, curse
    except:
        print("Table already exists or warnning")
        status = False
        conn.rollback()
        conn.commit()
        return status

def bama(conn, curse):
    global status
    try:
        for i in range(0, 100):
            status = True
            url = 'https://bama.ir/cad/api/search?pageIndex=' + str(i)
            headers = {
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'fa-CA,fa;q=0.9,en-CA;q=0.8,en;q=0.7,cs-CA;q=0.6,cs;q=0.5,en-US;q=0.4',
                'cookie': '_ga=GA1.1.1451051775.1727341135; auth.globalUserContextId=b58dac9a-92ab-421a-a5f3-f8d23827a507; auth.strategy=oidc; _ga_W7213Q6KZ0=GS1.1.1727941282.4.1.1727941288.54.0.0',
                'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Linux"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'traceparent': '00-203518110a972fb08f068cd9bf9a7e95-0b9e41fc79e77235-01',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                'x-user-context': 'b58dac9a-92ab-421a-a5f3-f8d23827a507'
            }

            r = requests.get(url, headers=headers)
            data = r.json()
            for ad in data['data']['ads']:
                car_title = ad['detail']['title']
                car_title = car_title.replace(',', '').replace('.', '').replace('،', '')
                car_year = ad['detail']['year']
                car_year = int(car_year)
                if car_year > 1900:
                    car_year = car_year - 621
                car_mileage = ad['detail']['mileage']
                if car_mileage == "صفر کیلومتر":
                    car_mileage = 0
                elif car_mileage== "کارکرده":
                    car_mileage = 1000000
                else:
                    car_mileage = int(car_mileage.replace(',','').replace(' km', ''))
                car_transmission = ad['detail']['transmission']
                car_fuel = ad['detail']['fuel']
                car_body_status = ad['detail']['body_status']
                car_price = ad['price']['price']
                car_price = car_price.replace(',', '')
                car_price = int(car_price)
                check_data = f"SELECT * FROM car WHERE name = '{car_title}' AND year={car_year} AND mileage='{car_mileage}' AND transmission='{car_transmission}' AND body_status='{car_body_status}' AND price={car_price};"
                curse.execute(check_data)
                result = curse.fetchall()

                if len(result) > 0:
                    print("hast")
                else:
                    if car_price > 0:
                        insert_data = f'''INSERT INTO "car" (name, year, mileage, transmission, fuel, body_status, price)
                                                 VALUES ('{car_title}', {car_year}, '{car_mileage}', '{car_transmission}', '{car_fuel}', '{car_body_status}', {car_price});'''
                        curse.execute(insert_data)
            i += 1
        conn.commit()
        return status
    except Exception as e:
        status = False
        print(f"error in bama {e}")
        return status


