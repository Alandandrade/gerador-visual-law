import streamlit as st
from docxtpl import DocxTemplate
import io

# --- Interface da Página ---
st.set_page_config(page_title="Gerador de Contrato Inteligente", layout="wide")
st.title("📝 Gerador Automático de Contrato")
st.write("Preencha os dados e selecione as cláusulas desejadas para gerar o documento.")

# --- Seção 1: Qualificação das Partes ---
st.subheader("1. Qualificação das Partes")
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Dados do Contratante")
    nome_contratante = st.text_input("Nome/Razão Social (Contratante)", value="")
    cnpj_contratante = st.text_input("CNPJ (Contratante)", value="")
    endereco_contratante = st.text_input("Endereço Sede (Contratante)", value="")
    repr_contratante = st.text_input("Nome do Representante", value="")
    rg_repr_contratante = st.text_input("RG do Representante", value="")
    cpf_repr_contratante = st.text_input("CPF do Representante", value="")

with col2:
    st.markdown("#### Dados da Contratada")
    nome_contratada = st.text_input("Nome/Razão Social (Contratada)", value="")
    cnpj_contratada = st.text_input("CNPJ (Contratada)", value="")
    endereco_contratada = st.text_input("Endereço Sede (Contratada)", value="")
    repr_contratada = st.text_input("Nome do Representante (Contratada)", value="")
    rg_repr_contratada = st.text_input("RG do Representante (Contratada)", value="")
    cpf_repr_contratada = st.text_input("CPF do Representante (Contratada)", value="")

st.write("---")

# --- Seção 2: Dados do Negócio e Encerramento ---
st.subheader("2. Dados Financeiros e de Encerramento")
col3, col4, col5 = st.columns(3)
with col3:
    valor_mensal = st.text_input("Valor Mensal (R$)", value="")
with col4:
    prazo_meses = st.text_input("Prazo do Contrato (meses)", value="")
with col5:
    data_assinatura = st.date_input("Data de Assinatura")
    foro_cidade = st.text_input("Cidade do Foro", value="Lorena - SP")

st.write("---")

# --- Seção 3: Seleção de Cláusulas (Opcionais) ---
st.subheader("3. Personalização das Cláusulas")
st.write("Selecione quais regras farão parte deste contrato:")

incluir_sigilo = st.checkbox("🔒 Incluir cláusula de Confidencialidade (NDA) e LGPD (Parágrafos 7º e 8º)", value=False)
incluir_residuos = st.checkbox("☣️ Incluir normas de descarte de resíduos biológicos/perfurocortantes e vacinação (Parágrafos 9º, 10º, 11º)", value=False)
incluir_multas = st.checkbox("⚖️ Incluir penalidades gradativas e Relatório de Não Conformidade - RNC (Cláusula 5ª, §1º)", value=False)
incluir_nao_exclusividade = st.checkbox("🤝 Incluir declaração expressa de Não Exclusividade (Parágrafo 5º)", value=False)

st.write("---")

# --- Lógica de Geração do Documento ---
if st.button("🚀 Gerar Contrato em Word", type="primary"):
    
    # Adicionamos todas as novas variáveis aqui no contexto
    contexto = {
        'nome_contratante': nome_contratante,
        'cnpj_contratante': cnpj_contratante,
        'endereco_contratante': endereco_contratante,
        'repr_contratante': repr_contratante,
        'rg_repr_contratante': rg_repr_contratante,
        'cpf_repr_contratante': cpf_repr_contratante,
        
        'nome_contratada': nome_contratada,
        'cnpj_contratada': cnpj_contratada,
        'endereco_contratada': endereco_contratada,
        'repr_contratada': repr_contratada,
        'rg_repr_contratada': rg_repr_contratada,
        'cpf_repr_contratada': cpf_repr_contratada,
        
        'valor_mensal': valor_mensal,
        'prazo_meses': prazo_meses,
        # Formatamos a data para o padrão brasileiro DD/MM/AAAA
        'data_assinatura': data_assinatura.strftime("%d/%m/%Y"), 
        'foro_cidade': foro_cidade,
        
        'incluir_sigilo': incluir_sigilo,
        'incluir_residuos': incluir_residuos,
        'incluir_multas': incluir_multas,
        'incluir_nao_exclusividade': incluir_nao_exclusividade
    }
    
    try:
        doc = DocxTemplate("template_padrao.docx")
        doc.render(contexto)
        
        buffer = io.BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        
        st.success("✅ Contrato gerado com sucesso!")
        
        st.download_button(
            label="📥 Baixar Contrato Final (.docx)", 
            data=buffer, 
            file_name=f"Contrato_{nome_contratante}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        
    except Exception as e:
        st.error(f"Erro ao gerar o documento. Detalhe do erro: {e}")