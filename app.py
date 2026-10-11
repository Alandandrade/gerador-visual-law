import streamlit as st
from docxtpl import DocxTemplate
import io
from datetime import date
import locale

# Tenta configurar o idioma para Português do Brasil para traduzir a data automaticamente
try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
except:
    pass

# --- INICIALIZAÇÃO DA MEMÓRIA (SESSION STATE) ---
if "etapa" not in st.session_state:
    st.session_state.etapa = 1

# Inicialização dos campos de moeda para evitar erros
if 'valor_mensal' not in st.session_state:
    st.session_state.valor_mensal = '1.000,00'
if 'multa_maxima' not in st.session_state:
    st.session_state.multa_maxima = '1.000,00'

# Inicialização fixa dos dados da CONTRATADA (A sua empresa)
# Se já estiverem na memória, não apaga. Se for a primeira vez, ficam em branco para preencher.
if 'nome_contratada' not in st.session_state:
    st.session_state.nome_contratada = ''
if 'cnpj_contratada' not in st.session_state:
    st.session_state.cnpj_contratada = ''
if 'endereco_contratada' not in st.session_state:
    st.session_state.endereco_contratada = ''
if 'repr_contratada' not in st.session_state:
    st.session_state.repr_contratada = ''
if 'rg_repr_contratada' not in st.session_state:
    st.session_state.rg_repr_contratada = ''
if 'cpf_repr_contratada' not in st.session_state:
    st.session_state.cpf_repr_contratada = ''

# --- Função de Formatação Automática de Moeda (Callback) ---
def formatar_moeda(chave):
    valor_digitado = str(st.session_state[chave])
    valor_limpo = valor_digitado.upper().replace('R$', '').replace(' ', '').replace('.', '')
    
    if not valor_limpo:
        st.session_state[chave] = '0,00'
        return
        
    if ',' in valor_limpo:
        partes = valor_limpo.split(',')
        reais = partes[0] if partes[0] else '0'
        centavos = partes[1][:2].ljust(2, '0')
    else:
        reais = valor_limpo
        centavos = '00'
        
    try:
        reais_int = int(reais)
        reais_formatado = f"{reais_int:,}".replace(',', '.')
        st.session_state[chave] = f"{reais_formatado},{centavos}"
    except ValueError:
        st.session_state[chave] = '0,00'

st.set_page_config(page_title="Gerador de Contrato Inteligente", layout="wide")

