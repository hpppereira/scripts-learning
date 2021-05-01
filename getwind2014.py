#! /usr/bin/env python
#
# python script to download selected files from rda.ucar.edu
# after you save the file, don't forget to make it executable
#   i.e. - "chmod 755 <name_of_script>"
#
import sys
import os
import urllib2
import cookielib
#
if (len(sys.argv) != 2):
  print "usage: "+sys.argv[0]+" [-q] password_on_RDA_webserver"
  print "-q suppresses the progress message for each file that is downloaded"
  sys.exit(1)
#
passwd_idx=1
verbose=True
if (len(sys.argv) == 3 and sys.argv[1] == "-q"):
  passwd_idx=2
  verbose=False
#
cj=cookielib.MozillaCookieJar()
opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
#
# check for existing cookies file and authenticate if necessary
do_authentication=False
if (os.path.isfile("auth.rda.ucar.edu")):
  cj.load("auth.rda.ucar.edu",False,True)
  for cookie in cj:
    if (cookie.name == "sess" and cookie.is_expired()):
      do_authentication=True
else:
  do_authentication=True
if (do_authentication):
  login=opener.open("https://rda.ucar.edu/cgi-bin/login","email=izabel.oceanografia@gmail.com&password="+sys.argv[1]+"&action=login")
#
# save the authentication cookies for future downloads
# NOTE! - cookies are saved for future sessions because overly-frequent authentication to our server can cause your data access to be blocked
  cj.clear_session_cookies()
  cj.save("auth.rda.ucar.edu",True,True)
#
# download the data file(s)
listoffiles=["2014/wnd10m.cdas1.201401.grb2","2014/wnd10m.cdas1.201402.grb2","2014/wnd10m.cdas1.201403.grb2","2014/wnd10m.cdas1.201404.grb2","2014/wnd10m.cdas1.201405.grb2","2014/wnd10m.cdas1.201406.grb2","2014/wnd10m.cdas1.201407.grb2","2014/wnd10m.cdas1.201408.grb2","2014/wnd10m.cdas1.201409.grb2","2014/wnd10m.cdas1.201410.grb2","2014/wnd10m.cdas1.201411.grb2","2014/wnd10m.cdas1.201412.grb2"]
for file in listoffiles:
  idx=file.rfind("/")
  if (idx > 0):
    ofile=file[idx+1:]
  else:
    ofile=file
  if (verbose):
    sys.stdout.write("downloading "+ofile+"...")
    sys.stdout.flush()
  infile=opener.open("http://rda.ucar.edu/data/ds094.1/"+file)
  outfile=open(ofile,"wb")
  outfile.write(infile.read())
  outfile.close()
  if (verbose):
    sys.stdout.write("done.\n")
