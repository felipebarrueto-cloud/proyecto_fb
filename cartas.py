# cartas.py
def obtener_mazo_oficial():
    pool = [
        {"nombre": "Crushing Arm", "cant": 2, "tipo": "CRIATURA", "defensa": 9, "img": "1.png", "efecto": "Destroyed: -3 HP al Jefe"},
        {"nombre": "Grappling Tentacle", "cant": 2, "tipo": "CRIATURA", "defensa": 6, "img": "3.png", "efecto": "Play: Captura recursos"},
        {"nombre": "Shield Arm", "cant": 2, "tipo": "CRIATURA", "defensa": 6, "img": "8.png", "efecto": "Taunt"},
        {"nombre": "Slippery Arm", "cant": 2, "tipo": "CRIATURA", "defensa": 3, "img": "10.png", "efecto": "Taunt"},
        {"nombre": "Tenacious Arm", "cant": 2, "tipo": "CRIATURA", "defensa": 3, "img": "12.png", "efecto": "Reap: Roba recursos"},
        {"nombre": "Lashing Tentacle", "cant": 2, "tipo": "CRIATURA", "defensa": 3, "img": "5.png", "efecto": "Skirmish"},

        {"nombre": "Beast of Dark Legend", "cant": 3, "tipo": "ACCION", "img": "14.png", "efecto": "Jefe gana 2 recursos por llave"},
        {"nombre": "Crimson Chuming", "cant": 3, "tipo": "ACCION", "img": "14.png", "efecto": "Jefe gana 2 recursos por llave"},
        # ... (todas las demás cartas hasta sumar 43)
    ]
    mazo = []
    for c in pool:
        for _ in range(c["cant"]):
            nueva = c.copy()
            del nueva["cant"]
            mazo.append(nueva)
    import random
    random.shuffle(mazo)
    return mazo
