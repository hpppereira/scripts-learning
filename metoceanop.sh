#!/bin/sh

HOST='ftp.atmosmarine.com'
USER='atmosmarine.com'
PASSWD='xPRg87@K'
PASSWD='VHVnWW91MTMwMzIwMTc='
ftp -nv $HOST << EOF
quote USER $USER
quote PASS $PASSWD
binary
lcd /home/hp/Dropbox/atmosmarine/web/metocean/fig/
cd /metocean/fig/
prompt -n
mput *.png
lcd /home/hp/Dropbox/pnboia/data/realtime/mb/
cd /lioc/santos/
prompt -n
mput PNBOIA_SAN.csv
bye
EOF
