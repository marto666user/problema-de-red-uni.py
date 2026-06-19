import streamlit as st
import pulp


def resolver_red(puertos_necesarios, ancho_necesario, energia_max):
    prob = pulp.LpProblem("Universidad_Min_Costo", pulp.LpMinimize)

    x1 = pulp.LpVariable("Switches", lowBound=0, cat="Integer")
    x2 = pulp.LpVariable("Routers", lowBound=0, cat="Integer")
    x3 = pulp.LpVariable("Servidores", lowBound=0, cat="Integer")

    # Función objetivo
    prob += 65 * x1 + 150 * x2 + 1200 * x3

    # Restricciones
    prob += 24 * x1 + 4 * x2 >= puertos_necesarios
    prob += 500 * x2 + 1000 * x3 >= ancho_necesario
    prob += 15 * x1 + 20 * x2 + 180 * x3 <= energia_max
    prob += x2 <= 3
    prob += x3 >= 1

    prob.solve(pulp.PULP_CBC_CMD(msg=0))

    estado = pulp.LpStatus[prob.status]

    if estado == "Optimal":
        return {
            "estado": estado,
            "costo": pulp.value(prob.objective),
            "switches": int(x1.varValue),
            "routers": int(x2.varValue),
            "servidores": int(x3.varValue),
        }

    return {"estado": estado}


# Interfaz Streamlit
st.set_page_config(
    page_title="Optimizador de Red Universitaria",
    page_icon="🌐",
    layout="centered"
)

st.title("🌐 Optimizador de Red Universitaria")
st.markdown(
    "Calcula la combinación de equipos de menor costo que cumple "
    "los requerimientos de la red."
)

with st.sidebar:
    st.header("Parámetros")

    puertos = st.number_input(
        "Puertos necesarios",
        min_value=1,
        value=494,
        step=1
    )

    ancho = st.number_input(
        "Ancho de banda requerido (Mbps)",
        min_value=100,
        value=3800,
        step=100
    )

    energia = st.number_input(
        "Energía máxima disponible (W)",
        min_value=100,
        value=700,
        step=50
    )

if st.button("Optimizar", type="primary"):
    resultado = resolver_red(puertos, ancho, energia)

    if resultado["estado"] == "Optimal":
        st.success("Solución óptima encontrada")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Switches 24p",
            resultado["switches"]
        )

        col2.metric(
            "Routers ONT",
            resultado["routers"]
        )

        col3.metric(
            "Servidores 1U",
            resultado["servidores"]
        )

        st.metric(
            "Costo Total",
            f"USD ${resultado['costo']:,.2f}"
        )

    else:
        st.error(
            f"No existe solución factible. Estado: {resultado['estado']}"
        )

        st.info(
            "Probá aumentar la energía máxima o reducir los requerimientos."
        )

st.divider()

st.subheader("Modelo utilizado")

st.latex(
    r"\min Z = 65x_1 + 150x_2 + 1200x_3"
)

st.markdown("""
Sujeto a:

- \(24x_1 + 4x_2 \geq\) Puertos requeridos
- \(500x_2 + 1000x_3 \geq\) Ancho de banda requerido
- \(15x_1 + 20x_2 + 180x_3 \leq\) Energía máxima
- \(x_2 \leq 3\)
- \(x_3 \geq 1\)
- Variables enteras
""")
