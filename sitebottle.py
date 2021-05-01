'''
Programa para criar site em html
utilizando o python - bottle

'''

from bottle import route, template
import bottle


@route('/lioc')
def hello():
	return "Hello World! Izabel"

bottle.run(host='localhost',port=8080,debug=True)