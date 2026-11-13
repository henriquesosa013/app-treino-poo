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
            # Abre a janela onde o personal monta o treino do zero
            JanelaMontarTreino(self.janela, self.personal, aluno, self.mostrar)
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


# =========================================================
# JANELA PARA MONTAR UM TREINO PERSONALIZADO
# Os exercícios ficam numa lista temporária (rascunho).
# O Treino só é criado no envio, e é ELE que cria os
# Exercicios (composição), via adicionar_exercicio().
# =========================================================
class JanelaMontarTreino:

    def __init__(self, pai, personal, aluno, ao_enviar):
        self.personal = personal
        self.aluno = aluno
        self.ao_enviar = ao_enviar   # função da tela principal para mostrar o resultado
        self.rascunho = []           # lista de (nome, series, repeticoes, carga)

        self.janela = tk.Toplevel(pai)
        self.janela.title(f"Montar treino para {aluno.nome}")
        self.janela.geometry("520x480")
        self.janela.transient(pai)
        self.janela.grab_set()       # bloqueia a tela principal enquanto monta o treino

        tk.Label(self.janela, text=f"Novo treino para {aluno.nome}",
                 font=("Arial", 14, "bold")).pack(pady=8)

        # ---------- NOME DO TREINO ----------
        topo = tk.Frame(self.janela)
        topo.pack(fill="x", padx=10)
        tk.Label(topo, text="Nome do treino:").pack(side="left")
        self.nome_treino = tk.Entry(topo, width=35)
        self.nome_treino.pack(side="left", padx=5)
        self.nome_treino.focus()

        # ---------- FORMULÁRIO DO EXERCÍCIO ----------
        form = tk.LabelFrame(self.janela, text="Adicionar exercício", padx=10, pady=5)
        form.pack(fill="x", padx=10, pady=8)

        self.campos = {}
        rotulos = ["Exercício", "Séries", "Repetições", "Carga (kg)"]
        larguras = [20, 6, 6, 8]
        for i, (rotulo, largura) in enumerate(zip(rotulos, larguras)):
            tk.Label(form, text=rotulo).grid(row=0, column=i, sticky="w", padx=3)
            entrada = tk.Entry(form, width=largura)
            entrada.grid(row=1, column=i, padx=3)
            entrada.bind("<Return>", lambda evento: self.adicionar())  # Enter adiciona
            self.campos[rotulo] = entrada

        tk.Button(form, text="Adicionar", command=self.adicionar).grid(row=1, column=4, padx=5)

        # ---------- LISTA DE EXERCÍCIOS ----------
        tk.Label(self.janela, text="Exercícios do treino:").pack(anchor="w", padx=10)
        self.lista = tk.Listbox(self.janela, height=8)
        self.lista.pack(fill="both", expand=True, padx=10)

        # ---------- BOTÕES ----------
        botoes = tk.Frame(self.janela)
        botoes.pack(pady=10)
        tk.Button(botoes, text="Remover exercício", width=16,
                  command=self.remover).grid(row=0, column=0, padx=3)
        tk.Button(botoes, text="Enviar para o aluno", width=16,
                  command=self.enviar).grid(row=0, column=1, padx=3)
        tk.Button(botoes, text="Cancelar", width=16,
                  command=self.janela.destroy).grid(row=0, column=2, padx=3)

    # ------------------------------------------------------
    def ler_exercicio(self):
        nome = self.campos["Exercício"].get().strip()
        if not nome:
            raise ValueError("Informe o nome do exercício.")
        try:
            series = int(self.campos["Séries"].get())
            repeticoes = int(self.campos["Repetições"].get())
            carga = float(self.campos["Carga (kg)"].get().replace(",", "."))
        except ValueError:
            raise ValueError("Séries e repetições precisam ser inteiros e a carga um número.")
        if series <= 0 or repeticoes <= 0 or carga < 0:
            raise ValueError("Séries e repetições devem ser maiores que zero e a carga não pode ser negativa.")
        return nome, series, repeticoes, carga

    def adicionar(self):
        try:
            nome, series, repeticoes, carga = self.ler_exercicio()
            self.rascunho.append((nome, series, repeticoes, carga))
            self.lista.insert(tk.END, f"{nome}: {series}x{repeticoes}, {carga} kg")
            for entrada in self.campos.values():
                entrada.delete(0, tk.END)
            self.campos["Exercício"].focus()
        except ValueError as e:
            messagebox.showerror("Erro", str(e), parent=self.janela)

    def remover(self):
        selecao = self.lista.curselection()
        if not selecao:
            messagebox.showerror("Erro", "Selecione um exercício para remover.", parent=self.janela)
            return
        self.rascunho.pop(selecao[0])
        self.lista.delete(selecao[0])

    def enviar(self):
        try:
            nome = self.nome_treino.get().strip()
            if not nome:
                raise ValueError("Dê um nome para o treino (ex: Treino B - Costas).")
            if not self.rascunho:
                raise ValueError("Adicione pelo menos um exercício.")

            treino = Treino(nome, date.today())
            for exercicio in self.rascunho:
                treino.adicionar_exercicio(*exercicio)  # o Treino cria os Exercicios

            resultado = self.personal.enviar_treino(self.aluno, treino)
            self.ao_enviar(f"{resultado}\n\n{treino.listar_exercicios()}")
            self.janela.destroy()
        except ValueError as e:
            messagebox.showerror("Erro", str(e), parent=self.janela)


if __name__ == "__main__":
    janela = tk.Tk()
    TelaPrincipal(janela)
    janela.mainloop()
