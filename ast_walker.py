#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ast
import inspect


class Ast_walker(ast.NodeVisitor):
    def __init__(self, grafo):
        self.grafo = grafo

    def visit_Module(self, node):
        #asts sempre iniciam com módulo,
        #coloquei ele chamando o resto
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        novoNo = self.grafo.criaNo(node.name, node.lineno)
        lastNode = None
        caminhoInvalido = None

        if node.body:
            notTransicao = None
            for no in node.body:
                if type(no).__name__ not in self.grafo.getTipos():
                    notTransicao = no
                    continue
                else:
                    if (type(no).__name__ == "Return" or type(no).__name__ == "Pass" or type(no).__name__ == "Continue" or type(no).__name__ == "Break") and (no is not node.body[-1]):
                        caminhoInvalido = True
                        self.visit(no)
                        continue
                    if notTransicao != None:
                        oi = self.visit(notTransicao)
                        if caminhoInvalido:
                            if type(oi) is list:
                                for i in oi:
                                    if i is not None:
                                        i.setSignInvalido(True)
                            elif(oi is not None):
                                oi.setSignInvalido(True)
                        notTransicao = None
                    lastNode = self.visit(no)
                    if caminhoInvalido:
                        if type(lastNode) is list:
                            for i in lastNode:
                                if i is not None:
                                    i.setSignInvalido(True)
                        elif (lastNode is not None):
                            lastNode.setSignInvalido(True)

        if notTransicao != None:
            notTransicao = self.visit(notTransicao)
            lastNode = notTransicao
        if (type(lastNode) is list):
            if caminhoInvalido:
                for i in lastNode:
                    i.setSignInvalido(True)
            for i in lastNode:
                if i is not None and i.getTipo() in self.grafo.getTipos():
                    lastNode.remove(i)
        else:
            if caminhoInvalido:
                lastNode.setSignInvalido(True)
                # novoNos.append(lastNode)
        return novoNo



    def visit_If(self, node):
        '''Todo If tem os parâmetros test(condição),
        #body(condição satisfeita) e orelse(condição não satisfeita).
        Os nós correspondentes a esses campos ficam dentro deles (são listas).
        *Ajuste para pegar o orelse certo, necessita de mais testes
        '''

        novoNos = []
        novoNo = self.grafo.criaNo("If", node.lineno)
        self.grafo.defCampo("body")
        caminhoInvalido = False
        lastNode = None
        novoNo2 = None
        if not node.body:
            novoNos.append(self.grafo.criaNo("bodyVazio", node.lineno))
        if node.body:
            notTransicao = None
            for no in node.body:
                if type(no).__name__ not in self.grafo.getTipos():
                    notTransicao = no

                    continue
                else:
                    if (type(no).__name__ == "Return" or type(no).__name__ == "Pass" or type(no).__name__ == "Continue" or type(no).__name__ == "Break") and (no is not node.body[-1]):
                        caminhoInvalido = True
                        self.visit(no)
                        continue
                    if notTransicao != None:
                        oi = self.visit(notTransicao)
                        if caminhoInvalido:
                            if type(oi) is list:
                                for i in oi:
                                    if i is not None:
                                        i.setSignInvalido(True)
                            elif (oi is not None):
                                oi.setSignInvalido(True)
                        notTransicao = None
                    lastNode = self.visit(no)
                    if caminhoInvalido:
                        if type(lastNode) is list:
                            for i in lastNode:
                                if i is not None:
                                    i.setSignInvalido(True)
                        elif (lastNode is not None):
                            lastNode.setSignInvalido(True)
        if notTransicao != None:
            notTransicao = self.visit(notTransicao)
            lastNode = notTransicao
        if(type(lastNode) is list):
            if caminhoInvalido:
                for i in lastNode:
                    i.setSignInvalido(True)
            for i in lastNode:
                if i.getTipo() in self.grafo.getTipos():
                    del i
            novoNos = lastNode
        else:
            if caminhoInvalido:
                lastNode.setSignInvalido(True)
            novoNos.append(lastNode)
        self.grafo.defCampo("orelse")
        caminhoInvalido = False
        if not node.orelse:
            novoNos.append(self.grafo.criaNo("orelseVazioIf", node.lineno))

        if node.orelse:
            #orelse pode ter tamanho maior que 1?
            notTransicao = None
            for no in node.orelse:
                if type(no).__name__ not in self.grafo.getTipos():
                    notTransicao = no
                    continue
                else:
                    if (type(no).__name__ == "Return" or type(no).__name__ == "Pass" or type(no).__name__ == "Continue" or type(no).__name__ == "Break") and (no is not node.orelse[-1]):
                        caminhoInvalido = True
                        self.visit(no)
                        continue
                    if notTransicao != None:
                        oi = self.visit(notTransicao)
                        if oi is not None and caminhoInvalido:
                            oi.setSignInvalido(True)
                        novoNo2 = self.visit(no)
                        if caminhoInvalido:
                            if type(novoNo2) is list:
                                for i in novoNo2:
                                    if i is not None:
                                        i.setSignInvalido(True)
                            elif(novoNo2 is not None):
                                novoNo2.setSignInvalido(True)
            if notTransicao != None:
                notTransicao = self.visit(notTransicao)
                novoNo2 = notTransicao
                if caminhoInvalido:
                    if novoNo2 is not None:
                        novoNo2.setSignInvalido(True)
                novoNos.append(novoNo2)
            elif novoNo2 is not None:
                for i in novoNo2:
                    if i in self.grafo.tiposNo() and i.getTipo()!= "Except":
                        novoNo2.pop(0)
                while novoNo2:
                    novoNos.append(novoNo2.pop(0))


        self.grafo.defCampo("fimOrelse")
        novoNos.insert(0, novoNo)

        return novoNos

    def visit_Pass(self, node):
        '''
        '''
        novoNo = self.grafo.criaNo("Pass", node.lineno)
        novoNo.temFilho = False
        return novoNo

    def visit_Assign(self, node):
        '''
        '''
        novoNo = self.grafo.criaNo("Assign", node.lineno)
        return novoNo

    def visit_Continue(self, node):
        '''
        '''
        novoNo = self.grafo.criaNo("Continue", node.lineno)
        novoNo.temFilho = False
        return novoNo

    def visit_Break(self, node):
        '''
        '''
        novoNo = self.grafo.criaNo("Break", node.lineno)
        novoNo.temFilho = False
        return novoNo

    def visit_Return(self, node):
        '''
        '''
        novoNo = self.grafo.criaNo("Return", node.lineno)
        novoNo.temFilho = False
        return novoNo

    def visit_TryFinally(self, node):
        '''
        '''
        novoNo1 = None
        novoNo = self.grafo.criaNo("TryFinally", node.lineno)

        notTransicao = None
        caminhoInvalido = False
        lastNode = None
        self.grafo.defCampo("body")
        if not node.body:
            self.grafo.criaNo("bodyVazio", node.lineno)
        if node.body:
            for no in node.body:
                novoNo1 = self.visit(no)
        if (type(novoNo1) is list and type(novoNo1[1]) is list):
            novoNo1 = novoNo1[1]
        if not node.finalbody:
            self.grafo.criaNo("bodyVazio", node.lineno)
        finallyNode = None
        caminhoInvalido = False
        lastNode = None
        if node.finalbody:
            finallyNode = self.grafo.criaNo("Finally", node.lineno)
            for no in node.finalbody:
                if type(no).__name__ not in self.grafo.getTipos():
                    notTransicao = no
                    continue
                else:
                    if (type(no).__name__ == "Return" or type(no).__name__ == "Pass" or type(no).__name__ == "Continue" or type(no).__name__ == "Break") and (no is not node.body[-1]):
                        caminhoInvalido = True
                        self.visit(no)
                        continue
                    if notTransicao != None:
                        oi = self.visit(notTransicao)
                        if caminhoInvalido:
                            if type(oi) is list:
                                for i in oi:
                                    if i is not None:
                                        i.setSignInvalido(True)
                            elif (oi is not None):
                                oi.setSignInvalido(True)
                        notTransicao = None
                    lastNode = self.visit(no)
                    if caminhoInvalido:
                        if type(lastNode) is list:
                            for i in lastNode:
                                if i is not None:
                                    i.setSignInvalido(True)
                        elif (lastNode is not None):
                            lastNode.setSignInvalido(True)

            if notTransicao != None:
                notTransicao = self.visit(notTransicao)
                lastNode = notTransicao
            if type(lastNode) is list:
                if caminhoInvalido:
                    for i in lastNode:
                        i.setSignInvalido(True)
                for i in lastNode:
                    if i.getTipo() == "If":
                        lastNode.remove(i)
            else:
                if caminhoInvalido:
                    lastNode.setSignInvalido(True)
                else:
                    if novoNo is not None:
                        novoNo.setPai(lastNode)
        for no in novoNo1:
            finallyNode.setPai(no)
        return novoNo

    def visit_TryExcept(self, node):
        '''
        '''
        handlerList = []
        novoNo = self.grafo.criaNo("TryExcept", node.lineno)
        novoNo1 = None
        lastNode = None
        notTransicao = None
        lastNode = None
        caminhoInvalido = False
        if not node.body:
            self.grafo.criaNo("bodyVazio", node.lineno)
        if node.body:
            for no in node.body:
                if type(no).__name__ not in self.grafo.getTipos():
                    notTransicao = no
                    continue
                else:
                    if (type(no).__name__ == "Return" or type(no).__name__ == "Pass" or type(
                            no).__name__ == "Continue" or type(no).__name__ == "Break") and (no is not node.body[-1]):
                        caminhoInvalido = True
                        self.visit(no)
                        continue
                    if notTransicao != None:
                        oi = self.visit(notTransicao)
                        if caminhoInvalido:
                            if (oi is not None):
                                oi.setSignInvalido(True)
                        notTransicao = None
                    lastNode = self.visit(no)
                    if caminhoInvalido:
                        if type(lastNode) is list:
                            for i in lastNode:
                                if i is not None:
                                    i.setSignInvalido(True)
                            for i in lastNode:
                                if i.getTipo() in self.grafo.getTipos():
                                    lastNode.remove(i)
                        elif (lastNode is not None):
                            lastNode.setSignInvalido(True)
            if notTransicao != None:
                notTransicao = self.visit(notTransicao)
                lastNode = notTransicao
            if type(lastNode) is list:
                for i in lastNode:
                    i.setSign(True)
            else:
                lastNode.setSign(True)
            if caminhoInvalido:
                if type(lastNode) is list:
                    for i in lastNode:
                        i.setSignInvalido(True)
                else:
                    lastNode.setSignInvalido(True)
        if caminhoInvalido:
            lastNode.setSignInvalido(True)

        #novoNo.setPai(lastNode)
        '''if not node.orelse:
            self.grafo.criaNo("orElseVazioTryExcept", node.lineno)'''
        if node.orelse:
            for no in node.orelse:
                self.visit(no)
        if not node.handlers:
            self.grafo.criaNo("handlerVazio", node.lineno)
        '''if type(novoNo1) is list:
            if novoNo1[0] in self.grafo.getTipos() and novoNo1[0].getTipo() != "Except" and len(novoNo1)>1:
                novoNo1.pop(0)
                for k in novoNo1:
                    k.setSign(True)'''
        if node.handlers:
            for no in node.handlers:
                handlerList.append(self.visit(no))
        flat_list = []
        for sublist in handlerList:
            for item in sublist:
                flat_list.append(item)

        if type(lastNode) is list:
            if lastNode[0].getTipo() in self.grafo.getTipos():
                lastNode.pop(0)
        for i in flat_list:
            if i.getTipo() == "Except":
                if type(lastNode) is list:
                    #for k in range(len(lastNode)):
                     #   i.setPai(lastNode[k])
                    i.setPai(lastNode)
                else:
                    i.setPai(lastNode)
        for i in handlerList:
            i.pop(0)
        return [novoNo, handlerList]

    def visit_ExceptHandler(self, node):
        '''
        '''
        novoNo = self.grafo.criaNo("Except", node.lineno)
        lastNode = None
        caminhoInvalido = False
        if node.body:

            for no in node.body:
                if type(no).__name__ not in self.grafo.getTipos():
                    notTransicao = no
                    continue
                else:
                    if (type(no).__name__ == "Return" or type(no).__name__ == "Pass" or type(no).__name__ == "Continue" or type(no).__name__ == "Break") and (no is not node.body[-1]):
                        caminhoInvalido = True
                        self.visit(no)
                        continue
                    if notTransicao != None:
                        oi = self.visit(notTransicao)
                        if caminhoInvalido:
                            if (oi is not None):
                                oi.setSignInvalido(True)
                        notTransicao = None
                    lastNode = self.visit(no)
                    if caminhoInvalido:
                        if type(lastNode) is list:
                            for i in lastNode:
                                if i is not None:
                                    i.setSignInvalido(True)
                            for i in lastNode:
                                if i.getTipo() in self.grafo.getTipos():
                                    lastNode.remove(i)
                        elif (lastNode is not None):
                            lastNode.setSignInvalido(True)
        if notTransicao != None:
            notTransicao = self.visit(notTransicao)
            lastNode = notTransicao
        if caminhoInvalido:
            if type(lastNode) is list:
                for i in lastNode:
                    i.setSignInvalido(True)
            else:
                lastNode.setSignInvalido(True)

        if not node.body:
            self.grafo.criaNo("bodyVazio", node.lineno)
        return [novoNo, lastNode]

    def visit_For(self, node):
        '''Visita do for: o último filho do body é pai do for atual,
        orelse suportado, sendo assim, o for atual caso tenha um else associado se torna pai do mesmo
        elses executados apenas se não houver nenhum break no for'''

        novoNo = self.grafo.criaNo("For", node.lineno)
        lastNode = None
        caminhoInvalido = False
        notTransicao = None
        self.grafo.defCampo("bodyFor")
        if not node.body:
            lastNode = self.grafo.criaNo("bodyVazio", node.lineno)

        if node.body:
            notTransicao = None
            for no in node.body:
                if type(no).__name__ not in self.grafo.getTipos():
                    notTransicao = no
                    continue
                else:
                    if (type(no).__name__ == "Return" or type(no).__name__ == "Pass" or type(no).__name__ == "Continue" or type(no).__name__ == "Break") and (no is not node.body[-1]):
                        caminhoInvalido = True
                        lastNode = self.visit(no)
                        if lastNode.getTipo() =="Continue":
                            novoNo.setPai(lastNode)
                        continue
                    if notTransicao != None:
                        oi = self.visit(notTransicao)
                        if caminhoInvalido:
                            if oi is not None:
                                oi.setSignInvalido(True)
                        notTransicao = None
                    lastNode = self.visit(no)
                    if caminhoInvalido:
                        if type(lastNode) is list:
                            for i in lastNode:
                                if i is not None:
                                    i.setSignInvalido(True)
                        elif (lastNode is not None):
                            lastNode.setSignInvalido(True)
                if type(lastNode) is list:
                    for n in range(len(lastNode)):
                        if hasattr(lastNode[n], 'getTipo'):
                            if lastNode[n].getTipo() != "If":
                                novoNo.setPai(lastNode[n])
                            if caminhoInvalido:
                                lastNode[n].setSignInvalido(True)
                    continue
                elif lastNode.getTipo() == "Continue":
                    novoNo.setPai(lastNode)
            lastNode = None
            if notTransicao != None:
                notTransicao = self.visit(notTransicao)
                lastNode = notTransicao
        if caminhoInvalido and lastNode is not None:
            lastNode.setSignInvalido(True)
        else:
            novoNo.setPai(lastNode)
        self.grafo.defCampo("orelseFor")
        lastNode = None
        notTransicao = None
        caminhoInvalido = False
        if node.orelse:
            for no in node.orelse:
                if type(no).__name__ not in self.grafo.getTipos():
                    notTransicao = no
                    continue
                else:
                    if (type(no).__name__ == "Return" or type(no).__name__ == "Pass" or type(no).__name__ == "Continue" or type(no).__name__ == "Break") and (no is not node.orelse[-1]):
                        caminhoInvalido = True
                    if notTransicao != None:
                        self.visit(notTransicao)
                        notTransicao = None
                    lastNode = self.visit(no)
            if notTransicao != None:
                notTransicao = self.visit(notTransicao)
                lastNode = notTransicao
        if type(lastNode) is list:
            if lastNode is not None and caminhoInvalido:
                for i in lastNode:
                    i.setSignInvalido(True)
            for i in lastNode:
                if i is not None and i in self.grafo.getTipos():
                    lastNode.remove(i)
            for i in lastNode:
                if i is not None:
                    i.setPai(novoNo)
        else:
            if lastNode is not None and caminhoInvalido:
                lastNode.setSignInvalido(True)
            if lastNode is not None:
                lastNode.setPai(novoNo)
        self.grafo.defCampo("fimOrelseFor")
        return novoNo

    def visit_While(self, node):
        '''Visita do while: o último filho do body é pai do for atual,
                orelse suportado, sendo assim, o for atual caso tenha um else associado se torna pai do mesmo
                elses executados apenas se não houver nenhum break no while'''


        novoNo = self.grafo.criaNo("While", node.lineno)
        lastNode = None
        caminhoInvalido = False
        notTransicao = None
        self.grafo.defCampo("bodyFor")
        if not node.body:
            lastNode = self.grafo.criaNo("bodyVazio", node.lineno)

        if node.body:
            notTransicao = None
            for no in node.body:
                if type(no).__name__ not in self.grafo.getTipos():
                    notTransicao = no
                    continue
                else:
                    if (type(no).__name__ == "Return" or type(no).__name__ == "Pass" or type(no).__name__ == "Continue" or type(no).__name__ == "Break") and (no is not node.body[-1]):
                        caminhoInvalido = True
                        lastNode = self.visit(no)
                        if lastNode.getTipo() =="Continue":
                            novoNo.setPai(lastNode)
                        continue
                    if notTransicao != None:
                        oi = self.visit(notTransicao)
                        if caminhoInvalido:
                            if oi is not None:
                                oi.setSignInvalido(True)
                        notTransicao = None
                    lastNode = self.visit(no)
                    if caminhoInvalido:
                        if type(lastNode) is list:
                            for i in lastNode:
                                if i is not None:
                                    i.setSignInvalido(True)
                        elif (lastNode is not None):
                            lastNode.setSignInvalido(True)
                if type(lastNode) is list:
                    for n in range(len(lastNode)):
                        if hasattr(lastNode[n], 'getTipo'):
                            if lastNode[n].getTipo() != "If":
                                novoNo.setPai(lastNode[n])
                            if caminhoInvalido:
                                lastNode[n].setSignInvalido(True)
                    continue
                elif lastNode.getTipo() == "Continue":
                    novoNo.setPai(lastNode)
            lastNode = None
            if notTransicao != None:
                notTransicao = self.visit(notTransicao)
                lastNode = notTransicao
        if caminhoInvalido and lastNode is not None:
            lastNode.setSignInvalido(True)
        else:
            novoNo.setPai(lastNode)
        self.grafo.defCampo("orelseFor")
        lastNode = None
        notTransicao = None
        caminhoInvalido = False
        if node.orelse:
            for no in node.orelse:
                if type(no).__name__ not in self.grafo.getTipos():
                    notTransicao = no
                    continue
                else:
                    if (type(no).__name__ == "Return" or type(no).__name__ == "Pass" or type(no).__name__ == "Continue" or type(no).__name__ == "Break") and (no is not node.orelse[-1]):
                        caminhoInvalido = True
                    if notTransicao != None:
                        self.visit(notTransicao)
                        notTransicao = None
                    lastNode = self.visit(no)
            if notTransicao != None:
                notTransicao = self.visit(notTransicao)
                lastNode = notTransicao
        if type(lastNode) is list:
            if lastNode is not None and caminhoInvalido:
                for i in lastNode:
                    i.setSignInvalido(True)
            for i in lastNode:
                if i is not None and i in self.grafo.getTipos():
                    lastNode.remove(i)
            for i in lastNode:
                if i is not None:
                    i.setPai(novoNo)
        else:
            if lastNode is not None and caminhoInvalido:
                lastNode.setSignInvalido(True)
            if lastNode is not None:
                lastNode.setPai(novoNo)
        self.grafo.defCampo("fimOrelseFor")
        return novoNo


    def visit_With(self, node):
        '''
        '''
        novoNo = self.grafo.criaNo("With", node.lineno)
        lastNode = None
        caminhoInvalido = False
        notTransicao = None
        self.grafo.defCampo("body")
        if not node.body:
            lastNode = self.grafo.criaNo("bodyVazio", node.lineno)
        if node.body:
            notTransicao = None
            for no in node.body:
                if type(no).__name__ not in self.grafo.getTipos():
                    notTransicao = no
                    continue
                else:
                    if (type(no).__name__ == "Return" or type(no).__name__ == "Pass" or type(
                            no).__name__ == "Continue" or type(no).__name__ == "Break") and (no is not node.body[-1]):
                        caminhoInvalido = True
                        self.visit(no)
                        continue
                    if notTransicao != None:
                        oi = self.visit(notTransicao)
                        if caminhoInvalido:
                            if oi is not None:
                                oi.setSignInvalido(True)
                        notTransicao = None
                    lastNode = self.visit(no)
                    if caminhoInvalido:
                        if type(lastNode) is list:
                            for i in lastNode:
                                if i is not None:
                                    i.setSignInvalido(True)
                        elif (lastNode is not None):
                            lastNode.setSignInvalido(True)
                if type(lastNode) is list:
                    for n in lastNode:
                        if caminhoInvalido:
                            n.setSignInvalido(True)
                    continue

            if notTransicao != None:
                notTransicao = self.visit(notTransicao)
                lastNode = notTransicao
        if type(lastNode) is list:
            if caminhoInvalido:
                for i in lastNode:
                    i.setSignInvalido(True)
        else:
            if caminhoInvalido:
                lastNode.setSignInvalido(True)
        self.grafo.defCampo("orelse")
        self.grafo.defCampo("fimOrelse")
        return lastNode


    def generic_visit(self, node):
        '''
        Nós de tipos cujas visitas não tiverem sido redefinidas
        pelos métodos acima serão visitadas por esse método.
        '''

        lineno = -1
        if hasattr(node, "lineno"):
            lineno = node.lineno
        novoNo = self.grafo.criaNo(type(node).__name__, lineno)
        ast.NodeVisitor.generic_visit(self, node)
        return novoNo


