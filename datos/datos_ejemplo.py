# Clinicas y datos de ejemplo del enunciado
# Incluye propietarios y mascotas de los casos de prueba para agilizar las demostraciones

CLINICAS_EJEMPLO = [
    {
        "nit": "901456789-1",
        "nombre": "Clínica Veterinaria Huellitas",
        "codigo_dane": "68679",
        "municipio": "San Gil",
        "departamento": "Santander",
        "direccion": "Calle 12 # 9-40",
        "barrio": "Centro",
        "veterinarios": [
            ("63512478", "Juliana Ortiz Ramírez", "TP-18452"),
            ("91254863", "Mauricio Pinzón Gómez", "TP-20117")
        ],
        "servicios": [
            ("CG", "Consulta general", 60000),
            ("VAC", "Vacunación", 45000),
            ("DES", "Desparasitación", 30000),
            ("PEL", "Baño y peluquería", 50000)
        ],
        "propietarios": [
            {
                "cedula": "1098765432",
                "nombre": "Laura Méndez Plata",
                "telefono": "3157894561",
                "municipio": "Bucaramanga",
                "mascotas": [
                    ("Rocky", "Perro", "Criolla", 2023, 18)
                ]
            },
            {
                "cedula": "1005678912",
                "nombre": "Camila Duarte Serrano",
                "telefono": "3204567812",
                "municipio": "San Gil",
                "mascotas": [
                    ("Copito", "Conejo", "Cabeza de león", 2025, 1.5)
                ]
            }
        ]
    },
    {
        "nit": "900987654-3",
        "nombre": "Clínica Veterinaria Patitas Felices",
        "codigo_dane": "68276",
        "municipio": "Floridablanca",
        "departamento": "Santander",
        "direccion": "Carrera 27 # 30-15",
        "barrio": "Cañaveral",
        "veterinarios": [
            ("13745821", "Sergio Arenas Villamizar", "TP-15893"),
            ("37896542", "Diana Carolina Rey Moreno", "TP-22406"),
            ("1098654321", "Felipe Castellanos Díaz", "TP-31578")
        ],
        "servicios": [
            ("CG", "Consulta general", 65000),
            ("VAC", "Vacunación", 48000),
            ("DES", "Desparasitación", 32000),
            ("ECO", "Ecografía", 120000)
        ],
        "propietarios": [
            {
                "cedula": "1102345678",
                "nombre": "Andrés Rueda Ardila",
                "telefono": "3016789023",
                "municipio": "Piedecuesta",
                "mascotas": [
                    ("Luna", "Gato", "Siamés", 2022, 4)
                ]
            }
        ]
    }
]
