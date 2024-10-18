import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Mock dos dados da planilha de orçamentos
planilha = {
    'Sprint 1': pd.DataFrame({
        'Tarefa': ['H1', 'H2', 'H3', 'H4'],
        'Junior': [2, 1, 1, 0],
        'Pleno': [1, 0, 0, 0],
        'Senior': [1, 0, 0, 0],
        'Total': [2.5, 1.5, 1, 0],
        'Custo Junior': [595.24, 178.57, 119.05, 0],
        'Custo Pleno': [231.90, 0, 0, 0],
        'Custo Senior': [368.33, 0, 0, 0]
    }),
    'Sprint 2': pd.DataFrame({
        'Tarefa': ['H1', 'H2', 'H3', 'H4'],
        'Junior': [4, 2, 1, 1],
        'Pleno': [1, 0, 0, 0],
        'Senior': [1, 0, 0, 0],
        'Total': [3, 1.5, 1.5, 1.5],
        'Custo Junior': [1428.57, 357.14, 178.57, 178.57],
        'Custo Pleno': [231.90, 0, 0, 0],
        'Custo Senior': [368.33, 0, 0, 0]
    }),
    'Sprint 3': pd.DataFrame({
        'Tarefa': ['H1', 'H2', 'H3', 'H4'],
        'Junior': [2, 1, 1, 0],
        'Pleno': [1, 0, 0, 0],
        'Senior': [1, 0, 0, 0],
        'Total': [2, 1.5, 2, 0],
        'Custo Junior': [476.19, 178.57, 238.10, 0],
        'Custo Pleno': [231.90, 0, 0, 0],
        'Custo Senior': [368.33, 0, 0, 0]
    }),
    'Sprint 4': pd.DataFrame({
        'Tarefa': ['H1', 'H2', 'H3', 'H4'],
        'Junior': [4, 2, 2, 0],
        'Pleno': [1, 0, 0, 0],
        'Senior': [1, 0, 0, 0],
        'Total': [3, 1, 2, 0],
        'Custo Junior': [1428.57, 238.10, 476.19, 0],
        'Custo Pleno': [231.90, 0, 0, 0],
        'Custo Senior': [368.33, 0, 0, 0]
    }),
    'Sprint 5': pd.DataFrame({
        'Tarefa': ['H1', 'H2', 'H3', 'H4'],
        'Junior': [2, 2, 0, 0],
        'Pleno': [1, 0, 0, 0],
        'Senior': [1, 0, 0, 0],
        'Total': [2.5, 2, 0, 0],
        'Custo Junior': [595.24, 476.19, 0, 0],
        'Custo Pleno': [231.90, 0, 0, 0],
        'Custo Senior': [368.33, 0, 0, 0]
    })
}

# Custos gerais da Release
custos_release = {
    'Mão de Obra': {
        'Junior': 7142.86,
        'Pleno': 2319.00,
        'Senior': 3683.30,
        'SM (1/N)': 0,
        'PO (1/N)': 0,
        'Total MO': 13145.16
    },
    'Lucro Empresa': 6572.58,  # 50% do custo de mão de obra
    'Custos Fixos': 2629.03,    # 20% do custo de mão de obra
    'Valor da Release': 22346.77
}

# Criar uma interface Streamlit
st.title('Dashboard de Orçamento por Sprint e Release')
st.sidebar.title('Opções de Visualização')

# Selecionar aba para visualizar
aba_selecionada = st.sidebar.selectbox('Selecione a Sprint', list(planilha.keys()) + ['Release'])

if aba_selecionada == 'Release':
    st.header('Resumo da Release')
    st.write("### Custos de Mão de Obra")
    for key, value in custos_release['Mão de Obra'].items():
        st.write(f"{key}: R$ {value:.2f}")

    st.write("### Margens e Custos Adicionais")
    st.write(f"Percentual de Lucro da Empresa: R$ {custos_release['Lucro Empresa']:.2f}")
    st.write(f"Custos Fixos: R$ {custos_release['Custos Fixos']:.2f}")
    st.write(f"### Valor Total da Release: R$ {custos_release['Valor da Release']:.2f}")

    # Gráfico de custo da Release com Plotly (Gráfico de Rosquinha)
    categorias = list(custos_release['Mão de Obra'].keys())[:-1] + ['Lucro Empresa', 'Custos Fixos']
    valores = list(custos_release['Mão de Obra'].values())[:-1] + [custos_release['Lucro Empresa'], custos_release['Custos Fixos']]
    fig = go.Figure(data=[go.Pie(labels=categorias, values=valores, hole=0.4)])
    fig.update_layout(title='Distribuição de Custos da Release')
    st.plotly_chart(fig)

    # Gráfico de quanto é dos desenvolvedores e quanto é da empresa
    total_mao_de_obra = custos_release['Mão de Obra']['Total MO']
    total_empresa = custos_release['Lucro Empresa'] + custos_release['Custos Fixos']
    fig = go.Figure(data=[
        go.Pie(labels=['Mão de Obra (Devs)', 'Empresa (Lucro + Custos Fixos)'], values=[total_mao_de_obra, total_empresa], hole=0.4)
    ])
    fig.update_layout(title='Distribuição de Custos: Mão de Obra vs Empresa')
    st.plotly_chart(fig)

else:
    dados = planilha[aba_selecionada]

    # Mostrar dados da sprint selecionada
    st.header(f'Sprint: {aba_selecionada}')
    st.write("### Tarefas e Desenvolvedores Alocados")
    st.dataframe(dados)

    # Calcular o total de horas e custos por desenvolvedor
    st.write("### Estimativa da Sprint")

    if 'Junior' in dados.columns and 'Pleno' in dados.columns and 'Senior' in dados.columns:
        total_junior = dados['Junior'].sum()
        total_pleno = dados['Pleno'].sum()
        total_senior = dados['Senior'].sum()

        st.write(f"Total de horas Junior: {total_junior} horas")
        st.write(f"Total de horas Pleno: {total_pleno} horas")
        st.write(f"Total de horas Senior: {total_senior} horas")

        # Calcular o custo total da sprint
        custo_junior = total_junior * 119.05  # Valor exemplo por hora
        custo_pleno = total_pleno * 231.90    # Valor atualizado por hora
        custo_senior = total_senior * 368.33   # Valor atualizado por hora

        custo_total = custo_junior + custo_pleno + custo_senior

        st.write(f"Custo total Junior: R$ {custo_junior:.2f}")
        st.write(f"Custo total Pleno: R$ {custo_pleno:.2f}")
        st.write(f"Custo total Senior: R$ {custo_senior:.2f}")
        st.write(f"### Custo Total da Sprint: R$ {custo_total:.2f}")

        # Gráficos da Sprint com Plotly (Gráfico de Rosquinha para Distribuição de Custos)
        fig = go.Figure(data=[
            go.Pie(labels=['Junior', 'Pleno', 'Senior'], values=[custo_junior, custo_pleno, custo_senior], hole=0.4)
        ])
        fig.update_layout(title=f'Distribuição de Custos da Sprint {aba_selecionada}')
        st.plotly_chart(fig)

        # Gráfico de barras para horas estimadas por tarefa
        fig = go.Figure(data=[
            go.Bar(x=dados['Tarefa'], y=dados['Total'], marker_color='coral')
        ])
        fig.update_layout(title=f'Horas Estimadas por Tarefa - Sprint {aba_selecionada}', yaxis_title='Horas Estimadas')
        st.plotly_chart(fig)
    else:
        st.write("As colunas 'Junior', 'Pleno' e 'Senior' são necessárias para o cálculo de custos.")
