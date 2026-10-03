import time

from ocr.ocr import ejecutar_ocr


def main():
    print("Primera prueba:")
    inicio = time.perf_counter()

    resultado = ejecutar_ocr("horario.jpeg")

    tiempo = time.perf_counter() - inicio
    print(f"Resultados: {len(resultado)}")
    print(f"Tiempo: {tiempo:.2f} segundos")


if __name__ == "__main__":
    main()