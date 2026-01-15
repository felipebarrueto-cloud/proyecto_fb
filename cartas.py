# cartas.py
def obtener_mazo_oficial():
    pool = [
        {"nombre": "Crushing Arm", "cant": 2, "tipo": "CRIATURA", "defensa": 9, "img": "1.png", "efecto": "Destroyed: -3 HP al Jefe"},
        {"nombre": "Grappling Tentacle", "cant": 2, "tipo": "CRIATURA", "defensa": 6, "img": "3.png", "efecto": "Play: Captura recursos","sube_marea": True},
        {"nombre": "Shield Arm", "cant": 2, "tipo": "CRIATURA", "defensa": 6, "img": "8.png", "efecto": "Taunt"},
        {"nombre": "Slippery Arm", "cant": 2, "tipo": "CRIATURA", "defensa": 3, "img": "10.png", "efecto": "Taunt","sube_marea": True},
        {"nombre": "Tenacious Arm", "cant": 2, "tipo": "CRIATURA", "defensa": 3, "img": "12.png", "efecto": "Reap: Roba recursos"},
        {"nombre": "Lashing Tentacle", "cant": 2, "tipo": "CRIATURA", "defensa": 3, "img": "5.png", "efecto": "Skirmish"},

        {"nombre": "Beast of Dark Legend", "cant": 1, "tipo": "ACCION", "img": "13.png", "efecto": "Jefe gana 2 recursos por llave","sube_marea": True},
        {"nombre": "Behold Its Grandeur", "cant": 2, "tipo": "ACCION", "img": "14.png", "efecto": "Jefe gana 2 recursos por llave"},
        {"nombre": "Crimson Chuming", "cant": 1, "tipo": "ACCION", "img": "16.png", "efecto": "Jefe gana 2 recursos por llave","ambar_regalo":1, "sube_marea": True},
        {"nombre": "Defend the Keyraken!", "cant": 2, "tipo": "ACCION", "img": "18.png", "efecto": "Jefe gana 2 recursos por llave","ambar_regalo":1,"sube_marea": True},
        {"nombre": "Devour Whole", "cant": 3, "tipo": "ACCION", "img": "19.png", "efecto": "Jefe gana 2 recursos por llave"},
        {"nombre": "Drag to Your Doom", "cant": 1, "tipo": "ACCION", "img": "22.png", "efecto": "Jefe gana 2 recursos por llave","sube_marea": True},
        {"nombre": "Emergence", "cant": 2, "tipo": "ACCION", "img": "23.png", "efecto": "Jefe gana 2 recursos por llave","ambar_regalo":1},
        {"nombre": "Into the Abyss", "cant": 1, "tipo": "ACCION", "img": "25.png", "efecto": "Jefe gana 2 recursos por llave","ambar_regalo":1,"sube_marea": True},
        {"nombre": "Left in Its Wake", "cant": 1, "tipo": "ACCION", "img": "26.png", "efecto": "Jefe gana 2 recursos por llave","ambar_regalo":1},
        {"nombre": "Preternatural Will", "cant": 3, "tipo": "ACCION", "img": "27.png", "efecto": "Jefe gana 2 recursos por llave","ambar_regalo":0,"sube_marea": True},
        {"nombre": "Race to the Surface", "cant": 3, "tipo": "ACCION", "img": "30.png", "efecto": "Jefe gana 2 recursos por llave","ambar_regalo":1},
        {"nombre": "The Evil in the Ranks", "cant": 3, "tipo": "ACCION", "img": "33.png", "efecto": "Jefe gana 2 recursos por llave","ambar_regalo":0,"sube_marea": True},
        {"nombre": "Tidal Troubel", "cant": 1, "tipo": "ACCION", "img": "34.png", "efecto": "Jefe gana 2 recursos por llave","ambar_regalo":1,"sube_marea": True},
        {"nombre": "Tide Down", "cant": 1, "tipo": "ACCION", "img": "35.png", "efecto": "Jefe gana 2 recursos por llave","ambar_regalo":1,"sube_marea": True},
        {"nombre": "Zealot's Revelation", "cant": 1, "tipo": "ACCION", "img": "36.png", "efecto": "Jefe gana 2 recursos por llave","ambar_regalo":0,"sube_marea": True},

        {"nombre": "Ascending Jet", "cant": 2, "tipo": "ARTEFACTO", "img": "37.png", "efecto": "Jefe gana 2 recursos por llave","ambar_regalo":0,"sube_marea": True},
        {"nombre": "Swift Current", "cant": 2, "tipo": "ARTEFACTO", "img": "39.png", "efecto": "Jefe gana 2 recursos por llave","ambar_regalo":2,"sube_marea": True},
        {"nombre": "Whirpool Eddy", "cant": 2, "tipo": "ARTEFACTO", "img": "41.png", "efecto": "Jefe gana 2 recursos por llave","ambar_regalo":1,"sube_marea": True},

        {"nombre": "Crimson Chuming", "cant": 3, "tipo": "ACCION", "img": "14.png", "efecto": "Jefe gana 2 recursos por llave"},
        {"nombre": "Defend the Keyraken!", "cant": 3, "tipo": "ACCION", "img": "14.png", "efecto": "Jefe gana 2 recursos por llave"},
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
