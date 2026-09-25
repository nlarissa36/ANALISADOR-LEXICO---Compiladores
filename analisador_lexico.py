import sys

# PALAVRAS-CHAVE DA LINGUAGEM JAVA

PALAVRAS_CHAVE = {
    "public",
    "private",
    "protected",
    "static",
    "class",
    "void",
    "int",
    "float",
    "double",
    "char",
    "boolean",
    "if",
    "else",
    "while",
    "for",
    "return",
    "new",
    "this",
    "true",
    "false",
    "null",
    "break",
    "continue",
}

# OPERADORES


OPERADORES = {
    "==": "OPERADOR_RELACIONAL",
    "!=": "OPERADOR_RELACIONAL",
    "<=": "OPERADOR_RELACIONAL",
    ">=": "OPERADOR_RELACIONAL",

    "&&": "OPERADOR_LOGICO",
    "||": "OPERADOR_LOGICO",

    "+=": "OPERADOR_ATRIBUICAO",
    "-=": "OPERADOR_ATRIBUICAO",
    "*=": "OPERADOR_ATRIBUICAO",
    "/=": "OPERADOR_ATRIBUICAO",
    "%=": "OPERADOR_ATRIBUICAO",

    "+": "OPERADOR_ARITMETICO",
    "-": "OPERADOR_ARITMETICO",
    "*": "OPERADOR_ARITMETICO",
    "/": "OPERADOR_ARITMETICO",
    "%": "OPERADOR_ARITMETICO",

    "<": "OPERADOR_RELACIONAL",
    ">": "OPERADOR_RELACIONAL",

    "!": "OPERADOR_LOGICO",

    "=": "OPERADOR_ATRIBUICAO",
}


# DELIMITADORES

DELIMITADORES = {
    ";",
    ",",
    ".",
    "(",
    ")",
    "{",
    "}",
    "[",
    "]",
}


# SISTEMA DE DOIS BUFFERS

class DoisBuffers:

    def __init__(self, codigo, tamanho_buffer=4096):

        self.codigo = codigo
        self.tamanho_buffer = tamanho_buffer

        # Dois buffers
        self.buffer_a = ""
        self.buffer_b = ""

        self.inicio_buffer_a = 0
        self.inicio_buffer_b = tamanho_buffer

        # Carrega inicialmente os dois buffers
        self.carregar_buffer_a()
        self.carregar_buffer_b()

    # Carrega o Buffer A

    def carregar_buffer_a(self):

        inicio = self.inicio_buffer_a

        fim = inicio + self.tamanho_buffer

        self.buffer_a = self.codigo[inicio:fim]

    # Carrega o Buffer B

    def carregar_buffer_b(self):

        inicio = self.inicio_buffer_b

        fim = inicio + self.tamanho_buffer

        self.buffer_b = self.codigo[inicio:fim]

    # Retorna um caractere através dos dois buffers

    def obter_caractere(self, posicao):

        if posicao < 0 or posicao >= len(self.codigo):

            return None

        # Verifica se a posição está no Buffer A

        if (
            self.inicio_buffer_a
            <= posicao
            < self.inicio_buffer_a + self.tamanho_buffer
        ):

            indice = posicao - self.inicio_buffer_a

            if indice < len(self.buffer_a):

                return self.buffer_a[indice]


        # Verifica se a posição está no Buffer B

        if (
            self.inicio_buffer_b
            <= posicao
            < self.inicio_buffer_b + self.tamanho_buffer
        ):

            indice = posicao - self.inicio_buffer_b

            if indice < len(self.buffer_b):

                return self.buffer_b[indice]

        # Caso a posição esteja além dos buffers atuais,
        # alternamos os buffers.

        numero_buffer = posicao // self.tamanho_buffer

        if numero_buffer % 2 == 0:

            self.inicio_buffer_a = (
                numero_buffer * self.tamanho_buffer
            )

            self.carregar_buffer_a()

            indice = (
                posicao - self.inicio_buffer_a
            )

            if indice < len(self.buffer_a):

                return self.buffer_a[indice]

        else:

            self.inicio_buffer_b = (
                numero_buffer * self.tamanho_buffer
            )

            self.carregar_buffer_b()

            indice = (
                posicao - self.inicio_buffer_b
            )

            if indice < len(self.buffer_b):

                return self.buffer_b[indice]

        return None

