import itertools
import time

from marketplace import get_all_heroes, get_hero_data, parse_hero_data, send_hero_webhook


def find_difference(first_data, second_data):
    intersec = [item for item in first_data if item in second_data]
    sym_diff = [item for item in itertools.chain(first_data, second_data) if item not in intersec]
    new_heroes = []

    for hero in sym_diff:
        if hero in second_data:
            new_heroes.append(hero)

    return new_heroes


WEBHOOK_URL = "https://discord.com/api/webhooks/919647726902313051/ckb7SqpFVCfYmxI2vbuxJvwV_7HFI0Wlj3sW-irZtOq-WyyPJdey49V46yzeXXVZO0k9"
FILTER = "sort=Latest&priceMin=0&priceMax=35000000"
SIZE = 6

alpha_scan = get_all_heroes(FILTER, SIZE)

time.sleep(0.5)

beta_scan = get_all_heroes(FILTER, SIZE)

while True:
    difference = find_difference(alpha_scan, beta_scan)
    if len(difference) != 0:
        for hero in difference:
            print(hero["lastModified"], hero["price"])
            hero_data = get_hero_data(hero["refId"])
            send_hero_webhook(parse_hero_data(hero_data, True), WEBHOOK_URL)

    time.sleep(0.5)

    alpha_scan = get_all_heroes(FILTER, SIZE)

    difference = find_difference(alpha_scan, beta_scan)
    if len(difference) != 0:
        for hero in difference:
            print(hero["lastModified"], hero["price"])
            hero_data = get_hero_data(hero["refId"])
            send_hero_webhook(parse_hero_data(hero_data, True), WEBHOOK_URL)

    time.sleep(0.5)

    beta_scan = get_all_heroes(FILTER, SIZE)
