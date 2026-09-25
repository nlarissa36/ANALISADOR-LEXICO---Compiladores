# 🔎 Analisador Léxico

Projeto desenvolvido para a disciplina de **Compiladores**, utilizando **Python**, com o objetivo de implementar um analisador léxico para código-fonte Java.

## 📌 Funcionalidades

O analisador reconhece:

* Palavras-chave
* Identificadores
* Números inteiros e reais
* Caracteres e strings
* Operadores aritméticos, relacionais, lógicos e de atribuição
* Delimitadores
* Comentários `//` e `/* */`
* Erros léxicos
* Tabela de símbolos
* Dois ponteiros (`begin` e `forward`)
* Dois buffers de 4096 caracteres

## Tecnologias

* Python 3.13+
* Java (arquivos utilizados nos testes)

## Como executar

Clone o repositório e entre na pasta do projeto:

```bash
git clone URL_DO_REPOSITORIO
cd trabalho_compiladores
```

Execute o analisador informando um arquivo `.java`:

```bash
python analisador_lexico.py exemplo_sucesso.java
```

##  Exemplos de testes

### Código válido

```bash
python analisador_lexico.py exemplo_sucesso.java
```

### Comentários

```bash
python analisador_lexico.py exemplo_comentarios.java
```

### Erros léxicos

```bash
python analisador_lexico.py exemplo_erro.java
```

### Operadores

```bash
python analisador_lexico.py exemplo_testeop.java
```

### Teste dos buffers

```bash
python analisador_lexico.py teste_buffers.java
```



**Larissa do Nascimento Vieira**

Projeto acadêmico — **Disciplina de Compiladores**.
