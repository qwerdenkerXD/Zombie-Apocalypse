from sys import argv as args
from matplotlib import pyplot as plt
import random

# https://www.deutschland123.de/z%C3%BClpich -> 20597k citizens
CITIZENS = 20597
HMN_CITIZENS = int(.9 * CITIZENS)
HERO_CITIZENS = CITIZENS - HMN_CITIZENS

SPECIES = {
    "HUMANS": 0,  # common humans without any skills

    "HEROES": 0,  # special humans, zombie killer

    "ZOMBIES": 0,  # undead

    "DEADS": 0  # just dead matter, no living-like thing
}

SPECIES_LEGEND = {
    "HUMANS": "Menschen",
    "HEROES": "Helden",
    "ZOMBIES": "Zombies",
    "DEADS": "Tote"
}

DAY = 0


def main():
    static_tasks = [population_growth]
    human_tasks = [zombie_fights, human_kills_human]
    random.seed(1)

    # The simulation without zombies -> blank
    simulate(3650,
             static_tasks,
             (HMN_CITIZENS, HERO_CITIZENS, 0, 0),
             "normal.png")

    # The simulation without heroes, so if all citizens were normal guys in a city with some zombies.
    # This is to adjust the humans' influence on the pandemic.
    simulate(30,
             human_tasks,
             (HMN_CITIZENS + HERO_CITIZENS, 0, 0, 1),
             "zombified_no_heroes.png")

    # The simulation without humans, so if all citizens were heroes in a city with some zombies.
    # This is to adjust the heroes' influence on the pandemic.
    # simulate(30,
    #          hero_tasks,
    #          (0, HMN_CITIZENS + HERO_CITIZENS, 0, 5000),
    #          "zombified_all_heroes.png")


def simulate(iterations: int, tasks: list, species_conf: tuple, plot_file: str):
    global DAY
    SPECIES["HUMANS"] = species_conf[0]
    SPECIES["HEROES"] = species_conf[1]
    SPECIES["DEADS"] = species_conf[2]
    SPECIES["ZOMBIES"] = species_conf[3]

    change = {"HUMANS": [], "HEROES": [], "ZOMBIES": [], "DEADS": []}
    for day in range(iterations):
        population_growth()
        DAY = day
        random.shuffle(tasks)
        for task in tasks:
            task()

        for i in change:
            change[i].append(SPECIES[i])

    plot(change, plot_file)


# ######################## static tasks ######################## #
def population_growth():
    """
        The daily growth of the population, independent to zombies

        let's take city Zuelpich with around 20k citizens
    """
    yearly_births = 191
    yearly_deaths = 287
    yearly_in = 1245
    yearly_out = 991
    growth = (yearly_in - yearly_out) / 365
    dying_species("HUMANS",  (yearly_deaths / CITIZENS) * SPECIES["HUMANS"] / 365)
    dying_species("HEROES",  (yearly_deaths / CITIZENS) * SPECIES["HEROES"] / 365)
    increase_species("HUMANS", growth / 2 * bool(SPECIES["HUMANS"]))
    increase_species("HEROES", growth / 2 * bool(SPECIES["HEROES"]))
    increase_species("HUMANS",  (yearly_births / CITIZENS) * SPECIES["HUMANS"] / 365)
    increase_species("HEROES",  (yearly_births / CITIZENS) * SPECIES["HEROES"] / 365)


# ######################## human tasks ######################## #
def zombie_fights():
    """
        The daily fights between the living ones and the zombies
    """
    population = int(SPECIES["HUMANS"] + SPECIES["HEROES"])
    possible_matches = population if population < SPECIES["ZOMBIES"] else int(SPECIES["ZOMBIES"])
    fights = random.choices(range(population), k=possible_matches)
    human_fights = len(list(filter(lambda x: x < SPECIES["HUMANS"], fights)))
    hero_fights = len(fights) - human_fights
    human_fights_zombie(human_fights)
    hero_fights_zombie(hero_fights)


def human_fights_zombie(fights: int):
    """
        The change of zombies killed by humans.
        One human has the skill to kill one of ten zombies.

        A tenth of the humans who failed the fight  is gonna be eaten completely, the other turn to a zombie.
    """
    current_population = SPECIES["HUMANS"] + SPECIES["HEROES"]
    results = random.choices(range(10), k=fights)
    success = len(list(filter(lambda x: x == 1, results)))
    dying_species("ZOMBIES", success)

    fail = fights - success
    dying_species("HUMANS", fail * .1)

    # transforming to zombie
    reduce_species("HUMANS", fail * .9)
    increase_species("ZOMBIES", fail * .9)


def zombie_transforms_human(fights: int):
    """
        The change of humans turned into zombies.
        This gets higher the more zombies exist.
        A zombie selects one human a day as meal.
        Ten percent of the victims are gonna be eaten completely, the other part morphs.
    """
    victims = int(SPECIES["ZOMBIES"]) if SPECIES["ZOMBIES"] < SPECIES["HUMANS"] else SPECIES["HUMANS"]
    dying_species("HUMANS", victims * .1)

    reduce_species("HUMANS", victims * .9)
    increase_species("ZOMBIES", victims * .9)


def human_kills_human():
    """
        The change of humans killed by humans.
        This gets higher everyday because of the stress that changes the humans' minds, the survival instinct, the fear of dying.
        In this small city, let's say that one human is gonna be killed by another a day, in maximum. This includes suicide as well.
    """
    global DAY
    stress = sigmoid(DAY, 100)  # after 100 days 1 human dies a day
    dying_species("HUMANS", stress)


def hero_fights_zombie(fights: int):
    pass


def sigmoid(x: float, where_to_be_one: float) -> float:
    """
        The sigmoid function, converges to 1.
        The normal function with e^-x, so factor 1 for x is close to 1 at x=6 -> factor=6/(x where it should be close 1)
    """
    from math import exp
    if where_to_be_one == 0:
        return 1
    return 1 / (1 + exp(-(6 / (where_to_be_one / 2)) * (x - (where_to_be_one / 2))))


def reduce_species(species: str, change: float):
    SPECIES[species] -= change if change < SPECIES[species] else SPECIES[species]


def increase_species(species: str, change: float):
    reduce_species(species, -change)


def dying_species(species: str, change: float):
    before = SPECIES[species]
    reduce_species(species, change)
    after = SPECIES[species]
    increase_species("DEADS", before - after)


def plot(species: dict, file: str, x_axis="Tag", y_axis="Anzahl Individuen"):
    plt.clf()
    for i in species:
        plt.plot(species[i], label=SPECIES_LEGEND[i])
    plt.legend(loc="upper left")
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.savefig(file)
    plt.clf()


if __name__ == '__main__':
    main()
