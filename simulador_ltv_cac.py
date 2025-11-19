
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

st.markdown("### 📘 Fórmula do CAC Amortizado")
st.markdown("O cálculo do CAC Amortizado utilizado neste simulador é:")
st.latex(r"CAC_{amortizado} = \left( \frac{CAPEX\ do\ Equipamento}{Vida\ Útil\ (meses)} \times Tempo\ Médio\ de\ Retenção \right) + Outros\ Custos\ de\ Aquisição")
st.markdown("""
**Onde:**
- **CAPEX do Equipamento**: custo total do equipamento instalado.
- **Vida Útil (meses)**: período em que o equipamento é depreciado.
- **Tempo Médio de Retenção**: calculado como 1 / Churn Rate Mensal.
- **Outros Custos de Aquisição**: marketing, vendas, etc.
""")

st.sidebar.header("Parâmetros de Entrada")

ticket_medio = st.sidebar.number_input("Ticket médio mensal (R$)", value=500.0)

margem_completa = st.sidebar.number_input(
    "Margem bruta completa (%)", 
    min_value=0.00, max_value=100.00, value=50.00, step=0.01
) / 100  # Converte para decimal

margem_sem_depreciacao = st.sidebar.number_input(
    "Margem bruta sem depreciação (%)", 
    min_value=0.00, max_value=100.00, value=60.00, step=0.01
) / 100  # Converte para decimal

churn_rate_mensal = st.sidebar.number_input(
    "Churn rate mensal (%)", 
    min_value=0.01, max_value=50.00, value=3.00, step=0.01
) / 100  # Converte para decimal

# Calcula tempo médio de retenção
tempo_retencao = 1 / churn_rate_mensal

# Calcula LTV com margem completa
ltv_completo = ticket_medio * margem_completa * tempo_retencao

# Calcula LTV sem depreciação
ltv_sem_depreciacao = ticket_medio * margem_sem_depreciacao * tempo_retencao

# Exibe no sidebar
st.sidebar.markdown(f"**Tempo Médio de Retenção:** {tempo_retencao:.2f} meses")
st.sidebar.markdown(f"**LTV (com depreciação):** R$ {ltv_completo:,.2f}")
st.sidebar.markdown(f"**LTV (sem depreciação):** R$ {ltv_sem_depreciacao:,.2f}")

capex_equipamento = st.sidebar.number_input("CAPEX do equipamento (R$)", value=3000.0)
custo_aquisicao_outros = st.sidebar.number_input("Outros custos de aquisição (R$)", value=500.0)
vida_util_meses = st.sidebar.number_input("Vida útil do equipamento (meses)", value=36)

# Calcula CACs
cac_completo = capex_equipamento + custo_aquisicao_outros
cac_amortizado = (capex_equipamento / vida_util_meses) * tempo_retencao + custo_aquisicao_outros
cac_sem_capex = custo_aquisicao_outros

# Exibe no sidebar
st.sidebar.markdown("### 📊 Valores Calculados")
st.sidebar.markdown(f"**CAC Completo:** R$ {cac_completo:,.2f}")
st.sidebar.markdown(f"**CAC Amortizado:** R$ {cac_amortizado:,.2f}")
st.sidebar.markdown(f"**CAC sem CAPEX:** R$ {cac_sem_capex:,.2f}")

# Simulação
df_resultados = simular_ltv_cac(ticket_medio, margem_completa, margem_sem_depreciacao,
                                churn_rate_mensal, capex_equipamento, custo_aquisicao_outros,
                                vida_util_meses)

st.subheader("Resultados da Simulação")
st.dataframe(df_resultados.style.format({"LTV/CAC": "{:.2f}"}))

# Gráfico
fig = go.Figure()
fig.add_trace(go.Bar(x=df_resultados["Cenário"], y=df_resultados["LTV/CAC"],
                        textposition="outside"  # exibe acima das barras
                    ))
fig.update_layout(
    title="Comparação de Cenários LTV/CAC",
    xaxis_title="Cenário",
    yaxis_title="Ratio LTV/CAC",
    bargap=0.4,
    height=600,  # aumenta a altura
    width=1000,  # aumenta a largura
    margin=dict(t=80, b=150)  # aumenta espaço superior e inferior
)

fig.update_xaxes(tickangle=-30)

colors = [
    "rgb(39, 80, 155)",   # Azul Michelin
    "rgb(252, 229, 0)",   # Amarelo Michelin
    "rgb(234, 75, 107)",  # Rosa
    "rgb(239, 125, 0)",   # Laranja
    "rgb(60, 175, 175)",  # Verde Água
    "rgb(173, 226, 93)"   # Verde Claro
]

fig = go.Figure()
fig.add_trace(go.Bar(
    x=df_resultados["Cenário"],
    y=df_resultados["LTV/CAC"],
    text=[f"{v:.2f}" for v in df_resultados["LTV/CAC"]],
    textposition="outside",
    textfont=dict(size=16, color="black"),  # Fonte maior e preta
    marker_color=colors  # Aplica cores diferentes
))
fig.update_layout(
    title="Comparação de Cenários LTV/CAC",
    xaxis_title="Cenário",
    yaxis_title="Ratio LTV/CAC",
    bargap=0.4
)

st.plotly_chart(fig)

st.markdown("---")  # Linha separadora
st.markdown("""
**Vinicius Bartelle Veronese**  
ESPECIALISTA DE PROGRESSO  
*Progress Specialist*
""")

# Se quiser incluir a imagem da assinatura (foto ou logo)
st.image("assinatura2.png", width=120)  # Coloque o caminho da imagem

