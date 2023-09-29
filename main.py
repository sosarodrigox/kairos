import streamlit as st
import openai
import os
from dotenv import load_dotenv

# from streamlit_tags import st_tags

# Cargar las variables de entorno desde .env
load_dotenv()

# Obtener la API key de las variables de entorno
api_key = os.getenv("OPENAI_API_KEY")

# Establecer la API key
openai.api_key = api_key

header = st.container()
constumer_segment = st.container()
value_proposition = st.container()

with header:
    st.title("The AI Value Proposition Canvas")

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
            out_token = 50
        elif output_size == "Concise":
            out_token = 128
        else:
            out_token = 516

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
                    "Estoy armando un lienzo de propuesta de valor canvas de A. Osterwalder, y estoy en la parte de las ganancias del cliente. Tengo esta lista de ganancias: "
                    + gains_input
                    + ". ¿Qué opinas de esta lista? ¿Agregarías o quitarías algo? Hazme una crítica "
                    + output_review
                )
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
