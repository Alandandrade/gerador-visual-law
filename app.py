from datetime import date
import base64
import locale
import streamlit as st
import streamlit.components.v1 as components

# Configuração do idioma para datas em Português
try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
except:
    pass

st.set_page_config(page_title="GERADOR DE CONTRATOS VISUAL LAW", layout="wide")

# Estilo global para garantir que os botões tenham apenas a largura do próprio texto
st.markdown("""
    <style>
    div.stButton > button {
        width: fit-content !important;
        padding-left: 16px !important;
        padding-right: 16px !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# INICIALIZAÇÃO DA MEMÓRIA (PERSISTÊNCIA TOTAL)
# ==========================================
if "etapa" not in st.session_state: 
    st.session_state.etapa = 1

chaves_iniciais = {
    'nome_contratante': 'Bella Estética', 'cnpj_contratante': '125121444512', 'endereco_contratante': 'Rua Brasil nº154, Lorena/SP',
    'repr_contratante': '54658454654', 'rg_repr_contratante': '546545646545', 'cpf_repr_contratante': '5854849845454',
    'prazo_meses': '12', 'dia_pagamento': '10', 'dias_cancelamento': '30',
    'dias_servico': 'Seg. a sáb.', 'indice_reajuste': 'IPCA / IBGE', 'foro_cidade': 'Lorena/SP',
    'ambientes_limpeza': 'Recepção, salas de atendimento, consultórios, banheiros e áreas comuns.',
    'check_nao_exclusividade': True,
    'valor_mensal': '1.000,00', 'multa_maxima': '1.000,00',
    'nome_contratada': 'Maxx Limpeza', 'cnpj_contratada': '2156165516', 'endereco_contratada': 'Rua das Flores nº 100, Lorena/SP',
    'repr_contratada': 'Maria Silva', 'rg_repr_contratada': '1516156516516', 'cpf_repr_contratada': '5561615651',
    'logo_b64': None, 'editando_idx': None
}

for k, v in chaves_iniciais.items():
    if k not in st.session_state:
        st.session_state[k] = v
    else:
        st.session_state[k] = st.session_state[k]

if 'banco_clausulas' not in st.session_state:
    st.session_state.banco_clausulas = [
        {"titulo": "CONFIDENCIALIDADE (NDA)", "juridico": "A CONTRATADA assume a obrigação irrevogável de guardar sigilo e manter total confidencialidade sobre todas as informações corporativas ou de pacientes a que tiver acesso, sob pena de responder por perdas e danos.", "visual": "Tudo o que você vir ou souber sobre a clínica e seus pacientes é confidencial. É proibido compartilhar ou divulgar.", "ativa": True, "categoria": "sigilo", "checklist": "Entendi o sigilo e não divulgar dados."},
        {"titulo": "NÃO DESCARTE DE RESÍDUOS BIOLÓGICOS", "juridico": "É expressamente vedado ao profissional designado o manuseio, segregação ou recolhimento de resíduos perfurocortantes soltos ou resíduos biológicos diretamente nas salas de procedimento, devendo a clínica gerir este descarte.", "visual": "É PROIBIDO mexer em agulhas ou objetos cortantes soltos e em lixo biológico nas salas de procedimento. A equipe da clínica cuida disso.", "ativa": True, "categoria": "saude", "checklist": "Entendi as regras de descarte de resíduos biológicos."},
        {"titulo": "PENALIDADES GRADATIVAS (RNC)", "juridico": "O descumprimento sujeita a infratora a: I - Emissão de RNC e adequação; II - Reincidência: multa de 10% a 30%; III - Infrações graves: rescisão imediata e multa máxima estipulada.", "visual": "1º erro: Relatório e corrige sem multa. 2º erro: Multa de 10% a 30%. Erro grave (ex: quebrar sigilo): Fim do contrato e multa máxima.", "ativa": True, "categoria": "dinheiro", "checklist": "Entendi como funcionam as multas."},
        {"titulo": "FORNECIMENTO PRÓPRIO DE MATERIAIS", "juridico": "A CONTRATADA é a única responsável pelo fornecimento de todos os materiais, produtos de higienização, ferramentas e Equipamentos de Proteção Individual (EPIs), assumindo integralmente os custos de sua atividade.", "visual": "Você paga e traz tudo: produtos, materiais, ferramentas, equipamentos e EPIs. Os custos e riscos do seu negócio são seus.", "ativa": True, "categoria": "custos", "checklist": "Entendi que os materiais são fornecimento próprio da Contratada."},
        {"titulo": "SEM VÍNCULO DE EMPREGO", "juridico": "As partes reforçam que não existe vínculo empregatício. Caso a CONTRATANTE seja acionada judicialmente por profissional da CONTRATADA, esta obriga-se a assumir a responsabilidade por eventuais condenações e excluir a clínica da lide.", "visual": "Não há vínculo de emprego. Se alguém enviado por você processar a clínica, você assume todos os custos, condenações e advogados no lugar da clínica.", "ativa": True, "categoria": "autonomia", "checklist": "Entendi que não há vínculo de emprego."},
        {"titulo": "RENOVAÇÃO AUTOMÁTICA", "juridico": "O contrato renova-se automaticamente por iguais períodos, caso não haja manifestação expressa em contrário por qualquer das partes.", "visual": "O contrato renova sozinho depois do prazo, se ninguém avisar que quer parar.", "ativa": True, "categoria": "prazo", "checklist": "Entendi as regras de renovação automática."},
        {"titulo": "TRABALHO AOS SÁBADOS", "juridico": "Fica estabelecido que os serviços contemplam a execução regular aos sábados, dentro da escala de horários estipulada.", "visual": "O serviço é realizado incluindo sábados.", "ativa": True, "categoria": "prazo", "checklist": "Entendi que o trabalho inclui os sábados."},
        {"titulo": "CHAMADOS DE EMERGÊNCIA", "juridico": "Eventuais chamados para atendimentos emergenciais fora dos dias pactuados dependerão de prévio acordo e orçamento por escrito aprovado pela CONTRATANTE.", "visual": "Chamado de emergência fora dos dias combinados: só com acordo e orçamento aprovados por escrito.", "ativa": True, "categoria": "atencao", "checklist": "Entendi as regras para chamados de emergência."}
    ]

if 'data_assinatura' not in st.session_state:
    st.session_state.data_assinatura = date.today()
else:
    st.session_state.data_assinatura = st.session_state.data_assinatura

cores = {
    "objeto": "#496376", "autonomia": "#249d81", "custos": "#296bb1", "sigilo": "#7250a1",
    "saude": "#b83280", "dinheiro": "#1f7b4c", "prazo": "#5c6d7a", "atencao": "#dda02b",
    "declaracoes": "#e8aa36"
}

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

def limpar_campos_cliente():
    st.session_state.nome_contratante = ''
    st.session_state.cnpj_contratante = ''
    st.session_state.endereco_contratante = ''
    st.session_state.repr_contratante = ''
    st.session_state.rg_repr_contratante = ''
    st.session_state.cpf_repr_contratante = ''
    st.session_state.ambientes_limpeza = ''
    st.session_state.valor_mensal = '0,00'
    st.session_state.multa_maxima = '0,00'
    st.session_state.prazo_meses = ''
    st.session_state.dia_pagamento = ''
    st.session_state.dias_cancelamento = ''
    st.session_state.dias_servico = ''
    st.session_state.indice_reajuste = ''
    st.session_state.foro_cidade = ''
    st.session_state.data_assinatura = date.today()
    st.session_state.check_nao_exclusividade = False
    
    for i, c in enumerate(st.session_state.banco_clausulas):
        c['ativa'] = False
        if f'chk_{i}' in st.session_state:
            st.session_state[f'chk_{i}'] = False

    st.session_state.etapa = 1

# ==========================================
# TELA 1: FORMULÁRIO DE CRIAÇÃO DO CONTRATO
# ==========================================
if st.session_state.etapa == 1:
    col_titulo, col_limpar = st.columns([0.75, 0.25])
    col_titulo.title("GERADOR DE CONTRATOS VISUAL LAW")
    
    col_limpar.button(" Limpar Campos (Novo Cliente)", on_click=limpar_campos_cliente)

    st.warning("ALUNOS 6º SEMESTRE DE DIREITO SERRA DOURADA")

    st.subheader("QUALIFICAÇÃO DAS PARTES")
    logo_file = st.file_uploader("Carregar Logo da Empresa (Opcional)", type=["png", "jpg", "jpeg", "bmp"])
    if logo_file is not None:
        b64_logo = base64.b64encode(logo_file.getvalue()).decode()
        st.session_state.logo_b64 = f"data:image/{logo_file.type.split('/')[-1]};base64,{b64_logo}"
        st.success("Logo carregada com sucesso!")
    elif st.session_state.logo_b64:
        st.info("Uma logo já está salva e será usada na impressão.")

    st.write("---")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Dados do Contratante (Cliente)")
        st.text_input("Nome/Razão Social", key='nome_contratante')
        st.text_input("CNPJ / CPF", key='cnpj_contratante')
        st.text_input("Endereço Completo", key='endereco_contratante')
        st.text_input("Nome do Representante Legal", key='repr_contratante')
        st.text_input("RG do Representante", key='rg_repr_contratante')
        st.text_input("CPF do Representante", key='cpf_repr_contratante')

    with col2:
        st.markdown("#### Dados da Contratada (Sua Empresa)")
        st.text_input("Nome/Razão Social", key="nome_contratada")
        st.text_input("CNPJ", key="cnpj_contratada")
        st.text_input("Endereço Completo", key="endereco_contratada")
        st.text_input("Nome do Representante Legal", key="repr_contratada")
        st.text_input("RG do Representante", key="rg_repr_contratada")
        st.text_input("CPF do Representante", key="cpf_repr_contratada")

    st.write("---")
    st.subheader("DEFINIÇÕES")
    col3, col4, col5 = st.columns(3)
    with col3:
        st.text_input("Valor Mensal (R$)", key="valor_mensal", on_change=formatar_moeda, args=("valor_mensal",))
        st.text_input("Prazo do Contrato (meses)", key='prazo_meses')
        st.text_input("Multa Máxima (R$)", key="multa_maxima", on_change=formatar_moeda, args=("multa_maxima",))
    with col4:
        st.text_input("Dia de Pagamento (Ex: 10)", key='dia_pagamento')
        st.text_input("Aviso de Cancelamento (dias)", key='dias_cancelamento')
        st.text_input("Dias de Serviço", key='dias_servico')
    with col5:
        st.text_input("Índice de Reajuste", key='indice_reajuste')
        st.date_input("Data de Assinatura", key='data_assinatura')
        st.text_input("Cidade do Foro", key='foro_cidade')
        st.checkbox("Incluir 'Não Exclusividade' no quadro 1", key='check_nao_exclusividade')

    st.markdown("#### ESCOPO DAS ATIVIDADES")
    st.text_area("Descreva os ambientes (Ex: Recepção, 2 banheiros, copa, sala de espera e 3 consultórios). Deixe em branco se não quiser esta cláusula no contrato.", 
                 key="ambientes_limpeza", height=68)

    st.write("---")
    st.subheader("3. Banco de Cláusulas (Opcionais)")
    st.write("Selecione quais regras extras farão parte do contrato. Adicione, edite ou exclua cláusulas para usar no futuro.")
    
    for i, clausula in enumerate(st.session_state.banco_clausulas):
        # LAYOUT RESPONSIVO: Checkbox em uma coluna e botões agrupados em outra (lado a lado)
        c_check, c_btns = st.columns([0.7, 0.3])
        with c_check:
            is_checked = st.checkbox(f"📄 {clausula['titulo']}", value=clausula['ativa'], key=f"chk_{i}")
            st.session_state.banco_clausulas[i]['ativa'] = is_checked
        with c_btns:
            b_edit, b_del = st.columns(2)
            with b_edit:
                if st.button("✏️ Editar", key=f"btn_edit_{i}", use_container_width=True):
                    st.session_state.editando_idx = i
                    st.rerun()
            with b_del:
                if st.button("❌ Excluir", key=f"btn_del_{i}", use_container_width=True):
                    st.session_state.banco_clausulas.pop(i)
                    st.rerun()

    if st.session_state.editando_idx is not None:
        idx = st.session_state.editando_idx
        st.markdown("---")
        with st.container(border=True):
            st.markdown(f"#### ✏️ Editando a cláusula: {st.session_state.banco_clausulas[idx]['titulo']}")
            
            c_ed1, c_ed2 = st.columns(2)
            with c_ed1:
                novo_tit = st.text_input("Título da Cláusula", value=st.session_state.banco_clausulas[idx]['titulo'])
            with c_ed2:
                cat_atual = st.session_state.banco_clausulas[idx].get('categoria', 'atencao')
                opcoes_cat = ["objeto", "autonomia", "custos", "sigilo", "saude", "dinheiro", "prazo", "atencao"]
                nova_cat = st.selectbox("Categoria (Define a Cor no Design)", opcoes_cat, index=opcoes_cat.index(cat_atual) if cat_atual in opcoes_cat else 7)
            
            novo_jur = st.text_area("Texto Jurídico (Obrigação Formal)", value=st.session_state.banco_clausulas[idx]['juridico'], height=100)
            novo_vis = st.text_area("Texto Visual Law (Explicação para o cliente)", value=st.session_state.banco_clausulas[idx]['visual'], height=100)
            novo_checklist = st.text_input("Item para Checklist (Aparecerá se a cláusula for ativada)", value=st.session_state.banco_clausulas[idx].get('checklist', ''))
            
            cb1, cb2 = st.columns([0.2, 0.8])
            if cb1.button("💾 Salvar Alterações", type="primary"):
                st.session_state.banco_clausulas[idx]['titulo'] = novo_tit
                st.session_state.banco_clausulas[idx]['categoria'] = nova_cat
                st.session_state.banco_clausulas[idx]['juridico'] = novo_jur
                st.session_state.banco_clausulas[idx]['visual'] = novo_vis
                st.session_state.banco_clausulas[idx]['checklist'] = novo_checklist
                st.session_state.editando_idx = None
                st.success("Cláusula atualizada no banco!")
                st.rerun()
            if cb2.button("Cancelar Edição"):
                st.session_state.editando_idx = None
                st.rerun()

    with st.expander("➕ NOVA CLÁUSULA"):
        ntit = st.text_input("Título da Nova Regra")
        ncat = st.selectbox("Categoria Visual", ["Objeto", "Autonomia", "Custos", "Sigilo", "Saude", "Dinheiro", "Prazo", "Atencao"])
        njur = st.text_area("Texto Jurídico", placeholder="Ex: O contratante obriga-se a...")
        nvis = st.text_area("Texto Simplificado", placeholder="Ex: O cliente tem que pagar a taxa X...")
        nchk = st.text_input("Item para Checklist (Opcional)", placeholder="Ex: Entendi as condições de uso.")
        if st.button("Adicionar Regra"):
            if ntit.strip() != "":
                st.session_state.banco_clausulas.append({
                    "titulo": ntit, "juridico": njur, "visual": nvis, "ativa": True, "categoria": ncat, "checklist": nchk
                })
                st.success("Nova regra inserida na lista acima!")
                st.rerun()
            else:
                st.error("Insira pelo menos um título.")

    st.write("---")
    if st.button("Avançar para Visualização e Impressão ", type="primary"):
        st.session_state.data_formatada = st.session_state.data_assinatura.strftime("%d de %B de %Y")
        st.session_state.etapa = 2 
        st.rerun() 

# ==========================================
# TELA 2: PRÉ-VISUALIZAÇÃO DO CONTRATO E IMPRESSÃO (PDF)
# ==========================================
if st.session_state.etapa == 2:
    
    col_v, col_n = st.columns([0.25, 0.75])
    with col_v:
        if st.button("⬅ Voltar e Editar"):
            st.session_state.etapa = 1
            st.rerun()
    with col_n:
        st.button(" Finalizar e Limpar para Novo Cliente", on_click=limpar_campos_cliente)

    ambientes_limpeza = st.session_state.ambientes_limpeza.strip()
    dias_cancelamento = st.session_state.dias_cancelamento.strip()
    prazo_meses = st.session_state.prazo_meses.strip()
    valor_mensal = st.session_state.valor_mensal.strip()
    dia_pagamento = st.session_state.dia_pagamento.strip()
    dias_servico = st.session_state.dias_servico.strip()
    indice_reajuste = st.session_state.indice_reajuste.strip()
    multa_maxima = st.session_state.multa_maxima.strip()
    foro_cidade = st.session_state.foro_cidade.strip()

    try:
        val_num = float(valor_mensal.replace('.', '').replace(',', '.')) if valor_mensal else 0
        m10 = "{:,.2f}".format(val_num * 0.10).replace(',', 'X').replace('.', ',').replace('X', '.')
        m30 = "{:,.2f}".format(val_num * 0.30).replace(',', 'X').replace('.', ',').replace('X', '.')
    except ValueError:
        m10, m30 = "[Erro]", "[Erro]"

    logo_html = f'<img src="{st.session_state.logo_b64}" class="logo-img">' if st.session_state.logo_b64 else ''
    exclusividade_texto = "Não há" if getattr(st.session_state, 'check_nao_exclusividade', True) else "Há"

    items_minuto = []
    
    if valor_mensal not in ['', '0,00']:
        items_minuto.append(f'<td class="cel-min"><span class="tit-minuto">VALOR MENSAL</span><span class="val-destaque val-verde">R$ {valor_mensal}</span><span class="desc-info">pago pela clínica</span></td>')
    if dia_pagamento:
        items_minuto.append(f'<td class="cel-min"><span class="tit-minuto">PAGAMENTO</span><span class="val-destaque val-verde">Até o dia {dia_pagamento}</span><span class="desc-info">do mês seguinte</span></td>')
    if dias_servico:
        items_minuto.append(f'<td class="cel-min"><span class="tit-minuto">DIAS DE SERVIÇO</span><span class="val-destaque val-azul">{dias_servico}</span><span class="desc-info">conforme pactuado</span></td>')
    if prazo_meses:
        items_minuto.append(f'<td class="cel-min"><span class="tit-minuto">DURAÇÃO</span><span class="val-destaque val-azul">{prazo_meses} meses</span><span class="desc-info">renovação automática</span></td>')
    if dias_cancelamento:
        items_minuto.append(f'<td class="cel-min"><span class="tit-minuto">CANCELAR</span><span class="val-destaque val-azul">{dias_cancelamento} dias de aviso</span><span class="desc-info">sem multa</span></td>')
    if indice_reajuste:
        items_minuto.append(f'<td class="cel-min"><span class="tit-minuto">REAJUSTE</span><span class="val-destaque val-verde">{indice_reajuste}</span><span class="desc-info">anual</span></td>')
    if multa_maxima not in ['', '0,00']:
        items_minuto.append(f'<td class="cel-min"><span class="tit-minuto">MULTA MÁXIMA</span><span class="val-destaque val-verm">R$ {multa_maxima}</span><span class="desc-info">infrações graves</span></td>')
    if getattr(st.session_state, 'check_nao_exclusividade', False):
        items_minuto.append(f'<td class="cel-min"><span class="tit-minuto">EXCLUSIVIDADE</span><span class="val-destaque val-verde">{exclusividade_texto}</span><span class="desc-info">atendimento a terceiros</span></td>')
    if foro_cidade:
        items_minuto.append(f'<td class="cel-min"><span class="tit-minuto">FORO</span><span class="val-destaque val-azul">{foro_cidade}</span><span class="desc-info">resolução de disputas</span></td>')
        
    tabela_1_minuto_html = '<table class="tab-minuto">'
    for i in range(0, len(items_minuto), 3):
        tabela_1_minuto_html += "<tr>"
        tabela_1_minuto_html += items_minuto[i] if i < len(items_minuto) else '<td style="border: none;"></td>'
        tabela_1_minuto_html += items_minuto[i+1] if i+1 < len(items_minuto) else '<td style="border: none;"></td>'
        tabela_1_minuto_html += items_minuto[i+2] if i+2 < len(items_minuto) else '<td style="border: none;"></td>'
        tabela_1_minuto_html += "</tr>"
    tabela_1_minuto_html += '</table>'

    html_clausulas = ""
    num_c = 1
    
    tem_clausula = any(c.get('ativa', False) for c in st.session_state.banco_clausulas)
    
    if ambientes_limpeza or tem_clausula:
        
        html_clausulas += f"""
            <table class="tab-clausulas" style="margin-top: 15px; margin-bottom: 15px;">
                <tr class="tr-titulo" style="background-color: {cores['declaracoes']}; color: white;" id="sec-atencao"><td colspan="3">ANTES DE COMEÇAR | DECLARAÇÕES INICIAIS</td></tr>
                
                <tr>
                    <td class="col-par" style="background-color: {cores['declaracoes']}; color: white;">§ 1º</td>
                    <td class="col-jur" style="background-color: white;">Na data deste documento, é firmado o presente acordo de prestação de serviços entre as partes acima qualificadas, que declaram agir de livre e espontânea vontade, sem qualquer vício de consentimento.</td>
                    <td class="col-vis" style="background-color: white;">Nós dois escolhemos fechar este negócio. Ninguém está sendo forçado, pressionado ou enganado para assinar este documento.</td>
                </tr>

                <tr>
                    <td class="col-par" style="background-color: {cores['declaracoes']}; color: white;">§ 2º</td>
                    <td class="col-jur" style="background-color: white;">A Contratada declara ter sido devidamente esclarecida acerca da modalidade de sua contratação, estando ciente e aceitando expressamente a ausência de vínculo empregatício nesta relação jurídica.</td>
                    <td class="col-vis" style="background-color: white;">Você atuará de forma independente. Isso significa que você é um(a) <b>prestador(a) de serviços</b>, e não um funcionário (CLT) da contratante.</td>
                </tr>
                
                <tr>
                    <td class="col-par" style="background-color: {cores['declaracoes']}; color: white;">§ 3º</td>
                    <td class="col-jur" style="background-color: white;">As partes declaram que dialogaram e acertaram a forma de prestação do serviço e a sua justa remuneração. As regras e condições estipuladas neste instrumento refletem exatamente o que foi combinado, sendo válidas como a real e expressa vontade das partes.</td>
                    <td class="col-vis" style="background-color: white;">Nós conversamos previamente sobre como o serviço será feito e qual será o valor pago. Tudo o que está escrito nas regras abaixo é exatamente a nossa vontade e o que combinamos.</td>
                </tr>
            </table>
        """
        
        html_clausulas += '<table class="tab-clausulas">'
        
        if ambientes_limpeza:
            html_clausulas += f"""
                <tr class="tr-titulo" style="background-color: {cores['objeto']}; color: white;" id="sec-objeto"><td colspan="3">CLÁUSULA {num_c}ª | O QUE SERÁ FEITO</td></tr>
                <tr>
                    <td class="col-par" style="background-color: {cores['objeto']}; color: white;">Caput</td>
                    <td class="col-jur">A CONTRATADA prestará a CONTRATANTE a prestação de serviço referente a limpeza e a higienização das instalações do local, englobando especificamente: {ambientes_limpeza}</td>
                    <td class="col-vis">Você vai limpar e higienizar os seguintes ambientes: {ambientes_limpeza}</td>
                </tr>
            """
            num_c += 1

        if dias_servico:
            html_clausulas += f"""
                <tr class="tr-titulo" style="background-color: {cores['prazo']}; color: white;" id="sec-prazo"><td colspan="3">CLÁUSULA {num_c}ª | QUANDO SERÁ FEITO</td></tr>
                <tr>
                    <td class="col-par" style="background-color: {cores['prazo']}; color: white;">Caput</td>
                    <td class="col-jur">Os serviços de que trata a Cláusula Primeira serão prestados conforme pactuado ({dias_servico}), cabendo à CONTRATADA organizar sua escala interna para higienização prévia aos atendimentos.</td>
                    <td class="col-vis">O serviço é feito nos dias combinados ({dias_servico}). Você organiza sua escala para que o local esteja pronto antes de abrir.</td>
                </tr>
            """
            num_c += 1

        if valor_mensal not in ['', '0,00'] or dia_pagamento:
            html_clausulas += f"""
                <tr class="tr-titulo" style="background-color: {cores['dinheiro']}; color: white;" id="sec-dinheiro"><td colspan="3">CLÁUSULA {num_c}ª | QUANTO E COMO SERÁ PAGO</td></tr>
            """
            if valor_mensal not in ['', '0,00']:
                html_clausulas += f"""
                <tr>
                    <td class="col-par" style="background-color: {cores['dinheiro']}; color: white;">Caput</td>
                    <td class="col-jur">A CONTRATANTE pagará à CONTRATADA o valor mensal de R$ {valor_mensal}, a ser creditado em conta bancária de titularidade jurídica da CONTRATADA.</td>
                    <td class="col-vis">O cliente paga R$ {valor_mensal} por mês, creditado exclusivamente na conta do CNPJ da sua empresa.</td>
                </tr>
                """
            if dia_pagamento:
                num_par = "§ 1º" if valor_mensal not in ['', '0,00'] else "Caput"
                html_clausulas += f"""
                <tr>
                    <td class="col-par" style="background-color: {cores['dinheiro']}; color: white;">{num_par}</td>
                    <td class="col-jur">O pagamento será realizado mensalmente até o dia {dia_pagamento} do mês subsequente, mediante apresentação de Nota Fiscal acompanhada das certidões de regularidade (quando aplicável).</td>
                    <td class="col-vis">O pagamento sai até o dia {dia_pagamento} do mês seguinte. Antes, você entrega a Nota Fiscal e documentos exigidos.</td>
                </tr>
                """
            num_c += 1

        for c in st.session_state.banco_clausulas:
            if c.get('ativa', False):
                cat = c.get('categoria', 'atencao')
                cor = cores.get(cat.lower(), cores['atencao'])
                
                jur_text = c['juridico']
                if "10%" in jur_text and "30%" in jur_text and multa_maxima not in ['', '0,00']:
                    jur_text = f"O descumprimento sujeita a infratora a: I - Emissão de RNC e adequação; II - Reincidência: multa de 10% (R$ {m10}) a 30% (R$ {m30}); III - Infrações graves: rescisão e multa máxima de R$ {multa_maxima}."
                    
                html_clausulas += f"""
                <tr class="tr-titulo" style="background-color: {cor}; color: white;" id="sec-{cat}"><td colspan="3">CLÁUSULA {num_c}ª | {c['titulo'].upper()}</td></tr>
                <tr>
                    <td class="col-par" style="background-color: {cor}; color: white;">Caput</td>
                    <td class="col-jur">{jur_text}</td>
                    <td class="col-vis">{c['visual']}</td>
                </tr>
                """
                num_c += 1
                
        if dias_cancelamento:
            html_clausulas += f"""
                <tr class="tr-titulo" style="background-color: {cores['prazo']}; color: white;"><td colspan="3">CLÁUSULA {num_c}ª | CANCELAMENTO</td></tr>
                <tr>
                    <td class="col-par" style="background-color: {cores['prazo']}; color: white;">Caput</td>
                    <td class="col-jur">O contrato poderá ser rescindido sem justa causa mediante aviso prévio por escrito com antecedência de {dias_cancelamento} dias, sem incidência de multa.</td>
                    <td class="col-vis">Qualquer um pode cancelar avisando por escrito com {dias_cancelamento} dias de antecedência. Não há multa nesse caso.</td>
                </tr>
            """
            num_c += 1
            
        if prazo_meses or indice_reajuste:
            html_clausulas += f"""
                <tr class="tr-titulo" style="background-color: {cores['prazo']}; color: white;"><td colspan="3">CLÁUSULA {num_c}ª | DURAÇÃO E REAJUSTE</td></tr>
            """
            txt_jur = "O presente contrato vigorará "
            txt_vis = "O contrato "
            
            if prazo_meses:
                txt_jur += f"pelo prazo de {prazo_meses} meses"
                txt_vis += f"dura {prazo_meses} meses"
                if indice_reajuste:
                    txt_jur += f", reajustados anualmente com base no {indice_reajuste}"
                    txt_vis += f", e reajusta uma vez por ano pela inflação"
            elif indice_reajuste:
                txt_jur += f"com valores reajustados anualmente com base no {indice_reajuste}"
                txt_vis += f"tem reajuste anual pela inflação"

            html_clausulas += f"""
                <tr>
                    <td class="col-par" style="background-color: {cores['prazo']}; color: white;">Caput</td>
                    <td class="col-jur">{txt_jur}.</td>
                    <td class="col-vis">{txt_vis}.</td>
                </tr>
            """
            num_c += 1
            
        html_clausulas += "</table>" 

    foro_html = ""
    if foro_cidade:
        foro_html = f"""
        <div class="header-section" style="margin-top: 20px;">FORO | ONDE RESOLVER DISPUTAS</div>
        <table class="tab-clausulas" style="margin-bottom: 20px;">
            <tr>
                <td class="col-par" style="width: 10%; background-color: {cores['atencao']}; color: white;">Foro</td>
                <td class="col-jur" style="width: 45%;">Fica eleito o foro da Comarca de {foro_cidade} para dirimir eventuais litígios.</td>
                <td class="col-vis" style="width: 45%;">Se surgir conflito, o caso vai para a Justiça de {foro_cidade}.</td>
            </tr>
        </table>
        """
        
    check_html = ""
    if valor_mensal not in ['', '0,00']:
        check_html += f'<li>&#9744; Entendi quanto vou receber (R$ {valor_mensal} por mês). <span class="rubrica">Rubrica: _____________</span></li>'
    if dia_pagamento:
        check_html += '<li>&#9744; Entendi as regras de emissão de Nota Fiscal. <span class="rubrica">Rubrica: _____________</span></li>'
    if dias_cancelamento:
        check_html += '<li>&#9744; Entendi como funcionam as regras de cancelamento. <span class="rubrica">Rubrica: _____________</span></li>'

    for c in st.session_state.banco_clausulas:
        if c.get('ativa', False) and c.get('checklist', '').strip() != "":
            check_html += f'<li>&#9744; {c["checklist"]} <span class="rubrica">Rubrica: _____________</span></li>'

    html_iframe_completo = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Imprimir Contrato</title>
        <style>
            body, html {{ 
                margin: 0; padding: 0; background-color: #f4f4f4; 
                font-family: Arial, sans-serif; display: flex; flex-direction: column; align-items: center;
                scroll-behavior: smooth;
            }}
            .barra-ferramentas {{
                width: 100%; max-width: 800px; display: flex; justify-content: space-between; align-items: center;
                margin: 20px 0; padding: 15px 20px; background-color: white; border-radius: 8px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1); box-sizing: border-box;
            }}
            .btn-imprimir {{
                width: fit-content; background-color: #FF4B4B; color: white; padding: 10px 18px; 
                border: none; border-radius: 5px; font-weight: bold; font-size: 14px; 
                cursor: pointer; transition: 0.2s; white-space: nowrap;
            }}
            .btn-imprimir:hover {{ background-color: #ff3333; }}
            .dica {{ font-size: 11px; color: #666; max-width: 65%; }}
            
            /* WRAPPER PARA O A4 */
            .page-wrapper {{
                width: 100%;
                display: flex;
                justify-content: center;
                overflow: hidden;
            }}

            .folha-contrato {{ 
                background-color: white; color: black; padding: 30px 40px 50px 40px; margin-bottom: 20px;
                width: 794px; /* Largura A4 em pixels */
                min-height: 1123px; /* Altura A4 em pixels */
                box-sizing: border-box; box-shadow: 0 2px 10px rgba(0,0,0,0.1); 
                font-size: 11px; line-height: 1.4; 
                transform-origin: top left;
            }}
            
            .logo-img {{ max-width: 220px; max-height: 100px; display: block; margin: 0 auto 15px auto; }}
            .titulo-doc {{ text-align: center; color: #1a365d; margin-bottom: 3px; font-family: Arial; font-size: 16px; }}
            .subtitulo-doc {{ text-align: center; color: #666; margin-top: 0; margin-bottom: 15px; font-size: 12px; }}
            .header-section {{ font-weight: bold; color: #1a365d; border-bottom: 2px solid #1a365d; margin-top: 15px; margin-bottom: 8px; font-size: 13px; padding-bottom: 2px;}}
            
            table {{ width: 100%; border-collapse: collapse; margin-bottom: 10px; }}
            .tab-assina th {{ padding: 6px; color: white; text-align: left; font-size: 10px; }}
            .tab-assina td {{ padding: 8px; background-color: #f8f9fa; vertical-align: top; border: 2px solid white; line-height: 1.2; }}
            .th-cli {{ background-color: #1a365d; }}
            .th-emp {{ background-color: #2b9eb3; }}
            
            .tab-minuto td {{ padding: 6px; border: 1px solid #ddd; vertical-align: top; width: 33.33%; }}
            .desc-info {{ font-size: 9px; color: #555; display: block; }}
            .val-destaque {{ font-size: 13px; font-weight: bold; display: block; margin-top: 2px; margin-bottom: 2px; }}
            .val-verde {{ color: #228B22; }}
            .val-azul {{ color: #2b6cb0; }}
            .val-verm {{ color: #B22222; }}
            .tit-minuto {{ font-weight: bold; color: #000; font-size: 10px; display: block; }}
            .cel-min {{ border-right: 1px solid #ddd; padding: 6px; vertical-align: top; }}
            
            .menu-cores td {{ 
                width: 25%; text-align: center; padding: 6px 3px; border: 2px solid white; 
                cursor: pointer; transition: 0.3s; color: white;
            }}
            .menu-cores td:hover {{ opacity: 0.8; }}
            .menu-cores b {{ font-size: 11px; }}

            .box-importante {{ background-color: #fdf6e3; border-left: 5px solid #df9d2d; padding: 10px 15px; font-size: 11px; margin: 10px 0; }}
            
            .tab-clausulas th, .tab-clausulas td {{ border: 1px solid #ddd; padding: 6px; vertical-align: top; }}
            .tr-titulo {{ font-weight: bold; text-align: left; font-size: 12px; }}
            .col-par {{ width: 10%; font-weight: bold; font-size: 10px; text-align: center; vertical-align: middle;}}
            .col-jur {{ width: 45%; text-align: justify; background-color: white;}}
            .col-vis {{ width: 45%; text-align: justify; background-color: white;}}
            .th-jur {{ background-color: #e2e8f0; text-align: center; font-size: 11px; }}
            
            .tab-assinaturas {{ text-align: center; margin-bottom: 8px; }}
            .tab-assinaturas td {{ border: none; padding: 0 10px; vertical-align: top; width: 50%; }}
            .bloco-assinatura {{ padding: 0 10px; font-size: 11px; }}
            .linha-assina {{ border-top: 1px solid black; width: 100%; margin: 0 auto 4px auto; }}
            .rubrica {{ float: right; margin-right: 30px; font-weight: bold; }}

            @media print {{
                * {{ -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }}
                @page {{ margin: 0.8cm; size: A4 portrait; }}
                body, html {{ background-color: white !important; margin: 0 !important; padding: 0 !important; }}
                .barra-ferramentas {{ display: none !important; }}
                .page-wrapper {{ 
                    display: block !important; 
                    width: 100% !important; 
                    overflow: visible !important;
                    height: auto !important;
                }}
                .folha-contrato {{ 
                    padding: 0 !important; margin: 0 !important; box-shadow: none !important; 
                    width: 100% !important; max-width: 100% !important; box-sizing: border-box !important;
                    transform: none !important;
                    min-height: auto !important;
                }}

                table {{ page-break-inside: auto !important; }}
                tr, td, th {{ page-break-inside: avoid !important; }}
                .tr-titulo {{ page-break-after: avoid !important; }}
                .header-section {{ page-break-after: avoid !important; }}
                .bloco-assinatura, .box-importante {{ page-break-inside: avoid !important; }}
                .menu-cores td {{ pointer-events: none; }}
            }}
        </style>
    </head>
    <body>
        <div class="barra-ferramentas">
            <span class="dica"><b>Para PDF perfeito:</b><br>1. Em Definições, marque "Gráficos de plano de fundo".<br>2. Desmarque "Cabeçalhos e rodapés".</span>
            <button class="btn-imprimir" onclick="window.print()"> Imprimir / Salvar PDF</button>
        </div>
        
        <div class="page-wrapper">
            <div class="folha-contrato">
                
                {logo_html}
                <h2 class="titulo-doc">CONTRATO DE PRESTAÇÃO DE SERVIÇOS<br><span style="font-size: 13px; font-weight: normal;">MODELO EM VISUAL LAW</span></h2>
                <p class="subtitulo-doc">Serviços de limpeza e higienização de clínica de estética</p>
                
                <div class="header-section">QUEM ASSINA ESTE CONTRATO</div>
                <table class="tab-assina">
                    <tr><th class="th-cli">CLÍNICA • CONTRATANTE</th><th class="th-emp">EMPRESA DE LIMPEZA • CONTRATADA</th></tr>
                    <tr>
                        <td>
                            <span style="font-size:8px; color:#666;">NOME</span><br><b>{st.session_state.nome_contratante}</b><br>
                            <span style="font-size:8px; color:#666;">CNPJ / CPF</span>: <b>{st.session_state.cnpj_contratante}</b> | 
                            <span style="font-size:8px; color:#666;">SEDE</span>: <b>{st.session_state.endereco_contratante}</b><br>
                            <span style="font-size:8px; color:#666;">REPRESENTANTE</span>: <b>{st.session_state.repr_contratante}</b> (RG: {st.session_state.rg_repr_contratante} | CPF: {st.session_state.cpf_repr_contratante})
                        </td>
                        <td>
                            <span style="font-size:8px; color:#666;">NOME</span><br><b>{st.session_state.nome_contratada}</b><br>
                            <span style="font-size:8px; color:#666;">CNPJ</span>: <b>{st.session_state.cnpj_contratada}</b> | 
                            <span style="font-size:8px; color:#666;">SEDE</span>: <b>{st.session_state.endereco_contratada}</b><br>
                            <span style="font-size:8px; color:#666;">REPRESENTANTE</span>: <b>{st.session_state.repr_contratada}</b> (RG: {st.session_state.rg_repr_contratada} | CPF: {st.session_state.cpf_repr_contratada})
                        </td>
                    </tr>
                </table>
                
                <div class="header-section">O CONTRATO EM 1 MINUTO</div>
                
                {tabela_1_minuto_html}
                
                <div class="header-section">COMO LER ESTE CONTRATO</div>
                
                <table class="menu-cores" style="margin-bottom: 10px;">
                    <tr>
                        <td style="background-color: {cores['objeto']};" onclick="document.getElementById('sec-objeto')?.scrollIntoView({{behavior: 'smooth', block: 'start'}})"><b>OBJETO</b><br>o que será feito</td>
                        <td style="background-color: {cores['autonomia']};" onclick="document.getElementById('sec-autonomia')?.scrollIntoView({{behavior: 'smooth', block: 'start'}})"><b>AUTONOMIA</b><br>liberdade de trabalho</td>
                        <td style="background-color: {cores['custos']};" onclick="document.getElementById('sec-custos')?.scrollIntoView({{behavior: 'smooth', block: 'start'}})"><b>SEUS CUSTOS</b><br>o que você paga e traz</td>
                        <td style="background-color: {cores['sigilo']};" onclick="document.getElementById('sec-sigilo')?.scrollIntoView({{behavior: 'smooth', block: 'start'}})"><b>SIGILO</b><br>informações protegidas</td>
                    </tr>
                    <tr>
                        <td style="background-color: {cores['saude']};" onclick="document.getElementById('sec-saude')?.scrollIntoView({{behavior: 'smooth', block: 'start'}})"><b>SAÚDE</b><br>saúde e biossegurança</td>
                        <td style="background-color: {cores['dinheiro']};" onclick="document.getElementById('sec-dinheiro')?.scrollIntoView({{behavior: 'smooth', block: 'start'}})"><b>DINHEIRO</b><br>valores e pagamento</td>
                        <td style="background-color: {cores['prazo']};" onclick="document.getElementById('sec-prazo')?.scrollIntoView({{behavior: 'smooth', block: 'start'}})"><b>PRAZO</b><br>datas e duração</td>
                        <td style="background-color: {cores['atencao']};" onclick="document.getElementById('sec-atencao')?.scrollIntoView({{behavior: 'smooth', block: 'start'}})"><b>ATENÇÃO</b><br>leia com cuidado</td>
                    </tr>
                </table>
                
                <table class="tab-clausulas" style="margin-bottom: 3px;">
                    <tr><th class="th-jur" style="width: 50%;">TEXTO DO CONTRATO</th><th class="th-jur" style="width: 50%;">EM PALAVRAS SIMPLES</th></tr>
                    <tr>
                        <td>Coluna da esquerda. É o texto jurídico, que vale para todos os efeitos legais.</td>
                        <td class="col-vis">Coluna da direita. Explica a mesma cláusula em linguagem do dia a dia.</td>
                    </tr>
                </table>
                
                <div class="box-importante">
                    <span style="color: #df9d2d; font-weight: bold; font-size: 12px;">IMPORTANTE:</span> As explicações em palavras simples servem para ajudar a entender, <b>mas não substituem o texto do contrato.</b> Em caso de dúvida, vale o texto jurídico. <b>Pergunte antes de assinar.</b>
                </div>
                
                {html_clausulas}

                {foro_html}
                
                <div class="header-section">CHECKLIST DE COMPREENSÃO</div>
                <p style="margin: 5px 0 8px 0;">Antes de assinar, marque cada item que você entendeu e coloque sua rubrica.</p>
                <ul style="list-style-type: none; padding-left: 0; line-height: 1.6; margin: 0 0 15px 0;">
                    {check_html}
                </ul>
                
                <p style="margin-top: 15px; margin-bottom: 15px;">E, por estarem justos e contratados, assinam o presente CONTRATO DE PRESTAÇÃO DE SERVIÇOS.</p>
                <p style="text-align: center; margin-bottom: 30px;">{st.session_state.foro_cidade.split('/')[0] if st.session_state.foro_cidade else "Local"}, {st.session_state.data_formatada}.</p>
                
                <table class="tab-assinaturas">
                    <tr>
                        <td class="bloco-assinatura">
                            <div class="linha-assina"></div>
                            <b>{st.session_state.nome_contratante}</b><br>
                            Repr. {st.session_state.repr_contratante}<br>
                            (CONTRATANTE)
                        </td>
                        <td class="bloco-assinatura">
                            <div class="linha-assina"></div>
                            <b>{st.session_state.nome_contratada}</b><br>
                            Repr. {st.session_state.repr_contratada}<br>
                            (CONTRATADA)
                        </td>
                    </tr>
                </table>
                
                <p style="text-align: center; margin-top: 25px; margin-bottom: 25px; font-weight: bold; font-size: 12px;">TESTEMUNHAS</p>
                
                <table class="tab-assinaturas">
                    <tr>
                        <td class="bloco-assinatura">
                            <div class="linha-assina"></div>
                            CPF: ______________________<br>
                            RG: _______________________
                        </td>
                        <td class="bloco-assinatura">
                            <div class="linha-assina"></div>
                            CPF: ______________________<br>
                            RG: _______________________
                        </td>
                    </tr>
                </table>
            </div>
        </div>

        <script>
            function adjustLayout() {{
                const folha = document.querySelector('.folha-contrato');
                const wrapper = document.querySelector('.page-wrapper');
                const toolbar = document.querySelector('.barra-ferramentas');
                
                if (!folha || !wrapper) return;

                const viewportWidth = window.innerWidth;
                const a4Width = 794;
                
                let scale = 1;
                if (viewportWidth < a4Width) {{
                    scale = viewportWidth / a4Width;
                }}

                // Reseta o transform para medir a altura real
                folha.style.transform = 'none';
                const unscaledHeight = folha.scrollHeight;
                
                if (scale < 1) {{
                    folha.style.transform = `scale(${{scale}})`;
                    folha.style.transformOrigin = 'top left';
                    
                    const scaledHeight = unscaledHeight * scale;
                    wrapper.style.height = scaledHeight + 'px';
                    wrapper.style.width = '100%';
                    wrapper.style.overflow = 'hidden';
                    wrapper.style.justifyContent = 'flex-start';
                }} else {{
                    folha.style.transform = 'none';
                    wrapper.style.height = 'auto';
                    wrapper.style.width = '100%';
                    wrapper.style.overflow = 'visible';
                    wrapper.style.justifyContent = 'center';
                }}

                // Ajusta a altura do iframe para caber o conteúdo
                setTimeout(() => {{
                    const totalHeight = wrapper.offsetHeight + (toolbar ? toolbar.offsetHeight + 40 : 60);
                    if (window.frameElement) {{
                        window.frameElement.style.height = totalHeight + 'px';
                    }}
                }}, 50);
            }}

            window.addEventListener('resize', adjustLayout);
            window.addEventListener('load', adjustLayout);
            setTimeout(adjustLayout, 100);
            setTimeout(adjustLayout, 500);
        </script>
    </body>
    </html>
    """
    
    components.html(html_iframe_completo, height=2200, scrolling=True)