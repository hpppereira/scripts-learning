# -*- coding: utf-8 -*-
"""
Created on Sun Feb 24 08:00:22 2019

@author: tobia
"""

def arredondar(num):
    return float( '%.0f' % ( num ) )

def arredondar1(num):
    return float( '%.1f' % ( num ) )


def bancodedados():

    local="pnboia-uol.mysql.uhserver.com"
    usr="pnboia"
    password="Ch@tasenha1"
    data_base="pnboia_uol"

    return local,usr,password,data_base