SE, A_ZERO, ENTAO, VA_PARA = "Se", "a_zero", "então", "vá_para"
SENAO, FACA, SUBTRAIR_A, ADICIONAR_B =  "senão", "Faça", "subtrair_a", "adicionar_b"
R, X = "R", "x"
SEP = ":"
FIM_LINHA = ";"


class Tokens:
    """ Tokens e ordem permitida na máquina 2REG """
    def __init__(self):
        self._tokens = {
            SE, A_ZERO, ENTAO, VA_PARA, SENAO, FACA, SUBTRAIR_A, ADICIONAR_B,
            R, X, SEP, FIM_LINHA
        }
        self._ordem = {
            SE: A_ZERO,
            A_ZERO: ENTAO,
            ENTAO: VA_PARA,
            VA_PARA: R,
            SENAO: VA_PARA,
            FACA: {SUBTRAIR_A, ADICIONAR_B},
            SUBTRAIR_A: VA_PARA,
            ADICIONAR_B: VA_PARA,
            SEP: {FACA, SE},
            R: SENAO
        }


class Compilador2Reg(Tokens):
    """ Classe para interpretar códigos 2REG """

    def __init__(self, arquivo: str):
        """ 
        Parameters
        ----------
        arquivo: str
            nome do arquivo com o caminho
        """
        self.__arquivo = open(arquivo, "r")
        self.__linha = 0
        self.__mapa = dict()
        super().__init__()

    def __erro(self, msg: str):
        """ Retorna exceção """
        raise Exception(msg)

    def compilar(self):
        """ Verifica se existe algum problema no código. """
        erro = False

        while linha := self.__arquivo.readline():
            self.__linha += 1

            comandos = linha.split(SEP)
            if len(comandos) == 2 and not self.__mapa.get(comandos[0]):
                r, comando = comandos
                comando = comando.strip().replace(FIM_LINHA, "")
                self.__mapa[r] = comando
                comando_anterior = SEP

                if self.__linha == 1:
                    self.__start = r
            else:
                erro = True

            for palavra in comando.split():
                proximo_comando = self._ordem[comando_anterior]

                if isinstance(proximo_comando, str):
                    proximo_comando = {proximo_comando}

                if not palavra in proximo_comando:
                    if palavra.startswith(R) and comando_anterior is not R:
                        palavra = palavra[1:]

                        if not (palavra.isnumeric() or palavra is X):
                            erro = True
                            break
                        else:
                            palavra = R
                    else:
                        erro = True
                        break

                comando_anterior = palavra

            if erro:
                self.__erro(f"Sintaxe inválida: {palavra} na linha {self.__linha}")
        
        self.__arquivo.close()

    def __resultado(self, r_exec: str, valor_a: int):
        """ Interpreta o código

        Parameters
        ----------
        r_exec: str
            linha que será executada
        valor_a: int
            valor de A
        """
        resposta = 0

        if r_exec == f"{R}{X}":
            return resposta
        elif not self.__mapa.get(r_exec):
            self.__erro(f"{r_exec} não foi encontrado.")
        else:
            comandos = self.__mapa[r_exec].split()

            if comandos[0] == FACA:
                if comandos[1] == SUBTRAIR_A:
                    if valor_a > 0:
                        valor_a -= 1
                elif comandos[1] == ADICIONAR_B:
                    resposta = 1

                proximo = comandos[3]
            else:
                if valor_a == 0:
                    proximo = comandos[4]
                else:
                    proximo = comandos[7]

        return resposta + self.__resultado(proximo, valor_a)

    def executar(self, n: int):
        """ Executa o script informado

        Parameters
        ----------
        n: int
            valor de A
        """
        self.compilar()
        
        try:
            return self.__resultado(self.__start, n)
        except RecursionError:
            self.__erro("O código entrou em loop infinito")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Interpretador Máquina 2REG")

    parser.add_argument("--arquivo", "-a", help="Nome do arquivo com o caminho. Exemplo: ~/Documents/2reg.txt")
    parser.add_argument("-n", type=int, help="Valor de A que será testado")

    args = parser.parse_args()
    if args.arquivo and args.n:
        print("Resultado:", Compilador2Reg(args.arquivo).executar(args.n))
    else:
        print("Comando Inválido")
