from clint.textui import colored, puts
import requests
import sys
import pickle

COIN_DICTIONARY = {
    "BTC": 1,
    "LTC": 2
}

savedCoins = []

args = sys.argv
saveCoin = False
removeCoin = False
coin = ""

url = "https://api.coinmarketcap.com/v2/ticker/"


def check_coin(search_coin):
    price = requests.get(url + str(COIN_DICTIONARY[search_coin]))
    if not price.ok:
        print("Error in API check, please try again later.")
        exit(1)

    response = price.json()

    coinText = colored.yellow("Coin:\t" + search_coin)
    price = colored.yellow("\nPrice:\t$" + str(response['data']['quotes']['USD']['price']))
    v24 = colored.yellow("\n24h Volume:\t$" + str(response['data']['quotes']['USD']['volume_24h']))
    marketCap = colored.yellow("\nMarket Cap:\t$" + str(response['data']['quotes']['USD']['market_cap']))
    perChange1h = str(response['data']['quotes']['USD']['percent_change_1h'])
    perChange24h = str(response['data']['quotes']['USD']['percent_change_24h'])
    perChange7d = str(response['data']['quotes']['USD']['percent_change_7d'])

    if float(perChange1h) < 0:
        perChange1h = colored.red("\nPercent Change - 1h:\t" + perChange1h + "%")
    elif float(perChange1h) > 0:
        perChange1h = colored.green("\nPercent Change - 1h:\t" + perChange1h + "%")
    else:
        perChange1h = "\nPercent Change - 1h:\t" + perChange1h + "%"

    if float(perChange24h) < 0:
        perChange24h = colored.red("\nPercent Change - 24h:\t" + perChange24h + "%")
    elif float(perChange24h) > 0:
        perChange24h = colored.green("\nPercent Change - 24h:\t" + perChange24h + "%")
    else:
        perChange24h = "\nPercent Change - 24h:\t" + perChange24h + "%"

    if float(perChange7d) < 0:
        perChange7d = colored.red("\nPercent Change - 74:\t" + perChange7d + "%")
    elif float(perChange7d) > 0:
        perChange7d = colored.green("\nPercent Change - 74:\t" + perChange7d + "%")
    else:
        perChange7d = "\nPercent Change - 74:\t" + perChange7d + "%"

    puts(coinText +
         price +
         v24 +
         marketCap +
         perChange1h +
         perChange24h +
         perChange7d)


def build_coin_dict():
    cd = {}
    puts(colored.blue("Building Coin Dict..."))
    response = requests.get("https://api.coinmarketcap.com/v2/listings/")
    listings = response.json()
    for listing in listings['data']:
        cd[listing['symbol']] = listing['id']
    puts(colored.blue("Done."))
    return cd


def save():
    puts(colored.blue("Saving!"))
    pickle.dump(COIN_DICTIONARY, open("CC_Coin_Config.txt", "wb"), protocol=pickle.HIGHEST_PROTOCOL)
    pickle.dump(savedCoins, open("User_Coins.txt", "wb"), protocol=pickle.HIGHEST_PROTOCOL)


def load():
    puts(colored.blue("Loading!"))
    try:
        cd = pickle.load(open("CC_Coin_Config.txt", "rb"))
    except:
        cd = build_coin_dict()

    try:
        sc = pickle.load(open("User_Coins.txt", "rb"))
    except:
        sc = []

    return cd, sc


COIN_DICTIONARY, savedCoins = load()

if len(args) == 1:
    curr = len(savedCoins)
    for coin in savedCoins:
        curr = curr - 1
        check_coin(coin)
        if curr > 0:
            print("========================")

if len(args) == 2:
    if args[1] == '--help' or args[1] == '-h':
        helpMessage = "To find the price of a coin, type the coins abbreviation alongside the call to this app. \n" \
                      "To see which coins you saved, use the flag --saved.\n" \
                      "To see a list of available coins, use the flag --coins.\n" \
                      "To save a coin, add --save after the coin symbol.\n" \
                      "To remove a coin, use --remove after the coin symbol.\n" \
                      "To print out the prices of your saved coins, just call this app with no additional argument.\n" \
                      "To update the coin dictionary, use --update.\n"
        puts(colored.yellow(helpMessage))
        exit(0)
    elif args[1] == "--coins":
        puts(colored.yellow("The available coins are as follows:"))
        for key, value in sorted(COIN_DICTIONARY.items()):
            puts(colored.yellow(key))
        exit(0)
    elif args[1] == "--saved":
        for coin in savedCoins:
            puts(colored.yellow(coin))
        exit(0)
    elif args[1] == '--update':
        build_coin_dict()
        save()
        exit(0)

if len(args) > 3:
    print("Too many arguments! Try --help to learn more.")
    exit(0)

if len(args) >= 2:
    coin = args[1]
    coin = str.upper(coin)
    if coin not in COIN_DICTIONARY:
        puts(colored.red(coin + " is not supported. Please try another coin or use --coins for available coins."))
        exit(0)
    if len(args) == 3:
        arg = args[2]
        if arg == "--save" or arg == "-s":
            if coin not in savedCoins:
                savedCoins.append(coin)
        elif arg == "--remove" or arg == "-r":
            savedCoins.remove(coin)

    check_coin(coin)

    save()
    exit(0)
