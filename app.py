from clint.textui import colored, puts
import requests
import sys
import json

COIN_DICTIONARY = {
    "BTC": 1,
    "LTC": 2
}

args = sys.argv
saveCoin = False
removeCoin = False
coin = ""

url = "https://api.coinmarketcap.com/v2/ticker/"

if len(args) == 2:
    if args[1] == '--help' or args[1] == '-h':
        print("Help!")
#         TODO: Help Message

if len(args) > 3:
    print("Too many arguments! Try --help to learn more.")
    exit(0)

if len(args) >= 2:
    coin = args[1]
    coin = str.upper(coin)
    if coin not in COIN_DICTIONARY:
        print(coin + " is not supported. Please try another coin or use --coins for available coins.")
        exit(0)
    if len(args) == 3:
        arg = args[2]
        if arg == "--save" or arg == "-s":
            saveCoin = True
        #     TODO: Save Coin
        elif arg == "--remove" or arg == "-r":
            removeCoin = True
    #         TODO: Remove Coin
        elif arg == "--coins":
            print("Coins!")
    #         TODO: Print coins
        elif arg == "--saved":
            print("Saved!")
    #         TODO: Saved coins

    price = requests.get(url + str(COIN_DICTIONARY[coin]))
    if not price.ok:
        print("Error in API check, please try again later.")
        exit(1)

    response = price.json()

    coinText = colored.yellow("Coin:\t" + coin)
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

    puts(coinText+
        price +
        v24 +
        marketCap +
        perChange1h +
        perChange24h +
        perChange7d)

    json.dumps(COIN_DICTIONARY)