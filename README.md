
# Simulador de Cenários LTV/CAC

Este projeto é um aplicativo interativo desenvolvido com Streamlit para simular diferentes cenários de LTV/CAC com base em parâmetros ajustáveis.

## 📦 Arquivos
- `simulador_ltv_cac.py`: código principal do aplicativo Streamlit.
- `requirements.txt`: lista de dependências necessárias.

---

## 🚀 Como rodar localmente

### 1. Instale o Python
Baixe e instale o [Python](https://www.python.org/downloads/) (versão 3.9 ou superior).

### 2. Instale as dependências
Abra o terminal e execute:
```bash
pip install -r requirements.txt
```

### 3. Execute o aplicativo
```bash
streamlit run simulador_ltv_cac.py
```

O aplicativo abrirá automaticamente no navegador em `http://localhost:8501`.

---

## ☁️ Como publicar no Streamlit Cloud

### 1. Crie um repositório no GitHub
Suba os arquivos `simulador_ltv_cac.py` e `requirements.txt`.

### 2. Acesse [Streamlit Cloud](https://streamlit.io/cloud)
- Faça login com sua conta GitHub.
- Clique em **“New app”**.

### 3. Preencha os campos:
- **Repository**: selecione o repositório que você criou.
- **Branch**: normalmente `main`.
- **Main file path**: digite `simulador_ltv_cac.py`

### 4. Clique em **Deploy**
Seu app estará disponível em um link público para acesso via navegador.

---

## ✨ Funcionalidades
- Interface interativa para entrada de parâmetros:
  - Ticket médio mensal
  - Margem bruta completa
  - Margem bruta sem depreciação
  - Churn rate mensal
  - CAPEX do equipamento
  - Outros custos de aquisição
  - Vida útil do equipamento
- Cálculo automático de 6 cenários LTV/CAC
- Tabela de resultados e gráfico comparativo

---

## 📬 Contato
Para dúvidas ou sugestões, entre em contato com o autor do repositório.
