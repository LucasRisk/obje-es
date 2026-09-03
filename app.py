import streamlit as st
import anthropic

# Configuração da API key (via Secrets do Streamlit Cloud)
client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

BASE_OBJECOES = """
1. Preço/Parcela: "A parcela está mais cara que financiamento" -> Entenda a preocupação, mas no financiamento há juros de 12-15% ao ano, enquanto no consórcio só há taxa de administração, sem juros.
2. Prazo: "Não sei quando vou ser contemplado" -> Pode dar lance desde a primeira assembleia e antecipar a contemplação.
3. Confiança: "Isso não é golpe/pirâmide?" -> Consórcio é regulamentado pelo Banco Central, sistema de compra coletiva regulado por lei.
4. Comparação: "Financiamento é mais rápido" -> No financiamento você recebe na hora, mas paga muito mais no total por juros.
5. Burocracia: "Não entendi como funciona" -> Explicação simples: grupo de pessoas pagando parcelas, contemplação por sorteio ou lance.
6. Taxa de administração: "Essa taxa é um absurdo" -> Taxa cobre a administração do grupo, diluída no plano, menor que juros de financiamento.
7. Desistência: "Já tive consórcio e não gostei" -> Perguntar o que não funcionou, ajustar plano/administradora.
"""

SYSTEM_PROMPT = f"""Você é um assistente de vendas especializado em CONTORNAR OBJEÇÕES em ligações de consórcio.

Categorias: Preço/Parcela, Prazo, Confiança, Comparação, Burocracia, Taxa de Administração, Desistência, Outra.

Base de referência:
{BASE_OBJECOES}

Formato de resposta:
**Objeção detectada**: [resumo]
**Categoria**: [categoria]
**Resposta sugerida**: [até 4 frases, terminando com pergunta quando possível]
**Dica extra**: [dica prática]

Se não houver objeção real, responda apenas: "Sem objeção detectada."
"""

st.set_page_config(page_title="Sales Copilot - Objeções", page_icon="📞")
st.title("📞 Copilot de Objeções - Consórcio")
st.write("Cole a fala do cliente e receba a sugestão de resposta.")

fala_cliente = st.text_area("Fala do cliente:", height=100,
                              placeholder="Ex: A parcela tá bem mais cara que financiamento...")

if st.button("Gerar sugestão"):
    if fala_cliente.strip():
        with st.spinner("Analisando..."):
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=500,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": fala_cliente}]
            )
            resultado = response.content[0].text
            st.markdown("---")
            st.markdown(resultado)

            with open("log_objecoes.txt", "a", encoding="utf-8") as f:
                f.write(f"{fala_cliente}\n{resultado}\n---\n")
    else:
        st.warning("Cole a fala do cliente primeiro.")
