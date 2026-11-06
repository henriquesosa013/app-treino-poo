import tkinter as tk
from tkinter import messagebox

from classes import *


class TelaPrincipal:

    def __init__(self, janela):
        self.janela = janela
        self.janela.title("App de Treino")
        self.janela.geometry("640x560")

        # Personal fixo do sistema
        self.personal = Personal("Carlos", "carlos@gym.com", 35, "123456-G/SP")
        self.alunos = []  # todos os alunos criados (existem mesmo fora do personal)

        # ---------- TÍTULO ----------
        tk.Label(janela, text="App de Treino", font=("Arial", 18, "bold")).pack(pady=8)
        tk.Label(janela, text=self.personal.exibir_perfil()).pack()

        # ---------- FORMULÁRIO DE CADASTRO ----------
        form = tk.LabelFrame(janela, text="Cadastrar aluno", padx=10, pady=5)
        form.pack(fill="x", padx=10, pady=8)

        self.campos = {}
        for i, campo in enumerate(["Nome", "Email", "Idade", "Peso", "Objetivo"]):
            tk.Label(form, text=campo).grid(row=i, column=0, sticky="w")
            entrada = tk.Entry(form, width=40)
            entrada.grid(row=i, column=1, pady=2)
            self.campos[campo] = entrada

        tk.Button(form, text="Cadastrar e adicionar ao personal",
                  command=self.cadastrar_aluno).grid(row=5, column=0, columnspan=2, pady=5)

        # ---------- LISTA DE ALUNOS ----------
        tk.Label(janela, text="Alunos (selecione um):").pack(anchor="w", padx=10)
        self.lista = tk.Listbox(janela, height=4)
        self.lista.pack(fill="x", padx=10)

        # ---------- BOTÕES ----------
        botoes = tk.Frame(janela)
        botoes.pack(pady=8)
        tk.Button(botoes, text="Listar alunos", width=14, command=self.listar_alunos).grid(row=0, column=0, padx=3)
        tk.Button(botoes, text="Enviar treino", width=14, command=self.enviar_treino).grid(row=0, column=1, padx=3)
        tk.Button(botoes, text="Ver treino", width=14, command=self.ver_treino).grid(row=0, column=2, padx=3)
        tk.Button(botoes, text="Remover aluno", width=14, command=self.remover_aluno).grid(row=0, column=3, padx=3)

        # ---------- SAÍDA ----------
        self.saida = tk.Text(janela, height=10, state="disabled")
        self.saida.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    # ======================================================
    # FUNÇÕES AUXILIARES
    # ======================================================
    def mostrar(self, texto):
        self.saida.config(state="normal")
        self.saida.delete("1.0", tk.END)
        self.saida.insert(tk.END, texto)
        self.saida.config(state="disabled")

    def aluno_selecionado(self):
        selecao = self.lista.curselection()
        if not selecao:
            raise ValueError("Selecione um aluno na lista.")
        return self.alunos[selecao[0]]

    # ======================================================
    # AÇÕES DOS BOTÕES (os erros viram uma janela de alerta)
    # ======================================================
    def cadastrar_aluno(self):
        try:
            try:
                idade = int(self.campos["Idade"].get())
                peso = float(self.campos["Peso"].get())
            except ValueError:
                raise ValueError("Idade e peso precisam ser números.")

            aluno = Aluno(
                self.campos["Nome"].get(),
                self.campos["Email"].get(),
                idade,
                peso,
                self.campos["Objetivo"].get(),
            )
            self.mostrar(self.personal.adicionar_aluno(aluno))
            self.alunos.append(aluno)
            self.lista.insert(tk.END, aluno.nome)
            for entrada in self.campos.values():
                entrada.delete(0, tk.END)
        except ValueError as e:
            messagebox.showerror("Erro", str(e))

    def listar_alunos(self):
        try:
            self.mostrar(self.personal.listar_alunos())
        except ValueError as e:
            messagebox.showerror("Erro", str(e))

    def enviar_treino(self):
        try:
            aluno = self.aluno_selecionado()
            treino = Treino("Treino A - Peito", date.today())
            treino.adicionar_exercicio("Supino reto", 4, 10, 40.0)
            treino.adicionar_exercicio("Crucifixo", 3, 12, 14.0)
            self.mostrar(self.personal.enviar_treino(aluno, treino))
        except ValueError as e:
            messagebox.showerror("Erro", str(e))

    def ver_treino(self):
        try:
            self.mostrar(self.aluno_selecionado().ver_treino())
        except ValueError as e:
            messagebox.showerror("Erro", str(e))

    def remover_aluno(self):
        try:
            self.mostrar(self.personal.remover_aluno(self.aluno_selecionado()))
        except ValueError as e:
            messagebox.showerror("Erro", str(e))


if __name__ == "__main__":
    janela = tk.Tk()
    TelaPrincipal(janela)
    janela.mainloop()
