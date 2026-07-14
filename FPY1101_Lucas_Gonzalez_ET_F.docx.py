"""Sistema de administración de productos y stock para PetMarket.

Evaluación Final Transversal - FPY1101 Fundamentos de Programación.

El programa usa dos diccionarios relacionados por el código de producto. Los
Diccionarios se crean en ``main`` y se pasan como argumentos a las funciones que
los necesitan; no se usan variables globales para almacenar los datos.
"""


def normalizar_codigo(codigo):
    """Retorna un código sin espacios externos y en mayúsculas."""
    return codigo.strip().upper()


def mostrar_menu():
    """Muestra las opciones disponibles del sistema."""
    print("\n========== MENÚ PRINCIPAL ==========")
    print("1. Unidades por categoría")
    print("2. Búsqueda de productos por rango de precio")
    print("3. Actualizar precio de producto")
    print("4. Agregar producto")
    print("5. Eliminar producto")
    print("6. Salir")
    print("=====================================")


def leer_opcion():
    """Solicita y retorna una opción entera válida entre 1 y 6."""
    while True:
        try:
            opcion = int(input("Ingrese opción: "))
            if 1 <= opcion <= 6:
                return opcion
            print("Debe seleccionar una opción válida")
        except ValueError:
            print("Debe seleccionar una opción válida")


def buscar_codigo(codigo, diccionario):
    """Retorna True si el código existe, sin distinguir mayúsculas/minúsculas."""
    codigo_buscado = normalizar_codigo(codigo)

    for codigo_existente in diccionario:
        if codigo_existente.upper() == codigo_buscado:
            return True

    return False


def unidades_categoria(categoria, productos, stock):
    """Muestra el total de unidades disponibles para una categoría."""
    categoria_buscada = categoria.strip().lower()
    total_unidades = 0

    for codigo, datos_producto in productos.items():
        categoria_producto = datos_producto[1]
        if categoria_producto.lower() == categoria_buscada and codigo in stock:
            total_unidades += stock[codigo][1]

    print(f"El total de unidades disponibles es: {total_unidades}")


def busqueda_precio(p_min, p_max, productos, stock):
    """Muestra productos con stock cuyo precio esté dentro del rango indicado."""
    encontrados = []

    for codigo, datos_stock in stock.items():
        precio = datos_stock[0]
        unidades = datos_stock[1]

        if p_min <= precio <= p_max and unidades != 0 and codigo in productos:
            nombre = productos[codigo][0]
            encontrados.append(f"{nombre}--{codigo}")

    encontrados.sort()

    if encontrados:
        print(f"Los productos encontrados son: {encontrados}")
    else:
        print("No hay productos en ese rango de precios.")


def actualizar_precio(codigo, nuevo_precio, stock):
    """Actualiza el precio y retorna True; retorna False si el código no existe."""
    codigo_normalizado = normalizar_codigo(codigo)

    if buscar_codigo(codigo_normalizado, stock):
        stock[codigo_normalizado][0] = nuevo_precio
        return True

    return False


def validar_codigo(codigo, productos, stock):
    """Valida que el código no esté vacío y no exista en los diccionarios."""
    if not isinstance(codigo, str) or not codigo.strip():
        return False

    return not buscar_codigo(codigo, productos) and not buscar_codigo(codigo, stock)


def validar_nombre(nombre):
    """Valida que el nombre sea texto no vacío."""
    return isinstance(nombre, str) and bool(nombre.strip())


def validar_categoria(categoria):
    """Valida que la categoría sea texto no vacío."""
    return isinstance(categoria, str) and bool(categoria.strip())


def validar_marca(marca):
    """Valida que la marca sea texto no vacío."""
    return isinstance(marca, str) and bool(marca.strip())


def validar_peso(peso_kg):
    """Valida que el peso sea numérico y mayor que cero."""
    return (
        isinstance(peso_kg, (int, float))
        and not isinstance(peso_kg, bool)
        and peso_kg > 0
    )


