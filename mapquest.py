import urllib.parse
import requests
from googletrans import Translator
import datetime

main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "Xd35VebxDItDc2GZLOopJW2kZRWgrbPL"

# Eficiencia promedio del combustible en MPG (millas por galón)
average_fuel_efficiency = 25

translator = Translator()

while True:
    orig = input("Ubicación de partida: ")
    if orig == "M" or orig == "m":
        break
    dest = input("Destino: ")
    if dest == "M" or dest == "m":
        break

    url = main_api + urllib.parse.urlencode({"key": key, "from": orig, "to": dest})
    print("URL: " + url)
    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]
    if json_status == 0:
        print("Estado de la API: " + str(json_status) + " = Llamada de ruta exitosa.\n")
        print("=============================================")
        
        # Obtener la hora local
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        print("Bienvenido a la prueba 2! La hora actual es: " + current_time)
        
        print("Cómo llegar desde " + orig + " a " + dest)
        print("Duración del viaje:   " + json_data["route"]["formattedTime"])
        print("Kilómetros: " + str("{:.2f}".format(json_data["route"]["distance"] * 1.61)))

        # Estimación del combustible utilizado
        if "fuelUsed" in json_data["route"]:
            fuel_used = json_data["route"]["fuelUsed"]
            print("Combustible utilizado (Ltr): " + str("{:.2f}".format(fuel_used * 3.78)))
        else:
            distance_miles = json_data["route"]["distance"]
            fuel_used_estimation = distance_miles / average_fuel_efficiency
            print("No se pudieron obtener los datos de combustible de MapQuest.")
            print("Estimado del combustible utilizado (Ltr): " + str("{:.2f}".format(fuel_used_estimation * 3.78)))

        print("=============================================")

        print("Maniobras en español:")
        maneuvers = json_data["route"]["legs"][0]["maneuvers"]
        for maneuver in maneuvers:
            narrative = maneuver["narrative"]
            distance_km = maneuver["distance"] * 1.61
            translated_narrative = translator.translate(narrative, dest="es").text
            print("- " + translated_narrative + " (" + str("{:.2f}".format(distance_km)) + " km)")

        print("=============================================")
        
    elif json_status == 402:
        print("**********************************************")
        print("Código de estado: " + str(json_status) + "; Entradas de usuario inválidas para una o ambas ubicaciones.")
        print("**********************************************\n")
    elif json_status == 611:
        print("**********************************************")
        print("Código de estado: " + str(json_status) + "; Falta una entrada para una o ambas ubicaciones.")
        print("**********************************************\n")
    else:
        print("************************************************************************")
       