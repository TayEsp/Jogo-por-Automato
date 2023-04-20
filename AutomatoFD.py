#Esqueleto de código Python para implementar algoritmos sobre automatos finitos.
import xmltodict

class AutomatoFD:

    #a função init é a função construtora da classe
    def __init__(self, Alfabeto):
        Alfabeto = str(Alfabeto)
        self.estados = set()
        self.alfabeto = Alfabeto
        self.transicoes = dict()
        self.inicial = None
        self.finais = set()

    #inicializa variaveis utilizadas no processamento de cadeias ("zera" o autômato)
    def limpaAfd(self):
        self.__deuErro = False
        self.__estadoAtual = self.inicial

    # Cria o estado int(id) se ele ainda não existe e retorna True. Se o estado já existe, não faz nada e retorna falso.
    def criaEstado(self, id, inicial=False, final=False):

        id = int(id)
        if id in self.estados: #verifica se o estado já está no conjunto de estados existentes, se ele já existe não faz nada
            return False
        self.estados = self.estados.union({id}) #se o estado ainda não existe, adiciona ele no conjunto de estados
        if inicial:
            self.inicial = id
        if final:
            self.finais = self.finais.union({id})
        return True

    #Cria a transição "(origem,simbolo)->destino", se os parametros são validos e retorna True. Caso contrário, não faz nada e retorna False.
    def criaTransicao(self, origem, destino, simbolo):

        origem=int(origem)
        destino = int(destino)
        simbolo = str(simbolo)

        if not origem in self.estados: #verifica se o estado está no conjunto de estados
            return False
        if not destino in self.estados: #verifica se o estado está no conjunto de estados
            return False
        if len(simbolo) != 1 or not simbolo in self.alfabeto: #verifica se o simbolo digitado possui apenas 1 caractere e se ele está no conjunto do alfabeto
            return False

        self.transicoes[(origem, simbolo)] = destino #se estiver tudo certo, a transição é criada
        return True

    #Define um estado já existente como inicial
    def mudaEstadoInicial(self, id):
        if not id in self.estados: #verifica se o estado faz parte do conjunto de estados
            return
        self.inicial = id #coloca o estado passado no parâmetro como sendo o novo estado inicial

    def mudaEstadoFinal(self, id, final):
        if not id in self.estados:
            return
        if final: #se o estado for final, ele será incluído no conjunto de estados finais
            self.finais = self.finais.union({id})
        else: #se o estado não for final e estiver no conjunto dos estados finais, ele é retirado
            self.finais = self.finais.difference({id})

    #Partindo do estado atual, processa a cadeia e retorna o estado de parada. Se ocorrer erro, liga a variavel __deuErro.
    def move(self, cadeia):
        for simbolo in cadeia: #o for percorre cada símbolo da cadeia
            if not simbolo in self.alfabeto: #verifica se o símbolo está presente no alfabeto.
                self.__deuErro = True #da erro se o símbolo nao estiver no alfabeto
                break
            if(self.__estadoAtual, simbolo) in self.transicoes.keys(): #verifica se a transição existe
                novoEstado = self.transicoes[(self.__estadoAtual, simbolo)] #o novo estado passa a ser o estado resultante da transição
                self.__estadoAtual = novoEstado
            else:
                self.__deuErro = True #da erro se a transição não existir
                break
        return self.__estadoAtual #a ultima vez que rodar no loop, o estado atual será o que tiver parado

    #a função retorna o valor da variavel __deuErro (usada na função move)
    def deuErro(self):
        return self.__deuErro

    # a função retorna o valor da variavel __estadoAtual (usada na função move)
    def estadoAtual(self):
        return self.__estadoAtual

    # a função retorna o estado final
    def estadoFinal(self, id):
        return id in self.finais

    #sempre que o python precisar enxergar o AFD como string, ele usa essa função. Essa função imprime o AFD
    def __str__(self):
        s = 'AFD(E, A, T, i, F): \n'
        s += ' E = { '
        for e in self.estados:
            s += '{}, '.format(str(e))
        s += '} \n'
        s += '  A = {'
        for a in self.alfabeto:
            s += "'{}', ".format(a)
        s += '} \n'
        s += '  T = {'
        for (e, a) in self.transicoes.keys():
            d = self.transicoes[(e, a)]
            s += "({}, '{}')-->{} ".format(e, a, d)
        s += '} \n'
        s += '  i = {} \n'.format(self.inicial)
        s += ' F = { '
        for e in self.finais:
            s += '{}, '.format(str(e))
        s += '}'
        return s

        # função que carrega o automato (cria os estados, as transições e define os estados finais e iniciais)

    def carregaAFD(self, afdXml):
        # laco for para criar os estados
        for i in range(len(afdXml["structure"]["automaton"][
                               "state"])):  # o parâmetro: len(afdXml["structure"]["automaton"]["state"]) + 1 me retorna o comprimento da lista que contém os estados e acrescenta em uma unidade, já que o for percorre de 0 a n - 1.
            self.criaEstado(i)

        # trecho do código chama o método que procura o estado inicial e o define como estado inicial
        inicial = int(self.procuraInicial(afdXml["structure"]["automaton"]["state"],
                                          len(afdXml["structure"]["automaton"]["state"])))
        self.mudaEstadoInicial(inicial)

        # trecho do código que chama o método que procura o(s) estado(s) final(is) e o define como estado final
        finais = []  # como pode haver mais de um estado final, eu crio uma lista para receber esses estados
        finais = self.procuraFinal(afdXml["structure"]["automaton"]["state"],
                                   len(afdXml["structure"]["automaton"]["state"]))
        for i in range(0, len(finais)):
            self.mudaEstadoFinal(int(finais[i]), True)

        # trecho do código que cria as transições
        for i in range(0, len(afdXml["structure"]["automaton"]["transition"])):
            self.criaTransicao(afdXml["structure"]["automaton"]["transition"][i]["from"],
                               afdXml["structure"]["automaton"]["transition"][i]["to"],
                               afdXml["structure"]["automaton"]["transition"][i]["read"])

        # a função le uma arquivo xml gerado pelo JFLAP

    def leXML(self, diretorio):
        try:
            with open(diretorio) as file:
                meuXml = file.read()
                # xmltodict.parse() analisa o conteúdo da variável e converte em um Dicionário
                meuXml = xmltodict.parse(meuXml)
        except:
            return None
        return meuXml

        # a função procura o estado inicial dentro da lista de estados gerada pelo arquivo XML

    def procuraInicial(self, estados, tam):
        for i in range(0, tam):
            if "initial" in estados[i]:
                return estados[i]["@id"]

        # a função procura o estado final dentro da lista de estados gerada pelo arquivo XML

    def procuraFinal(self, estados, tam):
        finais = []  # lista que guardará os estados finais
        for i in range(0, tam):
            if "final" in estados[i]:
                finais.append(estados[i]["@id"])

        return finais

    def aceitaCadeia(self, cadeia):
        self.limpaAfd()  # inicializa o autômato
        parada = self.move(cadeia)  # roda a cadeia e retorna o estado de parada
        if self.deuErro():
            print("Não foi possível rodar a cadeia. Tente novamente.")
        else:
            if not self.deuErro() and self.estadoFinal(parada):
                return 0 #aceita a cadeia
            else:
                return 1 #rejeita a cadeia

    def insereV(self, cadeia):
        if(cadeia == 'rs'):
            cadeia2 = list(cadeia)  # converte a cadeia em lista para poder fazer as inserções
            cadeia2.append('v')  # insere a letra v na ultima posição
            cadeia3 = "".join(cadeia2)  # volta a cadeia para string novamente
        else:
            cadeia2 = list(cadeia) #converte a cadeia em lista para poder fazer as inserções
            for i in range(0, 2*len(cadeia), 2): #for percorre a lista de 2 em 2, ou seja, i sempre será par
                cadeia2.insert(i+1, 'v') #insere a letra v nas posições ímpares da cadeia
            cadeia3 = "".join(cadeia2) #volta a cadeia para string novamente

        return cadeia3

    #cada estado que representa um golpe
    def acaoSprite(self, estado):
        if(estado == 0):
            img = "Stand/sprite_*.png"
        elif(estado == 1):
            img = "Andar/a_*.png"
            return img
        elif(estado == 2):
            img = "Chutar/ch_*.png"
            return img
        elif(estado == 6):
            img = "Correr/c_*.png"
            return img
        elif(estado == 3):
            img = "Pular/p_*.png"
            return img
        elif(estado == 5):
            img = "Socar/s_*.png"
            return img
        elif(estado == 4):
            img = "Combo/cm_*.png"
            return img

