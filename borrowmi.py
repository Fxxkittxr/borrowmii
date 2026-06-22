import streamlit as st
import re

# --- CONFIGURAÇÃO DA PÁGINA (RNF01, RNF02, RNF09) ---
st.set_page_config(page_title="BORROWMI", page_icon="🤝", layout="wide")

# --- ESTILIZAÇÃO CUSTOMIZADA (Fidelidade ao Mockup - RNF09, RNF01, RNF02) ---
st.markdown("""
    <style>
    /* Customização global de fontes e estilo */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Sans-Serif', sans-serif;
    }
    
    /* Estilização dos Cards de Produtos (Bordas arredondadas e sombra leve) */
    div[data-testid="stVerticalBlock"] > div:has(div[class*="stAlert"]) {
        border-radius: 12px;
    }
    
    .product-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #E0E0E0;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 15px;
    }
    
    /* Ajuste de cor e peso dos botões principais */
    div.stButton > button {
        border-radius: 8px !important;
        font-weight: 500 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- FUNÇÕES DE VALIDAÇÃO (Testes Unitários - RF01, RF03, RNF10) ---
def validar_email(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(regex, email))

def validar_senha(senha):
    return len(senha) >= 6

def validar_nome(nome):
    clean_name = nome.replace(" ", "")
    return clean_name.isalpha() and len(nome) >= 3

# --- GERENCIAMENTO DE ESTADO (Persistência de Dados - RNF03) ---
if "logado" not in st.session_state:
    st.session_state.logado = False
if "tela_atual" not in st.session_state:
    st.session_state.tela_atual = "Login"
if "carrinho" not in st.session_state:
    st.session_state.carrinho = []

if "itens_disponiveis" not in st.session_state:
    st.session_state.itens_disponiveis = [
        {"id": 1, "nome": "Furadeira de Impacto Bosch", "preco": 25.0, "distancia": "400m", "categoria": "Ferramentas", "avaliacao": "4.9", "proprio": True, "reserva_ativa": True},
        {"id": 2, "nome": "Escada Articulada 4m", "preco": 15.0, "distancia": "1.2km", "categoria": "Ferramentas", "avaliacao": "4.7", "proprio": False, "reserva_ativa": False},
        {"id": 3, "nome": "Cortador de Grama Elétrico", "preco": 40.0, "distancia": "800m", "categoria": "Jardinagem", "avaliacao": "4.8", "proprio": False, "reserva_ativa": False},
        {"id": 4, "nome": "Lavadora de Alta Pressão", "preco": 35.0, "distancia": "0m (Seu)", "categoria": "Ferramentas", "avaliacao": "5.0", "proprio": True, "reserva_ativa": False},
    ]

# --- FLUXO DE NAVEGAÇÃO DE TELAS (RF08) ---

# TELA 1: LOGIN E AUTENTICAÇÃO
if not st.session_state.logado and st.session_state.tela_atual == "Login":
    col1, col2 = st.columns([1.2, 1], gap="large")
    
    with col1:
        st.write("\n" * 5)
        st.title("borrowmi")
        st.markdown("<h2 style='color:#00875A; font-weight:700;'>Sua vizinhança é o seu melhor almoxarifado.</h2>", unsafe_allow_html=True)
        st.write("Entre para localizar itens próximos, conversar com vizinhos e gerar renda extra.")
        
    with col2:
        with st.container(border=True):
            st.subheader("Bem-vindo de volta")
            st.caption("Entre para continuar emprestando")
            
            st.button("Continuar com Google 🌐", use_container_width=True)
            st.write("---")
            
            email_input = st.text_input("E-mail", placeholder="nome@email.com")
            senha_input = st.text_input("Senha", type="password", placeholder="••••••••")
            
            if st.button("Entrar →", use_container_width=True, type="primary"):
                if not email_input or not senha_input:
                    st.error("Erro: Todos os campos são obrigatórios! (RF10)")
                elif not validar_email(email_input):
                    st.error("Erro: O formato do e-mail é inválido! Falta o '@'. (RF03)")
                elif not validar_senha(senha_input):
                    st.error("Erro: A senha deve ter no mínimo 6 caracteres. (RF03)")
                else:
                    st.session_state.logado = True
                    st.session_state.tela_atual = "Dashboard"
                    st.success("Login realizado com sucesso! (RF07)")
                    st.rerun()

# AMBIENTE LOGADO (DASHBOARD, MEUS ITENS E CARRINHO)
else:
    # Header minimalista idêntico ao Mockup superior
    nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns([2, 1, 1, 1, 1.2])
    
    with nav_col1:
        st.markdown("<h2 style='color:#00875A; margin:0; font-weight:700;'>borrowmi</h2>", unsafe_allow_html=True)
    with nav_col2:
        if st.button("🗺️ Explorar Itens", use_container_width=True, type="secondary" if st.session_state.tela_atual != "Dashboard" else "primary"):
            st.session_state.tela_atual = "Dashboard"
            st.rerun()
    with nav_col3:
        if st.button("📦 Meus Itens", use_container_width=True, type="secondary" if st.session_state.tela_atual != "MeusItens" else "primary"):
            st.session_state.tela_atual = "MeusItens"
            st.rerun()
    with nav_col4:
        if st.button(f"🛒 Carrinho ({len(st.session_state.carrinho)})", use_container_width=True, type="secondary" if st.session_state.tela_atual != "Carrinho" else "primary"):
            st.session_state.tela_atual = "Carrinho"
            st.rerun()
    with nav_col5:
        if st.button("🚪 Sair", use_container_width=True):
            st.session_state.logado = False
            st.session_state.tela_atual = "Login"
            st.session_state.carrinho = []
            st.rerun()
            
    st.write("---")

    # TELA 2: DASHBOARD PRINCIPAL
    if st.session_state.tela_atual == "Dashboard":
        # Botão de call-to-action no topo lateral para casar com o Mockup
        dash_col1, dash_col2 = st.columns([3, 1])
        with dash_col1:
            st.header("Explorar Itens")
        with dash_col2:
            # Estilizado com "primary" para herdar o verde correto do config.toml
            if st.button("➕ Anunciar Item", use_container_width=True, type="primary"):
                st.session_state.tela_atual = "Anunciar"
                st.rerun()
        
        search_query = st.text_input("🔍 O que você está procurando hoje?", placeholder="Ex: Furadeira, Cortador...")
        
        # Filtros por categoria em formato de pílulas visuais no mockup
        categoria_selecionada = st.radio(
            "Categorias", 
            ["Todas", "Ferramentas", "Jardinagem", "Cozinha", "Esportes"], 
            horizontal=True
        )
        
        st.write("---")
        st.subheader("Itens disponíveis na sua região")
        
        itens_filtrados = [i for i in st.session_state.itens_disponiveis if not i["proprio"]]
        if categoria_selecionada != "Todas":
            itens_filtrados = [i for i in itens_filtrados if i["categoria"] == categoria_selecionada]
        if search_query:
            itens_filtrados = [i for i in itens_filtrados if search_query.lower() in i["nome"].lower()]
            
        if not itens_filtrados:
            st.info("Nenhum item de vizinhos encontrado para os filtros selecionados.")
            
        cols = st.columns(3)
        for idx, item in enumerate(itens_filtrados):
            with cols[idx % 3]:
                # Div simulando o container estruturado em CSS
                st.markdown(f"""
                <div class="product-card">
                    <h3>{item['nome']}</h3>
                    <p style='color:#757575; font-size:14px;'>📍 A {item['distancia']} de você &nbsp;•&nbsp; ⭐ {item['avaliacao']}</p>
                    <p style='font-size:18px; font-weight:bold;'>R$ {item['preco']:.2f} <span style='font-size:14px; font-weight:normal; color:#757575;'>/ dia</span></p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Alugar", key=f"alugar_{item['id']}", use_container_width=True, type="primary"):
                    st.session_state.carrinho.append(item)
                    st.toast(f"✅ {item['nome']} adicionado ao carrinho! (RF07)")
                    st.rerun()

    # TELA ADICIONAL: FORMULÁRIO DE ANÚNCIO (Separado para manter a UI limpa)
    elif st.session_state.tela_atual == "Anunciar":
        st.header("Anunciar Novo Item para Empréstimo")
        with st.container(border=True):
            nome_item = st.text_input("Nome do Item")
            cat_item = st.selectbox("Categoria do Item", ["Ferramentas", "Jardinagem", "Cozinha", "Esportes"])
            preco_item = st.number_input("Preço por dia (R$)", min_value=1.0, value=10.0)
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Adicionar Item", use_container_width=True, type="primary"):
                    if not validar_nome(nome_item):
                        st.error("Erro: O nome do item precisa ter letras e no mínimo 3 caracteres! (RF01)")
                    else:
                        novo = {
                            "id": len(st.session_state.itens_disponiveis) + 1,
                            "nome": nome_item,
                            "preco": preco_item,
                            "distancia": "0m (Seu)",
                            "categoria": cat_item,
                            "avaliacao": "5.0",
                            "proprio": True,
                            "reserva_ativa": False
                        }
                        st.session_state.itens_disponiveis.append(novo)
                        st.success(f"Sucesso: '{nome_item}' foi cadastrado! (RF02, RF07)")
                        st.session_state.tela_atual = "Dashboard"
                        st.rerun()
            with c2:
                if st.button("Cancelar", use_container_width=True):
                    st.session_state.tela_atual = "Dashboard"
                    st.rerun()

    # TELA 3: GESTÃO DE MEUS ITENS (RF09)
    elif st.session_state.tela_atual == "MeusItens":
        st.header("Gerenciamento de Meus Itens")
        st.caption("Visualize, edite ou remova os objetos que você disponibilizou para a comunidade.")
        
        meus_itens = [i for i in st.session_state.itens_disponiveis if i["proprio"]]
        
        if not meus_itens:
            st.info("Você ainda não cadastrou nenhum objeto para aluguel.")
        else:
            for idx, item in enumerate(meus_itens):
                with st.container(border=True):
                    m_col1, m_col2, m_col3 = st.columns([3, 1, 1])
                    with m_col1:
                        st.write(f"#### {item['nome']}")
                        st.caption(f"Categoria: {item['categoria']} | Valor atual: R$ {item['preco']:.2f}")
                        if item["reserva_ativa"]:
                            st.warning("⚠️ Este item possui uma proposta de reserva ativa no momento.")
                        else:
                            st.success("🟢 Item livre de pendências.")
                            
                    with m_col2:
                        novo_preco = st.number_input(f"Novo Preço (R$)", min_value=1.0, value=float(item['preco']), key=f"edit_p_{item['id']}")
                        if st.button("✏️ Salvar", key=f"btn_edit_{item['id']}", use_container_width=True):
                            for i in st.session_state.itens_disponiveis:
                                if i["id"] == item["id"]:
                                    i["preco"] = novo_preco
                            st.toast("Preço atualizado com sucesso! (RF07)")
                            st.rerun()
                            
                    with m_col3:
                        st.write("") 
                        if st.button("🗑️ Excluir", key=f"btn_del_{item['id']}", use_container_width=True):
                            if item["reserva_ativa"]:
                                st.error(f"Não permitido: O item possui uma reserva em andamento. (RNF08)")
                            else:
                                st.session_state.itens_disponiveis = [i for i in st.session_state.itens_disponiveis if i["id"] != item["id"]]
                                st.success("Item removido da sua conta com sucesso! (RF09)")
                                st.rerun()

    # TELA 4: TELA DE CARRINHO (Fiel à Tela 03 do PDF)
    elif st.session_state.tela_atual == "Carrinho":
        st.header("Seu carrinho")
        st.caption("Ajuste os dias de aluguel ou remova itens antes de confirmar.")
        
        if not st.session_state.carrinho:
            st.write("\n" * 2)
            st.markdown("""
                <div style='text-align: center; padding: 40px; background-color: #F8F9FA; border-radius: 12px;'>
                    <p style='font-size: 24px;'>🛒</p>
                    <h4 style='margin-bottom: 10px;'>Carrinho vazio</h4>
                    <p style='color: #757575;'>Que tal explorar o que sua vizinhança tem disponível?</p>
                </div>
            """, unsafe_allow_html=True)
            st.write("\n")
            if st.button("Explorar itens", key="btn_explorar_vazio", type="primary", use_container_width=True):
                st.session_state.tela_atual = "Dashboard"
                st.rerun()
        else:
            for idx, item in enumerate(st.session_state.carrinho):
                with st.container(border=True):
                    c_col1, c_col2, c_col3 = st.columns([3, 1, 1])
                    with c_col1:
                        st.write(f"#### {item['nome']}")
                        st.caption(f"Categoria: {item['categoria']} | Reputação: {item['avaliacao']}")
                    with c_col2:
                        dias = st.number_input("Dias", min_value=1, value=1, key=f"dias_{idx}")
                        st.write(f"**Total:** R$ {item['preco'] * dias:.2f}")
                    with c_col3:
                        st.write("\n")
                        if st.button("❌ Remover", key=f"rem_{idx}", use_container_width=True):
                            st.session_state.carrinho.pop(idx)
                            st.rerun()
            
            st.write("---")
            if st.button("Confirmar Solicitação de Reserva 🤝", use_container_width=True, type="primary"):
                st.success("Proposta de data enviada com sucesso para o dono do item! (RF06, RF07)")
                st.session_state.carrinho = []