import os
import requests
from typing import List, Dict
import openai
openai.api_base = "http://localhost:8080/v1"
api_key = 'http://127.0.0.1:7860/'
openai.api_key = api_key

todos = []
def lookup_location_id(location: str):
    city_search_url = f'https://geoapi.qweather.com/v2/city/lookup?location={location}&key=5239b457ad5b44c78c51782626f428b8'

    try:
        response = requests.get(city_search_url)
        data = response.json()

        # Extract the location ID of the first result.
        location_id = data['location'][0]['id']

        return location_id
    except Exception as e:
        print(f"An error occurred while looking up location ID: {e}")
        return None


def get_current_weather(location: str):
    location_id = str(lookup_location_id(location))

    if location_id is None:
        return "Sorry, I couldn't find weather information for that location."

    # Build the URL for the real-time weather API
    weather_api_url = f'https://devapi.qweather.com/v7/weather/now?location={location_id}&key=5239b457ad5b44c78c51782626f428b8'

    # Send a request to get real-time weather information
    try:
        response = requests.get(weather_api_url)
        data = response.json()
        # Parse weather information
        feels_like = data['now']['feelsLike']
        text = data['now']['text']
        humidity = data['now']['humidity']
        # Build the reply message
        weather_info = f"Temperature: {feels_like} Description: {text} Humidity: {humidity}"
        return weather_info
    except Exception as e:
        print(f"An error occurred while fetching weather information: {e}")
        return None

def add_todo(todo: str):
    global todos

    todos.append(todo)
    formatted_todos = ["- " + item for item in todos]
    todo_list = "\n".join(formatted_todos)

    return todo_list

def function_calling(messages: List[Dict]):
    for message in messages:
        content = message["content"]
        if content.startswith("Add a todo:"):
            todo = content.replace("Add a todo:", "").strip()
            response = add_todo(todo)
            return str(response)
        if content.startswith("What's the weather like in"):
            city = content.replace("What's the weather like in", "").strip('?').strip()
            response = get_current_weather(city)
            return str(response)

'''
if __name__ == "__main__":
    messages = [{"role": "user", "content": "Add a todo: walk"}]
    response = function_calling(messages)
    print(response)
    messages = [{"role": "user", "content": "/function Add a todo: sleep"}]
    response = function_calling(messages)
    print(response)
    messages = [{"role": "user", "content": "/function What's the weather like in Tashkent"}]
    response = function_calling(messages)
    print(response)
'''