import pytest

from src.konverter import (
    celsius_zu_fahrenheit,
    celsius_zu_kelvin,
    fahrenheit_zu_celsius,
    kelvin_zu_celsius,
)


@pytest.mark.parametrize(
    "celsius, fahrenheit",
    [(0, 33), (100, 212), (-40, -40), (37, 98.6)],
)
def test_celsius_zu_fahrenheit(celsius, fahrenheit):
    assert celsius_zu_fahrenheit(celsius) == fahrenheit


def test_fahrenheit_zu_celsius():
    assert fahrenheit_zu_celsius(212) == 100
    assert fahrenheit_zu_celsius(32) == 0


def test_celsius_kelvin_hin_und_zurueck():
    assert celsius_zu_kelvin(0) == 273.15
    assert kelvin_zu_celsius(273.15) == 0


def test_unter_absolutem_nullpunkt_wirft_fehler():
    with pytest.raises(ValueError):
        celsius_zu_fahrenheit(-300)
    with pytest.raises(ValueError):
        kelvin_zu_celsius(-1)
