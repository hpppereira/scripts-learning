#!/usr/bin/env python
"""
Retrieves a list of granules matching simple time and space criteria.
The list of granules from a given collection (dataset) can be retrieved through a NAIAD REST web service. This scripts encapuslate the call to this web service (which could be performed through any other client or even a web navigator (entering for instance sth like : http://www.ifremer.fr/naiad/naiad/services-2.3.0/index.php?method=GetListOfGranules&AUTHENTICATION=guest&TIME=2008-04-12T00:00:00/2008-04-13T00:00:00&COLLECTION=EUR-L2P-AVHRR_METOP_A)

To see the various options, use : getgranulelist --help
"""

__author__      = "Jean-Francois Piolle"
__copyright__   = "Copyright 2010, Ifremer"
__version__ = "0.1.0"
__maintainer__ = "Jean-Francois Piolle"
__email__ = "jfpiolle@ifremer.fr"


import sys
import urllib
import datetime
from optparse import OptionParser
import xml.etree.ElementTree

WEBSERVICES_URL_ROOT = "http://www.ifremer.fr/naiad/naiad/services-2.3.0/"

DATASETS = ["EUR-L2P-AVHRR_METOP_A","UPA-L2P-ATS_NR_2P","JPL-L2P-MODIS_A","NAVO-L2P-AVHRR19_G","NAVO-L2P-AVHRR19_L","QSCATL2B", "OSI_SAF-ASCAT-METOP_A","GW_L2P_SAR_ENVI_GDR","GW_L2P_ALT_JAS1_GDR", "GW_L2P_ALT_JAS2_GDR","GW_L2P_ALT_ERS1_GDR","GW_L2P_ALT_ERS2_GDR","GW_L2P_ALT_ENVI_GDR","GW_L2P_ALT_TOPX_GDR","GW_L2P_ALT_GFO_GDR","GW_L2P_ALT_GEOS_GDR",]




parser = OptionParser()
parser.add_option("-p", "--product", dest="dataset", action="store", metavar="identifier",
                  help="collection (dataset) to search for granules")
parser.add_option("-d", "--date", dest="date", action="store", metavar="date,date",
                  help="start and end dates for which to the search the dataset granules, expressed as <start,stop> with each date as <YYYY-MM-DDThh:mm:ss>")
parser.add_option("-b", "--bbox", dest="bbox", action="store", metavar=" minLat,maxLat,minLon,maxLon",
                  help="geographical selection frame, expressed as <minLat,maxLat,minLon,maxLon> with longitudes (between -180 and 180) and latitudes (between -90 and 90) in degrees (ex: --bbox=-80/80/-180/180)")
parser.add_option("-l", "--list", dest="list", action="store_false",
                  help="list some of the available products")
parser.add_option("-u", "--url", dest="url", action="store_false",
                  help="list also the available URLs for each product")


# Build query to Web Service
# --------------------------
(options, args) = parser.parse_args()

if options.list !=None:
    print "Available products"
    print "------------------"
    for k in DATASETS:
        print k
    sys.exit(0)
    
if options.dataset == None or not options.dataset in DATASETS:
    print "No valid dataset was specified. Use <getgranulelist --help> for more information or <getgranulelist -p ?> to see a list of some available products."
    sys.exit(-1)

if options.date == None:
    print "No valid date was specified"
    sys.exit(-1)
else:
    start_date = datetime.datetime.strptime( options.date.split(',')[0], "%Y-%m-%dT%H:%M:%S" )
    stop_date = datetime.datetime.strptime( options.date.split(',')[1], "%Y-%m-%dT%H:%M:%S" )

    

url = WEBSERVICES_URL_ROOT + "index.php?method=GetListOfGranules&AUTHENTICATION=guest&TIME=%s/%s&COLLECTION=%s" % \
      (start_date.strftime("%Y-%m-%dT%H:%M:%S"), stop_date.strftime("%Y-%m-%dT%H:%M:%S"), options.dataset)

if options.bbox != None:
    latMin,latMax,lonMin,lonMax = options.bbox.split(',')
    url += "&BBOX=%s,%s,%s,%s" % (lonMin,latMin,lonMax,latMax)

if options.url != None:
    url = url + "&URL=true&PUBLIC=true"

print "QUERYING.....", url

# Perform the query
# -----------------
result = urllib.urlopen(url).readlines()[0]
print result


# Parse result
# ------------
tree = xml.etree.ElementTree.fromstring( result )
for g in tree.getiterator("Granule"):
    print g.attrib['name']
    if options.url != None:
        for u in g.getiterator("Url"):
            if u.attrib.has_key('extensions') and u.attrib["extensions"] != "":
                print "%s.%s" % (u.attrib["url"], u.attrib["extensions"])
            else:
                print u.attrib["url"]