class MyDict:
    def __init__(self, sdict={}):
        self.mydict = sdict

    def __getitem__(self, item):
        print 'Get %s' % item
        return self.mydict[item]

    def __setitem__(self, item, value):
        print 'Set %s' % item
        self.mydict[item] = value


d = MyDict()

d['a'] = 1
d['b'] = 2
print d['a']
