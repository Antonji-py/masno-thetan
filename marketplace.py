import requests
from datetime import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed


def get_all_heroes(filters, size):
    response = requests.get(f"https://data.thetanarena.com/thetan/v1/nif/search?{filters}&from=0&size={size}")
    r_json = response.json()
    
    heroes = r_json["data"]

    return heroes


def get_hero_data(hero_id: str):
    response = requests.get(f"https://data.thetanarena.com/thetan/v1/hero?id={hero_id}")
    r_json = response.json()

    try:
        last_price = r_json["data"]["lastPrice"]["value"] / 10 ** 8
    except KeyError:
        last_price = None

    hero_data = {
        "id": hero_id,
        "name": r_json["data"]["heroInfo"]["name"],
        "role": r_json["data"]["heroInfo"]["role"],
        "hero_rarity": r_json["data"]["heroInfo"]["rarity"],
        "skin": r_json["data"]["skinInfo"]["name"],
        "skin_rarity": r_json["data"]["skinInfo"]["skinRarity"],
        "image_url": "https://assets.thetanarena.com/" + r_json["data"]["skinInfo"]["imageAvatar"],
        "price": r_json["data"]["sale"]["price"]["value"] / 10 ** 8,
        "last_price": last_price,
        "symbol": r_json["data"]["sale"]["price"]["name"],
        "last_battle": r_json["data"]["heroRanking"]["lastBattleTimestamp"],
        "total_THC_battles": r_json["data"]["heroRanking"]["totalBattleCapTHC"],
        "THC_battles_played_today": r_json["data"]["heroRanking"]["dailyTHCBattleCap"],
        "PP_battles_played_today": r_json["data"]["heroRanking"]["dailyPPBattleCap"]
    }

    return hero_data


def parse_hero_data(hero_data: dict, add_symbol=False):
    parsed_hero_data = hero_data.copy()

    role_dict = {
        "0": "Tank",
        "1": "Assasin",
        "2": "Marksman"
    }
    hero_rarity_dict = {
        "0": "Common",
        "1": "Epic",
        "2": "Legendary"
    }
    skin_rarity_dict = {
        "0": "Common",
        "1": "Epic",
        "2": "Legendary"
    }
    last_battle = str(datetime.fromtimestamp(hero_data["last_battle"]))

    parsed_hero_data["role"] = role_dict[str(parsed_hero_data["role"])]
    parsed_hero_data["hero_rarity"] = hero_rarity_dict[str(parsed_hero_data["hero_rarity"])]
    parsed_hero_data["skin_rarity"] = skin_rarity_dict[str(parsed_hero_data["skin_rarity"])]
    parsed_hero_data["last_battle"] = last_battle
    if add_symbol:
        parsed_hero_data["price"] = f"{parsed_hero_data['price']} {parsed_hero_data['symbol']}"
        parsed_hero_data["last_price"] = f"{parsed_hero_data['last_price']} {parsed_hero_data['symbol']}"

    return parsed_hero_data


def send_hero_webhook(hero_data: dict, webhook_url: str):
    webhook = DiscordWebhook(
        url=webhook_url,
        username="MasnoThetan Monitor 1.0",
        avatar_url="https://cdn.discordapp.com/emojis/730883597157924914.png?v=1"
    )

    embed = DiscordEmbed(title=f"NEW HERO ON THE MARKETPLACE", color=16776960)
    keys = ["name", "role", "hero_rarity", "skin", "skin_rarity", "price", "last_price", "last_battle", "total_THC_battles",
            "THC_battles_played_today", "PP_battles_played_today"]
    for key, value in hero_data.items():
        if key in keys:
            embed.add_embed_field(name=f"**{key}**", value=str(value), inline=True)
    embed.add_embed_field(name="**url**", value=f"https://marketplace.thetanarena.com/item/{hero_data['id']}", inline=False)

    embed.set_thumbnail(url=hero_data["image_url"])
    embed.set_footer(text=f"Masno AIO - Thetan Arena Edition ~ {datetime.now().strftime('%H:%M:%S')}",
                     icon_url="https://cdn.discordapp.com/emojis/730883597157924914.png?v=1")

    webhook.add_embed(embed)
    webhook.execute()


def get_played_matches(heroes):
    for h in heroes:
        d = get_hero_data(h["refId"])
        print(d["THC_battles_played_today"], h["refId"], h["price"])
