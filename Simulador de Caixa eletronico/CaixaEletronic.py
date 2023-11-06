class CaixaEletronico:
    def __init__(self):
        self.saldo = 0.0  # Inicialize o saldo como 0

    def depositar(self, money):
        self.saldo += money
        print("Valor Depositado foi:", self.saldo)

    def sacar(self, money):
        if self.saldo >= money:
            self.saldo -= money
            print("Valor Sacado foi:", money)
        else:
            print("Saldo Insuficiente")

    def vizualizarsaldo(self):
        print("Saldo Atual:", self.saldo)

