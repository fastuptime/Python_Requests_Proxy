import httpx
import time

proxy_file = "proxy.txt"

def get_next_proxy(proxy_file: str) -> str:
    with open(proxy_file, "r") as f:
        proxies = f.readlines()
        proxy = proxies.pop(0).strip()
        proxies.append(proxy)
    with open(proxy_file, "w") as f:
        f.writelines(proxies)
    return proxy

proxy = get_next_proxy(proxy_file)
proxy_address, proxy_port, proxy_username, proxy_password = proxy.split(":")

proxy = f"http://{proxy_username}:{proxy_password}@{proxy_address}:{proxy_port}"
proxies = {
    "http://": proxy,
    "https://": proxy
}

client = httpx.Client(proxies=proxies)

response = client.get("https://api.ipify.org/?format=json")

if response.status_code == 200:
    data = response.json()
    ip_address = data["ip"]
    print("IP Adresi:", ip_address)
else:
    print("İstek başarısız! Hata kodu:", response.status_code)

client.close()