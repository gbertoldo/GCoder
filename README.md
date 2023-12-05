# GCoder

GCoder é uma interface gráfica em Python 2 para criação de operações de frasagem e torneamento simples.

Estrutura dos Widgets
Todo Widget a ser incorporado na interface gráfica deve derivar da classe abstrata GCoderFrame e implementar os seguintes métodos
    - @staticmethod
      getOperationLabel()
    -getFields(self)
    -setFields(self, fields)
    -getGCode(self)