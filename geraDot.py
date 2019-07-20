from no import No
from graphviz import Digraph

def geraDot(listaNos, listCoverage, listSource, sourceCode, testResult, func_name):
    totNos = 0
    totNosCobertos = 0
    totArestasCobertas = 0
    totArestas = 0
    dot = Digraph(comment='CFG')
    for no in listaNos:
        if no.getPais() and no.getTipo() == "Except":

            for i in no.getPais():
                if i is not None and i.getSign() != True:
                    no.getPais().remove(i)

    '''for no in listaNos:
        pais = []
        if no.getPais():
            for i in no.getPais():
                if i is not None and i.getSignInvalido() and no.getTipo()!= "For" and no.getTipo()!= "While" and no.getTipo()!= "Finally" and no.getTipo()!= "Except"  and (i.getNumLinha()<no.getNumLinha()):
                    no.setSignInvalido(True)
                    break'''
    '''
    for no in listaNos:
        if no.getSignInvalido():
            print('genji')'''

    for no in listaNos:
        if no.getNumLinha() in listCoverage and listSource:
            if no.getTipo() == "Return" or no.getTipo() == "Break" or no.getTipo() == "Pass":
                dot.node(str(no), no.getTipoLinha() + '\n' + listSource[no.getNumLinha() - 1], color='darkgreen',
                         style="bold")
                totNos += 1
                totNosCobertos += 1
                continue
            else:
                dot.node(str(no), no.getTipoLinha() + '\n' + listSource[no.getNumLinha() - 1], color='darkgreen')
                totNos += 1
                totNosCobertos += 1
                continue
        if len(listSource) > 1:
            try:
                if no.getSignInvalido():
                    dot.node(str(no), no.getTipoLinha() + '\n' + listSource[no.getNumLinha() - 1], color='red')
                else:
                    dot.node(str(no), no.getTipoLinha() + '\n' + listSource[no.getNumLinha() - 1])
                totNos += 1
            except:
                if no.getSignInvalido():
                    dot.node(str(no), no.getTipoLinha() + '\n' + "node info not found", color='red')
                else:
                    dot.node(str(no), no.getTipoLinha() + '\n'+ "node info not found")
                totNos += 1
        else:
            if (no.getTipo() == "Return" or no.getTipo() == "Break" or no.getTipo() == "Pass") and no.getSignInvalido():
                dot.node(str(no), no.getTipoLinha() + '\n', style="bold", color="red")
                totNos += 1
                continue
            if no.getTipo() == "Return" or no.getTipo() == "Break" or no.getTipo() == "Pass":
                dot.node(str(no), no.getTipoLinha() + '\n', style="bold")
                totNos += 1
                continue
            if no.signInvalido:
                dot.node(str(no), no.getTipoLinha() + '\n', color="red", style="bold")
                totNos += 1
                continue
            else:
                dot.node(str(no), no.getTipoLinha() + '\n')
                totNos += 1

    for no in listaNos:
        pais = []

        if no.getPais():

            '''for i in no.getPais():
                if i is not None and i.getSignInvalido() and (no.getTipo()!= "Finally" or no.getTipo()!= "Except"):
                    no.setSignInvalido(True)
                    print('oioioioioisssss')'''

            '''for i in no.getPais():
                if (i is not None) and (i.getSign() != True) and (no.getTipo()== "Except"):
                    no.getPais().remove(i)'''

            pais = list(set(no.getPais()))
            po = len(pais) - 1
            i = 0

            while i <= po:
                if hasattr(pais[i], 'getTipo'):
                    if (pais[i].getTipo() == "Break" or pais[i].getTipo() == "Pass" or pais[
                        i].getTipo() == "Return") and no.getTipo() != "Finally" and not no.getSignInvalido():
                        pais.pop(i)
                        po = len(pais) - 1
                        continue
                i += 1

            for pai in pais:
                if (pai is not None):
                    if no.getNumLinha() in listCoverage and pai.getNumLinha() in listCoverage and no.getTipo() == "Except" and pai.getSign() == True:
                        dot.edge(str(pai), str(no), style='dashed', color='darkgreen')
                        totArestasCobertas += 1
                        totArestas += 1
                        continue

                    if no.getNumLinha() in listCoverage and pai.getNumLinha() in listCoverage:
                        dot.edge(str(pai), str(no), color='darkgreen')
                        totArestasCobertas += 1
                        totArestas += 1
                        continue
                    if no.getTipo() == "Except" and pai.getSign() == True:
                        dot.edge(str(pai), str(no), style='dashed')
                        totArestas += 1
                        continue
                    if no.getSignInvalido() or pai.getSignInvalido():
                        dot.edge(str(pai), str(no), style='dotted', color="red")
                        continue

                    else:
                        dot.edge(str(pai), str(no))
                        totArestas += 1

    '''dot.node('nos: '+str(totNos))
    dot.node('coberto: '+ str(totNosCobertos))
    dot.node("arestas: \n"+str(totArestas))
    dot.node("arestas cobertas : \n" + str(totArestasCobertas))'''
    if len(listSource) > 1:
        dot.node("Cobertura por nos: \n " + str(round((float(totNosCobertos) / float(totNos)), 3)),
                 shape='box')
        dot.node(
            "Cobertura por arestas: \n " + str(round((float(totArestasCobertas) / float(totArestas)), 3)),
            shape='box')
        dot.node("Source code: \n\t" + sourceCode, shape='box')
    dot.node("Test results:\n\t " + str(testResult), shape='box')
    dot.render(func_name, view=True)
