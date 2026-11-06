from abc import ABC, abstractmethod
from datetime import date


# =========================================================
# CLASSE ABSTRATA
# =========================================================
class Pessoa(ABC):

    def __init__(self, nome: str, email: str, idade: int):
        self.nome = nome
        self._email = email
        self._idade = idade

    @abstractmethod
    def exibir_perfil(self):
        pass

    def get_email(self):
        return self._email


# =========================================================
# HERANÇA: Aluno é uma Pessoa
# AGREGAÇÃO: Aluno TEM treinos, mas o Treino existe sem o Aluno
#            (ele é criado fora e só é "entregue" ao aluno)
# =========================================================
class Aluno(Pessoa):

    def __init__(self, nome: str, email: str, idade: int, peso: float, objetivo: str):
        super().__init__(nome, email, idade)
        self._peso = peso
        self._objetivo = objetivo
        self._treinos = []

    def exibir_perfil(self):
        return f"Aluno: {self.nome} | Idade: {self._idade} | Peso: {self._peso} kg | Objetivo: {self._objetivo}"

    def pedir_treino(self):
        return f"{self.nome} solicitou um treino."

    def receber_treino(self, treino):
        # O Personal usa este método em vez de mexer direto em aluno._treinos
        self._treinos.append(treino)

    def ver_treino(self):
        if not self._treinos:
            raise ValueError(f"{self.nome} não possui nenhum treino cadastrado.")
        return "\n\n".join(treino.listar_exercicios() for treino in self._treinos)

    def registrar_carga(self, exercicio, carga: float):
        exercicio.carga = carga
        return f"Carga de {exercicio.nome} atualizada para {carga} kg."


# =========================================================
# HERANÇA: Personal é uma Pessoa
# AGREGAÇÃO: Personal TEM uma lista de alunos, mas os alunos
#            continuam existindo se o personal for removido
# =========================================================
class Personal(Pessoa):

    def __init__(self, nome: str, email: str, idade: int, cref: str):
        super().__init__(nome, email, idade)
        self._cref = cref
        self._alunos = []  # LISTA DE ALUNOS

    def exibir_perfil(self):
        return f"Personal: {self.nome} | Idade: {self._idade} | CREF: {self._cref}"

    def adicionar_aluno(self, aluno):
        if aluno in self._alunos:
            raise ValueError(f"{aluno.nome} já é aluno de {self.nome}.")
        self._alunos.append(aluno)
        return f"{aluno.nome} agora é aluno de {self.nome}."

    def remover_aluno(self, aluno):
        if aluno not in self._alunos:
            raise ValueError(f"{aluno.nome} não é aluno de {self.nome}.")
        self._alunos.remove(aluno)
        return f"{aluno.nome} foi removido da lista de {self.nome}."

    def enviar_treino(self, aluno, treino):
        if aluno not in self._alunos:
            self.adicionar_aluno(aluno)
        aluno.receber_treino(treino)
        return f"Treino '{treino.nome}' enviado para {aluno.nome}."

    def listar_alunos(self):
        if not self._alunos:
            raise ValueError("Nenhum aluno cadastrado.")
        return "\n".join(f"- {aluno.exibir_perfil()}" for aluno in self._alunos)


# =========================================================
# COMPOSIÇÃO: o Treino CRIA os próprios exercícios.
#             O Exercicio só existe dentro do Treino;
#             se o Treino for apagado, os exercícios somem junto.
# =========================================================
class Treino:

    def __init__(self, nome: str, data: date):
        self.nome = nome
        self._data = data
        self._exercicios = []

    def adicionar_exercicio(self, nome: str, series: int, repeticoes: int, carga: float):
        exercicio = Exercicio(nome, series, repeticoes, carga)  # criado AQUI DENTRO
        self._exercicios.append(exercicio)
        return exercicio

    def buscar_exercicio(self, nome: str):
        for exercicio in self._exercicios:
            if exercicio.nome.lower() == nome.lower():
                return exercicio
        raise ValueError(f"Exercício '{nome}' não encontrado no treino '{self.nome}'.")

    def listar_exercicios(self):
        if not self._exercicios:
            raise ValueError(f"O treino '{self.nome}' não possui exercícios.")
        lista = "\n".join(f"  • {exercicio.descricao()}" for exercicio in self._exercicios)
        return f"Treino: {self.nome} | Data: {self._data.strftime('%d/%m/%Y')}\n{lista}"


class Exercicio:

    def __init__(self, nome: str, series: int, repeticoes: int, carga: float):
        self.nome = nome
        self.series = series
        self.repeticoes = repeticoes
        self.carga = carga

    def descricao(self):
        return f"{self.nome}: {self.series} séries de {self.repeticoes} repetições, {self.carga} kg"
