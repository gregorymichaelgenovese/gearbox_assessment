"""Helper functions"""

from os import system as cmd


def n_print(s: str):
    print("\n" + s)


def print_n(s: str):
    print(s + "\n")


def clear():
    cmd("cls")
    cmd("clear")
    print("")