def validar_es_importado(respuesta):
    """Valida una respuesta 's' o 'n' para el campo es_importado."""
    return isinstance(respuesta, str) and respuesta.strip().lower() in ("s", "n")


def validar_es_para_cachorro(respuesta):
    """Valida una respuesta 's' o 'n' para el campo es_para_cachorro."""
    return isinstance(respuesta, str) and respuesta.strip().lower() in ("s", "n")


def validar_precio(precio):
    """Valida que el precio sea un entero mayor que cero."""
    return isinstance(precio, int) and not isinstance(precio, bool) and precio > 0


def validar_unidades(unidades):
    """Valida que las unidades sean un entero mayor o igual a cero."""
    return isinstance(unidades, int) and not isinstance(unidades, bool) and unidades >= 0


def convertir_respuesta_booleana(respuesta):
    """Convierte una respuesta válida 's'/'n' a True/False."""
    return respuesta.strip().lower() == "s"


def agregar_producto(
    codigo,
    nombre,
    categoria,
    marca,
    peso_kg,
    es_importado,
    es_para_cachorro,
    precio,
    unidades,
    productos,
    stock,
):
    """Agrega el producto en ambos diccionarios y retorna el resultado."""
    codigo_normalizado = normalizar_codigo(codigo)

    if buscar_codigo(codigo_normalizado, productos) or buscar_codigo(
        codigo_normalizado, stock
    ):
        return False

    productos[codigo_normalizado] = [
        nombre.strip(),
        categoria.strip(),
        marca.strip(),
        peso_kg,
        es_importado,
        es_para_cachorro,
    ]
    stock[codigo_normalizado] = [precio, unidades]
    return True


def eliminar_producto(codigo, productos, stock):
    """Elimina un producto de ambos diccionarios y retorna el resultado."""
    codigo_normalizado = normalizar_codigo(codigo)

    if buscar_codigo(codigo_normalizado, productos) and buscar_codigo(
        codigo_normalizado, stock
    ):
        del productos[codigo_normalizado]
        del stock[codigo_normalizado]
        return True

    return False


def solicitar_rango_precios():
    """Solicita un rango válido y retorna una tupla (mínimo, máximo)."""
    while True:
        try:
            p_min = int(input("Ingrese precio mínimo: "))
            p_max = int(input("Ingrese precio máximo: "))
        except ValueError:
            print("Debe ingresar valores enteros")
            continue

        if p_min < 0 or p_max < 0 or p_min > p_max:
            print(
                "El precio mínimo y máximo deben ser mayores o iguales a cero, "
                "y el mínimo no puede superar al máximo"
            )
            continue

        return p_min, p_max


def solicitar_entero_positivo(mensaje):
    """Solicita y retorna un número entero mayor que cero."""
    while True:
        try:
            valor = int(input(mensaje))
        except ValueError:
            print("Debe ingresar un número entero mayor que cero")
            continue

        if validar_precio(valor):
            return valor

        print("Debe ingresar un número entero mayor que cero")


def solicitar_respuesta_sn(mensaje):
    """Solicita y retorna una respuesta válida 's' o 'n'."""
    while True:
        respuesta = input(mensaje).strip().lower()
        if respuesta in ("s", "n"):
            return respuesta
        print("Debe responder con 's' o 'n'")


