import requests
import urllib3
from bs4 import BeautifulSoup
import subprocess
from colorama import init, Fore
init()
urllib3.disable_warnings()
url = 'https://servers.opennic.org/'
dictionary = {}
headers = {

            "User-Agent": "Mozilla/5.0 (Linux; Linux i655 x86_64) AppleWebKit/601.35 (KHTML, like Gecko) Chrome/55.0.3744.375 Safari/534"}


def get_dns_list(url):
    req = requests.get(url, headers=headers, verify=False)
    bs = BeautifulSoup(req.content, 'lxml')
    ipv4_addresses = []
    addresses = bs.findAll('span', {"class": "mono ipv4"})
    for items in addresses:
        ipv4_addresses.append(items.text)

    for u in ipv4_addresses:
        if u is None or u == '':
            ipv4_addresses.remove(u)
    return ipv4_addresses


res = get_dns_list(url=url)


def refract_result(data):
    try:
        return data[data.find('Average ='):].replace('Average = ', '').replace('ms', '')
    except Exception as e:
        return e


def get_response(addresses, number_of_servs):
    print('Processing, please wait...\nIt may takes 2-4 minutes\n')
    for server in addresses:
        command = 'ping ' + server
        prcs = subprocess.getoutput(command)
        try:
            dictionary.update({f"{server}": int(refract_result(data=prcs))})
        except ValueError:
            continue
    for ity in dictionary:
        if ity == ',' or ity is None or ity == '' or ity == ' ':
            dictionary.pop(ity)
        else:
            pass

    sorted_dict = sorted(dictionary.items(), key=lambda k: k[1])

    return sorted_dict[0:int(number_of_servs)]


print(Fore.CYAN, '''
  _____  _   _  _____         _                       
 |  __ \| \ | |/ ____|       (_)                      
 | |  | |  \| | (___    _ __  _ _ __   __ _  ___ _ __ 
 | |  | | . ` |\___ \  | '_ \| | '_ \ / _` |/ _ \ '__|
 | |__| | |\  |____) | | |_) | | | | | (_| |  __/ |   
 |_____/|_| \_|_____/  | .__/|_|_| |_|\__, |\___|_|   
                       | |             __/ |          
                       |_|            |___/           
\n\n''')
try:
    ans = int(input("Input desired number of DNS servers(max 40): "))
except ValueError:
    print("You've entered an invalid number")
if ans < 40 or ans == 40:
    dic = get_response(addresses=res, number_of_servs=ans)
    for thing in dic:
        if ans == 1:
            print(f"The fastest server: {thing[0]}, {thing[1]} ms")

        print(str(thing[0]) + ", ping: " + str(thing[1]) + "ms" + "\n")
else:
    print(Fore.RED, 'Incorrect number of servers')

input()