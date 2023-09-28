import streamlit as st

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
    st.header("A cat")
    st.image("https://static.streamlit.io/examples/cat.jpg", width=200)
