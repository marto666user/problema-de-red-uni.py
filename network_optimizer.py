import streamlit as st
import pulp


def resolver_red(
    puertos_necesarios,
    ancho_necesario,
    energia_max,
    costo_switch,
    costo_router,
    costo_servidor,
    puertos_switch,
    puertos_router,
    ancho_router,
    ancho_servidor,
    energia_switch,
    energia_router,
    energia_servidor,
    max_routers,
    min_servidores,
):

    prob = pulp.LpProblem(
        "Optimizacion_Red",
        pulp.LpMinimize
    )

    # Variables de decisión
    x1 = pulp.LpVariable(
        "Switches",
        lowBound=0,
        cat="Integer"
    )

    x2 = pulp.LpVariable(
        "Routers",
        lowBound=0,
        cat="Integer"
    )

    x3 = pulp.LpVariable(
        "Servidores",
        lowBound=0,
        cat="Integer"
    )

    # Función objetivo
    prob += (
        costo_switch * x1
        + costo_router * x2
        + costo_servidor * x3
    )

    # Restricciones
    prob += (
        puertos_switch * x1
        + puertos_router * x2
        >= puertos_necesarios
    ), "Puertos"

    prob += (
        ancho_router * x2
        + ancho_servidor * x3
        >= ancho_necesario
    ), "Ancho_Banda"

    prob += (
        energia_switch * x1
        + energia_router * x2
        + energia_servidor * x3
        <= energia_max
    ), "Energia"

    prob += x2 <= max_routers, "Max_Routers"
    prob += x3 >= min_servidores, "Min_Servidores"

    # Resolver
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


# ----------------------------
# INTERFAZ STREAMLIT
# ----------------------------

st.set_page_config(
    page_title="Optimizador de Red",
    page_icon="🌐",
    layout="wide"
)

st.title("🌐 Optimizador de Infraestructura de Red")
st.markdown(
    "Modificá los parámetros y encontrá la combinación de equipos de menor costo."
)

# Sidebar
with st.sidebar:

    st.header("📋 Requerimientos")

    puertos = st.number_input(
        "Puertos necesarios",
        min_value=1,
        value=494
    )

    ancho = st.number_input(
        "Ancho de banda requerido (Mbps)",
        min_value=1,
        value=3800
    )

    energia = st.number_input(
        "Energía máxima disponible (W)",
        min_value=1,
        value=700
    )

    st.divider()

    st.header("💲 Costos")

    costo_switch = st.number_input(
        "Costo por Switch",
        value=65
    )

    costo_router = st.number_input(
        "Costo por Router",
        value=150
    )

    costo_servidor = st.number_input(
        "Costo por Servidor",
        value=1200
    )

    st.divider()

    st.header("🔌 Capacidades")

    puertos_switch = st.number_input(
        "Puertos por Switch",
        value=24
    )

    puertos_router = st.number_input(
        "Puertos por Router",
        value=4
    )

    ancho_router = st.number_input(
        "Mbps por Router",
        value=500
    )

    ancho_servidor = st.number_input(
        "Mbps por Servidor",
        value=1000
    )

    st.divider()

    st.header("⚡ Consumo energético")

    energia_switch = st.number_input(
        "Watts por Switch",
        value=15
    )

    energia_router = st.number_input(
        "Watts por Router",
        value=20
    )

    energia_servidor = st.number_input(
        "Watts por Servidor",
        value=180
    )

    st.divider()

    st.header("🚦 Restricciones")

    max_routers = st.number_input(
        "Máximo de Routers",
        min_value=0,
        value=3
    )

    min_servidores = st.number_input(
        "Mínimo de Servidores",
        min_value=0,
        value=1
    )

# ----------------------------
# BOTÓN DE OPTIMIZACIÓN
# ----------------------------

if st.button("🚀 Optimizar", use_container_width=True):

    resultado = resolver_red(
        puertos,
        ancho,
        energia,
        costo_switch,
        costo_router,
        costo_servidor,
        puertos_switch,
        puertos_router,
        ancho_router,
        ancho_servidor,
        energia_switch,
        energia_router,
        energia_servidor,
        max_routers,
        min_servidores,
    )

    if resultado["estado"] == "Optimal":

        st.success("Se encontró una solución óptima.")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Switches",
            resultado["switches"]
        )

        c2.metric(
            "Routers",
            resultado["routers"]
        )

        c3.metric(
            "Servidores",
            resultado["servidores"]
        )

        st.metric(
            "💰 Costo Total",
            f"USD ${resultado['costo']:,.2f}"
        )

    else:

        st.error(
            f"No existe una solución factible. Estado: {resultado['estado']}"
        )

        st.info(
            "Probá aumentar la energía máxima, reducir los requerimientos o modificar los parámetros."
        )

# ----------------------------
# INFORMACIÓN DEL MODELO
# ----------------------------

with st.expander("📚 Ver modelo matemático"):

    st.latex(
        r"""
        \min Z =
        C_sx_1 + C_rx_2 + C_vx_3
        """
    )

    st.markdown(
        """
**Sujeto a:**

- Puertos:
  
  \[
  P_sx_1 + P_rx_2 \geq \text{Puertos requeridos}
  \]

- Ancho de banda:
  
  \[
  A_rx_2 + A_sx_3 \geq \text{Ancho requerido}
  \]

- Energía:
  
  \[
  E_sx_1 + E_rx_2 + E_vx_3 \leq \text{Energía máxima}
  \]

- Routers máximos:

  \[
  x_2 \leq \text{Máx Routers}
  \]

- Servidores mínimos:

  \[
  x_3 \geq \text{Mín Servidores}
  \]

Variables enteras:

\[
x_1,x_2,x_3 \in \mathbb{Z}^{+}
\]
"""
    )
