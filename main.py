import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
import os
from dotenv import load_dotenv

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name:", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")

        layout = QVBoxLayout()
        layout.addWidget(self.city_label)
        layout.addWidget(self.city_input)
        layout.addWidget(self.get_weather_button)
        layout.addWidget(self.temperature_label)
        layout.addWidget(self.emoji_label)
        layout.addWidget(self.description_label)

        self.setLayout(layout)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
            QLabel, QPushButton {
                font-family: papyrus;
            }
            QLabel#city_label {
                font-size: 40px;
                font-style: italic;
            }
            QLineEdit#city_input {
                font-size: 40px;
            }
            QPushButton#get_weather_button {
                font-size: 30px;
                font-weight: bold;
            }
            QLabel#temperature_label {
                font-size: 75px;
            }
            QLabel#emoji_label {
                font-size: 100px;
                font-family: Segoe UI emoji
            }
            QLabel#description_label {
                font-size: 50px;
            }
                        """)
        
        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        load_dotenv()
        api_key = os.getenv("OPENWEATHER_API_KEY")
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)
        except requests.exceptions.HTTPError as e:
            match response.status_code:
                case 400:
                    self.display_error("Bad request. Please check the city name.")
                case 404:
                    self.display_error("City not found.")
                case 401:
                    self.display_error("Invalid API key.")
                case 403:
                    self.display_error("Access forbidden. Please check your API key.")
                case 500:
                    self.display_error("Internal server error. Please try again later.")
                case 502:
                    self.display_error("Bad gateway. Please try again later.")
                case 503:
                    self.display_error("Service unavailable. Please try again later.")
                case 504:
                    self.display_error("Gateway timeout. Please try again later.")
                case _:
                    self.display_error("An error occurred while fetching the weather data.")
        except requests.exceptions.RequestException as e:
            self.display_error("Request Error: \n", e)
        except requests.exceptions.ConnectionError as e:
            self.display_error("Network error. Please check your internet connection.")
        except requests.exceptions.Timeout as e:
            self.display_error("Request timed out. Please try again later.")
        except requests.exceptions.TooManyRedirects as e:
            self.display_error("Too many redirects. Please check the URL.")

    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self, data):
        self.temperature_label.setStyleSheet("font-size: 75px;")
        temperature_c = data["main"]["temp"] - 273.15
        temperature_f = (temperature_c * 9/5) + 32
        self.temperature_label.setText(f"{temperature_f:.2f} °F")
        weather_description = data["weather"][0]["description"]
        weather_id = data["weather"][0]["id"]
        emoji = self.get_emoji(weather_id)
        self.description_label.setText(weather_description)
        self.emoji_label.setText(emoji)

    def get_emoji(self, weather_id):
        if 200 <= weather_id < 300:
            return "🌩️"
        elif 300 <= weather_id < 400:
            return "🌧️"
        elif 500 <= weather_id < 600:
            return "🌧️"
        elif 600 <= weather_id < 700:
            return "❄️"
        elif 700 <= weather_id < 800:
            return "🌫️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id < 900:
            return "⛅"
        else:
            return "❓"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())