# ==========================================
# TELA 1: O FORMULÁRIO DE PREENCHIMENTO
# ==========================================
if st.session_state.etapa == 1:
    st.title("📝 Gerador Automático de Contrato")
    st.write("Preencha os dados abaixo e use a tecla **Tab** para saltar rapidamente entre os campos.")

    st.subheader("1. Qualificação das Partes")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Dados do Contratante (Cliente)")
        # Estes campos começam sempre vazios quando se faz um novo contrato
        nome_contratante = st.text_input("Nome/Razão Social (Contratante)", value=st.session_state.get('nome_contratante', ''))
        cnpj_contratante = st.text_input("CNPJ (Contratante)", value=st.session_state.get('cnpj_contratante', ''))
        endereco_contratante = st.text_input("Endereço Sede (Contratante)", value=st.session_state.get('endereco_contratante', ''))
        repr_contratante = st.text_input("Nome do Representante", value=st.session_state.get('repr_contratante', ''))
        rg_repr_contratante = st.text_input("RG do Representante", value=st.session_state.get('rg_repr_contratante', ''))
        cpf_repr_contratante = st.text_input("CPF do Representante", value=st.session_state.get('cpf_repr_contratante', ''))

    with col2:
        st.markdown("#### Dados da Contratada (Sua Empresa)")
        # Estes campos puxam sempre a informação da memória, para nunca perder o que digitou por último
        nome_contratada = st.text_input("Nome/Razão Social (Contratada)", value=st.session_state.nome_contratada)
        cnpj_contratada = st.text_input("CNPJ (Contratada)", value=st.session_state.cnpj_contratada)
        endereco_contratada = st.text_input("Endereço Sede (Contratada)", value=st.session_state.endereco_contratada)
        repr_contratada = st.text_input("Nome do Representante (Contratada)", value=st.session_state.repr_contratada)
        rg_repr_contratada = st.text_input("RG do Representante (Contratada)", value=st.session_state.rg_repr_contratada)
        cpf_repr_contratada = st.text_input("CPF do Representante (Contratada)", value=st.session_state.cpf_repr_contratada)

    st.write("---")
    
    st.subheader("2. Dados Financeiros e Operacionais")
    st.write("Configure as regras base do quadro 'O Contrato em 1 Minuto':")
    
    col3, col4, col5 = st.columns(3)
    with col3:
        st.text_input("Valor Mensal (R$)", key="valor_mensal", on_change=formatar_moeda, args=("valor_mensal",), help="Digite apenas os números (ex: 1000) e pressione Tab.")
        prazo_meses = st.text_input("Prazo do Contrato (meses)", value=st.session_state.get('prazo_meses', '12'))
        st.text_input("Multa Máxima (R$)", key="multa_maxima", on_change=formatar_moeda, args=("multa_maxima",), help="Digite o valor e pressione Tab. Normalmente equivale a uma mensalidade.")
        
    with col4:
        dia_pagamento = st.text_input("Dia de Pagamento", value=st.session_state.get('dia_pagamento', '10'), help="Dia limite para o cliente pagar.")
        dias_cancelamento = st.text_input("Aviso de Cancelamento (dias)", value=st.session_state.get('dias_cancelamento', '30'))
        dias_servico = st.text_input("Dias de Serviço", value=st.session_state.get('dias_servico', 'Seg. a sáb.'), help="Ex: 'Seg. a sáb.' ou 'Seg. a sex.'")
        
    with col5:
        indice_reajuste = st.text_input("Índice de Reajuste", value=st.session_state.get('indice_reajuste', 'IPCA / IBGE'))
        data_assinatura = st.date_input("Data de Assinatura", value=st.session_state.get('data_assinatura_raw', date.today()))
        foro_cidade = st.text_input("Cidade do Foro", value=st.session_state.get('foro_cidade', 'Lorena - SP'))

    st.write("---")
    
    st.subheader("3. Personalização das Cláusulas")
    st.write("Selecione quais regras farão parte deste contrato:")
    
    # As checkboxes agora forçam o valor False (desmarcado) sempre que a Tela 1 carrega de fresco, 
    # exceto aquelas que você queira que sejam padrão (como o sábado).
    incluir_sigilo = st.checkbox("🔒 Incluir cláusula de Confidencialidade (NDA)", value=False, help="Garante que tudo o que for visto ou ouvido sobre a clínica e pacientes é confidencial.")
    incluir_residuos = st.checkbox("☣️ Incluir normas de descarte de resíduos biológicos", value=False, help="Proíbe a equipa de limpeza de manipular lixo hospitalar e agulhas.")
    incluir_multas = st.checkbox("⚖️ Incluir penalidades gradativas (RNC)", value=False, help="Estabelece um sistema justo de advertências e multas progressivas em caso de falhas leves.")
    incluir_nao_exclusividade = st.checkbox("🤝 Incluir declaração de Não Exclusividade", value=False, help="Deixa claro que a sua empresa de limpeza é livre para atender outros clientes.")
    incluir_materiais = st.checkbox("🧹 Incluir regra de Fornecimento Próprio de Materiais/EPIs (Cláusula 1ª, § 4º)", value=False, help="Define que a sua empresa arca com todos os custos de vassouras, detergentes e EPIs.")
    incluir_trabalhista = st.checkbox("🛡️ Incluir blindagem contra Vínculo Trabalhista (Cláusula 4ª)", value=False, help="Se algum dos seus funcionários processar a clínica, a sua empresa assume os custos.")
    incluir_renovacao = st.checkbox("🔄 Incluir regra de Renovação Automática", value=False, help="O contrato renova-se sozinho ao fim de 12 meses.")
    incluir_sabados = st.checkbox("📅 Incluir trabalho aos Sábados (Cláusula 2ª)", value=False, help="Define que a limpeza ocorre de segunda a sábado. Desmarque se for apenas de segunda a sexta.") # Mantive True por ser o seu padrão
    incluir_emergencia = st.checkbox("🚨 Incluir regras para chamados de Emergência/Orçamento Extra", value=False, help="Obriga a clínica a aprovar orçamentos por escrito antes de limpezas extras.")

    st.write("---")
    
    if st.button("Próximo Passo: Revisar ➡️", type="primary"):
        # Guarda os dados do Contratante (Cliente)
        st.session_state.nome_contratante = nome_contratante
        st.session_state.cnpj_contratante = cnpj_contratante
        st.session_state.endereco_contratante = endereco_contratante
        st.session_state.repr_contratante = repr_contratante
        st.session_state.rg_repr_contratante = rg_repr_contratante
        st.session_state.cpf_repr_contratante = cpf_repr_contratante
        
        # Guarda os dados da Contratada para não os perder NUNCA
        st.session_state.nome_contratada = nome_contratada
        st.session_state.cnpj_contratada = cnpj_contratada
        st.session_state.endereco_contratada = endereco_contratada
        st.session_state.repr_contratada = repr_contratada
        st.session_state.rg_repr_contratada = rg_repr_contratada
        st.session_state.cpf_repr_contratada = cpf_repr_contratada
        
        st.session_state.prazo_meses = prazo_meses
        st.session_state.data_assinatura_raw = data_assinatura 
        st.session_state.data_formatada = data_assinatura.strftime("%d de %B de %Y")
        st.session_state.foro_cidade = foro_cidade
        st.session_state.dia_pagamento = dia_pagamento
        st.session_state.dias_cancelamento = dias_cancelamento
        st.session_state.dias_servico = dias_servico
        st.session_state.indice_reajuste = indice_reajuste
        
        st.session_state.incluir_sigilo = incluir_sigilo
        st.session_state.incluir_residuos = incluir_residuos
        st.session_state.incluir_multas = incluir_multas
        st.session_state.incluir_nao_exclusividade = incluir_nao_exclusividade
        st.session_state.incluir_materiais = incluir_materiais
        st.session_state.incluir_trabalhista = incluir_trabalhista
        st.session_state.incluir_renovacao = incluir_renovacao
        st.session_state.incluir_sabados = incluir_sabados
        st.session_state.incluir_emergencia = incluir_emergencia
        
        st.session_state.etapa = 2 
        st.rerun() 

