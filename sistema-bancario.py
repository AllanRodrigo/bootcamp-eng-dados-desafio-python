from abc import ABC, abstractmethod
from datetime import datetime

class Cliente:
    
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
        
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)
    
class PessoaFisica(Cliente):
    
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

class Transacao(ABC):
    
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass
    
class Deposito(Transacao):
    
    def __init__(self, valor):        
        self._valor = valor
        
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)
    
class Saque(Transacao):
    
    def __init__(self, valor):        
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)

class Historico():
    
    def __init__(self):
        self._transacoes = []
        
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now()
            }
        )

class Conta:
    
    def __init__(self, agencia, numero, cliente):
        self._agencia = agencia
        self._numero = numero
        self._cliente = cliente
        self._saldo = 0
        self._historico = Historico()
    
    @classmethod
    def nova_conta(cls, agencia, numero, cliente):
        return cls(agencia, numero, cliente)
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        if valor <= 0:
            print("\nValor do saque precisa ser maior que zero.")
        elif self._saldo < valor:
            print("\nSaldo insuficiente para saque.")
        else:
            self._saldo -= valor
            print("\nSaque realizado com sucesso")
            return True
        
        return False
    
    def depositar(self, valor):
        if valor <= 0:
            print("\nValor do deposito precisa ser maior que zero.")
        else:
            self._saldo += valor
            print("\nDeposito realizado com sucesso")
            return True
        
        return False

class ContaCorrente(Conta):
    
    def __init__(self, agencia, numero, cliente, limite=500, limite_saque=3):
        super().__init__(agencia, numero, cliente)
        
        self._limite = limite
        self._limite_saque = limite_saque
    
    @property
    def limite(self):
        return self._limite
    
    @property
    def limite_saque(self):
        return self._limite_saque
    
    def sacar(self, valor):
        saques_dia = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == "Saque"])
        
        if saques_dia >= self.limite_saque:
            print(f"\nJá foi realizado o limite de Saques diários: {self.limite_saque}")
        elif valor > self.limite:
            print(f"\nJá foi atingido o limite em valor de Saques diários: R$ {self.limite:.2f}")
        else:
            return super().sacar(valor)
        
        return False

    def __str__(self):
        return f"""\
            Agência: {self.agencia}
                C/C: {self.numero}
                Cpf: {self.cliente.cpf}
               Nome: {self.cliente.nome}
        """
        
class Main:
    
    def inicializar(self):
        clientes = []
        contas = []
        
        while True:

            opcao = self.exibir_menu()

            if opcao == "1":
                self.novo_cliente(clientes)

            elif opcao == "2":
                self.nova_conta(contas, clientes)

            elif opcao == "3":
                self.listar_contas(contas)
            
            elif opcao == "4":
                self.sacar(contas, clientes)
            
            elif opcao == "5":
                self.depositar(contas, clientes)
            
            elif opcao == "6":
                self.visualizar_extrato(clientes)

            elif opcao == "7":
                break

            else:
                print("Operação inválida, por favor selecione novamente a operação desejada.")
    
    
    def exibir_menu(self):
        menu = """

        ##### SISTEMA BANCÁRIO ALLAN S.A #####

            [1] Nova Cliente
            [2] Nova Conta
            [3] Listar Contas
            [4] Sacar
            [5] Depositar
            [6] Visualizar Extrato
            [7] Sair

        => """
        
        return input(menu)

    def validar_cliente(self, clientes):
        cpf = input("Informe o CPF: ")
        
        filtro_cliente = self.filtro_cliente(clientes, cpf)
        
        if not filtro_cliente:
            print("\Cliente não tem cadastro no Banco")
        
        return filtro_cliente
    
    def validar_conta(self, contas, numero_conta, cpf=""):
        if cpf == "":
            cpf = input("Informe o CPF: ")
        
        filtro_conta = self.filtro_contas(contas, numero_conta)
        
        if not filtro_conta:
            print("\Conta não encontrada")
        
        return filtro_conta
    
    def filtro_cliente(self, clientes, cpf):
        filtro_clientes = [cliente for cliente in clientes if cliente.cpf == cpf]
        
        return filtro_clientes[0] if filtro_clientes else None
    
    def filtro_contas(self, contas, numero_conta):
        filtro_contas = [conta for conta in contas if conta.numero == numero_conta]
        
        return filtro_contas[0] if filtro_contas else None

    def novo_cliente(self, clientes):
        cpf = input("Informe o CPF: ")
        
        valida_existe = self.filtro_cliente(clientes, cpf)
        
        if valida_existe:
            print("\Cliente já cadastrado no Banco")
        else:
            nome = input("Informe o nome: ")
            data_nascimento = input("Informe a data de nascimento: ")
            endereco = input("Informe o endereço: ")
            
            cliente = PessoaFisica(cpf, nome, data_nascimento, endereco)
            clientes.append(cliente)
            
            print("\Cliente cadastrado com sucesso!!!")
    
    def nova_conta(self, contas, clientes):
        filtro_cliente = self.validar_cliente(clientes)
        if not filtro_cliente:
            return
        
        numero_agencia = input("Informe o número da agência: ")
        numero_conta = input("Informe o número da conta: ")
        
        existe_conta = len([conta for conta in contas if conta.agencia == numero_agencia and conta.numero == numero_conta])
        
        if existe_conta > 0:
            print("\Agência e Conta informada já está em uso")
            return
        
        nova_conta = ContaCorrente.nova_conta(numero_agencia, numero_conta, filtro_cliente)
        
        contas.append(nova_conta)
        filtro_cliente.contas.append(nova_conta)
        
        print("\Conta cadastrada com sucesso!!!")

    def listar_contas(self, contas):
        for conta in contas:
            print("*" * 50)
            print(conta)
    
    def sacar(self, contas, clientes):
        filtro_cliente = self.validar_cliente(clientes)
        if not filtro_cliente:
            return
        
        print("\##### Informe o número da conta desejada #####")
        self.listar_contas(filtro_cliente.contas)
        numero_conta = input("=>")
        
        filtro_conta = self.validar_conta(contas, numero_conta, cpf=filtro_cliente.cpf)
        if not filtro_conta:
            return
        
        valor = float(input("Informe o valor do saque: "))
        filtro_cliente.realizar_transacao(filtro_conta, Saque(valor))
        
    def depositar(self, contas, clientes):
        filtro_cliente = self.validar_cliente(clientes)
        if not filtro_cliente:
            return
        
        print("\##### Informe o número da conta desejada #####")
        self.listar_contas(filtro_cliente.contas)
        numero_conta = input("=>")
        
        filtro_conta = self.validar_conta(contas, numero_conta, cpf=filtro_cliente.cpf)
        if not filtro_conta:
            return
        
        valor = float(input("Informe o valor do deposito: "))
        filtro_cliente.realizar_transacao(filtro_conta, Deposito(valor))
        
    def visualizar_extrato(self, clientes):
        filtro_cliente = self.validar_cliente(clientes)
        if not filtro_cliente:
            return
        
        print("\##### EXTRATOS #####")
        for conta in filtro_cliente.contas:
            print(conta)
            
            transacoes = conta.historico.transacoes
            
            extrato = ""
            if not transacoes:
                extrato = "Nenhum extrato para exibição."
            else:
                for transacao in transacoes:
                    extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"
            
            print(extrato)
            print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
            print("\n##### FIM-EXTRATOS #####\n\n")
        
    
Main().inicializar()