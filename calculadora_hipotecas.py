import pandas as pd
import numpy_financial as npf
import matplotlib.pyplot as plt


def solicitar_datos():
    """
    Solicita los datos de la hipoteca al usuario de forma segura.
    Devuelve el capital, la tasa de interés anual y el plazo en años.
    """
    print("--- Calculadora de Hipotecas ---")
    capital = solicitar_dato_numerico("Ingrese el capital del préstamo: ")
    interes_anual = solicitar_dato_numerico("Ingrese la tasa de interés anual (%): ")
    plazo_anios = int(solicitar_dato_numerico("Ingrese el plazo en años: "))
    return capital, interes_anual, plazo_anios


def solicitar_dato_numerico(mensaje):
    """Solicita un valor numérico y valida que sea un número positivo."""
    while True:
        try:
            valor = float(input(mensaje))
            if valor > 0:
                return valor
            else:
                print("Error: El valor debe ser un número positivo.")
        except ValueError:
            print("Error: Por favor, introduce un número válido.")


def calcular_y_generar_tabla(capital, interes_anual, plazo_anios):
    """
    Calcula la cuota, los intereses y genera la tabla de amortización.
    Devuelve la cuota mensual y la tabla (DataFrame).
    """
    tasa_interes_mensual = interes_anual / 100 / 12
    numero_pagos = plazo_anios * 12

    # Usamos npf.pmt para consistencia con el resto de la librería
    cuota_mensual = npf.pmt(tasa_interes_mensual, numero_pagos, -capital)

    periodos = range(1, numero_pagos + 1)
    intereses_pagados = npf.ipmt(tasa_interes_mensual, periodos, numero_pagos, -capital)
    capital_pagado = npf.ppmt(tasa_interes_mensual, periodos, numero_pagos, -capital)

    tabla = pd.DataFrame({
        "Mes": periodos,
        "Cuota Mensual": cuota_mensual,
        "Pago Capital": capital_pagado,
        "Pago Intereses": intereses_pagados,
    })
    tabla["Saldo Restante"] = capital - tabla["Pago Capital"].cumsum()

    # Aseguramos que el último saldo sea exactamente 0
    tabla.loc[tabla.index[-1], 'Saldo Restante'] = 0

    return cuota_mensual, tabla.round(2)


def mostrar_resultados(cuota_mensual, tabla):
    """Muestra los resultados principales y la tabla de amortización."""
    total_pagado = tabla["Cuota Mensual"].sum()
    total_intereses = tabla["Pago Intereses"].sum()

    print("\n--- RESUMEN DEL PRÉSTAMO ---")
    print(f"Cuota mensual: ${cuota_mensual:.2f}")
    print(f"Total pagado durante la vida del préstamo: ${total_pagado:.2f}")
    print(f"Total de intereses pagados: ${total_intereses:.2f}")
    print("\n--- Tabla de Amortización (primeros y últimos 5 meses) ---")
    print(tabla.head())
    print("...")
    print(tabla.tail())


def graficar_saldo(tabla):
    """Genera y muestra un gráfico de la evolución del saldo."""
    plt.style.use('ggplot')
    plt.figure(figsize=(10, 6))
    plt.plot(tabla["Mes"], tabla["Saldo Restante"], label="Saldo Restante", color='blue')
    plt.title("Evolución del Saldo del Préstamo")
    plt.xlabel("Mes")
    plt.ylabel("Saldo Restante ($)")
    plt.grid(True)
    plt.legend()
    plt.show()


def main():
    """Función principal que ejecuta el programa en un bucle."""
    while True:
        capital, interes_anual, plazo_anios = solicitar_datos()
        cuota_mensual, tabla_amortizacion = calcular_y_generar_tabla(capital, interes_anual, plazo_anios)
        mostrar_resultados(cuota_mensual, tabla_amortizacion)

        # Preguntar si se quiere ver el gráfico
        ver_grafico = input("¿Deseas ver el gráfico de la evolución del saldo? (s/n): ").lower()
        if ver_grafico == 's':
            graficar_saldo(tabla_amortizacion)

        # Preguntar si se quiere hacer otro cálculo
        otro_calculo = input("\n¿Deseas realizar otro cálculo? (s/n): ").lower()
        if otro_calculo != 's':
            print("Gracias por usar la calculadora. ¡Hasta pronto!")
            break


# Punto de entrada del programa
if __name__ == "__main__":
    main()
