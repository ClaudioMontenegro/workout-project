import requests
from datetime import datetime
import os
import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns


GENDER = "cis male"
WEIGHT_KG = "100"
HEIGHT_CM = "192"
AGE = "30"

APP_ID = os.environ.get("APP_ID")
API_KEY = os.environ.get("API_KEY")
SHEETY_ENDPOINT = os.environ.get("SHEETY_ENDPOINT")
EXER_ENDPOINT = os.environ.get("EXER_ENDPOINT")
TOKEN = os.environ.get("TOKEN")

SHEETY_HEADERS = {
    "Authorization": TOKEN
}

headers = {
    'x-app-id': APP_ID,
    'x-app-key': API_KEY,
    "Content-Type": "application/json"
}

RES = input("What you did today?\n")

parameters = {
    "query": RES,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response = requests.post(EXER_ENDPOINT, headers=headers, json=parameters)
response.raise_for_status()
result = response.json()['exercises']


today = datetime.now()

for exercise in result:
    sheety_parameters = {
         "workout": {
            "date": today.strftime("%d/%m/%Y"),
            "time": today.strftime("%X"),
            "exercise": result[0]['name'].title(),
            "duration": result[0]['duration_min'],
            "calories": result[0]['nf_calories']

          }
    }

sheety_response = requests.post(url=SHEETY_ENDPOINT, json=sheety_parameters, headers=SHEETY_HEADERS)
sheety_response.raise_for_status()

sheety_response = requests.get(url=SHEETY_ENDPOINT, json=sheety_parameters, headers=SHEETY_HEADERS)
overall_result = json.dumps(sheety_response.json()['workouts'])
df = pd.read_json(overall_result)
print(df)
if input("Want to see your overall metrics? y/n\n").lower() == "y":
    overall_df = df[["date", "duration", "calories"]]
    print("Your overall statistics: \n")
    print(overall_df.describe())
    print("Your burning calories during time")
    plt.figure(figsize=(10, 5))
    sns.lineplot(x="date", y="calories", data=overall_df)
    plt.show()
    print("See you tomorrow! Keep going! o/")
else:
    print("See you tomorrow! Keep going! o/")
