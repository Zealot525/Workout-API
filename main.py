import requests
import datetime as dt
import os

main_endpoint = os.environ.get("NUTRITIONIX_ENDPOINT")
X_ID  = os.environ.get("NUTRITIONIX_ID")
X_KEY = os.environ.get("NUTRITIONIX_KEY")
SHEETY_TOKEN = os.environ.get("SHEETY_TOKEN")
sheety_main_endpoint = os.environ.get("SHEETY_ENDPOINT")

header_auth = {
    "x-app-id": X_ID,
    "x-app-key": X_KEY
}

prompt = input("What did you do for trainning today?\n")

natural_exercise_endpoint = f"{main_endpoint}/v2/natural/exercise"
natural_exercise_params = {
    "query": prompt,
    "gender": "male",
    "weight_kg": "75",
    "height_cm": "170",
    "age": "21"
}


reponse = requests.post(url=natural_exercise_endpoint, json=natural_exercise_params,headers=header_auth)
reponse.raise_for_status()
data = reponse.json()

today = dt.datetime.now()
date = today.date().strftime("%Y-%m-%d")
time = today.time().strftime("%X")

#----------------------------------- SHEETY DOCS--------------------------------------#
first_sheet = "sheet1"
headers = {
    "Authorization": SHEETY_TOKEN,
}
sheety_endpoint = f"{sheety_main_endpoint}/{first_sheet}"

for exercise in data["exercises"]:
    exercise_record = {
        first_sheet: {
            "date" :  date,
            "time" : time,
            "exercise" : exercise["name"].title(),
            "duration" : exercise["duration_min"],
            "calories" : exercise["nf_calories"]
        }
    }

    post_request = requests.post(url=sheety_endpoint, json=exercise_record, headers=headers)
    post_request.raise_for_status()
    value =post_request.json()