# ANALISADOR LÉXICO

class AnalisadorLexico:

    def __init__(self, codigo):

        self.codigo = codigo

        # DOIS BUFFERS

        self.buffers = DoisBuffers(codigo)

        # DOIS PONTEIROS

        self.begin = 0
        self.forward = 0

        # Posição atual durante a leitura
        self.posicao = 0

        # Lista de tokens
        self.tokens = []

        # Tabela de símbolos
        self.tabela_simbolos = {}

    # Adiciona token


    def adicionar_token(self, tipo, lexema, atributo=None):

        self.tokens.append({
            "tipo": tipo,
            "lexema": lexema,
            "atributo": atributo
        })


    # Adiciona identificador à tabela de símbolos


    def adicionar_simbolo(self, identificador):

        if identificador in self.tabela_simbolos:

            self.tabela_simbolos[identificador] += 1

        else:

            self.tabela_simbolos[identificador] = 1


    # Verifica se ainda existem caracteres


    def ainda_tem_caractere(self):

        return self.posicao < len(self.codigo)


    # Retorna o caractere na posição atual
    # usando os dois buffers


    def caractere_atual(self):

        return self.buffers.obter_caractere(
            self.posicao
        )

    # Lookahead:
    # olha o próximo caractere sem avançar
 

    def olhar_proximo(self):

        return self.buffers.obter_caractere(
            self.posicao + 1
        )


    # Avança o forward pointer


    def avancar(self):

        if self.posicao < len(self.codigo):

            self.posicao += 1

            # forward acompanha a posição atual
            self.forward = self.posicao

    # Obtém lexema usando begin e forward


    def obter_lexema(self):

        return self.codigo[self.begin:self.forward]


    # ANÁLISE LÉXICA


    def analisar(self):

        tamanho = len(self.codigo)

        while self.posicao < tamanho:

            caractere = self.caractere_atual()

        
            # ESPAÇOS EM BRANCO
          

            if caractere.isspace():

                self.avancar()

                self.begin = self.posicao

                continue

      
            # IDENTIFICADORES E PALAVRAS-CHAVE
       

            if caractere.isalpha() or caractere == "_":

                self.begin = self.posicao

                self.avancar()

                while self.posicao < tamanho:

                    atual = self.caractere_atual()

                    if atual.isalnum() or atual == "_":

                        self.avancar()

                    else:

                        break

                self.forward = self.posicao

                lexema = self.obter_lexema()

                if lexema in PALAVRAS_CHAVE:

                    self.adicionar_token(
                        "PALAVRA_CHAVE",
                        lexema,
                        lexema
                    )

                else:

                    self.adicionar_token(
                        "IDENTIFICADOR",
                        lexema,
                        lexema
                    )

                    self.adicionar_simbolo(lexema)

                continue

          
            # STRING
         

            if caractere == '"':

                self.begin = self.posicao

                self.avancar()

                string_fechada = False

                while self.posicao < tamanho:

                    atual = self.caractere_atual()

                    # Caractere de escape
                    if atual == "\\":

                        self.avancar()

                        if self.posicao < tamanho:

                            self.avancar()

                        continue

                    # Fechamento da string
                    if atual == '"':

                        self.avancar()

                        string_fechada = True

                        break

                    # Quebra de linha antes de fechar
                    if atual == "\n":

                        break

                    self.avancar()

                self.forward = self.posicao

                lexema = self.obter_lexema()

                if string_fechada:

                    self.adicionar_token(
                        "STRING",
                        lexema,
                        lexema
                    )

                else:

                    self.adicionar_token(
                        "ERROR",
                        lexema,
                        "String não terminada"
                    )

                continue

        
            # CARACTERE
          

            if caractere == "'":

                self.begin = self.posicao

                self.avancar()

                caractere_fechado = False

                while self.posicao < tamanho:

                    atual = self.caractere_atual()

                    # Escape
                    if atual == "\\":

                        self.avancar()

                        if self.posicao < tamanho:

                            self.avancar()

                        continue

                    # Fechamento
                    if atual == "'":

                        self.avancar()

                        caractere_fechado = True

                        break

                    # Quebra de linha
                    if atual == "\n":

                        break

                    self.avancar()

                self.forward = self.posicao

                lexema = self.obter_lexema()

                if caractere_fechado:

                    self.adicionar_token(
                        "CARACTERE",
                        lexema,
                        lexema
                    )

                else:

                    self.adicionar_token(
                        "ERROR",
                        lexema,
                        "Caractere não terminado"
                    )

                continue

      
            # NÚMEROS
    

            if caractere.isdigit():

                self.begin = self.posicao

                # Parte inteira
                while self.posicao < tamanho:

                    atual = self.caractere_atual()

                    if atual.isdigit():

                        self.avancar()

                    else:

                        break

         
                # Identificador começando por número
                # Exemplo: 2idade
            

                if self.posicao < tamanho:

                    atual = self.caractere_atual()

                    if atual.isalpha() or atual == "_":

                        while self.posicao < tamanho:

                            atual = self.caractere_atual()

                            if atual.isalnum() or atual == "_":

                                self.avancar()

                            else:

                                break

                        self.forward = self.posicao

                        lexema = self.obter_lexema()

                        self.adicionar_token(
                            "ERROR",
                            lexema,
                            "Identificador inválido: não pode começar com número"
                        )

                        continue

            
                # Número decimal com vírgula
                # Exemplo: 3,14
              

                if self.posicao < tamanho:

                    atual = self.caractere_atual()

                    proximo = self.olhar_proximo()

                    if atual == "," and proximo is not None and proximo.isdigit():

                        self.avancar()

                        while self.posicao < tamanho:

                            atual = self.caractere_atual()

                            if atual.isdigit():

                                self.avancar()

                            else:

                                break

                        self.forward = self.posicao

                        lexema = self.obter_lexema()

                        self.adicionar_token(
                            "ERROR",
                            lexema,
                            "Número real inválido: use ponto em vez de vírgula"
                        )

                        continue

              
                # Número real com ponto
              

                if self.posicao < tamanho:

                    atual = self.caractere_atual()

                    proximo = self.olhar_proximo()

                    if (
                        atual == "."
                        and proximo is not None
                        and proximo.isdigit()
                    ):

                        self.avancar()

                        while self.posicao < tamanho:

                            atual = self.caractere_atual()

                            if atual.isdigit():

                                self.avancar()

                            else:

                                break

                        self.forward = self.posicao

                        lexema = self.obter_lexema()

                        self.adicionar_token(
                            "REAL",
                            lexema,
                            float(lexema)
                        )

                    else:

                        self.forward = self.posicao

                        lexema = self.obter_lexema()

                        self.adicionar_token(
                            "INTEIRO",
                            lexema,
                            int(lexema)
                        )

                else:

                    self.forward = self.posicao

                    lexema = self.obter_lexema()

                    self.adicionar_token(
                        "INTEIRO",
                        lexema,
                        int(lexema)
                    )

                continue

         
            # COMENTÁRIO DE UMA LINHA
          

            if (
                caractere == "/"
                and self.olhar_proximo() == "/"
            ):

                self.avancar()
                self.avancar()

                while self.posicao < tamanho:

                    atual = self.caractere_atual()

                    if atual == "\n":

                        break

                    self.avancar()

                self.begin = self.posicao

                continue

          
            # COMENTÁRIO DE VÁRIAS LINHAS
         

            if (
                caractere == "/"
                and self.olhar_proximo() == "*"
            ):

                self.begin = self.posicao

                self.avancar()
                self.avancar()

                comentario_fechado = False

                while self.posicao < tamanho:

                    atual = self.caractere_atual()

                    proximo = self.olhar_proximo()

                    if atual == "*" and proximo == "/":

                        self.avancar()
                        self.avancar()

                        comentario_fechado = True

                        break

                    self.avancar()

                self.forward = self.posicao

                if not comentario_fechado:

                    self.adicionar_token(
                        "ERROR",
                        self.obter_lexema(),
                        "Comentário não terminado"
                    )

                self.begin = self.posicao

                continue

           
            # OPERADORES DE DOIS CARACTERES
          

            if self.olhar_proximo() is not None:

                dois_caracteres = (
                    caractere + self.olhar_proximo()
                )

                if dois_caracteres in OPERADORES:

                    self.begin = self.posicao

                    self.avancar()
                    self.avancar()

                    self.forward = self.posicao

                    self.adicionar_token(
                        OPERADORES[dois_caracteres],
                        dois_caracteres,
                        dois_caracteres
                    )

                    continue

           
            # OPERADORES DE UM CARACTERE
        

            if caractere in OPERADORES:

                self.begin = self.posicao

                self.avancar()

                self.forward = self.posicao

                self.adicionar_token(
                    OPERADORES[caractere],
                    caractere,
                    caractere
                )

                continue

        
            # DELIMITADORES
        

            if caractere in DELIMITADORES:

                self.begin = self.posicao

                self.avancar()

                self.forward = self.posicao

                self.adicionar_token(
                    "DELIMITADOR",
                    caractere,
                    caractere
                )

                continue

    
            # ERRO LÉXICO
            

            self.begin = self.posicao

            self.avancar()

            self.forward = self.posicao

            self.adicionar_token(
                "ERROR",
                caractere,
                "Caractere inválido"
            )

        return self.tokens



