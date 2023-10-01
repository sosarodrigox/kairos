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
    st.subheader("Business context")
    # business_name = st.text_input("Business name:")
    business_area = st.selectbox(
        "Business knowledge:",
        (
            "Technology",
            "Healthcare",
            "Finance",
            "Education",
            "Hospitality",
            "Food and Beverage",
            "Real Estate",
            "Automotive",
            "Fashion",
            "Manufacturing",
        ),
    )
    business_knowledge = st.selectbox(
        "Business knowledge:", ("Familiar", "Intermediate", "Advanced", "Expert")
    )
    business_stage = st.selectbox(
        "Business Stage:", ("Idea", "Startup", "Growth", "Mature")
    )
    st.divider()
    language = st.selectbox(
        "Select language:", ("English", "Spanish (Soon)", "Portuguese (Soon)")
    )

if selected == "What is?":
    st.title("The AI Value Proposition Canvas")
    st.subheader("What is?")
    st.markdown(
        """The AI Value Proposition Canvas is a tool that helps you to design and implement an AI solution. It is based on the Value Proposition Canvas by Alex Osterwalder. """
    )
if selected == "Constumer Segment":
    st.subheader("Constumer Segment")
    st.markdown(
        """To create a customer profile, you need to conduct some research on your target market and understand their motivations, challenges, and desires. You can use surveys, interviews, observations, or other methods to gather data. Then, you need to organize the data into three categories: jobs, pains, and gains. Jobs are the tasks, problems, or needs that your customers have. Pains are the negative outcomes, risks, or frustrations that they experience or fear. Gains are the positive outcomes, benefits, or aspirations that they seek or expect."""
    )

    menu_costumer_segment = option_menu(
        menu_title=None,
        options=[
            "Gains",
            "Jobs",
            "Pains",
        ],
        icons=[
            "emoji-laughing",
            "card-checklist",
            "emoji-frown-fill",
        ],
        default_index=0,
        orientation="horizontal",
    )

    if menu_costumer_segment == "Gains":
        st.subheader("Constumer Gains:")
        st.text("The benefits or positive outcomes that customers seek or expect.")

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
                    prompt_edit = (
                        f"As a business professional focusing on the customer section and customer gains in the Business Value Proposition Canvas by Alexander Osterwalder, I have compiled the following list of costumer gains: {gains_input}. "
                        f"My understanding of the business context is as follows: "
                        f"I have {business_knowledge.lower()} knowledge of the business domain, and the business is currently at the {business_stage.lower()} stage. "
                        f"I am seeking feedback on this list to refine and optimize the value proposition. "
                        f"I would appreciate your {output_review.lower()} feedback on the gains and any suggestions to improve. Consider mentioning the most critical gains for the {business_area.lower()} area. "
                        f"Please provide me with your {output_size.lower()} feedback, and keep your response within {out_token} words."
                    )
                    print(
                        "prompt_edit: "
                        + prompt_edit
                        + "// out_token: "
                        + str(out_token)
                        + "."
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

    if menu_costumer_segment == "Jobs":
        st.subheader("Constumer Jobs:")
        st.text("The tasks or problems that customers are trying to perform or solve.")

        jobs_input = st.text_area(
            "Enter at least 3 jobs or tasks that the client needs to solve:"
        )

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

        if len(jobs_input) > 10:
            if st.button("Review with AI", type="primary"):
                with st.spinner("Wait for it..."):
                    prompt_edit = (
                        f"As a business professional focusing on the customer section and customer jobs in the Business Value Proposition Canvas by Alexander Osterwalder, I have compiled the following list of costumer jobs: {jobs_input}. "
                        f"My understanding of the business context is as follows: "
                        f"I have {business_knowledge.lower()} knowledge of the business domain, and the business is currently at the {business_stage.lower()} stage. "
                        f"I am seeking feedback on this list to refine and optimize the value proposition. "
                        f"I would appreciate your {output_review.lower()} feedback on the jobs list and any suggestions to improve. Consider mentioning the most critical jobs for the {business_area.lower()} area. "
                        f"Please provide me with your {output_size.lower()} feedback, and keep your response within {out_token} words."
                    )
                    print(
                        "prompt_edit: "
                        + prompt_edit
                        + "// out_token: "
                        + str(out_token)
                        + "."
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
            st.error(
                "Enter at least 3 expected jobs or tasks that the client needs to solve"
            )

    if menu_costumer_segment == "Pains":
        st.subheader("Constumer Pains:")
        st.text(
            "The negative outcomes, risks, or frustrations that customers experience or fear."
        )

        pains_input = st.text_area(
            "Enter at least 3 pains or frustrations that the customer needs to resolve:"
        )

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

        if len(pains_input) > 10:
            if st.button("Review with AI", type="primary"):
                with st.spinner("Wait for it..."):
                    prompt_edit = (
                        f"As a business professional focusing on the customer section and customer pains in the Business Value Proposition Canvas by Alexander Osterwalder, I have compiled the following list of costumer pains: {pains_input}. "
                        f"My understanding of the business context is as follows: "
                        f"I have {business_knowledge.lower()} knowledge of the business domain, and the business is currently at the {business_stage.lower()} stage. "
                        f"I am seeking feedback on this list to refine and optimize the value proposition. "
                        f"I would appreciate your {output_review.lower()} feedback on the pains list and any suggestions to improve. Consider mentioning the most critical pains for the {business_area.lower()} area. "
                        f"Please provide me with your {output_size.lower()} feedback, and keep your response within {out_token} words."
                    )
                    print(
                        "prompt_edit: "
                        + prompt_edit
                        + "// out_token: "
                        + str(out_token)
                        + "."
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
            st.error(
                "Enter at least 3 pains or frustrations that the customer needs to resolve"
            )