# ==========================================
# TELA 2: A REVISÃO COMPLETADA (SIM OU NÃO)
# ==========================================
if st.session_state.etapa == 2:
    st.title("🧐 Revisão do Contrato")
    st.warning("Verifique se todas as informações estão corretas. O documento será gerado com estes dados.")
    
    st.subheader("1. Qualificação das Partes")
    col_rev1, col_rev2 = st.columns(2)
    with col_rev1:
        st.markdown(f"**CONTRATANTE:**\n"
                    f"- **Nome:** {st.session_state.nome_contratante}\n"
                    f"- **CNPJ:** {st.session_state.cnpj_contratante}\n"
                    f"- **Endereço:** {st.session_state.endereco_contratante}\n"
                    f"- **Representante:** {st.session_state.repr_contratante} (RG: {st.session_state.rg_repr_contratante} | CPF: {st.session_state.cpf_repr_contratante})")
    with col_rev2:
        st.markdown(f"**CONTRATADA:**\n"
                    f"- **Nome:** {st.session_state.nome_contratada}\n"
                    f"- **CNPJ:** {st.session_state.cnpj_contratada}\n"
                    f"- **Endereço:** {st.session_state.endereco_contratada}\n"
                    f"- **Representante:** {st.session_state.repr_contratada} (RG: {st.session_state.rg_repr_contratada} | CPF: {st.session_state.cpf_repr_contratada})")

    st.divider()

    st.subheader("2. Dados Financeiros e Operacionais")
    col_rev3, col_rev4, col_rev5 = st.columns(3)
    with col_rev3:
        st.markdown(f"- **Valor Mensal:** R$ {st.session_state.valor_mensal}\n"
                    f"- **Prazo:** {st.session_state.prazo_meses} meses\n"
                    f"- **Multa Máxima:** R$ {st.session_state.multa_maxima}")
    with col_rev4:
        st.markdown(f"- **Dia de Pagamento:** {st.session_state.dia_pagamento}\n"
                    f"- **Aviso Cancelamento:** {st.session_state.dias_cancelamento} dias\n"
                    f"- **Dias de Serviço:** {st.session_state.dias_servico}")
    with col_rev5:
        st.markdown(f"- **Reajuste:** {st.session_state.indice_reajuste}\n"
                    f"- **Data:** {st.session_state.data_formatada}\n"
                    f"- **Foro:** {st.session_state.foro_cidade}")

    st.divider()

    st.subheader("3. Cláusulas Opcionais Selecionadas")
    clausulas_ativas = []
    if st.session_state.incluir_sigilo: clausulas_ativas.append("Confidencialidade (NDA)")
    if st.session_state.incluir_residuos: clausulas_ativas.append("Descarte de resíduos biológicos")
    if st.session_state.incluir_multas: clausulas_ativas.append("Penalidades gradativas (RNC)")
    if st.session_state.incluir_nao_exclusividade: clausulas_ativas.append("Não Exclusividade")
    if st.session_state.incluir_materiais: clausulas_ativas.append("Fornecimento Próprio de Materiais/EPIs")
    if st.session_state.incluir_trabalhista: clausulas_ativas.append("Blindagem contra Vínculo Trabalhista")
    if st.session_state.incluir_renovacao: clausulas_ativas.append("Renovação Automática")
    if st.session_state.incluir_sabados: clausulas_ativas.append("Trabalho aos Sábados")
    if st.session_state.incluir_emergencia: clausulas_ativas.append("Chamados de Emergência/Orçamento Extra")

    if clausulas_ativas:
        for c in clausulas_ativas:
            st.markdown(f"- ✅ {c}")
    else:
        st.info("Nenhuma cláusula opcional foi selecionada para este contrato.")
    
    st.write("---")
    st.subheader("O contrato está revisado e aprovado?")
    
    col_nao, col_sim = st.columns(2)
    with col_nao:
        if st.button("❌ Não, voltar e editar", use_container_width=True):
            st.session_state.etapa = 1
            st.rerun()
            
    with col_sim:
        if st.button("✅ Sim, Gerar Documento", type="primary", use_container_width=True):
            st.session_state.etapa = 3
            st.rerun()

