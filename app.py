import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="Controle de Equipe",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para interface moderna com cards
css_styles = """
<style>
.main-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 15px;
    color: white;
    margin-bottom: 1rem;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.stat-card {
    background: white;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    margin-bottom: 1rem;
    border-left: 4px solid #667eea;
}

.request-card {
    background: white;
    padding: 1rem;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    margin-bottom: 0.5rem;
    border-left: 3px solid #667eea;
}

.priority-alta {
    border-left-color: #e74c3c !important;
}

.priority-média {
    border-left-color: #f39c12 !important;
}

.priority-baixa {
    border-left-color: #27ae60 !important;
}

.status-novo {
    background-color: #3498db;
    color: white;
    padding: 0.2rem 0.8rem;
    border-radius: 15px;
    font-size: 0.8rem;
}

.status-em-andamento {
    background-color: #f39c12;
    color: white;
    padding: 0.2rem 0.8rem;
    border-radius: 15px;
    font-size: 0.8rem;
}

.status-concluido {
    background-color: #27ae60;
    color: white;
    padding: 0.2rem 0.8rem;
    border-radius: 15px;
    font-size: 0.8rem;
}
</style>
"""

st.markdown(css_styles, unsafe_allow_html=True)

# Inicializar banco de dados
def init_db():
    conn = sqlite3.connect('equipe_app.db')
    cursor = conn.cursor()

    # Tabela de membros da equipe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS membros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            cargo TEXT NOT NULL,
            data_entrada DATE NOT NULL
        )
    """)

    # Tabela de solicitações
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS solicitacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT,
            solicitante_id INTEGER,
            responsavel_id INTEGER,
            prioridade TEXT DEFAULT 'Média',
            status TEXT DEFAULT 'Novo',
            data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
            data_prazo DATE,
            FOREIGN KEY (solicitante_id) REFERENCES membros (id),
            FOREIGN KEY (responsavel_id) REFERENCES membros (id)
        )
    """)

    # Inserir dados iniciais se não existirem
    cursor.execute('SELECT COUNT(*) FROM membros')
    if cursor.fetchone()[0] == 0:
        membros_iniciais = [
            ('Ana Silva', 'ana@empresa.com', 'Líder de Equipe', '2024-01-15'),
            ('João Santos', 'joao@empresa.com', 'Desenvolvedor', '2024-02-01'),
            ('Maria Costa', 'maria@empresa.com', 'Designer', '2024-02-15'),
            ('Pedro Lima', 'pedro@empresa.com', 'Analista', '2024-03-01')
        ]
        cursor.executemany("""
            INSERT INTO membros (nome, email, cargo, data_entrada) 
            VALUES (?, ?, ?, ?)
        """, membros_iniciais)

    conn.commit()
    conn.close()

# Funções do banco de dados
def get_membros():
    conn = sqlite3.connect('equipe_app.db')
    df = pd.read_sql_query('SELECT * FROM membros', conn)
    conn.close()
    return df