# LEITURA DO ARQUIVO


def ler_arquivo(nome_arquivo):

    with open(
        nome_arquivo,
        "r",
        encoding="utf-8"
    ) as arquivo:

        return arquivo.read()



# MOSTRAR TABELA DE TOKENS

def mostrar_tokens(tokens):

    print()

    print("=" * 75)
    print("TABELA DE TOKENS")
    print("=" * 75)

    print(
        f"{'TIPO':<25}"
        f"{'LEXEMA':<25}"
        f"{'ATRIBUTO'}"
    )

    print("-" * 75)

    for token in tokens:

        atributo = token["atributo"]

        if atributo is None:

            atributo = "-"

        print(
            f"{token['tipo']:<25}"
            f"{token['lexema']:<25}"
            f"{atributo}"
        )

    print("=" * 75)


# MOSTRAR TABELA DE SÍMBOLOS


def mostrar_tabela_simbolos(tabela):

    print()

    print("=" * 50)
    print("TABELA DE SÍMBOLOS")
    print("=" * 50)

    print(
        f"{'IDENTIFICADOR':<30}"
        f"{'OCORRÊNCIAS'}"
    )

    print("-" * 50)

    for identificador, quantidade in tabela.items():

        print(
            f"{identificador:<30}"
            f"{quantidade}"
        )

    print("=" * 50)



# FUNÇÃO PRINCIPAL


def main():

    if len(sys.argv) != 2:

        print(
            "Uso: python analisador_lexico.py arquivo.java"
        )

        return

    nome_arquivo = sys.argv[1]

    try:

        codigo = ler_arquivo(nome_arquivo)

        analisador = AnalisadorLexico(codigo)

        tokens = analisador.analisar()

        print()

        print("=" * 50)
        print("CÓDIGO-FONTE")
        print("=" * 50)

        print(codigo)

        print("=" * 50)

        mostrar_tokens(tokens)

        mostrar_tabela_simbolos(
            analisador.tabela_simbolos
        )

    except FileNotFoundError:

        print(
            f"ERRO: arquivo não encontrado: {nome_arquivo}"
        )

    except Exception as erro:

        print(
            f"ERRO ao analisar o arquivo: {erro}"
        )



# EXECUÇÃO


if __name__ == "__main__":

    main()