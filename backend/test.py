import requests

def main():
    r = requests.get("https://httpbin.org/get")
    print(r.status_code, r.headers.get("Content-Type"))

if __name__ == "__main__":
    main()