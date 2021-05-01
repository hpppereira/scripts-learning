'''
Class for data quality control
Used for raw wave data and meteo-oceanographic
parameters

Developed by: Henrique P. P. Pereira
'''


class WaveProc(object):
    
    def __init__(self, var):

    	self.var = var #one value (not a time serie)
    	self.flag = None

    def range(self, linf, lsup):

    	if self.var < linf:
    		self.flag = 'a'

    	elif self.var > lsup:
    		self.flag = 'b'

    	else:
    		self.flag = '1'
            

