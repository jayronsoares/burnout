import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from functools import reduce

# Define probabilidades a priori
prior_burnout_forte = 0.3
prior_burnout_fraco = 0.7

# Função para mapear respostas para pontuações de probabilidade
def mapear_resposta_para_probabilidade(resposta, tipo_burnout):
    probabilidades = {
        "forte": {
            "Nunca": 0.1, "Raramente": 0.2, "Às vezes": 0.4, "Frequentemente": 0.7, "Sempre": 0.9,
            "Nada": 0.1, "Pouco": 0.3, "Moderadamente": 0.5, "Muito": 0.7, "Extremamente": 0.9,
            "Ruim": 0.8, "Regular": 0.6, "Bom": 0.4, "Muito Bom": 0.2, "Excelente": 0.1,
            "Sim": 0.9, "Não": 0.1, "Positivo": 0.1, "Neutro": 0.5, "Negativo": 0.8
        },
        "fraco": {
            "Nunca": 0.7, "Raramente": 0.6, "Às vezes": 0.4, "Frequentemente": 0.2, "Sempre": 0.1,
            "Nada": 0.8, "Pouco": 0.6, "Moderadamente": 0.4, "Muito": 0.3, "Extremamente": 0.1,
            "Ruim": 0.2, "Regular": 0.4, "Bom": 0.6, "Muito Bom": 0.8, "Excelente": 0.9,
            "Sim": 0.1, "Não": 0.9, "Positivo": 0.9, "Neutro": 0.5, "Negativo": 0.2
        }
    }
    return probabilidades.get(tipo_burnout, {}).get(resposta, 0.5)

# Função para calcular a probabilidade combinada
def calcular_probabilidade(respostas, tipo_burnout):
    try:
        probabilidade = reduce(lambda x, y: x * y, [mapear_resposta_para_probabilidade(resp, tipo_burnout) for resp in respostas])
        return probabilidade
    except Exception as e:
        st.error(f"Ocorreu um erro ao calcular a probabilidade: {e}")
        return 1  # Valor padrão para evitar falhas

# Função para aplicar o Teorema de Bayes
def aplicar_bayes(probabilidade_forte, probabilidade_fraca):
    try:
        posterior_forte = (probabilidade_forte * prior_burnout_forte) / (
                (probabilidade_forte * prior_burnout_forte) + (probabilidade_fraca * prior_burnout_fraco)
        )
        posterior_fraco = 1 - posterior_forte
        return posterior_forte, posterior_fraco
    except ZeroDivisionError:
        st.error("Divisão por zero ocorreu ao calcular as probabilidades.")
        return 0.5, 0.5  # Probabilidades neutras para lidar com o erro

# Função para exibir resultados e recomendações
def exibir_resultados(posterior_forte, posterior_fraco):
    st.subheader("Resultados da Avaliação")
    if posterior_forte > 0.5:
        st.warning(f"Probabilidade de burnout forte: {posterior_forte:.2f}. É recomendado procurar ajuda profissional.")
    else:
        st.info(f"Probabilidade de burnout fraco: {posterior_fraco:.2f}. Considere fazer uma pausa, melhorar sua dieta e dormir mais.")

# Função para plotar probabilidades de burnout com cores personalizadas
def plotar_probabilidades(forte, fraco):
    # Definir paleta de cores com base nas probabilidades
    if forte > 0.5:
        cores = ["#FF6F61", "#FFD700"]  # Vermelho Suave para Forte, Amarelo Suave para Fraco
    elif fraco > 0.5:
        cores = ["#FFD700", "#98FB98"]  # Amarelo Suave para Fraco, Verde Suave para Mínimo
    else:
        cores = ["#98FB98", "#FFD700"]  # Verde Suave para Mínimo, Amarelo Suave para Fraco

    labels = ['Burnout Forte', 'Burnout Fraco']
    probabilidades = [forte, fraco]

    plt.figure(figsize=(8, 5))
    sns.barplot(x=labels, y=probabilidades, palette=cores)
    plt.ylim(0, 1)
    plt.ylabel('Probabilidade')
    plt.title('Avaliação da Probabilidade de Burnout')
    st.pyplot(plt)

