"""Kleiner Temperaturkonverter für Celsius, Fahrenheit und Kelvin."""

ABSOLUTER_NULLPUNKT_C = -273.15


def celsius_zu_fahrenheit(celsius: float) -> float:
    """Rechnet Grad Celsius in Grad Fahrenheit um."""
    _pruefe_celsius(celsius)
    return round(celsius * 9 / 5 + 32, 2)


def fahrenheit_zu_celsius(fahrenheit: float) -> float:
    """Rechnet Grad Fahrenheit in Grad Celsius um."""
    celsius = (fahrenheit - 32) * 5 / 9
    _pruefe_celsius(celsius)
    return round(celsius, 2)


def celsius_zu_kelvin(celsius: float) -> float:
    """Rechnet Grad Celsius in Kelvin um."""
    _pruefe_celsius(celsius)
    return round(celsius - ABSOLUTER_NULLPUNKT_C, 2)


def kelvin_zu_celsius(kelvin: float) -> float:
    """Rechnet Kelvin in Grad Celsius um."""
    if kelvin < 0:
        raise ValueError("Kelvin kann nicht negativ sein.")
    return round(kelvin + ABSOLUTER_NULLPUNKT_C, 2)


def _pruefe_celsius(celsius: float) -> None:
    if celsius < ABSOLUTER_NULLPUNKT_C:
        raise ValueError("Temperatur liegt unter dem absoluten Nullpunkt.")


if __name__ == "__main__":
    for wert in (-40, 0, 37, 100):
        print(f"{wert} °C = {celsius_zu_fahrenheit(wert)} °F = {celsius_zu_kelvin(wert)} K")
