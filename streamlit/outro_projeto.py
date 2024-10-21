import streamlit as st
import pandas as pd

# Definição dos cargos e salários padrão
cargos_salarios = {
    'Web': {
        'Dev Junior': 119.05,
        'Dev Pleno': 231.90,
        'Dev Senior': 368.33
    },
    'Mobile': {
        'Dev Junior': 151.05,
        'Dev Pleno': 312.95,
        'Dev Senior': 552.38
    },
    'Outros': {
        'Scrum M.': 404.76,
        'Product O.': 397.62
    }
}

# Mapeamento de nomes abreviados para nomes completos
nomes_completos = {
    'Dev Junior': 'Desenvolvedor Junior',
    'Dev Pleno': 'Desenvolvedor Pleno',
    'Dev Senior': 'Desenvolvedor Senior',
    'Scrum M.': 'Scrum Master',
    'Product O.': 'Product Owner'
}

# Lista de story points
story_points = [0.25, 0.5, 1, 2, 3, 5, 8, 13]

# Inicialização do estado da sessão
if 'sprints' not in st.session_state:
    st.session_state.sprints = {}

if 'salarios' not in st.session_state:
    st.session_state.salarios = {categoria: {cargo: valor for cargo, valor in cargos.items()} 
                                 for categoria, cargos in cargos_salarios.items()}

# Página de configuração de salários
def configurar_salarios():
    st.title("Configuração de Salários")
    
    st.markdown("Defina os salários médios por dia para cada função:")
    
    for categoria, cargos in st.session_state.salarios.items():
        st.subheader(categoria)
        for cargo, valor in cargos.items():
            st.session_state.salarios[categoria][cargo] = st.number_input(
                f"Salário por dia - {nomes_completos[cargo]}",
                min_value=0.0,
                value=float(valor),
                step=0.01,
                format="%.2f",
                key=f"{categoria}_{cargo}"
            )
    
    if st.button("Salvar Configurações"):
        st.success("Salários salvos com sucesso!")

# Página para listar e criar sprints
def listar_sprints():
    st.title("Gerenciar Sprints")
    
    # Criar nova sprint
    nova_sprint = st.text_input("Nome da nova sprint:")
    if st.button("Criar Nova Sprint") and nova_sprint:
        if nova_sprint not in st.session_state.sprints:
            st.session_state.sprints[nova_sprint] = {}
            st.success(f"Sprint '{nova_sprint}' criada com sucesso!")
        else:
            st.error("Uma sprint com esse nome já existe.")
    
    # Listar sprints existentes
    st.subheader("Sprints Existentes")
    for sprint in st.session_state.sprints:
        st.write(f"- {sprint}")

