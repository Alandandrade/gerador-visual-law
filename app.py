import streamlit as st
from docxtpl import DocxTemplate
import io

# --- Interface da Página ---
st.set_page_config(page_title="Gerador de Contrato Inteligente", layout="wide")
st.title("📝 Gerador Automático de Contrato")
st.write("Preencha os dados e selecione as cláusulas desejadas para gerar o documento.")

# --- Seção 1: Formulário de Dados ---
st.subheader("1. Qualificação das Partes")
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Dados do Contratante")
    nome_contratante = st.text_input("Nome/Razão Social (Contratante)", value="BELA DAMA ESTÉTICA")
    cnpj_contratante = st.text_input("CNPJ (Contratante)", value="12.557.705/0001-14")
    repr_contratante = st.text_input("Nome do Representante", value="Renata Soares Dama")

with col2:
    st.markdown("#### Dados da Contratada")
    nome_contratada = st.text_input("Nome/Razão Social (Contratada)", value="MAX LIMPEZA")
    cnpj_contratada = st.text_input("CNPJ (Contratada)", value="12.458.777/0001-33")
    repr_contratada = st.text_input("Nome do Representante (Contratada)", value="Marcela Ferraz Cruz")

st.write("---")

# --- Seção 2: Dados do Negócio ---
st.subheader("2. Dados Financeiros e Prazos")
col3, col4 = st.columns(2)
with col3:
    valor_mensal = st.text_input("Valor Mensal (R$)", value="7.000,00")
with col4:
    prazo_meses = st.text_input("Prazo do Contrato (meses)", value="12")

st.write("---")

# --- Seção 3: Seleção de Cláusulas (Opcionais) ---
st.subheader("3. Personalização das Cláusulas")
st.write("Selecione quais regras farão parte deste contrato:")

incluir_sigilo = st.checkbox("🔒 Incluir cláusula de Confidencialidade (NDA) e LGPD (Parágrafos 7º e 8º)", value=True)
incluir_residuos = st.checkbox("☣️ Incluir normas de descarte de resíduos biológicos/perfurocortantes e vacinação (Parágrafos 9º, 10º, 11º)", value=True)
incluir_multas = st.checkbox("⚖️ Incluir penalidades gradativas e Relatório de Não Conformidade - RNC (Cláusula 5ª, §1º)", value=True)
incluir_nao_exclusividade = st.checkbox("🤝 Incluir declaração expressa de Não Exclusividade (Parágrafo 5º)", value=True)

st.write("---")

# --- Lógica de Geração do Documento ---
if st.button("🚀 Gerar Contrato em Word", type="primary"):
    
    # 1. Agrupar todas as respostas em um "Dicionário" (Contexto)
    contexto = {
        'nome_contratante': nome_contratante,
        'cnpj_contratante': cnpj_contratante,
        'repr_contratante': repr_contratante,
        'nome_contratada': nome_contratada,
        'cnpj_contratada': cnpj_contratada,
        'repr_contratada': repr_contratada,
        'valor_mensal': valor_mensal,
        'prazo_meses': prazo_meses,
        # As variáveis booleanas (Verdadeiro ou Falso) que controlam os blocos de texto:
        'incluir_sigilo': incluir_sigilo,
        'incluir_residuos': incluir_residuos,
        'incluir_multas': incluir_multas,
        'incluir_nao_exclusividade': incluir_nao_exclusividade
    }
    
    try:
        # 2. Abrir o template Word
        # IMPORTANTE: Você precisa criar um arquivo chamado 'template_padrao.docx' na mesma pasta!
        doc = DocxTemplate("template_padrao.docx")
        
        # 3. Injetar os dados no template
        doc.render(contexto)
        
        # 4. Salvar na memória para download
        buffer = io.BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        
        st.success("✅ Contrato gerado com sucesso!")
        
        # 5. Botão de Download
        st.download_button(
            label="📥 Baixar Contrato Final (.docx)", 
            data=buffer, 
            file_name=f"Contrato_{nome_contratante}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        
    except Exception as e:
        st.error(f"Erro ao gerar o documento. Certifique-se de que o arquivo 'template_padrao.docx' existe na pasta. Detalhe do erro: {e}")