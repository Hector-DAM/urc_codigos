# Estadística Multivariada

# Progrmando la media de la varibale i

import ast, numpy as np

while True:
  # Esto no es mas que un menu para la selección de lo que se desea hacer, conforme avanzemos se agregaran mas opciones
    print("Bienvenido al calculador de medias aritmeticas en multivariada, por favor elige una opción")
    print("1. Calcular la media de unos datos \n2. Salir")

    try:
        n = int(input("Inserte la opción deseada:\n"))

        if n == 1:
            print("Antes de iniciar, verifica que tus vectores tengan la misma cantidad de datos")
            pre_lista = input("Insera los valores de tu matriz con el formato [[a,b,c,d....,z], [a1,b1,c1,d1,...,z1],....,[an,bn,cn,dn,....,dn]]:Ejemplo [1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15]\n")
            # Por como funciona los comandos y librerias usadas pedimos que los datos tengan la forma mencionada en el jemplo, de esta forma podemos proceder con el calculo de la media
            # Esto considerando que tenemos datos timpios y que se encuentran de la forma solicitada, de ser el caso contrario se haría un proceso de limpiea y acomodo de los datos

            lista = ast.literal_eval(pre_lista)
            # Con este comando convertimos la cadena que contiene muestras listas en una lista con listas, la cual puede se convertida en una matriz
            # Con el comando de np.array convertimos nuestra lista de listas en una matriz mientras que con np.mean calculamos la media de cada una de las columnas de nuestra matriz
            A = np.array(lista)
            media_multivariada = np.mean(A, axis=0)

            print("Las variables quedaron de la siguiente forma:")
            for i in range(len(lista)):
                print(f"Variable: {i}, Valores: {A[:,i]}")

            media_desada = int(input("Selecciona la variable que deseas calcular la media:\n"))

            print(f"La media de la variable {media_desada} es {media_multivariada[media_desada]}")

        elif n == 2:
            break

    except ValueError:
        print("No es un valor valido")