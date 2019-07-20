import ast
import inspect
import coverage
import testCoverage
import importlib
def getCoverage(pythonFile, mainString,fun_name, mod_name):
    import os
    oi = inspect.getsource(pythonFile)
    cod = ast.parse(inspect.getsource(pythonFile))
    n_ele = []
    elem = dir(testCoverage)
    for i in elem:
        if callable(getattr(testCoverage, i)):
            n_ele.append(getattr(testCoverage, i))
    u_module = importlib.import_module(str(mod_name))
    user_module = dir(u_module)
    call_user = []
    for i in user_module:
        if callable(getattr(u_module, i)):
            call_user.append(getattr(u_module, i))
    print('aaa ')
    print(call_user)
    with open('testCoverage.py', 'w+') as f:
        f.write(oi)
        f.write(mainString)
    l_1 = ""
    leu = False
    with open(mod_name+'.py', 'r') as f:
        if not leu:
            l_1 = f.readline()
        if l_1.strip()!=False:
            leu = True
    leu = False
    l_2 = ""

    with open('testCoverage.py', 'r') as f:
        if not leu:
            l_2 = f.readline()
        if l_2.strip()!=False:
            leu = True
    print("oi "+l_1)
    print(l_2)
    if os.path.isfile('.coverage'):
        dictResultFile = ast.literal_eval(str(open(".coverage", "r").read()).replace('!coverage.py: This is a private format, don\'t read it directly!', ''))
        #cov.erase()
        cov = coverage.Coverage()
        cov.start()
        cov.stop()
        cov.annotate('testCoverage.py')
        #cov.erase()
        #os.system('coverage annotate ' + 'testCoverage.py' + '')
        codeAnnotation = []

        with open('testCoverage.py'+',cover','r') as f:
            codeAnnotation = f.readlines()
        codeAnnotation = [(x[1:].strip()).replace('\n', '') for x in codeAnnotation]
        #fixing line bug
        lines = []
        dicc = list(dictResultFile['lines'].keys())
        print dicc
        aux_name = ""
        for i in dicc:
            if mod_name in i:
                aux_name = i
        lines = dictResultFile['lines'][aux_name]
        if l_1!=l_2:
            aux_l = []
            for i in lines:
                if i !=1:
                    aux_l.append(i)
            lines = aux_l
            aux_l = []
            menor_ele = min(lines)
            for i in lines:
                aux_l.append(i-menor_ele+1)
            lines = aux_l
        print(dictResultFile['lines'].values())

    if lines:
        print lines
        return [lines, codeAnnotation, oi]
    else:
        return [[], codeAnnotation, oi]
