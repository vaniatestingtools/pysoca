#primeiro arg sao os metodos que terao os grafos gerados e o segundo testes
def hi():
    print('ooo')
    print(str(sys.argv))
    print(len(sys.argv))
    try:
        if(len(sys.argv)==4):
            imp = importlib.import_module(str(sys.argv[1]))
            print(imp)
            code = inspect.getsource(imp)
            print "koe"
            with open('foo.py', "w") as f:
                f.write(code)
            print("first")
            imp2 = importlib.import_module(str(sys.argv[2]))
            print(imp2)
            cod = inspect.getsource(imp2)
            import os
            os.system('coverage erase')
            os.system('coverage run '+sys.argv[2]+'.py')
            os.system('coverage annotate '+sys.argv[1]+'.py')
            os.system('python test.py '+sys.argv[3]+' '+sys.argv[1])

    except:
        print "Wrong input or file not found"
if __name__ == '__main__':
    import sys
    import ast
    import inspect
    import importlib
    hi()

#import test
