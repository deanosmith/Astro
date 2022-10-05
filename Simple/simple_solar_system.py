# Python 3.10.1

from SolarSystem import SolarSystem, Sun, Planet

solar_system = SolarSystem(width=1600, height=900)

sun = Sun(solar_system, mass=10000)
planets = (
    Planet(
        solar_system,
        mass=3,
        position=(-400, 0),
        velocity=(0, 5),
    ),
    Planet(
        solar_system,
        mass=3,
        position=(-350, 0),
        velocity=(0, 5),
    ),
    Planet(
        solar_system,
        mass=3,
        position=(-300, 0),
        velocity=(0, 5),
    ),
    Planet(
        solar_system,
        mass=3,
        position=(-250, 0),
        velocity=(0, 5),
    ),
)

while True:
    solar_system.calculate_all_body_interactions()
    solar_system.update_all()

