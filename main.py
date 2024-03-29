import streamlit as st
import openai
import os
from dotenv import load_dotenv
from streamlit_option_menu import option_menu

# Cargar las variables de entorno desde .env
load_dotenv()

# Obtener la API key de las variables de entorno
api_key = os.getenv("OPENAI_API_KEY")

# Establecer la API key
openai.api_key = api_key

# canvas_section = "customer section", "value proposition section"
# canvas_section_area = "customer jobs", "customer pains", "customer gains", "pain relievers", "products and services", "gain creators"

canvas_section: str
canvas_section_area: str

# Session states: Verifico si existe información en los input, si no existe, lo inicio con un string vacío
if "gains_input" not in st.session_state:
    st.session_state["gains_input"] = ""

if "jobs_input" not in st.session_state:
    st.session_state["jobs_input"] = ""

if "pains_input" not in st.session_state:
    st.session_state["pains_input"] = ""

if "gain_creators_input" not in st.session_state:
    st.session_state["gain_creators_input"] = ""

if "prod_serv_input" not in st.session_state:
    st.session_state["prod_serv_input"] = ""

if "pain_relievers_input" not in st.session_state:
    st.session_state["pain_relievers_input"] = ""

if "business_description_input" not in st.session_state:
    st.session_state["business_description_input"] = ""

# # Show the state of the session to testing:
# st.write(st.session_state)


def ai_review(
    canvas_section,
    canvas_section_area,
    list_input,
    business_knowledge: str,
    business_stage: str,
    output_review: str,
    business_area: str,
    output_size: str,
    out_token,
    temp,
):
    prompt_edit = (
        f"I am an entrepreneur and I am creating a value proposition canvas using Alexander Osterwalder's methodology. "
        f"Here's the context of the business: {business_description_input}. "
        f'Now I am working in the {canvas_section} and within it in the {canvas_section_area} area and identify the following information: "{list_input}". '
        f"The business currently stands at the {business_stage.lower()} stage. "
        f"I'm seeking a review of this information to refine and optimize the value proposition canvas of my business. "
        f"If the information provided above seems unclear or does not align with my business context, do not be afraid to tell me before offering suggestions, explain to me what to correct considering that I have {business_knowledge.lower()} knowledge of the business. "
        f"I welcome your {output_review.lower()} feedback on this {canvas_section_area} information and any suggestions for improvement. Please highlight the most critical {canvas_section_area} for the {business_area.lower()} sector. "
        f"Please provide your comments in a {output_size.lower()} manner, keeping your response within a maximum of {round(out_token/4)} words."
    )

    print("prompt_edit: " + prompt_edit + "// out_token: " + str(out_token) + ".")

    review = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt_edit,
        max_tokens=out_token,
        temperature=temp,
    )
    print(review)

    return review["choices"][0]["text"]


def check_fit(state_data, temp):
    prompt_evaluate = (
        f"I am an entrepreneur and I am creating a value proposition canvas using Alexander Osterwalder's methodology. My business area is {business_area.lower()} and I am currently in the {business_stage.lower()} stage. "
        f"I need you to review the information I have collected from my business to refine and optimize my business value proposition canvas. "
        f"In the value proposition section I wrote: "
        f"Products and services: {state_data['prod_serv_input']}. "
        f"Pain relievers: {state_data['pain_relievers_input']}. "
        f"Gain creators: {state_data['gain_creators_input']}. "
        f"In the customer segment section I wrote: "
        f"Customer jobs: {state_data['jobs_input']}. "
        f"Customer pains: {state_data['pains_input']}. "
        f"Customer gains: {state_data['gains_input']}. "
        f"If the information provided does not seem clear or does not align with the commercial context of my business, please do not be afraid to let me know before giving me suggestions. "
        f"Otherwise, focus on giving me an evaluation on the fit between my value proposition and the customer segment I am targeting. I accept any suggestion for improvement or constructive criticism. Highlights the most important aspects for the {business_area.lower()} sector. Please be detailed in your response, keeping it within a maximum of 300 words."
        f"Start the message with a rating based on your evaluation, the options you can use are: Confusing, Unclear, Needs development, Appropriate, Innovative, Very innovative, Excellent work, Challenging, Creative, Very creative."
    )

    print(f"prompt_evaluate: {prompt_evaluate}.")

    evaluation = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt_evaluate,
        max_tokens=1000,
        temperature=temp,
    )

    print(evaluation)

    return evaluation["choices"][0]["text"]


