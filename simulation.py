from sys import argv as args
from matplotlib import pyplot as plt
import random

HMN_CITIZENS = 9000
HERO_CITIZENS = 1000

SPECIES = {
    "HUMANS": 0,  # common humans without any skills

    "HEROES": 0,  # special humans, zombie killer

    "DEADS": 0,  # just dead matter, no living-like thing

    "ZOMBIES": 0  # undead
}


def main():
    random.seed(1)
    duration = 3650
    simulate_normal(duration)
    simulate_with_zombies_no_heroes(duration)


def simulate_normal(iterations: int):
    """
        The simulation without zombies -> blank
    """
    SPECIES["HUMANS"] = HMN_CITIZENS
    SPECIES["HEROES"] = HERO_CITIZENS
    SPECIES["DEADS"] = 0
    SPECIES["ZOMBIES"] = 0

    change = {"HUMANS": [], "HEROES": [], "DEADS": [], "ZOMBIES": []}
    for day in range(iterations):
        population_growth()
        for i in change:
            change[i].append(SPECIES[i])
    plot(change, "normal.png")


def population_growth():
    """
        The daily growth of the population, independent to zombies

        let's take city Bramsche with 10k citizens
        https://www.deutschland123.de/bramsche-geburten -> 260 / a
        https://www.deutschland123.de/bramsche-todesfaelle -> 301 / a -> 3.01% / a
        https://www.deutschland123.de/bramsche-umz%C3%BCge-zu-und-fortz%C3%BCge -> (1779 - 1815) / a
    """
    growth = (260 + 1779 - 1815) / 365
    SPECIES["DEADS"] += .0301 * (SPECIES["HUMANS"] + SPECIES["HEROES"]) / 365
    SPECIES["HUMANS"] += growth / 2 * bool(SPECIES["HUMANS"])
    SPECIES["HEROES"] += growth / 2 * bool(SPECIES["HEROES"])


def simulate_with_zombies_no_heroes(iterations: int):
    """
        The simulation without heroes, so if all citizens were normal guys in a city with some zombies.
    """
    SPECIES["HUMANS"] = HMN_CITIZENS + HERO_CITIZENS
    SPECIES["HEROES"] = 0
    SPECIES["DEADS"] = 0
    SPECIES["ZOMBIES"] = 10

    change = {"HUMANS": [], "HEROES": [], "DEADS": [], "ZOMBIES": []}
    tasks = [human_kills_zombie, zombie_transforms_human, human_kills_human]
    for i in range(iterations):
        population_growth()
        for day in range(iterations):
            random.shuffle(tasks)
            for task in tasks:
                task()

        for i in change:
            change[i].append(SPECIES[i])
    plot(change, "zombified_no_heroes.png")


def human_kills_zombie():
    """
        The change of zombies killed by humans.
        This gets higher the more zombies exist.
    """
    pass


def zombie_transforms_human():
    """
        The change of humans turned into zombies.
        This gets higher the more zombies exist.
    """
    pass


def human_kills_human():
    """
        The change of humans killed by humans.
        This gets higher everyday because of the stress that changes the humans' minds.
    """
    pass


def plot(species: dict, file: str):
    plt.clf()
    for i in species:
        plt.plot(species[i], label=i)
    plt.legend(loc="upper left")
    plt.savefig(file)
    plt.clf()


if __name__ == '__main__':
    main()
