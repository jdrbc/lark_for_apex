import sys

from lark import Lark, Transformer, v_args

"""
python apex_parser.py apex.lark test_apex_files/fflib_QueryFactory.cls

apex grammer: https://github.com/forcedotcom/apex-tmLanguage/blob/master/grammars/apex.tmLanguage
"""

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

class TreeToApex(Transformer):
    unsupported_rules = ['comment', 'inline_comment', 'multiline_comment']
    def throwErrorIfSupportedItem(self, item):
        if item.data not in self.unsupported_rules:
            raise ValueError('unexpected token: {0}'.format(str(item)))
    def class_def(self, items):
        apexClass = ApexClass()
        for item in items:
            if isinstance(item, ApexAccessModifier):
                apexClass.accessModifier = item
            elif isinstance(item, ApexName):
                apexClass.name = item
            elif isinstance(item, ApexClassContents):
                apexClass.contents = item
            else:
                raise ValueError('unexpected type for class contents: {0}'.format(str(item)))
        return apexClass
    def access_modifier(self, items):
        return ApexAccessModifier(str(items[0]))
    def class_contents(self, items):
        classContents = ApexClassContents()
        for item in items:
            if isinstance(item, ApexLine):
                classContents.addLine(item)
            elif isinstance(item, ApexMethod):
                classContents.addMethod(item)
            else:
                self.throwErrorIfSupportedItem(item)
        return classContents
    def method_contents(self, lines):
        return ApexMethodContents(lines)
    def method_def(self, items):
        methodDef = ApexMethod()
        for item in items:
            if isinstance(item, ApexAccessModifier):
                methodDef.accessModifier = item
            elif isinstance(item, ApexIsStatic):
                methodDef.isStatic = item
            elif isinstance(item, ApexType):
                methodDef.returnType = item
            elif isinstance(item, ApexName):
                methodDef.name = item
            elif isinstance(item, ApexParameter):
                methodDef.addParameter(item)
            elif isinstance(item, ApexMethodContents):
                methodDef.contents = item
            else:
                self.throwErrorIfSupportedItem(item)
        return methodDef
    def static(self, items):
        return ApexIsStatic(True)
    def type(self, items):
        return ApexType(str(items[0]))
    def name(self, items):
        return ApexName(str(items[0]))
    def parameter(self, items):
        param = ApexParameter()
        for item in items:
            if isinstance(item, ApexType):
                param.type = item
            elif isinstance(item, ApexName):
                param.name = item
            else:
                raise ValueError('unexpected type{0}')
        return param
    def line(self, items):
        return ApexLine(str(items[0]))

def parse(grammer, target):
    apex_parser = Lark(grammer, parser='earley', lexer='standard')
    return apex_parser.parse(target)

def debug(grammer, target):
    return parse(grammer, target).pretty()

def transform(grammer, target):
    return TreeToApex().transform(parse(grammer, target))

def inject_profiling(apexClass):
    className = apexClass.name.getContents()
    for method in apexClass.getMethods():
        name = method.name.getContents()
        method.addLineToStart(ApexLine("Profiler.start('" + className + "', '" + name + "');"))
        method.addLineToEnd(ApexLine("Profiler.exit('" + className + "', '" + name + "');"))
        
        # TODO 
        # method.addLineBeforeThrows(ApexLine("Profiler.exit('" + className + "', '" + name + "');"))
        # if (method.isVoid()):
            # method.addLineToEnd(ApexLine("Profiler.exit('" + className + "', '" + name + "');"))
        # TODO
        #else:
            # TODO 
            # inject so that return someExpensiveMethod() turns into
            # obj = someExpensiveMethod(); return obj
            # method.injectGenericObjectBeforeReturns();
            # inject before all returns 
            # method.addLineBeforeReturns(ApexLine("Profiler.exit('" + className + "', '" + name + "');"))

if __name__ == '__main__':
    grammer_file_name = sys.argv[1]
    file_to_parse_name = sys.argv[2]
    with open(grammer_file_name) as grammer_file:
        with open(file_to_parse_name) as file_to_parse:
            grammer = grammer_file.read()
            file_contents = file_to_parse.read()
            print(debug(grammer, file_contents))
            # apexClass = transform(grammer, file_contents)
            # inject_profiling(apexClass)
            # print('apexClass: ' + str(apexClass.getContents()))
