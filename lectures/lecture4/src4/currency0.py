import requests

def main():
    #res = requests.get("https://api.fixer.io/latest?base=USD&symbols=EUR")
    res = requests.get("https://data.fixer.io/api/latest?access_key=apikey&base=EUR&symbols=USD")
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")
    data = res.json()
    print(data)

if __name__ == "__main__":
    main()