def procesar_agregar_producto(productos, stock):
    """Solicita, valida y agrega un producto desde la opción 4 del menú."""
    codigo = input("Ingrese código del producto: ")
    nombre = input("Ingrese nombre: ")
    categoria = input("Ingrese categoría: ")
    marca = input("Ingrese marca: ")
    peso_texto = input("Ingrese peso (kg): ")
    importado_texto = input("¿Es importado? (s/n): ")
    cachorro_texto = input("¿Es para cachorro? (s/n): ")
    precio_texto = input("Ingrese precio: ")
    unidades_texto = input("Ingrese unidades: ")

    try:
        peso_kg = float(peso_texto)
    except ValueError:
        peso_kg = None

    try:
        precio = int(precio_texto)
    except ValueError:
        precio = None

    try:
        unidades = int(unidades_texto)
    except ValueError:
        unidades = None

    codigo_valido = validar_codigo(codigo, productos, stock)
    if not codigo_valido:
        if not codigo.strip():
            print("El código no puede estar vacío")
        else:
            print("El código ya existe")
        return

    validaciones = [
        (validar_nombre(nombre), "El nombre no puede estar vacío"),
        (validar_categoria(categoria), "La categoría no puede estar vacía"),
        (validar_marca(marca), "La marca no puede estar vacía"),
        (validar_peso(peso_kg), "El peso debe ser un número mayor que cero"),
        (
            validar_es_importado(importado_texto),
            "La respuesta de importación debe ser 's' o 'n'",
        ),
        (
            validar_es_para_cachorro(cachorro_texto),
            "La respuesta para cachorro debe ser 's' o 'n'",
        ),
        (validar_precio(precio), "El precio debe ser un entero mayor que cero"),
        (
            validar_unidades(unidades),
            "Las unidades deben ser un entero mayor o igual a cero",
        ),
    ]

    for es_valido, mensaje_error in validaciones:
        if not es_valido:
            print(mensaje_error)
            return

    es_importado = convertir_respuesta_booleana(importado_texto)
    es_para_cachorro = convertir_respuesta_booleana(cachorro_texto)

    agregado = agregar_producto(
        codigo,
        nombre,
        categoria,
        marca,
        peso_kg,
        es_importado,
        es_para_cachorro,
        precio,
        unidades,
        productos,
        stock,
    )

    if agregado:
        print("Producto agregado")
    else:
        print("El código ya existe")


def main():
    """Programa principal de PetMarket."""
    productos = {
        "M001": ["Alimento Premium", "comida", "DogPlus", 10, True, False],
        "M002": ["Arena Aglomerante", "higiene", "CatClean", 8, False, False],
        "M003": ["Snack Dental", "snack", "BiteJoy", 1, True, True],
        "M004": ["Shampoo Suave", "higiene", "PetCare", 0.5, False, True],
        "M005": ["Correa Nylon", "accesorio", "WalkPro", 0.3, True, False],
        "M006": ["Cama Mediana", "accesorio", "CozyPet", 2, False, False],
    }

    stock = {
        "M001": [32990, 12],
        "M002": [9990, 0],
        "M003": [5490, 25],
        "M004": [7990, 5],
        "M005": [11990, 7],
        "M006": [24990, 3],
    }

    programa_activo = True

    while programa_activo:
        mostrar_menu()
        opcion = leer_opcion()

        if opcion == 1:
            categoria = input("Ingrese categoría a consultar: ")
            unidades_categoria(categoria, productos, stock)

        elif opcion == 2:
            p_min, p_max = solicitar_rango_precios()
            busqueda_precio(p_min, p_max, productos, stock)

        elif opcion == 3:
            continuar_actualizando = "s"

            while continuar_actualizando == "s":
                codigo = input("Ingrese código del producto: ")
                nuevo_precio = solicitar_entero_positivo("Ingrese nuevo precio: ")

                actualizado = actualizar_precio(codigo, nuevo_precio, stock)
                if actualizado:
                    print("Precio actualizado")
                else:
                    print("El código no existe")

                continuar_actualizando = solicitar_respuesta_sn(
                    "¿Desea actualizar otro precio (s/n)?: "
                )

        elif opcion == 4:
            procesar_agregar_producto(productos, stock)

        elif opcion == 5:
            codigo = input("Ingrese código del producto a eliminar: ")
            eliminado = eliminar_producto(codigo, productos, stock)

            if eliminado:
                print("Producto eliminado")
            else:
                print("El código no existe")

        else:
            programa_activo = False
            print("Programa finalizado.")


if __name__ == "__main__":
    main()
