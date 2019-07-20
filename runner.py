import ast
import inspect
from geraDot import *
import coverage
from grafo import Grafo
from ast_walker import *
from instrumentation import *
import sys
import importlib
def runner(nomeFunc, mainString, testResult, fun_name, mod_name):
    grafo = Grafo()
    walker = Ast_walker(grafo)
    import my_func
    codeAst = ast.parse(inspect.getsource(nomeFunc))
    listCoverage = getCoverage(nomeFunc, mainString,fun_name, mod_name)
    walker.visit(codeAst)

    geraDot(grafo.listaNos,listCoverage[0],listCoverage[1],listCoverage[2], testResult, fun_name)
    del grafo