from CaixaEletronic import CaixaEletronico

def main():
    caixa = CaixaEletronico()  
    e = True
    while e:
        c = int(input("Digite\n(1)-Depositar\n(2)-Sacar\n(3)-Visualizar Status\n(4)-sair: "))
        if c == 1:
            money = float(input("Digite o Valor a Ser depositado: "))
            caixa.depositar(money)
        elif c == 2:
            money = float(input("Digite o Valor a Ser Sacado: "))
            caixa.sacar(money)
        elif c == 3:
            caixa.vizualizarsaldo()
        else:
            e = False
            print("Saiu")

if __name__ == '__main__':
    main()
