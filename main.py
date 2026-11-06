from classes import *


def main():
    print("=== CADASTRO ===")
    personal = Personal("Carlos", "carlos@gym.com", 35, "123456-G/SP")
    aluno1 = Aluno("Henrique", "henrique@email.com", 20, 75.0, "Hipertrofia")
    aluno2 = Aluno("Maria", "maria@email.com", 22, 60.0, "Emagrecimento")

    print(personal.exibir_perfil())
    print(aluno1.exibir_perfil())
    print(aluno2.exibir_perfil())

    print("\n=== LISTA DE ALUNOS ===")
    try:
        print(personal.listar_alunos())          # vazia
    except ValueError as e:
        print(f"[ERRO] {e}")

    print(personal.adicionar_aluno(aluno1))
    print(personal.adicionar_aluno(aluno2))

    try:
        print(personal.adicionar_aluno(aluno1))  # duplicado
    except ValueError as e:
        print(f"[ERRO] {e}")

    print(personal.listar_alunos())

    print("\n=== TREINO (COMPOSIÇÃO) ===")
    print(aluno1.pedir_treino())
    treino_a = Treino("Treino A - Peito", date.today())
    treino_a.adicionar_exercicio("Supino reto", 4, 10, 40.0)
    treino_a.adicionar_exercicio("Crucifixo", 3, 12, 14.0)
    print(treino_a.listar_exercicios())

    print("\n=== ENVIO (AGREGAÇÃO) ===")
    print(personal.enviar_treino(aluno1, treino_a))
    print(aluno1.ver_treino())

    try:
        print(aluno2.ver_treino())               # sem treino
    except ValueError as e:
        print(f"[ERRO] {e}")

    print("\n=== REGISTRAR CARGA ===")
    supino = treino_a.buscar_exercicio("supino reto")
    print(aluno1.registrar_carga(supino, 45.0))
    print(aluno1.ver_treino())

    print("\n=== REMOVER ALUNO ===")
    print(personal.remover_aluno(aluno2))
    print(personal.listar_alunos())
    print(aluno2.exibir_perfil())                # aluna continua existindo (agregação)


if __name__ == "__main__":
    main()
