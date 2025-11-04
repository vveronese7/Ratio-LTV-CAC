
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Função para calcular tempo médio de retenção
def tempo_medio_retencao(churn_rate):
    return 1 / churn_rate

# Função principal para simular os cenários
def simular_ltv_cac(ticket_medio, margem_completa, margem_sem_depreciacao,
                    churn_rate_mensal, capex_equipamento, custo_aquisicao_outros,
                    vida_util_meses):
    tempo_retencao = tempo_medio_retencao(churn_rate_mensal)

    # CACs
    cac_completo = capex_equipamento + custo_aquisicao_outros
    cac_amortizado = (capex_equipamento / vida_util_meses) * tempo_retencao + custo_aquisicao_outros
    cac_sem_capex = custo_aquisicao_outros

    # LTVs
    ltv_completo = ticket_medio * margem_completa * tempo_retencao
    ltv_sem_depreciacao = ticket_medio * margem_sem_depreciacao * tempo_retencao

    # Cálculo dos ratios
    resultados = {
        "Cenário": [
            "LTV Completo vs CAC Completo",
            "LTV MB Sem Deprec. vs CAC Completo",
            "LTV Completo vs CAC Amortizado",
            "LTV MB Sem Deprec. vs CAC Amortizado",
            "LTV Completo vs CAC sem CAPEX",
            "LTV MB Sem Deprec. vs CAC sem CAPEX"
        ],
        "LTV/CAC": [
            ltv_completo / cac_completo,
            ltv_sem_depreciacao / cac_completo,
            ltv_completo / cac_amortizado,
            ltv_sem_depreciacao / cac_amortizado,
            ltv_completo / cac_sem_capex,
            ltv_sem_depreciacao / cac_sem_capex
        ]
    }

    return pd.DataFrame(resultados)

# Interface Streamlit
st.title("Simulador de Cenários LTV/CAC")

st.markdown("### 📘 Fórmula do LTV")
st.markdown("O cálculo do Lifetime Value (LTV) utilizado neste simulador é:")
st.latex(r"LTV = Ticket\ Médio\ Mensal \times Margem\ Bruta \times \left( \frac{1}{Churn\ Rate\ Mensal} \right)")
st.markdown("""
**Onde:**
- **Ticket Médio Mensal**: valor médio pago pelo cliente por mês.
- **Margem Bruta**: pode considerar ou não a depreciação dos equipamentos.
- **Churn Rate Mensal**: taxa de cancelamento mensal dos clientes.
""")

st.sidebar.header("Parâmetros de Entrada")
ticket_medio = st.sidebar.number_input("Ticket médio mensal (R$)", value=500.0)
margem_completa = st.sidebar.slider(
    "Margem bruta completa (%)", 
    0.00, 1.00, 0.50, step=0.0001, format="%.4f"
)
margem_sem_depreciacao = st.sidebar.slider(
    "Margem bruta sem depreciação (%)", 
    0.00, 1.00, 0.60, step=0.0001, format="%.4f"
)

churn_rate_mensal = st.sidebar.slider(
    "Churn rate mensal (%)", 
    0.0001, 0.5000, 0.0300, step=0.0001, format="%.4f"
)
capex_equipamento = st.sidebar.number_input("CAPEX do equipamento (R$)", value=3000.0)
custo_aquisicao_outros = st.sidebar.number_input("Outros custos de aquisição (R$)", value=500.0)
vida_util_meses = st.sidebar.number_input("Vida útil do equipamento (meses)", value=36)

# Simulação
df_resultados = simular_ltv_cac(ticket_medio, margem_completa, margem_sem_depreciacao,
                                churn_rate_mensal, capex_equipamento, custo_aquisicao_outros,
                                vida_util_meses)

st.subheader("Resultados da Simulação")
st.dataframe(df_resultados.style.format({"LTV/CAC": "{:.2f}"}))

# Gráfico
fig = go.Figure()
fig.add_trace(go.Bar(x=df_resultados["Cenário"], y=df_resultados["LTV/CAC"]))
fig.update_layout(title="Comparação de Cenários LTV/CAC",
                  xaxis_title="Cenário",
                  yaxis_title="Ratio LTV/CAC",
                  bargap=0.4)

st.plotly_chart(fig)