def ad_libs(state_data, temp, business_area: str, business_stage: str):
    prompt_ad_libs = (
        f"I am an entrepreneur and have created a value proposition canvas using Alexander Osterwalder's methodology. "
        f"My business area is {business_area} and I am currently in the {business_stage} stage. "
        f"I need you to help me create a phrase that summarizes my value proposition in one sentence using the Ad-libs methodology. "
        f"An Ad-libs forces you to indicate exactly how you plan to create value for your customers. To do this, you must fill in the spaces in the following sentence:\n\n"
        f"Our(s) (Products and services) help(n) (to the Customer segment) "
        f"what they want (Costumer Jobs) for (the verb you choose. Example: Reduce, avoid frustration, etc.) and (the verb you choose. Example: increase, allow, etc) and add the Costumer Gains. "
        f"\n\nNow, review the information I have collected:\n"
        f"Here's the context of the business: {business_description_input}.\n "
        f"* Value Proposition Section:\n"
        f"- Products and services: {state_data['prod_serv_input']}.\n"
        f"- Analgesics: {state_data['pain_relievers_input']}.\n"
        f"- Profit creators: {state_data['gain_creators_input']}.\n"
        f"* Customers Segment Section:\n"
        f"- Customers Jobs: {state_data['jobs_input']}.\n"
        f"- Customers Pains: {state_data['pains_input']}.\n"
        f"- Customers Gains: {state_data['gains_input']}.\n\n"
        f"If the information provided does not seem clear or does not align with the commercial context of my business, please do not be afraid to let me know before giving me suggestions. "
        f"If not, summarize all the information in my value proposition into one sentence that I can use to appeal to my customer segment in my area of business. "
        f"Please be concise in your response, keeping it to a maximum of 100 words."
    )

    print(f"prompt_evaluate: {prompt_ad_libs}.")

    ad_libs_result = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt_ad_libs,
        max_tokens=1000,
        temperature=temp,
    )
    print(ad_libs_result)
    return ad_libs_result["choices"][0]["text"]


