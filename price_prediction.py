from crawler import bama, connect_to_db
from car_ai import predict_price, creat_ai

db, conn, curse = connect_to_db()
if db == True:
    bama = bama(conn, curse)
    if bama == True:
        creat_ai, label_encoders, model = creat_ai()
        if creat_ai == True:
            car_name = input("نام ماشین را وارد کنید: ")
            car_year = int(input("سال تولید ماشین را وارد کنید: "))
            car_mileage = int(input("کیلومتر ماشین را وارد کنید: "))
            car_transmission = input("مدل دنده ای یا اتوماتیک بودن ماشین را وارد کنید: ")
            car_fuel = input("مدل سوخت یعنی بنزینی گازسوز یا دوگانه سوز بودن ماشین خود را وارد کنید: ")
            car_body_status = input("میزان لک و خطو خش ماشین را وارد کنید: ")

            predicted_price = predict_price(car_name, car_year, car_mileage, car_transmission, car_fuel, car_body_status, label_encoders, model)
            print("Predicted Price:", predicted_price)
        else:
            print("There is a problem when creating ai")
    else:
        print("There was a problem in receiving information from the Bama site")
else:
    print("The connection to the database could not be established")