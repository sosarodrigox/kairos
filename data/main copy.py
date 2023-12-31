import streamlit as st
import openai
import os
from dotenv import load_dotenv
from streamlit_option_menu import option_menu

# from streamlit_tags import st_tags

# Cargar las variables de entorno desde .env
load_dotenv()

# Obtener la API key de las variables de entorno
api_key = os.getenv("OPENAI_API_KEY")

# Establecer la API key
openai.api_key = api_key


with st.sidebar:
    selected = option_menu(
        menu_icon="robot",
        menu_title="The AI Value Proposition Canvas",
        options=[
            "What is?",
            "Constumer Segment",
            "Value Proposition",
            "Check engagment",
            "Contact",
        ],
        icons=[
            "patch-question",
            "person-bounding-box",
            "box2-heart",
            "arrow-left-right",
            "envelope",
        ],
        default_index=0,
    )
if selected == "What is?":
    st.title("The AI Value Proposition Canvas")
    st.subheader("What is?")
    st.markdown(
        """The AI Value Proposition Canvas is a tool that helps you to design and implement an AI solution. It is based on the Value Proposition Canvas by Alex Osterwalder. """
    )
if selected == "Constumer Segment":
    st.title("The AI Value Proposition Canvas")
    st.subheader("Constumer Segment")
    st.markdown(
        """To create a customer profile, you need to conduct some research on your target market and understand their motivations, challenges, and desires. You can use surveys, interviews, observations, or other methods to gather data. Then, you need to organize the data into three categories: jobs, pains, and gains. Jobs are the tasks, problems, or needs that your customers have. Pains are the negative outcomes, risks, or frustrations that they experience or fear. Gains are the positive outcomes, benefits, or aspirations that they seek or expect."""
    )


header = st.container()
constumer_segment = st.container()
value_proposition = st.container()

# with header:
#     st.title("The AI Value Proposition Canvas")

with constumer_segment:
    st.subheader("Constumer Segment:")
    st.markdown(
        """To create a customer profile, you need to conduct some research on your target market and understand their motivations, challenges, and desires. You can use surveys, interviews, observations, or other methods to gather data. Then, you need to organize the data into three categories: jobs, pains, and gains. Jobs are the tasks, problems, or needs that your customers have. Pains are the negative outcomes, risks, or frustrations that they experience or fear. Gains are the positive outcomes, benefits, or aspirations that they seek or expect."""
    )

tab1, tab2, tab3 = st.tabs(
    [
        "Gains",
        "Jobs",
        "Pains",
    ]
)

with tab1:
    st.header("Constumer Gains:")
    st.text("The benefits or positive outcomes that customers seek or expect.")

    # TODO: Obtener los gains a partir de los tags
    # # Obtener los gains a partir de los tags
    # gains_list = st_tags(
    #     label="Enter at least 3 expected gains or benefits:",
    #     text="Press enter to add more",
    #     suggestions=["Enter up to 5 wins"],
    #     maxtags=-1,  # -1 for unlimited tags
    #     key="gains_keywords",
    # )

    gains_input = st.text_area("Enter at least 3 expected gains or benefits:")

    st.subheader("AI Review:")

    col1, col2 = st.columns(2)

    with col1:
        output_size = st.radio(
            label="What kind of answer do you want?",
            options=["To-The-Point", "Concise", "Detailed"],
        )
        if output_size == "To-The-Point":
            out_token = 100
        elif output_size == "Concise":
            out_token = 250
        else:
            out_token = 500

    with col2:
        # Create Radio Buttons
        output_review = st.radio(
            label="What kind of feedback do you want?",
            options=["Constructive", "Destructive"],
        )

    temp = st.slider(
        "Randomness or creativity of the text generated",
        min_value=0.0,
        max_value=1.0,
        step=0.2,
    )

    if len(gains_input) > 10:
        if st.button("Review with AI", type="primary"):
            with st.spinner("Wait for it..."):
                # Revisar los gains con IA
                prompt_edit = (
                    "Estoy creando un lienzo de propuesta de valor canvas de A. Osterwalder, sección cliente, apartado ganancias del cliente. Tengo esta lista de ganancias: "
                    + gains_input
                    + ". ¿Qué opinas de esta lista? ¿Agregarías o quitarías algo? Hazme una crítica "
                    + output_review
                    + " puedes usar hasta "
                    + str(out_token)
                    + " palabras."
                )
                print(prompt_edit)
                review = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=prompt_edit,
                    max_tokens=out_token,
                    temperature=temp,
                )
                print(review)

                review_ai = review["choices"][0]["text"]
                st.info(review_ai)

            st.success("Done!")
    else:
        st.error("Enter at least 3 expected gains or benefits")

with tab2:
    st.header("Constumer Jobs:")
    st.text("The tasks or problems that customers are trying to perform or solve.")

with tab3:
    st.header("Constumer Pains:")
    st.text(
        "The negative outcomes, risks, or frustrations that customers experience or fear."
    )


###Prompts:
# Creación del prompt en primera persona
prompt_edit = (
    f"As a business professional focusing on the customer section and customer gains in the Business Value Proposition Canvas by Alexander Osterwalder, "
    f"I have gathered a list of gains based on the provided information: {gains_input}. "
    f"My understanding of the business context is as follows: "
    f"I have {business_knowledge} knowledge of the business domain, and the business is currently at the {business_stage} stage. "
    f"I am seeking feedback on this list to refine and optimize the value proposition. "
    f"I would appreciate your {output_review.lower()} feedback on the gains and any suggestions to improve. "
    f"Please keep your response {output_size.lower()} and within {out_token} words. Thank you!"
)

print(prompt_edit)  # Imprime el prompt para verificar

# Llama a la API de OpenAI con el prompt generado
review = openai.Completion.create(
    engine="text-davinci-003",
    prompt=prompt_edit,
    max_tokens=out_token,
    temperature=temp,
)
