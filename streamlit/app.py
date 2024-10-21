import streamlit as st
import pandas as pd
import plotly.graph_objects as go

import plotly.express as px
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

# Mock dos dados dos tickets
tickets = pd.DataFrame({
    'Sprint e Ticket': [
        'Gestão de Usuários e Perfis - H1', 'Gestão de Usuários e Perfis - H2', 'Gestão de Usuários e Perfis - H3',
        'Cadastro e Manutenção de Veículos - H1', 'Cadastro e Manutenção de Veículos - H2', 'Cadastro e Manutenção de Veículos - H3', 'Cadastro e Manutenção de Veículos - H4',
        'Automatização do Agendamento e Alertas - H1', 'Automatização do Agendamento e Alertas - H2', 'Automatização do Agendamento e Alertas - H3',
        'Monitoramento e Relatórios de Manutenção - H1', 'Monitoramento e Relatórios de Manutenção - H2', 'Monitoramento e Relatórios de Manutenção - H3',
        'Gestão de Manutenções - H1', 'Gestão de Manutenções - H2'
    ],
    'Usuários': [
        'Gerente Geral', 'Gerente Geral', 'Gerente Geral', 'Funcionária do RH', 'Funcionária do RH',
        'Funcionária do RH', 'Funcionária do RH', 'Funcionária do RH', 'Funcionária do RH', 'Motorista',
        'Gerente de Frotas', 'Gerente de Frotas', 'Gerente Geral', 'Técnico de Manutenção', 'Técnico de Manutenção'
    ],
    'Descrição das histórias': [
        'Eu quero criar meu perfil e criar minha empresa dentro da plataforma',
        'Eu quero cadastrar perfis de usuários e quais serão suas atribuições (Permissões)',
        'Eu quero cadastrar meus funcionários e definir quais serão suas atribuições',
        'Eu quero cadastrar os caminhões na plataforma para gerenciar suas informações e manutenção',
        'Eu quero registrar o histórico completo de manutenções e reparos de cada veículo',
        'Eu quero definir os intervalos de tempo ou quilometragem para manutenções preventiva',
        'Eu quero cadastrar os diferentes tipos de manutenção necessários para cada veículo',
        'Eu quero que o sistema agende automaticamente as manutenções com base nos intervalos definidos',
        'Eu quero receber alertas automáticos quando um veículo estiver próximo de sua manutenção',
        'Eu quero ser notificado quando meu veículo estiver programado para manutenção',
        'Eu quero acessar relatórios sobre o estado da manutenção de cada veículo',
        'Eu quero identificar veículos que estão com manutenção atrasada',
        'Eu quero verificar qual o estado dos veículos da frota',
        'Eu quero consultar as manutenções pendentes e o histórico de reparos',
        'Eu quero registrar o status de cada manutenção realizada'
    ],
    'Dias': [2.5, 1.5, 1, 3, 1.5, 1.5, 1.5, 2, 1.5, 2, 3, 1, 2, 2.5, 2]
})

st.set_page_config(page_title='Dashboard de Orçamento', page_icon=':bar_chart:', layout='wide', initial_sidebar_state='expanded')

# Criar uma interface Streamlit
st.title('Dashboard de Orçamento por Sprint e Release')
st.sidebar.title('Opções de Visualização')

# Selecionar aba para visualizar
aba_selecionada = st.sidebar.selectbox('Selecione a Sprint', list(planilha.keys()) + ['Release', 'Tickets'])

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
    fig.update_layout(title='Distribuição de Custos da Release', template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig)

    # Gráfico de quanto é dos desenvolvedores e quanto é da empresa
    total_mao_de_obra = custos_release['Mão de Obra']['Total MO']
    total_empresa = custos_release['Lucro Empresa'] + custos_release['Custos Fixos']
    fig = go.Figure(data=[
        go.Pie(labels=['Mão de Obra (Devs)', 'Empresa (Lucro + Custos Fixos)'], values=[total_mao_de_obra, total_empresa], hole=0.4)
    ])
    fig.update_layout(title='Distribuição de Custos: Mão de Obra vs Empresa', template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig)



# Adicionar gráfico de Gantt para visualização da sequência de execução dos tickets
    st.write("### Cronograma de Execução dos Tickets")
    gantt_data = tickets[['Sprint e Ticket', 'Usuários', 'Descrição das histórias', 'Dias']].copy()
    gantt_data['Início'] = pd.Timestamp('2024-01-01') + pd.to_timedelta(gantt_data.index * 2, unit='D')
    gantt_data['Fim'] = gantt_data['Início'] + pd.to_timedelta(gantt_data['Dias'], unit='D')
    fig_gantt = px.timeline(gantt_data, x_start='Início', x_end='Fim', y='Usuários', color='Sprint e Ticket', title='Cronograma de Execução dos Tickets', template='plotly_dark')
    st.plotly_chart(fig_gantt)

elif aba_selecionada == 'Tickets':
    st.header('Gestão de Tickets')
    st.write("### Informações dos Tickets")
    st.dataframe(tickets)

else:
    dados = planilha[aba_selecionada]

    

    # Adicionar uma linha que é a soma das colunas relevantes (Total e custos)
    soma_colunas = dados[['Junior', 'Pleno', 'Senior', 'Total', 'Custo Junior', 'Custo Pleno', 'Custo Senior']].sum()
    soma_linha = pd.DataFrame([soma_colunas], columns=dados.columns)
    soma_linha['Tarefa'] = 'Total'
    soma_linha['Tarefa'] = 'Total'
    dados = pd.concat([dados, soma_linha], ignore_index=True)

    st.write("### Tarefas e Desenvolvedores Alocados (com Total)")
    st.dataframe(dados)

    
    # Calcular o total de horas e custos por desenvolvedor
    st.write("### Estimativa da Sprint")

    if 'Junior' in dados.columns and 'Pleno' in dados.columns and 'Senior' in dados.columns:
        total_junior = dados['Junior'].sum()
        total_pleno = dados['Pleno'].sum()
        total_senior = dados['Senior'].sum()

        # st.write(f"Total de horas Junior: {total_junior} horas")
        # st.write(f"Total de horas Pleno: {total_pleno} horas")
        # st.write(f"Total de horas Senior: {total_senior} horas")

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
        fig.update_layout(title=f'Distribuição de Custos da Sprint {aba_selecionada}', template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig)

        # Gráfico de barras para horas estimadas por tarefa
        fig = go.Figure(data=[
            go.Bar(x=dados['Tarefa'], y=dados['Total'], marker_color='coral')
        ])
        fig.update_layout(title=f'Dias Estimados por Tarefa - Sprint {aba_selecionada}', yaxis_title='Dias Estimados', template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig)
    else:
        st.write("As colunas 'Junior', 'Pleno' e 'Senior' são necessárias para o cálculo de custos.")
