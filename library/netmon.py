#!/usr/bin/env python3
import sqlite3
import requests
import json
from dotenv import load_dotenv
import os
from library.utils import say

load_dotenv()

PI_IP = os.getenv("PI_IP")
API_KEY = os.getenv("API_KEY")

def scannet():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    print("[*] Creating table if it doesn't exist...")
    say("Creating table if it doesn't exist.")
    c.execute('''CREATE TABLE IF NOT EXISTS network (addres,name,macaddr,maccompany)''')
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Sec-GPC': '1',
        'DNT': '1',
    }

    params = (
        ('auth', API_KEY),
        ('network', ''),
        ('_', '1624463201689'),
    )

    response = requests.get(f'http://{PI_IP}/admin/api_db.php', headers=headers,params=params)
    print("[*] Sending request...")
    say("Sending request to DNS server.")
    devices = response.text
    json_data = json.loads(devices)
    json_data = json_data['network']
    print("[*] Sending data to database...")
    say("Sending data to database.")
    for entry in json_data:
        host = None
        hostname = None
        macaddr = None
        maccompany = None
        if entry['ip']:
            host = entry['ip'][0]
        if entry['name']:
            hostname = entry['name'][0]
        if entry['hwaddr']:
            macaddr = entry['hwaddr']
        if entry['macVendor']:
            maccompany = entry['macVendor']
        c.execute("insert into network values (?,?,?,?);", (host,hostname,macaddr,maccompany))
        conn.commit()
    print("[*] Network scan has completed and has been uploaded...")
    return ""

def client():
    query = conn.execute('select distinct * from network')
    fetch_query = query.fetchall()
    print("[*] Fetching results from database...")
    for entry in fetch_query:
        host = None
        hostname = None
        macaddr = None
        maccompany = None
        if entry[0]:
            host = entry[0]
        if entry[1]:
            hostname = entry[1]
        if entry[2]:
            macaddr = entry[2]
        if entry[3]:
            maccompany = entry[3]
    conn.close()

def main():
    scannet()
    #client()


if __name__ == "__main__":
    main()
