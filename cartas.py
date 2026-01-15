# cartas.py
def obtener_mazo_oficial():
    pool = [
        {"nombre": "Crushing Arm", "cant": 2, "tipo": "CRIATURA", "defensa": 9, "img": "1.png","presa": True},
        {"nombre": "Grappling Tentacle", "cant": 2, "tipo": "CRIATURA", "defensa": 6, "img": "3.png","sube_marea": True,"presa": True},
        {"nombre": "Shield Arm", "cant": 2, "tipo": "CRIATURA", "defensa": 6, "img": "8.png"},
        {"nombre": "Slippery Arm", "cant": 2, "tipo": "CRIATURA", "defensa": 3, "img": "10.png","sube_marea": True,"no_hace_danio": True, "ambar_generado": 1},
        {"nombre": "Tenacious Arm", "cant": 2, "tipo": "CRIATURA", "defensa": 3, "img": "12.png","no_hace_danio": True, "ambar_generado": 1},
        {"nombre": "Lashing Tentacle", "cant": 2, "tipo": "CRIATURA", "defensa": 3, "img": "5.png","presa": True},

        {"nombre": "Beast of Dark Legend", "cant": 1, "tipo": "ACCION", "img": "13.png","sube_marea": True,"habilidad": "archivar",
        "valor": 1},
        {"nombre": "Behold Its Grandeur", "cant": 2, "tipo": "ACCION", "img": "14.png"},
        {"nombre": "Crimson Chuming", "cant": 1, "tipo": "ACCION", "img": "16.png","ambar_regalo":1, "sube_marea": True,"habilidad": "archivar",
        "valor": 1},
        {"nombre": "Defend the Keyraken!", "cant": 2, "tipo": "ACCION", "img": "18.png","ambar_regalo":1,"sube_marea": True},
        {"nombre": "Devour Whole", "cant": 3, "tipo": "ACCION", "img": "19.png"},
        {"nombre": "Drag to Your Doom", "cant": 1, "tipo": "ACCION", "img": "22.png","sube_marea": True,"habilidad": "forzar_marea_baja"},
        {"nombre": "Emergence", "cant": 2, "tipo": "ACCION", "img": "23.png","ambar_regalo":1},
        {"nombre": "Into the Abyss", "cant": 1, "tipo": "ACCION", "img": "25.png","ambar_regalo":1,"sube_marea": True,"habilidad": "forzar_marea_baja"},
        {"nombre": "Left in Its Wake", "cant": 1, "tipo": "ACCION", "img": "26.png","ambar_regalo":1,"sube_marea": True,"habilidad": "archivar",
        "valor": 1},
        {"nombre": "Preternatural Will", "cant": 3, "tipo": "ACCION", "img": "27.png","ambar_regalo":0,"sube_marea": True},
        {"nombre": "Race to the Surface", "cant": 3, "tipo": "ACCION", "img": "30.png","ambar_regalo":1},
        {"nombre": "The Evil in the Ranks", "cant": 3, "tipo": "ACCION", "img": "33.png","ambar_regalo":0,"sube_marea": True,"habilidad": "archivar",
        "valor": 1},
        {"nombre": "Tidal Troubel", "cant": 1, "tipo": "ACCION", "img": "34.png","ambar_regalo":1,"sube_marea": True,"habilidad": "forzar_marea_baja"},
        {"nombre": "Tide Down", "cant": 1, "tipo": "ACCION", "img": "35.png","ambar_regalo":1,"sube_marea": True,"habilidad": "archivar",
        "valor": 1},
        {"nombre": "Zealot's Revelation", "cant": 1, "tipo": "ACCION", "img": "36.png","ambar_regalo":0,"sube_marea": True},

        {"nombre": "Ascending Jet", "cant": 2, "tipo": "ARTEFACTO", "img": "37.png","ambar_regalo":0,"sube_marea": True},
        {"nombre": "Swift Current", "cant": 2, "tipo": "ARTEFACTO", "img": "39.png","ambar_regalo":2,"sube_marea": True},
        {"nombre": "Whirpool Eddy", "cant": 2, "tipo": "ARTEFACTO", "img": "41.png","ambar_regalo":1,"sube_marea": True},

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
