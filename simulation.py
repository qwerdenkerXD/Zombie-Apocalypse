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

    "DEADS": 0,  # just dead matter, no living-like thing

    "ZOMBIES": 0  # undead
}

DAY = 0


def main():
    static_tasks = [population_growth]
    human_tasks = [human_kills_zombie, zombie_transforms_human, human_kills_human]
    hero_tasks = [hero_kills_zombie, zombie_transforms_hero, hero_kills_hero]
    random.seed(1)
    duration = 3650
    duration = 30

    # The simulation without zombies -> blank
    simulate(duration,
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
    simulate(300,
             hero_tasks,
             (0, HMN_CITIZENS + HERO_CITIZENS, 0, 1),
             "zombified_all_heroes.png")


def simulate(iterations: int, tasks: list, species_conf: tuple, plot_file: str):
    global DAY
    SPECIES["HUMANS"] = species_conf[0]
    SPECIES["HEROES"] = species_conf[1]
    SPECIES["DEADS"] = species_conf[2]
    SPECIES["ZOMBIES"] = species_conf[3]

    change = {"HUMANS": [], "HEROES": [], "DEADS": [], "ZOMBIES": []}
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
def human_kills_zombie():
    """
        The change of zombies killed by humans.
        One human has the skill to kill one of ten zombies if he has no choice.
        So if there were ten zombies and two humans, they would kill one only still because one of them can flee.
        If there were 20 zombies and two humans, they would kill two of them.
        And if there are less then ten, no zombie is gonna be killed.
        In short, the zombies reduce by a tenth if they are less than the tenfold of the humans, else by the number of humans.

        In the beginning humans hesitate with killing because of moral issues, but the growing crowd of zombies changes their mind.
    """
    current_population = SPECIES["HUMANS"] + SPECIES["HEROES"]
    hesitation_factor = sigmoid(SPECIES["ZOMBIES"], current_population / 10)
    if int(SPECIES["ZOMBIES"]) < 10 * int(current_population):
        killed_zombies = hesitation_factor * (SPECIES["ZOMBIES"] // 10)
    else:
        killed_zombies = hesitation_factor * (SPECIES["HUMANS"])
    dying_species("ZOMBIES", killed_zombies)


def zombie_transforms_human():
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
        In this small city, let's say that on human is gonna be killed by another a day, in maximum.
    """
    global DAY
    stress = sigmoid(DAY, 100)  # after 100 days 1 human dies a day
    dying_species("HUMANS", stress) 


# ######################## hero tasks ######################## #
def hero_kills_zombie():
    pass


def zombie_transforms_hero():
    pass


def hero_kills_hero():
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
    reduce_species(species, change)
    increase_species("DEADS", change)


def plot(species: dict, file: str):
    plt.clf()
    for i in species:
        plt.plot(species[i], label=i)
    plt.legend(loc="upper left")
    plt.savefig(file)
    plt.clf()


if __name__ == '__main__':
    main()