with st.sidebar:
    selected = option_menu(
        menu_icon="robot",
        menu_title="The AI Value Proposition Canvas",
        options=[
            "What is?",
            "Constumer Segment",
            "Value Proposition",
            "Check VPC Fit",
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

    business_description_input = st.text_area(
        "Brief description of the business:",
        value=st.session_state["business_description_input"],
    )
    if business_description_input:
        st.session_state["business_description_input"] = business_description_input

    business_area = st.selectbox(
        "Business area:",
        (
            "Technology",
            "Healthcare",
            "Finance",
            "Education",
            "Hospitality",
            "Food and Beverage",
            "Real Estate",
            "Transportation",
            "Fashion",
            "Manufacturing",
            "Forniture",
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
    st.image(
        "https://www.iiba.org/contentassets/6213b737b4c9428e9fe24cf5cb61a138/value-proposition.png",
        use_column_width=True,
    )
    st.markdown(
        """The AI Value Proposition Canvas seamlessly integrates Alex Osterwalder's VPC methodology with the power of artificial intelligence, serving as a dynamic assistant throughout the canvas creation process. This strategic management tool empowers businesses to comprehend and convey the value they provide to their customers. With the AI Value Proposition Canvas, users receive guided support in crafting value for their customers, identifying key components like customer gains, jobs, pain relievers, products, and gain creators. Effectively align your solution with the needs and expectations of your target audience. After completing the value proposition and customer segment sections, leverage the "Check Value Proposition Fit" function for insightful tips based on your canvas."""
    )
    st.subheader("How to Use:")
    st.markdown(
        """1. **Start in the Sidebar: "Business Context" Section**
   - Describe your business briefly in the "Brief Description of the Business" text box, using at least 10 words to outline your current idea or business.


2. **Configure Your Business Context in the Sidebar**
   - Choose your "Business Area," indicate your "Business Knowledge," and select the appropriate "Business Stage" for your current business situation.

3. **Navigate to "Customer Segment" or "Value Proposition" in the Sidebar**
   - In each section, find a brief description and a horizontal menu with its three respective areas (e.g., "Gains," "Jobs," and "Pains" for Customer Segment).
   
4. **Complete Each Area**
   - Use the text box in each area to input information relevant to your business. It's recommended to add at least three points for more comprehensive feedback.

5. **Utilize "AI Review" Controls**
   - Specify the type of response you desire using the "AI Review" controls. Choose between a detailed, concise, or to-the-point answer. You can receive constructive or destructive feedback on your list. Adjust creativity expectations with the slider.

6. **Proceed to "Check Value Proposition Fit" in the Sidebar**
   - Once you've filled all areas in "Customer Segment" and "Value Proposition," go to the "Check VPC Fit" section in the Sidebar. A summary of your value proposition canvas will be displayed. Click the "Check Value Proposition Fit" button to receive an overall evaluation of your business. The AI Value Proposition Canvas will provide feedback on the fit between your value proposition and customer segment. You can also receive suggestions for improvement and constructive criticism.

That's it! This user-friendly guide ensures a smooth and effective experience with the AI Value Proposition Canvas."""
    )

# Constumer Segment
############################################################################################################
if selected == "Constumer Segment":
    canvas_section = "customer segment"
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
        canvas_section_area = "customer gains"
        st.subheader("Constumer Gains:")
        st.text("The benefits or positive outcomes that customers seek or expect.")

        gains_input = st.text_area(
            "Enter at least 3 expected gains or benefits:",
            value=st.session_state["gains_input"],
        )
        if gains_input:
            st.session_state["gains_input"] = gains_input

        list_input = gains_input

    if menu_costumer_segment == "Jobs":
        canvas_section_area = "customer jobs"
        st.subheader("Constumer Jobs:")
        st.text("The tasks or problems that customers are trying to perform or solve.")

        jobs_input = st.text_area(
            "Enter at least 3 jobs or tasks that the client needs to solve:",
            value=st.session_state["jobs_input"],
        )
        if jobs_input:
            st.session_state["jobs_input"] = jobs_input

        list_input = jobs_input

    if menu_costumer_segment == "Pains":
        canvas_section_area = "customer pains"
        st.subheader("Constumer Pains:")
        st.text(
            "The negative outcomes, risks, or frustrations that customers experience or fear."
        )

        pains_input = st.text_area(
            "Enter at least 3 pains or frustrations that the customer needs to resolve:",
            value=st.session_state["pains_input"],
        )

        if pains_input:
            st.session_state["pains_input"] = pains_input

        list_input = pains_input

    st.subheader("AI Review:")

    col1, col2 = st.columns(2)

    with col1:
        output_size = st.radio(
            label="What kind of answer do you want?",
            options=["Detailed", "Concise", "To-The-Point"],
        )
        if output_size == "To-The-Point":
            out_token = 200
        elif output_size == "Concise":
            out_token = 400
        else:
            out_token = 800

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

    if (
        st.session_state["business_description_input"] == ""
        or len(business_description_input) < 20
    ):
        st.error("Enter a brief description of the business in the lateral menu")
    elif len(list_input) < 10:
        st.error(f"Enter at least 3 {canvas_section_area}")
    else:
        if st.button("Review with AI", type="primary"):
            with st.spinner("Wait for it..."):
                st.info(
                    ai_review(
                        canvas_section=canvas_section,
                        canvas_section_area=canvas_section_area,
                        list_input=list_input,
                        business_knowledge=business_knowledge,
                        business_stage=business_stage,
                        output_review=output_review,
                        business_area=business_area,
                        output_size=output_size,
                        out_token=out_token,
                        temp=temp,
                    )
                )

            st.success("Done!")


# Value Proposition Segment
############################################################################################################
if selected == "Value Proposition":
    canvas_section = "value proposition segment"
    st.subheader("Value Proposition")
    st.markdown(
        """The 'Value Proposition' section outlines the unique benefits and value that your product or service provides to address the specific needs and desires of your target customer segment. It encapsulates the core offering and what sets it apart, showcasing the compelling reasons why customers should choose your solution over others in the market."""
    )

    menu_value_proposition = option_menu(
        menu_title=None,
        options=[
            "Gain Creators",
            "Products & Services",
            "Pain Relievers",
        ],
        icons=[
            "graph-up-arrow",
            "cart4",
            "capsule",
        ],
        default_index=0,
        orientation="horizontal",
    )

    if menu_value_proposition == "Gain Creators":
        canvas_section_area = "gain creators"
        st.subheader("Gain Creators:")
        st.text(
            "Enhancing value by delivering benefits and positive outcomes for customers."
        )

        gain_creators_input = st.text_area(
            "Enter at least 3 gain creators:",
            value=st.session_state["gain_creators_input"],
        )

        if gain_creators_input:
            st.session_state["gain_creators_input"] = gain_creators_input

        list_input = gain_creators_input

    if menu_value_proposition == "Products & Services":
        canvas_section_area = "products and services"
        st.subheader("Products & Services:")
        st.text("The products and services that create value for the customer.")

        prod_serv_input = st.text_area(
            "Enter at least 3 products or services:",
            value=st.session_state["prod_serv_input"],
        )

        if prod_serv_input:
            st.session_state["prod_serv_input"] = prod_serv_input

        list_input = prod_serv_input

    if menu_value_proposition == "Pain Relievers":
        canvas_section_area = "pain relievers"
        st.subheader("Pain Relievers:")
        st.text(
            "Describe how your products and services alleviate specific customer pains."
        )

        pain_relievers_input = st.text_area(
            "Introduce at least 3 pain relievers that help the client resolve their frustrations:",
            value=st.session_state["pain_relievers_input"],
        )

        if pain_relievers_input:
            st.session_state["pain_relievers_input"] = pain_relievers_input

        list_input = pain_relievers_input

    st.subheader("AI Review:")

    col1, col2 = st.columns(2)

    with col1:
        output_size = st.radio(
            label="What kind of answer do you want?",
            options=["Detailed", "Concise", "To-The-Point"],
        )
        if output_size == "To-The-Point":
            out_token = 200
        elif output_size == "Concise":
            out_token = 400
        else:
            out_token = 800

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

    if (
        st.session_state["business_description_input"] == ""
        or len(business_description_input) < 20
    ):
        st.error("Enter a brief description of the business in the lateral menu")
    elif len(list_input) < 10:
        st.error(f"Enter at least 3 {canvas_section_area}")
    else:
        if st.button("Review with AI", type="primary"):
            with st.spinner("Wait for it..."):
                st.info(
                    ai_review(
                        canvas_section=canvas_section,
                        canvas_section_area=canvas_section_area,
                        list_input=list_input,
                        business_knowledge=business_knowledge,
                        business_stage=business_stage,
                        output_review=output_review,
                        business_area=business_area,
                        output_size=output_size,
                        out_token=out_token,
                        temp=temp,
                    )
                )

            st.success("Done!")

# Check Value Proposition Fit:
############################################################################################################
if selected == "Check VPC Fit":
    st.subheader("Check Value Proposition Fit")
    st.markdown(
        """“Value Proposition Fit” refers to how sections of the canvas interact to create a strong value proposition. For example, the connection between "Customer Jobs" and "Pain Relievers" involves how products solve customer needs. The relationship between "Gains" and "Gain Creators" shows how the benefits offered match customer expectations. An effective fit involves coherence and synergy between these areas to address customer needs and expectations, thus creating a comprehensive value proposition."""
    )
    st.image(
        "https://optimatraining.co.uk/wp-content/uploads/Value-Proposition-Canvas.png",
        use_column_width=True,
    )
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Value Proposition", divider="gray")
        st.write(f"Products and services: {st.session_state['prod_serv_input']}")
        st.write(f"Pain relievers: {st.session_state['pain_relievers_input']}")
        st.write(f"Gain creators: {st.session_state['gain_creators_input']}")

    with col2:
        st.subheader("Costumer Segment", divider="gray")
        st.write(f"Customer jobs: {st.session_state['jobs_input']}")
        st.write(f"Customer pains: {st.session_state['pains_input']}")
        st.write(f"Customer gains: {st.session_state['gains_input']}")

    st.divider()
    temp = st.slider(
        "Randomness or creativity of the text generated",
        min_value=0.0,
        max_value=1.0,
        step=0.2,
    )
    # st.divider()
    if st.button("Check Value Proposition Fit", type="primary"):
        with st.spinner("Wait for it..."):
            st.info(check_fit(state_data=st.session_state, temp=temp))

        st.success("Done!")

    if st.button("Generate Ad-libs (Beta Version)", type="primary"):
        with st.spinner("Wait for it..."):
            st.subheader(
                ad_libs(
                    state_data=st.session_state,
                    temp=temp,
                    business_area=business_area,
                    business_stage=business_stage,
                )
            )

        st.success("Done!")


if selected == "Contact":
    st.subheader("Contact")

    st.write("Feel free to reach out to me via:")

    # LinkedIn
    st.divider()
    st.write("[LinkedIn](https://www.linkedin.com/in/sosarodrigo/)")

    # GitHub
    st.divider()
    st.write("[GitHub](https://github.com/sosarodrigox)")

    # Email
    st.divider()
    st.write("sosarodrigox@gmail.com")
