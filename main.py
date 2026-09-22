# To run and test the code you need to update 4 places:
# 1. Change MY_EMAIL/MY_PASSWORD to your own details.
# 2. Go to your email provider and make it allow less secure apps.
# 3. Update the SMTP ADDRESS to match your email provider.
# 4. Update birthdays.csv to contain today's month and day.
# See the solution video in the 100 Days of Python Course for explainations.


import datetime as dt
import pandas
import random
import smtplib
import os

# import os and use it to get the Github repository secrets
MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")



def random_letter():
    letter_examples = ["letter_1.txt", "letter_3.txt", "letter_3.txt"] #cmt esta función nos escoge uno de los archivos aleatorios
    random_letter_pick = random.choice(letter_examples)
    return random_letter_pick #cmt y lo regresa para que podmaos utilizarlo


birthday_data = pandas.read_csv("birthdays.csv") #cmt Con ayuda de pandas leemos el archivo csv

friends_birthdays = { #cmt creamos un diccionario con los datos que vamos a agregar
    "name": ["Blanca", "Juan"],
    "email": ["burankita@gmail.com", "enriqueazpilcuet@hotmail.com"],
    "year": [1986, 1987],
    "month": [9,9],
    "day": [23, 23]
}

new_data =pandas.DataFrame(friends_birthdays) #cmt Creamos un Data Frame con los nuevos datos

all_birthdate_data = pandas.concat([birthday_data, new_data], axis=0, ignore_index=True) #cmt Concatenamos los diccionarios para tener toda la info
all_birthdate_data.to_csv("friends_birthdays2.csv", index=False) #cmt Después lo guardarmos en un CSV para que podmaos usar esa info posteriormente

#blq#################### Step 2 ######################
clean_birthday_data = pandas.read_csv("friends_birthdays2.csv").dropna() #cmt dropna hace que se eliminen
#cmt las filas con tengan valores nulos
final_df = pandas.DataFrame(clean_birthday_data) #cmt Convertimos el csv en un DataFrame

now = dt.datetime.now() #cmt Tomamos los valores de la fecha actual del sistema
today = now.day #cmt tomamos el valor del día de hoy
month = now.month

for index, row in final_df.iterrows(): #cmt Ahora vamos a recorrer las filas con iterrows
    if row["month"] == month and row["day"] == today: #cmt si el valor de la fila month coincide con el mes actual
        the_letter = random_letter() #cmt Almacenamos una carta aleatorio
        email_destination = row["email"]
        print(row["name"], email_destination)
        with open(f"letter_templates/{the_letter}", "r") as letter: #cmt abrimos el archivo como lectura
            letter_content = letter.read() #cmt Leemos el contenido y lo almacenamos
        new_letter = letter_content.replace("[NAME]", row["name"]) #cmt reemplazamos lo de los corchetes con el valor
        #cmt de la fila name en que los valores hayan coincidido con el bloque if (row[month) y row[day]

        # blq#################### Step 4.1 ######################
        connection = smtplib.SMTP("smtp.gmail.com", port=587)  # cmt Inicializamos la clase que se conectará al servicio
        connection.starttls()  # cmt Comienza la protección del intercambio de información
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)  # cmt Hacemos login con nuestras credenciales

        connection.sendmail(  # cmt La estructura para poder enviar el correo
            from_addr=MY_EMAIL,
            to_addrs=f"{email_destination}",
            msg=f"Subject: Happy Birthday\n\n{new_letter}")
        connection.close()  # cmt Cerramos la conexión
