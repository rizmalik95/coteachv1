import os
import openai
import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI

openai_api_key = os.environ["OPENAI_API_KEY"]

template = """
     
You are an expert English Language Arts teacher and you teach a wide range of student needs. Your goal is to create an instructional support that can be given to students to help them access and engage with an essay question. 

Below is an essay question that you want to make more accessible for the students in the classroom. Below is also the instructional support to create for the teacher. You should provide just one of Sentence Stems, Glossary or Extension Questions.

Here are some examples of Sentence Stems: 
- What surprised me was...because....
- I think that...for example
- First...then...next...
- In my opinion....in addition...
- Based on the passage, I can infer that...for example....
- I don't understand why....
- Based on the pattern, the numbers will...  
    
A Glossary is a list of key words and definitions that the student will need to answer the essay question. These should be challenging and important words from the question itself but also words they are likely to need when answering the question.

An Extension Question is an additional question to give to the top-performing students once they have completed this question. It should aim to build the depth of their knowledge. 
    
If Phase: Elementary is selected the resulting output should be appropriate for elementary students. If Phase: Middle is selected the output should be appropriate for middle-school students. If Phase: High is selected the output should be appropriate for high-school students.

Below is the phase, support and resource:
    
    PHASE: {phase}
    SUPPORT: {support}
    QUESTION: {resource}
    
    YOUR RESPONSE:
"""

prompt = PromptTemplate(
    input_variables=["phase", "support", "resource"],
    template=template,
)

def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=.7, openai_api_key=openai_api_key)
    return llm

st.set_page_config(page_title="coteach.ai", page_icon=":robot:")
st.header("coteach.ai")

col1, col2 = st.columns(2)

with col1:
    st.markdown("Meeting the needs of all students in ELA lessons is hard. We want to help. \n\n This tool lets you input an essay question and instantly create 'Scaffolds for Success' that are aligned to the Universal Design for Learning (UDL) framework.")

with col2:
    st.image(image='titleimage.jpg', width=500, caption='')

st.markdown("## Input Essay Question")

col1, col2 = st.columns(2)
with col1:
    option_phase = st.selectbox(
        'What phase do you teach?',
        ('Elementary', 'Middle', 'High'))
    
with col2:
    option_support = st.selectbox(
        'What instructional support do you need?',
        ('Sentence Stems', 'Glossary', 'Extension Question'))

def get_text():
    input_text = st.text_area(label="Your Question", label_visibility='collapsed', placeholder="Your Resource...", key="resource_input")
    return input_text

resource_input = get_text()

if len(resource_input.split(" ")) > 700:
    st.write("Please enter a shorter resource. The maximum length is 700 words.")
    st.stop()

def update_text_with_example():
    print ("in updated")
    st.session_state.resource_input = "How does Shakespeare treat death in Romeo and Juliet? Frame your answer in terms of legal, moral, familial, and personal issues. Bearing these issues in mind, compare the deaths of Romeo and Juliet, Romeo and Mercutio, and Mercutio and Tybalt."

st.button("*See An Example*", type='secondary', help="Click to see an example of a resource you will be differentiating.", on_click=update_text_with_example)

st.markdown("### Your Differentiated Support:")

if resource_input:

    llm = load_LLM(openai_api_key=openai_api_key)

    prompt_with_resource = prompt.format(phase=option_phase, support=option_support, resource=resource_input)

    formatted_resource = llm(prompt_with_resource)

    st.write(formatted_resource)