def add_membro(nome, email, cargo):
    conn = sqlite3.connect('equipe_app.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO membros (nome, email, cargo, data_entrada) 
        VALUES (?, ?, ?, ?)
    """, (nome, email, cargo, datetime.now().date()))
    conn.commit()
    conn.close()

def get_solicitacoes():
    conn = sqlite3.connect('equipe_app.db')
    query = """
        SELECT s.*, 
               m1.nome as solicitante_nome,
               m2.nome as responsavel_nome
        FROM solicitacoes s
        LEFT JOIN membros m1 ON s.solicitante_id = m1.id
        LEFT JOIN membros m2 ON s.responsavel_id = m2.id
        ORDER BY s.data_criacao DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def add_solicitacao(titulo, descricao, solicitante_id, responsavel_id, prioridade, data_prazo):
    conn = sqlite3.connect('equipe_app.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO solicitacoes (titulo, descricao, solicitante_id, responsavel_id, prioridade, data_prazo)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (titulo, descricao, solicitante_id, responsavel_id, prioridade, data_prazo))
    conn.commit()
    conn.close()

def update_status_solicitacao(solicitacao_id, novo_status):
    conn = sqlite3.connect('equipe_app.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE solicitacoes SET status = ? WHERE id = ?', (novo_status, solicitacao_id))
    conn.commit()
    conn.close()

# Inicializar banco
init_db()

# Sidebar
st.sidebar.title("🏢 Menu Principal")
pagina = st.sidebar.selectbox("Navegação", ["Dashboard", "Solicitações", "Equipe", "Nova Solicitação"])

if pagina == "Dashboard":
    # Header principal
    st.markdown("""
    <div class="main-card">
        <h1>🎯 Dashboard da Equipe</h1>
        <p>Acompanhe o desempenho e status das solicitações</p>
    </div>
    """, unsafe_allow_html=True)

    # Estatísticas
    solicitacoes_df = get_solicitacoes()
    membros_df = get_membros()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_sol = len(solicitacoes_df)
        st.markdown(f"""
        <div class="stat-card">
            <h3>📊 Total Solicitações</h3>
            <h2 style="color: #667eea;">{total_sol}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        novas = len(solicitacoes_df[solicitacoes_df['status'] == 'Novo'])
        st.markdown(f"""
        <div class="stat-card">
            <h3>🆕 Novas</h3>
            <h2 style="color: #3498db;">{novas}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        em_andamento = len(solicitacoes_df[solicitacoes_df['status'] == 'Em Andamento'])
        st.markdown(f"""
        <div class="stat-card">
            <h3>⚡ Em Andamento</h3>
            <h2 style="color: #f39c12;">{em_andamento}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        concluidas = len(solicitacoes_df[solicitacoes_df['status'] == 'Concluído'])
        st.markdown(f"""
        <div class="stat-card">
            <h3>✅ Concluídas</h3>
            <h2 style="color: #27ae60;">{concluidas}</h2>
        </div>
        """, unsafe_allow_html=True)

    # Gráficos
    col1, col2 = st.columns(2)

    with col1:
        if not solicitacoes_df.empty:
            status_counts = solicitacoes_df['status'].value_counts()
            fig = px.pie(
                values=status_counts.values, 
                names=status_counts.index,
                title="📈 Status das Solicitações",
                color_discrete_sequence=['#3498db', '#f39c12', '#27ae60']
            )
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        if not solicitacoes_df.empty:
            prioridade_counts = solicitacoes_df['prioridade'].value_counts()
            fig = px.bar(
                x=prioridade_counts.index, 
                y=prioridade_counts.values,
                title="🎯 Distribuição por Prioridade",
                color=prioridade_counts.values,
                color_continuous_scale='Viridis'
            )
            st.plotly_chart(fig, use_container_width=True)

elif pagina == "Solicitações":
    st.title("📋 Gerenciar Solicitações")

    solicitacoes_df = get_solicitacoes()

    if not solicitacoes_df.empty:
        # Filtros
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.selectbox("Filtrar por Status", ["Todos"] + list(solicitacoes_df['status'].unique()))
        with col2:
            prioridade_filter = st.selectbox("Filtrar por Prioridade", ["Todos"] + list(solicitacoes_df['prioridade'].unique()))
        with col3:
            responsavel_filter = st.selectbox("Filtrar por Responsável", ["Todos"] + list(solicitacoes_df['responsavel_nome'].dropna().unique()))

        # Aplicar filtros
        df_filtrado = solicitacoes_df.copy()
        if status_filter != "Todos":
            df_filtrado = df_filtrado[df_filtrado['status'] == status_filter]
        if prioridade_filter != "Todos":
            df_filtrado = df_filtrado[df_filtrado['prioridade'] == prioridade_filter]
        if responsavel_filter != "Todos":
            df_filtrado = df_filtrado[df_filtrado['responsavel_nome'] == responsavel_filter]

        # Cards das solicitações
        for _, solicitacao in df_filtrado.iterrows():
            priority_class = f"priority-{solicitacao['prioridade'].lower()}"

            descricao_text = solicitacao['descricao'] if solicitacao['descricao'] else 'Sem descrição'
            solicitante_text = solicitacao['solicitante_nome'] if solicitacao['solicitante_nome'] else 'N/A'
            responsavel_text = solicitacao['responsavel_nome'] if solicitacao['responsavel_nome'] else 'Não atribuído'

            st.markdown(f"""
            <div class="request-card {priority_class}">
                <h4>🎯 {solicitacao['titulo']}</h4>
                <p><strong>Descrição:</strong> {descricao_text}</p>
                <p><strong>Solicitante:</strong> {solicitante_text} | 
                   <strong>Responsável:</strong> {responsavel_text}</p>
                <p><strong>Prioridade:</strong> {solicitacao['prioridade']} | 
                   <strong>Status:</strong> <span class="status-{solicitacao['status'].lower().replace(' ', '-')}">{solicitacao['status']}</span></p>
                <p><strong>Data:</strong> {solicitacao['data_criacao'][:10]}</p>
            </div>
            """, unsafe_allow_html=True)

            # Botões para alterar status
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button(f"📝 Em Andamento", key=f"andamento_{solicitacao['id']}"):
                    update_status_solicitacao(solicitacao['id'], 'Em Andamento')
                    st.rerun()
            with col2:
                if st.button(f"✅ Concluir", key=f"concluir_{solicitacao['id']}"):
                    update_status_solicitacao(solicitacao['id'], 'Concluído')
                    st.rerun()
            with col3:
                if st.button(f"🔄 Reabrir", key=f"reabrir_{solicitacao['id']}"):
                    update_status_solicitacao(solicitacao['id'], 'Novo')
                    st.rerun()

            st.divider()
    else:
        st.info("Nenhuma solicitação encontrada.")

elif pagina == "Equipe":
    st.title("👥 Gerenciar Equipe")

    membros_df = get_membros()

    # Adicionar novo membro
    with st.expander("➕ Adicionar Novo Membro"):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome")
            cargo = st.text_input("Cargo")
        with col2:
            email = st.text_input("Email")
            if st.button("Adicionar Membro"):
                if nome and email and cargo:
                    add_membro(nome, email, cargo)
                    st.success(f"Membro {nome} adicionado com sucesso!")
                    st.rerun()
                else:
                    st.error("Preencha todos os campos!")

    st.subheader("👥 Membros da Equipe")

    # Cards dos membros
    for _, membro in membros_df.iterrows():
        st.markdown(f"""
        <div class="request-card">
            <h4>👤 {membro['nome']}</h4>
            <p><strong>Cargo:</strong> {membro['cargo']}</p>
            <p><strong>Email:</strong> {membro['email']}</p>
            <p><strong>Data de Entrada:</strong> {membro['data_entrada']}</p>
        </div>
        """, unsafe_allow_html=True)

elif pagina == "Nova Solicitação":
    st.title("📝 Nova Solicitação")

    membros_df = get_membros()

    with st.form("nova_solicitacao"):
        col1, col2 = st.columns(2)

        with col1:
            titulo = st.text_input("Título da Solicitação*")
            if not membros_df.empty:
                solicitante_id = st.selectbox(
                    "Solicitante*", 
                    options=membros_df['id'].tolist(),
                    format_func=lambda x: membros_df[membros_df['id'] == x]['nome'].iloc[0]
                )
            else:
                st.error("Nenhum membro cadastrado!")
                solicitante_id = None
            prioridade = st.selectbox("Prioridade", ["Baixa", "Média", "Alta"])

        with col2:
            responsavel_options = [None] + membros_df['id'].tolist()
            responsavel_id = st.selectbox(
                "Responsável", 
                options=responsavel_options,
                format_func=lambda x: "Não atribuído" if x is None else membros_df[membros_df['id'] == x]['nome'].iloc[0]
            )
            data_prazo = st.date_input("Data Prazo")

        descricao = st.text_area("Descrição", height=100)

        submitted = st.form_submit_button("🚀 Criar Solicitação")

        if submitted:
            if titulo and solicitante_id:
                add_solicitacao(titulo, descricao, solicitante_id, responsavel_id, prioridade, data_prazo)
                st.success("✅ Solicitação criada com sucesso!")
                st.rerun()
            else:
                st.error("Preencha os campos obrigatórios!")

# Footer
st.markdown("---")
st.markdown("🏢 **Sistema de Controle de Equipe** - Desenvolvido para facilitar a gestão interna")
