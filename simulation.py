from sys import argv as args
from matplotlib import pyplot as plt
import random

HMN_CITIZENS = 9000
HERO_CITIZENS = 1000

SPECIES = {
    "HUMANS": HMN_CITIZENS,  # common humans without any skills

    "HEROES": HERO_CITIZENS,  # special humans, zombie killer

    "DEADS": 0,  # just dead matter, no living-like thing

    "ZOMBIES": 0  # undead
}

DAY = 0


def main():
    random.seed(1)
    duration = 3650
    simulate_normal(duration)
    simulate(duration)


def simulate(iterations: int):
    global DAY
    import random
    SPECIES["ZOMBIES"] = 10


def simulate_normal(iterations: int):
    global DAY
    import random
    change = {"HUMANS": [], "HEROES": [], "DEADS": [], "ZOMBIES": []}
    for i in range(iterations):
        population_growth()
        DAY += 1
        for i in change:
            change[i].append(SPECIES[i])
    plot(change, "normal.png")


def plot(species: dict, file: str):
    plt.clf()
    for i in species:
        plt.plot(species[i], label=i)
    plt.legend(loc="upper left")
    plt.savefig(file)
    plt.clf()


def population_growth():
    """
        let's take city Bramsche with 10k citizens
        https://www.deutschland123.de/bramsche-geburten -> 260 / a
        https://www.deutschland123.de/bramsche-todesfaelle -> -301
        https://www.deutschland123.de/bramsche-umz%C3%BCge-zu-und-fortz%C3%BCge -> 1779 - 1815
    """
    growth = (260 - 301 + 1779 - 1815) / 365
    SPECIES["HUMANS"] += growth / 2
    SPECIES["HEROES"] += growth / 2


if __name__ == '__main__':
    main()
