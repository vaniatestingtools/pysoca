
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from no import No
from graphviz import Digraph


class Grafo:
    """Gera um grafo cujos nos vao sendo
    definidos a partir de seu tipo, numero de linha,
    etc.
    Disponibiliza a opcao de gerar uma visualizacao do grafo
    utilizando a ferramenta graphviz.
    """

    numNos = 0
    listaNos = []
    listaSemFilhos = []  # para usar como pais do no seguinte ao orelse
    listaReturn = []
    pilhaIf = []
    pilhaFor = []
    pilhaWhile = []
    pilhaCampo = []  # guarda campos para restaurar (if dentro de if, etc)
    anterior = None
    campo = None  # define se esta no body ou orelse de um if, por exemplo
    transicaoDeCampo = False
    tiposNo = ["If", "For", "While", "Return", "Continue", "Break", "Pass", "Try", "Except", "Finally", "TryExcept", "With"]
    totNos = 0
    totNosCobertos = 0
    totArestas = 0
    totArestasCobertas = 0
    def __init__(self):
        self.totNos = 0
        self.totNosCobertos = 0
        self.totArestas = 0
        self.totArestasCobertas = 0
        pass

    def verificador(self, tipo):
        """
        Verifica se o no desvia o fluxo.
        Por enquanto, o if que lida com isso de alterar o fluxo so
        verifica se o no eh do tipo If.
        Retorna True caso desvie o fluxo."""

        if (self.transicaoDeCampo is True):
            return True  # se ta mudando de campo numa estrutura de controle
        if (tipo == "Module"):
            return False
        if (self.anterior is None):  # se for o primeiro no do grafo, o cria
            return True
        if tipo not in self.tiposNo and self.anterior.getTipo() not in self.tiposNo:
            return False
        return True

    def defCampo(self, campo):  # define o contexto do proximo no
        print(self.campo)
        if (campo == "orelse" or campo=="orelseFor"):
            self.transicaoDeCampo = True
            if((self.anterior).temFilho == True):
                self.listaSemFilhos.append(self.anterior)
        self.campo = campo  # pode ser body, orelse, fimOrelse, etc.

    def defPai(self, no):
        """
        Quando for o primeiro elemento do orelse, define o pai dele
        como o if mais recente da pilha e desempilha esse if.
        Quando for o primeiro elemento depois de um orelse, define
        seus pais como sendo todos os nos sem filhos (que nao sao return).
        Caso contrario, define o pai como sendo o no anterior.
        """
        if (self.transicaoDeCampo is True):
            self.transicaoDeCampo = False
            if self.campo == "orelse" and self.pilhaIf:
                print('entrei')
                print(self.pilhaIf)
                no.setPai(self.pilhaIf.pop())
            if self.campo == "orelseFor" and self.pilhaFor:
                no.setPai(self.pilhaFor.pop())
            if (self.campo == "fimOrelse" or self.campo ==  "fimOrelseFor"):
                lista = []
                # esvazia a lista de nos sem filhos e coloca como pais do no
                while (len(self.listaSemFilhos) > 0):
                    o = self.listaSemFilhos.pop()
                    if o.temFilho == True:
                        lista.append(o)
                    if no.getTipo() == "Except":
                        for i in range(len(lista)):
                            if lista[i].getSign() == True:
                                no.setPai(lista[i])
                        continue
                    else:
                        no.setPai(lista)

        else:
            no.setPai(self.anterior)
    def getTipos(self):
        return self.tiposNo

    def criaNo(self, tipo, numlinha):
        """
        Cria no apenas se ele mudar o fluxo do programa, para que
        no se repitam nos seguidos que nao alterem o fluxo;
        para duas atribuicoes seguidas, por exemplo, sera criado
        apenas um no.
        """

        if (not self.verificador(tipo)):
            pass  # se nao altera fluxo, ignora no da ast e nao cria no grafo
        else:
            no = No(tipo, numlinha)
            self.defPai(no)
            self.numNos += 1
            self.listaNos.append(no)
            if (tipo == "If"):
                self.pilhaIf.append(no)
            if (tipo == "Return"):
                self.listaReturn.append(no)
            # Definir os outros tipos aqui.
            if (tipo == "For"):
                self.pilhaFor.append(no)
            if (tipo == "While"):
                self.pilhaFor.append(no)
            self.anterior = no # no recem incluido eh anterior ao proximo
            return self.anterior

    def printGrafo(self):
        #print "quantidade de nos: ", self.numNos
        for no in self.listaNos:
            #print no.getTipo(), "numLinha: ", no.getNumLinha(), " filho de:"
            for pai in no.getPais():
                try:
                    print (pai.getTipo())
                except (AttributeError):  # se nao tiver pais
                    print ("Ninguem")

    def printCampo(self):
        print "Campo: ", self.campo

