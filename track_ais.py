
#module import
import urllib.request
from bs4 import BeautifulSoup
import re
import pandas as pd
from datetime import datetime
import locale
locale.setlocale(locale.LC_ALL, locale='en_US.utf8') #as we need to deal with names of monthes later on.
import os

def coords2lalon(coords):
    """
    """
    lat, lon = coords.split('/')
    if 'S' in lat: 
        lat = float(lat.split()[0])*-1
    if 'W' in lon: 
        lon = float(lon.split()[0])*-1
    return lat, lon

def dms2dd(degrees,direction):
    dd = float(degrees) ;
    if direction == 'S' or direction == 'W':
        dd *= -1
    return dd

def parse_dms(dms):
    parts = re.split(' ', dms)
    lat = dms2dd(parts[0], parts[1])
    return lat

if __name__ == "__main__":

    IMOS = [9318436]

    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}

    items = []
    for IMO in IMOS:
        # url = r'https://www.marinetraffic.com/en/ais/details/ships/shipid:774433/mmsi:710000077/imo:9318436/vessel:NORSUL_BELMONTE'
        url = r'https://www.vesselfinder.com/en/vessels/VOS-TRAVELLER-IMO-' + str(IMO)
        req = urllib.request.Request(url, None, hdr)
        with urllib.request.urlopen(req) as response:
            the_page = response.read()
        parsed_html = BeautifulSoup(the_page)

        vessel_name = parsed_html.find("td", text="Vessel Name").find_next_sibling("td").text
        ship_type = parsed_html.find("td", text="Ship type").find_next_sibling("td").text
        flag = parsed_html.find("td", text="Flag").find_next_sibling("td").text
        course_speed = parsed_html.find("td", text="Course / Speed").find_next_sibling("td").text
        coords = parsed_html.find("td", text="Coordinates").find_next_sibling("td").text

        for l in parsed_html.findAll("tr"): 
            if "Last report" in str(l):
                    last_report = datetime.strptime(str(l).split('>')[6].split('<')[0].strip(), '%b %d, %Y %H:%M %Z')

        lat, lon = coords2lalon(coords)
        items.append((lat, lon, vessel_name, last_report))

    filename = 'ship_positions.txt'
    if os.path.exists(filename):
        append_write = 'a' # append if already exists
        fw = open(filename,append_write)
    else:
        append_write = 'w' # make a new file if not
        fw = open(filename,append_write)
        fw.write("lat;lon;name;time\n")
    for item in items:
        fw.write("%3.5f;%3.5f;%s;%s\n" % item)
    fw.close()


    #get it on a map:
    from arcgis.gis import GIS
    gis = GIS()
    map = gis.map()
    df = pd.DataFrame.from_records(items)
    df.columns = ['y', 'x', 'name', 'zeit']
    ships = gis.content.import_data(df)
    map.add_layer(ships)
    map.center = [lat, lon]
    map