# Função para exibir a interface simplificada por ticket
def montar_sprint(sprint_name):
    st.title(f"Montar Sprint: {sprint_name}")
    
    # CSS para o layout do grid
    st.markdown("""
    <style>
    .grid-cell {
        width: 100%;
        height: 60px;
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
        text-align: center;
        padding: 5px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
    }
    .grid-cell input[type="number"] {
        width: 100%;
        height: 36px;
        text-align: center;
        font-size: 14px;
        padding: 0;
        border: 1px solid #ccc;
        border-radius: 4px;
    }
    .grid-cell .stCheckbox {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 36px;
    }
    .grid-cell .stCheckbox > label {
        width: 36px;
        height: 36px;
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 0;
    }
    .grid-cell .stCheckbox > label > div {
        width: 24px;
        height: 24px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    num_tickets = st.number_input('Número de tickets', min_value=1, value=1, step=1)
    
    # Inicializa os dados dos tickets se ainda não foi feito
    for i in range(1, num_tickets + 1):
        ticket_id = f"Ticket_{i}"
        if ticket_id not in st.session_state.sprints[sprint_name]:
            st.session_state.sprints[sprint_name][ticket_id] = {
                categoria: {
                    cargo: {'pessoas': 0, 'story_points': [0 for _ in story_points]} 
                    for cargo in cargos
                } for categoria, cargos in cargos_salarios.items()
            }
    
    # Interface para definir story points e número de pessoas por ticket
    for i in range(1, num_tickets + 1):
        ticket_id = f"Ticket_{i}"
        with st.expander(f'{ticket_id}'):
            st.markdown(f"<h5 style='text-align: center;'>Definir número de pessoas e story points para {ticket_id}</h5>", unsafe_allow_html=True)
            
            for categoria, cargos in cargos_salarios.items():
                show_categoria = st.checkbox(f"{categoria}", value=True, key=f"{sprint_name}_{ticket_id}_{categoria}_checkbox")
                if show_categoria:
                    # Criar as colunas para a tabela
                    cols = st.columns([2, 2] + [1.5 for _ in story_points])

                    # Cabeçalhos
                    cols[0].markdown("<div class='grid-cell'><b>Cargo</b></div>", unsafe_allow_html=True)
                    cols[1].markdown("<div class='grid-cell'><b>Nº Pessoas</b></div>", unsafe_allow_html=True)
                    for j, point in enumerate(story_points):
                        cols[j + 2].markdown(f"<div class='grid-cell'><b>{point} SP</b></div>", unsafe_allow_html=True)

                    # Para cada cargo, adicionamos o campo de número de pessoas e a matriz de story points
                    for cargo in cargos:
                        # Cargo (usando nome abreviado)
                        cols[0].markdown(f"<div class='grid-cell'>{cargo}</div>", unsafe_allow_html=True)

                        # Número de pessoas
                        with cols[1]:
                            num_pessoas = st.number_input(
                                "", 
                                min_value=0, 
                                value=st.session_state.sprints[sprint_name][ticket_id][categoria][cargo]['pessoas'],
                                step=1, 
                                key=f"{sprint_name}_{ticket_id}_{categoria}_{cargo}_pessoas", 
                                label_visibility="collapsed"
                            )
                        st.session_state.sprints[sprint_name][ticket_id][categoria][cargo]['pessoas'] = num_pessoas
                        
                        # Story points (checkboxes)
                        for j, point in enumerate(story_points):
                            with cols[j + 2]:
                                checked = st.checkbox(
                                    "", value=st.session_state.sprints[sprint_name][ticket_id][categoria][cargo]['story_points'][j],
                                    key=f"{sprint_name}_{ticket_id}_{categoria}_{cargo}_{point}_checkbox",
                                    label_visibility="collapsed"
                                )
                            st.session_state.sprints[sprint_name][ticket_id][categoria][cargo]['story_points'][j] = checked

    if st.button("Salvar Sprint"):
        st.success(f"Sprint '{sprint_name}' salva com sucesso!")

# Página de orçamento
def mostrar_orcamento():
    st.title("Orçamento das Sprints")
    
    if not st.session_state.sprints:
        st.warning("Nenhuma sprint foi criada ainda. Por favor, crie uma sprint primeiro.")
        return
    
    sprint_selecionada = st.selectbox("Selecione a sprint para ver o orçamento:", 
                                      ["Todas as Sprints"] + list(st.session_state.sprints.keys()))
    
    if sprint_selecionada == "Todas as Sprints":
        sprints_para_calcular = st.session_state.sprints
    else:
        sprints_para_calcular = {sprint_selecionada: st.session_state.sprints[sprint_selecionada]}
    
    total_orcamento_geral = 0
    total_horas_geral = 0
    
    for sprint_name, sprint_data in sprints_para_calcular.items():
        st.subheader(f"Orçamento para Sprint: {sprint_name}")
        total_orcamento_sprint = 0
        total_horas_sprint = 0
        
        for ticket_id, ticket_data in sprint_data.items():
            st.write(f"Ticket: {ticket_id}")
            ticket_total = 0
            ticket_horas = 0
            
            for categoria, cargos in ticket_data.items():
                for cargo, dados in cargos.items():
                    num_pessoas = dados['pessoas']
                    story_points_cargo = sum([sp * checked for sp, checked in zip(story_points, dados['story_points'])])
                    horas = story_points_cargo  # Agora cada story point é 1 hora
                    custo = horas * num_pessoas * (st.session_state.salarios[categoria][cargo] / 8)  # Custo por hora
                    ticket_total += custo
                    ticket_horas += horas * num_pessoas
                    if num_pessoas > 0:
                        st.write(f"  {num_pessoas} {nomes_completos[cargo]}(s) trabalhando {horas:.2f} horas - Custo: R$ {custo:.2f}")
            
            st.write(f"Total para {ticket_id}: {ticket_horas:.2f} horas - Custo: R$ {ticket_total:.2f}")
            total_orcamento_sprint += ticket_total
            total_horas_sprint += ticket_horas
        
        st.write(f"Total para Sprint {sprint_name}: {total_horas_sprint:.2f} horas - Custo: R$ {total_orcamento_sprint:.2f}")
        total_orcamento_geral += total_orcamento_sprint
        total_horas_geral += total_horas_sprint
        st.write("---")
    
    if sprint_selecionada == "Todas as Sprints":
        st.subheader("Resumo Geral")
        st.write(f"Total de horas de todas as Sprints: {total_horas_geral:.2f} horas")
        st.write(f"Custo total de todas as Sprints: R$ {total_orcamento_geral:.2f}")
        
        # Cálculo do custo médio por hora
        custo_medio_hora = total_orcamento_geral / total_horas_geral if total_horas_geral > 0 else 0
        st.write(f"Custo médio por hora: R$ {custo_medio_hora:.2f}")

# Menu de navegação
st.sidebar.title("Navegação")
page = st.sidebar.radio("Escolha a página", ["Gerenciar Sprints", "Configurar Salários", "Montar Sprint", "Orçamento"])

if page == "Gerenciar Sprints":
    listar_sprints()
elif page == "Configurar Salários":
    configurar_salarios()
elif page == "Montar Sprint":
    if st.session_state.sprints:
        sprint_selecionada = st.sidebar.selectbox("Selecione a sprint para montar:", list(st.session_state.sprints.keys()))
        montar_sprint(sprint_selecionada)
    else:
        st.warning("Nenhuma sprint foi criada ainda. Por favor, crie uma sprint primeiro na página 'Gerenciar Sprints'.")
elif page == "Orçamento":
    mostrar_orcamento()
