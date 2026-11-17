import random


def calcular_dano(ataque, defesa, critico=False):
    dano = max(1, ataque - defesa)
    if critico:
        dano = dano * 2
    return dano


def aplicar_dano(vida, dano):
    return max(0, vida - dano)


def curar(vida, vida_max, cura=30):
    return min(vida_max, vida + cura)


def barra_de_vida(vida, vida_max, tamanho=10):
    quantidade = vida * tamanho // vida_max
    barra = ""
    for i in range(tamanho):
        if i < quantidade:
            barra += "#"
        else:
            barra += "-"
    return f"[{barra}] {vida}/{vida_max}"


def classificar_resultado(vida, vida_max):
    if vida == 0:
        return "Derrota"
    elif vida == vida_max:
        return "Vitória perfeita"
    elif vida >= vida_max / 2:
        return "Vitória"
    else:
        return "Vitória apertada"


def ler_acao():
    while True:
        print("1 - Atacar   2 - Tomar poção   3 - Fugir")
        acao = input("Escolha: ").strip()
        if acao in ("1", "2", "3"):
            return acao
        print("Ação inválida!")


def batalha(heroi, inimigo, pocoes=3):
    turno = 0
    while heroi["vida"] > 0 and inimigo["vida"] > 0:
        turno = turno + 1
        print(f"\n--- Turno {turno} ---")
        print(f"{heroi['nome']:<12} {barra_de_vida(heroi['vida'], heroi['vida_max'])}")
        print(f"{inimigo['nome']:<12} {barra_de_vida(inimigo['vida'], inimigo['vida_max'])}")

        acao = ler_acao()
        if acao == "1":
            critico = random.randint(1, 10) == 10
            dano = calcular_dano(heroi["ataque"], inimigo["defesa"], critico)
            inimigo["vida"] = aplicar_dano(inimigo["vida"], dano)
            if critico:
                print(f"Golpe crítico! Você causou {dano} de dano.")
            else:
                print(f"Você causou {dano} de dano.")
        elif acao == "2":
            if pocoes > 0:
                pocoes -= 1
                heroi["vida"] = curar(heroi["vida"], heroi["vida_max"])
                print(f"Você usou uma poção. Restam {pocoes}.")
            else:
                print("Você não tem mais poções!")
        else:
            print(f"{heroi['nome']} fugiu da batalha!")
            return {"resultado": "fuga", "turnos": turno,
                    "vida_restante": heroi["vida"], "pocoes": pocoes}

        if inimigo["vida"] > 0:
            dano = calcular_dano(inimigo["ataque"], heroi["defesa"])
            heroi["vida"] = aplicar_dano(heroi["vida"], dano)
            print(f"{inimigo['nome']} causou {dano} de dano.")

    if heroi["vida"] > 0:
        resultado = "vitoria"
    else:
        resultado = "derrota"
    print("\n" + classificar_resultado(heroi["vida"], heroi["vida_max"]) + "!")
    return {"resultado": resultado, "turnos": turno,
            "vida_restante": heroi["vida"], "pocoes": pocoes}


if __name__ == "__main__":
    heroi = {"nome": "Gork", "vida": 100, "vida_max": 100, "ataque": 18, "defesa": 5}
    inimigo = {"nome": "Goblin", "vida": 60, "vida_max": 60, "ataque": 12, "defesa": 3}
    final = batalha(heroi, inimigo)
    print(final)
