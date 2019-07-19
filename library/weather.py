from weather import Weather, Unit
def weather():
    weather = Weather(unit=Unit.CELSIUS)
    #location=input("Where do you want to know the weather from?")

    lookup = weather.lookup_by_location('stockholm')
    condition = lookup.condition

    print(condition.text)