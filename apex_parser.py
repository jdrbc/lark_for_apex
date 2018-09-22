import sys
import os
import argparse
import multiprocessing
from time import time
from lark import Lark, Transformer, v_args, UnexpectedToken

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

def parse(grammer, target, namespace=None):
    if (namespace != None):
        namespace.tree = None
        namespace.error_msg = ''
    try:
        apex_parser = Lark(grammer, parser='earley', lexer='standard')
        tree = apex_parser.parse(target)
        if (namespace != None):
            namespace.tree = tree
        return tree
    except UnexpectedToken as exception:
        if (namespace != None):
            namespace.error_msg = 'unexpected token!' + str(exception)
        return None

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

def parse_file(grammer, file_name):
    print("parsing {}".format(file_name))
    with open(file_name) as file_to_parse:
        file_contents = file_to_parse.read()
        manager = multiprocessing.Manager()
        namespace = manager.Namespace()

        # Start parse as process
        p = multiprocessing.Process(target=parse, args=(grammer, file_contents, namespace))
        time_start = time()
        p.start()

        # Wait
        p.join(10)

        # If thread is still active
        if p.is_alive():
            print("too slow parse of {}!".format(file_name))
            p.terminate()
            p.join()
        else:
            if (namespace.tree != None):
                delta = round(time() - time_start, 2)
                print("successful parse {} in {}s".format(file_name, delta))
                # apexClass = transform(namespace.tree)
                # inject_profiling(apexClass)
                # print('apexClass: ' + str(apexClass.getContents()))
            else:
                print("error during parse of {}: {}".format(file_name, namespace.error_msg))


def parse_dir(grammer, apex_directory_name):
    def walkErrorHandler(exception):
        raise exception
    for root, dirs, files in os.walk(apex_directory_name, onerror=walkErrorHandler):
        for file in files:
            file_name, file_extension = os.path.splitext(file)
            if file_extension == '.cls':
                parse_file(grammer, os.path.join(root, file))

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='Manipulate Apex')
    arg_parser.add_argument('grammer_file')
    arg_parser.add_argument('-f', '--apex_file')
    arg_parser.add_argument('-d', '--apex_dir')
    args = arg_parser.parse_args()

    grammer_file_name = args.grammer_file
    with open(grammer_file_name) as grammer_file:
        grammer = grammer_file.read()
        if args.apex_file != None:
            parse_file(grammer, args.apex_file)

        if args.apex_dir != None:
            parse_dir(grammer, args.apex_dir)

