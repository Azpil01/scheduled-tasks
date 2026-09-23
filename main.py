import datetime as dt
import pandas
import random
import smtplib
import os


MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")



def random_letter():
    letter_examples = ["letter_1.txt", "letter_3.txt", "letter_3.txt"] #cmt esta función nos escoge uno de los archivos aleatorios
    random_letter_pick = random.choice(letter_examples)
    return random_letter_pick #cmt y lo regresa para que podmaos utilizarlo


final_df = pandas.read_csv("birthdays.csv").dropna() 



now = dt.datetime.now()
today = now.day 
month = now.month

for index, row in final_df.iterrows(): #cmt Ahora vamos a recorrer las filas con iterrows
    if row["month"] == month and row["day"] == today: #cmt si el valor de la fila month coincide con el mes actual
        the_letter = random_letter() #cmt Almacenamos una carta aleatorio
        email_destination = row["email"]
        print(row["name"], email_destination)
        with open(f"letter_templates/{the_letter}", "r") as letter: #cmt abrimos el archivo como lectura
            letter_content = letter.read() #cmt Leemos el contenido y lo almacenamos
        new_letter = letter_content.replace("[NAME]", row["name"]) #cmt reemplazamos lo de los corchetes con el valor

        connection = smtplib.SMTP("smtp.gmail.com", port=587)  # cmt Inicializamos la clase que se conectará al servicio
        connection.starttls()  # cmt Comienza la protección del intercambio de información
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)  # cmt Hacemos login con nuestras credenciales

        connection.sendmail(  # cmt La estructura para poder enviar el correo
            from_addr=MY_EMAIL,
            to_addrs=f"{email_destination}",
            msg=f"Subject: Happy Birthday\n\n{new_letter}")
        connection.close()  # cmt Cerramos la conexión
