
class ApexIsStatic():
    def __init__(self, isStatic):
        self._isStatic = isStatic

    def __repr__(self):
        return 'ApexIsStatic: ' + self._isStatic

    def getContents(self):
        if not self._isStatic:
            return ''
        else:
            return 'static'

class ApexName():
    def __init__(self, name):
        self._name = name

    def __repr__(self):
        return 'ApexName: ' + self._name

    def getContents(self):
        return self._name

class ApexType():
    def __init__(self, type):
        self._type = type

    def __repr__(self):
        return 'ApexType: ' + self._type

    def getContents(self):
        return self._type

class ApexLine():
    def __init__(self, contents):
        self._contents = contents

    def __repr__(self):
        return 'ApexLine: ' + self._contents

    def getContents(self):
        return self._contents + '\n'

class ApexAccessModifier():
    def __init__(self, type):
        self._type = type

    def __repr__(self):
        return 'ApexAccessModifier: ' + self._type

    def getContents(self):
        return self._type

class ApexMethodContents():
    
    def __init__(self, lines):
        self._lines = lines

    def __repr__(self):
        return 'ApexMethodContents: {0} lines'.format(len(self._lines))

    def addLineToStart(self, line):
        self._lines = [line] + self._lines

    def addLineToEnd(self, line):
        self._lines.append(line)

    def getContents(self):
        ret = ''
        for line in self._lines:
            ret += line.getContents()
        return ret

class ApexParameter():

    def __init__(self):
        self.type = ApexType('foo')
        self.name = 'bar'

    def getContents(self):
        return '{0} {1}'.format(self.type.getContents(), self.name.getContents())

class ApexMethod():

    def __init__(self):
        self.accessModifier = ApexAccessModifier('')
        self.isStatic = ApexIsStatic(False)
        self.returnType = ApexType('void')
        self.name = ApexName('foo')
        self._parameters = []
        self.contents = ApexMethodContents([])

    def __repr__(self):
        self._parameters = []
        return 'ApexMethod: {0}'.format(self.getSignature())

    def addParameter(self, param):
        self._parameters.append(param)

    def getParameterContents(self):
        ret = ''
        for param in self._parameters:
            ret += '{0},'.format(param.getContents())
        ret = ret.rstrip(',')
        return ret

    def addLineToStart(self, line):
        self.contents.addLineToStart(line)

    def addLineToEnd(self, line):
        self.contents.addLineToEnd(line)

    def getSignature(self):
        return '{0} {1} {2} {3} ({4})'.format(
            self.accessModifier.getContents(), 
            self.isStatic.getContents(),
            self.returnType.getContents(),
            self.name.getContents(),
            self.getParameterContents(),
            self.contents.getContents()
        )

    def getContents(self):
        return '{0} {{\n {1} \n}}'.format(
            self.getSignature(),
            self.contents.getContents()
        )

class ApexClassContents():

    def __init__(self):
        self._lines = []
        self._methods = []

    def __repr__(self):
        return 'ApexClassContents: {0} lines, {1} methods'.format(len(self._lines), len(self._methods))

    def addLine(self, apexLine):
        self._lines.append(apexLine)

    def addMethod(self, apexMethod):
        self._methods.append(apexMethod)

    def getLineContents(self):
        ret = ''
        for line in self._lines:
            ret += line.getContents()
        return ret

    def getMethods(self):
        return self._methods

    def getMethodContents(self):
        ret = ''
        for method in self._methods:
            ret += method.getContents() + '\n'
        return ret

    def getContents(self):
        return '{0}\n{1}'.format(
            self.getLineContents(),
            self.getMethodContents()
        )

class ApexClass():
    def __repr__(self):
        self.accessModifier = ApexAccessModifier('')
        self.name = ApexName('foo')
        self.contents = ApexClassContents()
        return 'ApexClass: {0}'.format(name)

    def addLine(self, apexLine):
        self._lines.append(apexLine)

    def getMethods(self):
        return self.contents.getMethods()

    def getContents(self):
        return '{0} class {1} {{\n {2} \n}}'.format(
            self.accessModifier.getContents(),
            self.name.getContents(),
            self.contents.getContents()
        )
        self._methods.append(apexMethod)