# Interface Streamlit para coletar entrada do usuário
def principal():
    st.title("Ferramenta de Avaliação de Burnout")
    st.markdown(
        """
        <style>
        .main {
            padding: 2rem;
        }
        .stButton button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("### Por favor, responda às seguintes perguntas:")

    # Coletando respostas do usuário com valores iniciais neutros ou padrão
    respostas = [
        st.selectbox("Com que frequência você se sente fisicamente e emocionalmente exausto?", 
                     ["Selecione uma opção", "Nunca", "Raramente", "Às vezes", "Frequentemente", "Sempre"], index=0),
        st.slider("Avalie seus níveis de energia durante e após o trabalho em uma escala de 1-10", 1, 10, value=None),
        st.selectbox("Como você avaliaria a qualidade do seu sono?", 
                     ["Selecione uma opção", "Ruim", "Regular", "Bom", "Muito Bom", "Excelente"], index=0),
        st.slider("Em uma escala de 1-10, quão estressado você se sente no trabalho?", 1, 10, value=None),
        st.selectbox("Quão interessado você está em suas tarefas diárias?", 
                     ["Selecione uma opção", "Nada", "Pouco", "Moderadamente", "Muito", "Extremamente"], index=0),
        st.selectbox("Como você descreveria sua atitude em relação aos colegas ou clientes?", 
                     ["Selecione uma opção", "Positivo", "Neutro", "Negativo"], index=0),
        st.selectbox("Você sente que seu trabalho carece de sentido?", 
                     ["Selecione uma opção", "Sim", "Não", "Às vezes"], index=0),
        st.slider("Avalie sua confiança em desempenhar seu trabalho efetivamente em uma escala de 1-10", 1, 10, value=None),
        st.selectbox("Quão satisfeito você está com suas conquistas no trabalho?", 
                     ["Selecione uma opção", "Nada", "Pouco", "Moderadamente", "Muito", "Extremamente"], index=0),
        st.selectbox("Você notou uma queda na sua produtividade ou eficiência?", 
                     ["Selecione uma opção", "Sim", "Não"], index=0),
        st.selectbox("Você experimenta sintomas físicos como dores de cabeça ou tensão muscular com frequência?", 
                     ["Selecione uma opção", "Nunca", "Raramente", "Às vezes", "Frequentemente", "Sempre"], index=0),
        st.selectbox("Você frequentemente se sente ansioso ou deprimido?", 
                     ["Selecione uma opção", "Nunca", "Raramente", "Às vezes", "Frequentemente", "Sempre"], index=0),
        st.selectbox("Com que frequência você tira dias de licença ou folgas devido a se sentir sobrecarregado?", 
                     ["Selecione uma opção", "Nunca", "Raramente", "Às vezes", "Frequentemente", "Sempre"], index=0),
        st.selectbox("Você evita interações sociais com colegas ou amigos?", 
                     ["Selecione uma opção", "Nunca", "Raramente", "Às vezes", "Frequentemente", "Sempre"], index=0),
        st.selectbox("Você começou a usar estratégias de enfrentamento não saudáveis (por exemplo, comer em excesso, álcool)?", 
                     ["Selecione uma opção", "Nunca", "Raramente", "Às vezes", "Frequentemente", "Sempre"], index=0),
        st.selectbox("Você está trabalhando horas excessivas?", 
                     ["Selecione uma opção", "Sim", "Não"], index=0),
        st.selectbox("As expectativas do seu trabalho estão claras?", 
                     ["Selecione uma opção", "Sim", "Não", "Às vezes"], index=0),
        st.selectbox("Você tem apoio de colegas ou supervisores?", 
                     ["Selecione uma opção", "Sim", "Não", "Às vezes"], index=0),
        st.slider("Avalie seu equilíbrio entre trabalho e vida pessoal em uma escala de 1-10", 1, 10, value=None),
        st.selectbox("Você consegue relaxar e se recuperar fora do horário de trabalho?", 
                     ["Selecione uma opção", "Nunca", "Raramente", "Às vezes", "Frequentemente", "Sempre"], index=0),
    ]

    # Verificar se todas as respostas foram fornecidas
    if all([resp != "Selecione uma opção" and resp is not None for resp in respostas]):
        # Calcular probabilidades
        probabilidade_forte = calcular_probabilidade(respostas, "forte")
        probabilidade_fraca = calcular_probabilidade(respostas, "fraco")
        
        # Aplicar o Teorema de Bayes
        posterior_forte, posterior_fraco = aplicar_bayes(probabilidade_forte, probabilidade_fraca)
        
        # Exibir resultados e recomendações
        exibir_resultados(posterior_forte, posterior_fraco)
        
        # Plotar as probabilidades
        plotar_probabilidades(posterior_forte, posterior_fraco)
    else:
        st.info("Por favor, complete todas as perguntas para ver os resultados da avaliação de burnout.")

    # Adicionar botão de Atualizar para recarregar a página
    if st.button("Atualizar"):
        st.rerun()
    
    # Adicionar rodapé com crédito
    st.markdown(
        """
        <div class="footer">
            Desenvolvido por Jayron Soares
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    principal()