# ==========================================
# TELA 3: GERAR E BAIXAR O ARQUIVO
# ==========================================
if st.session_state.etapa == 3:
    st.title("🎉 Seu Contrato está Pronto!")
    
    valor_texto = st.session_state.valor_mensal.replace('.', '').replace(',', '.')
    
    try:
        valor_numero = float(valor_texto)
        multa_10_num = valor_numero * 0.10
        multa_30_num = valor_numero * 0.30
        
        multa_10_formatada = "{:,.2f}".format(multa_10_num).replace(',', 'X').replace('.', ',').replace('X', '.')
        multa_30_formatada = "{:,.2f}".format(multa_30_num).replace(',', 'X').replace('.', ',').replace('X', '.')
    except ValueError:
        multa_10_formatada = "[Erro no cálculo]"
        multa_30_formatada = "[Erro no cálculo]"

    contexto = {
        'nome_contratante': st.session_state.nome_contratante,
        'cnpj_contratante': st.session_state.cnpj_contratante,
        'endereco_contratante': st.session_state.endereco_contratante,
        'repr_contratante': st.session_state.repr_contratante,
        'rg_repr_contratante': st.session_state.rg_repr_contratante,
        'cpf_repr_contratante': st.session_state.cpf_repr_contratante,
        'nome_contratada': st.session_state.nome_contratada,
        'cnpj_contratada': st.session_state.cnpj_contratada,
        'endereco_contratada': st.session_state.endereco_contratada,
        'repr_contratada': st.session_state.repr_contratada,
        'rg_repr_contratada': st.session_state.rg_repr_contratada,
        'cpf_repr_contratada': st.session_state.cpf_repr_contratada,
        
        'valor_mensal': st.session_state.valor_mensal,
        'multa_10': multa_10_formatada,
        'multa_30': multa_30_formatada,
        'multa_maxima': st.session_state.multa_maxima,
        'dia_pagamento': st.session_state.dia_pagamento,
        'prazo_meses': st.session_state.prazo_meses,
        'dias_cancelamento': st.session_state.dias_cancelamento,
        'dias_servico': st.session_state.dias_servico,
        'indice_reajuste': st.session_state.indice_reajuste,
        
        'data_assinatura': st.session_state.data_formatada,
        'foro_cidade': st.session_state.foro_cidade,
        
        'incluir_sigilo': st.session_state.incluir_sigilo,
        'incluir_residuos': st.session_state.incluir_residuos,
        'incluir_multas': st.session_state.incluir_multas,
        'incluir_nao_exclusividade': st.session_state.incluir_nao_exclusividade,
        'incluir_materiais': st.session_state.incluir_materiais,
        'incluir_trabalhista': st.session_state.incluir_trabalhista,
        'incluir_renovacao': st.session_state.incluir_renovacao,
        'incluir_sabados': st.session_state.incluir_sabados,
        'incluir_emergencia': st.session_state.incluir_emergencia
    }
    
    try:
        doc = DocxTemplate("template_padrao.docx")
        doc.render(contexto)
        
        buffer = io.BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        
        st.success("✅ O documento foi gerado com sucesso!")
        
        st.download_button(
            label="📥 Baixar Contrato Final (.docx)", 
            data=buffer, 
            file_name=f"Contrato_{st.session_state.nome_contratante}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        
    except Exception as e:
        st.error(f"Erro ao gerar o documento. Detalhe do erro: {e}")
        
    st.write("---")
    
    # --- BOTÃO NOVO CONTRATO ATUALIZADO ---
    if st.button("Fazer um Novo Contrato"):
        # Apaga todos os dados da memória, EXCETO os dados da sua empresa (Contratada) e os campos de moeda limpos
        chaves_para_apagar = []
        for key in list(st.session_state.keys()):
            if "contratada" not in key and key not in ["valor_mensal", "multa_maxima"]:
                chaves_para_apagar.append(key)
                
        for key in chaves_para_apagar:
            del st.session_state[key]
            
        # Zera os valores de dinheiro para um novo cliente, mas mantém o formato para não dar erro
        st.session_state.valor_mensal = '0,00'
        st.session_state.multa_maxima = '0,00'
        
        st.rerun()