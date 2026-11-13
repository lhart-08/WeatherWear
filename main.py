from dataclasses import dataclass
from bakery import assert_equal
from drafter import *

@dataclass
class Outfit:
    top: str
    bottom: str
    accessories: list[str]
    style: str

"""Outfit stores the individual clothing recommendations"""

@dataclass
class State:
    location: str
    temperature: float
    weather_condition: str
    preferred_style: str
    include_accessories: bool
    outfit_history: list[Outfit]

"""outfit_history stores multiple Outfit instances, include_accessories stores whether the user wants additional accessories, State stores the information that needs to be carried between routes"""

# HOME PAGE
@route
def index(state: State) -> Page:
    return Page(state, [
        Header("Welcome to WeatherWear!"),
        Text("Get personalized outfit recommendations based on your local weather."),
        Button("Plan My Outfit", location_page)])

# LOCATION PAGE
@route
def location_page(state: State) -> Page:
    return Page(state, [
        Header("Where are you located?"),
        Text("Enter your city below."),
        TextBox("new_location", state.location),
        Button("Continue", save_location),
        Button("Home", index)])


# SAVE LOCATION
@route
def save_location(state: State, new_location: str) -> Page:
    state.location = new_location
    return preferences_page(state)


# PREFERENCES PAGE
@route
def preferences_page(state: State) -> Page:
    return Page(state, [
        Header("Choose Your Style"),
        Text("What type of clothing do you prefer?"),
        SelectBox("new_style",
                  ["Casual", "Sporty", "Formal"],
                  state.preferred_style),
        Text("Would you like additional accessories?"),
        CheckBox("new_accessories", state.include_accessories),
        Button("Continue", save_preferences),
        Button("Back", location_page)])


# SAVE PREFERENCES
@route
def save_preferences(state: State, new_style: str,
                     new_accessories: bool) -> Page:
    state.preferred_style = new_style
    state.include_accessories = new_accessories
    return weather_page(state)


# WEATHER PAGE
@route
def weather_page(state: State) -> Page:
    return Page(state, [
        Header("Today's Weather"),
        Text("Enter the current temperature in Fahrenheit."),
        TextBox("new_temperature", state.temperature, "number"),
        Text("Select the current weather condition."),
        SelectBox("new_weather",
                  ["Sunny", "Cloudy", "Rainy", "Snowy", "Windy"],
                  state.weather_condition),
        Button("Save Weather", save_weather),
        Button("Back", preferences_page)])


# SAVE WEATHER
@route
def save_weather(state: State, new_temperature: float,
                 new_weather: str) -> Page:
    state.temperature = new_temperature
    state.weather_condition = new_weather
    return generate_outfit(state)


# GENERATE OUTFIT
@route
def generate_outfit(state: State) -> Page:

    # Determine clothing based on temperature
    if state.temperature < 50:
        top = "Sweater or jacket"
        bottom = "Long pants"

    elif state.temperature <= 75:
        top = "Long sleeve shirt or T-shirt"
        bottom = "Jeans"

    else:
        top = "Tank top or T-shirt"
        bottom = "Shorts or skirt"

    # Determine clothing based on preferred style
    if state.preferred_style == "Sporty":
        top = "Athletic sweatshirt or shirt"
        bottom = "Leggings or athletic shorts"

    elif state.preferred_style == "Formal":
        top = "Blouse"
        bottom = "Dress pants"

    # Create an accessories list
    accessories = []

    if state.weather_condition == "Rainy":
        accessories.append("Umbrella")
        accessories.append("Rain boots")

    elif state.weather_condition == "Snowy":
        accessories.append("Scarf")
        accessories.append("Gloves")

    elif state.weather_condition == "Sunny":
        accessories.append("Sunglasses")

    elif state.weather_condition == "Windy":
        accessories.append("Windbreaker")

        # Check whether the user wants accessories
    if not state.include_accessories:
        accessories = []
    # Create a new Outfit instance
    new_outfit = Outfit(
        top,
        bottom,
        accessories,
        state.preferred_style)

    # Add the outfit to the user's history
    state.outfit_history.append(new_outfit)
    
    return Page(state, [
        Header("Your Outfit Recommendation!"),
        Text("Location: " + state.location),
        Text("Top: " + top),
        Text("Bottom: " + bottom),
        Text("Accessories: " + str(accessories)),
        Text("Style: " + state.preferred_style),
        Button("Generate Another Outfit", generate_outfit),
        Button("View Outfit History", outfit_history),
        Button("Home", "index")])


# OUTFIT HISTORY PAGE
@route
def outfit_history(state: State) -> Page:
    content = [
        Header("Your Outfit History!"),
        Text("Here are your previously generated outfits:")]

    # Display each saved outfit
    for outfit in state.outfit_history:
        content.append(Header(outfit.style + " Outfit"))
        content.append(Text("Top: " + outfit.top))
        content.append(Text("Bottom: " + outfit.bottom))
        content.append(Text("Accessories: " + str(outfit.accessories)))

    content.append(Button("Generate Another Outfit", generate_outfit))
    content.append(Button("Clear History", clear_history))
    content.append(Button("Home", index))

    return Page(state, content)


# CLEAR OUTFIT HISTORY
@route
def clear_history(state: State) -> Page:
    state.outfit_history = []

    return Page(state, [
        Header("Outfit History Cleared!"),
        Text("Your saved outfits have been removed."),
        Button("Generate an Outfit", generate_outfit),
        Button("Home", index)])


start_server(State(
    location="",
    temperature=70.0,
    weather_condition="Sunny",
    preferred_style="Casual",
    include_accessories=True,
    outfit_history=[]))
