antennae = int(input())
eyes = int(input())

def at_least_3_antennae():
    return antennae >= 3

def at_most_4_eyes():
    return eyes <= 4

def at_most_6_antennae():
    return antennae <= 6

def at_least_2_eyes():
    return eyes >= 2

def at_most_2_antennae():
    return antennae <= 2

def at_most_3_eyes():
    return eyes <= 3

if at_most_2_antennae() and at_most_3_eyes():
    print("GraemeMercurian")
if at_least_3_antennae() and at_most_4_eyes():
    print("TroyMartian")
if at_most_6_antennae() and at_least_2_eyes():
    print("VladSaturnian")
