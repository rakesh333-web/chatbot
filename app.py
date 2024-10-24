import streamlit as st
import open ai
import pandas as pd
import os  
from openai import AzureOpenAI  
from azure.identity import DefaultAzureCredential, get_bearer_token_provider  

st.title("File Uploader Example")


uploaded_file = st.file_uploader("Choose a file", type=['csv'])
if uploaded_file is not None:
    # Display the file name
    st.write("Uploaded file:", uploaded_file.name)

    # Read the content of the CSV file
    df = pd.read_csv(uploaded_file)

    # Display the DataFrame
    st.write(df)
st.title("Text Input Example")

user_input = st.text_input("Enter some text:")
   
endpoint = os.getenv("ENDPOINT_URL", "https://gpt35turbomodel.openai.azure.com/")  
deployment = os.getenv("DEPLOYMENT_NAME", "gpt35turbo")  
subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "edd24fb0c2c4449a920e3dd4cf027833")  
  
client = AzureOpenAI(  
    azure_endpoint=endpoint,  
    azure_ad_token_provider=token_provider,  
    api_version="2024-05-01-preview",  
)  
if st.button("Get Response"):
  if user_question:
      
      messages = [
          {
              "role": "system",
              "content": "You are an AI model designed to analyze Apache Spark log data. Your task is to provide insights based on log entries, focusing on the following:\n\n1. Identify common errors and their frequency.\n2. Analyze execution times and performance issues.\n3. Suggest methods for detecting anomalies in the logs.\n4. Provide recommendations for optimizing Spark applications.\n\nPlease analyze the provided log entries and summarize key findings."
          },
          {
              "role": "user",
              "content": user_question
          }
      ]

      
      completion = client.chat.completions.create(
          model=deployment,
          messages=messages,
          past_messages=10,
          max_tokens=800,
          temperature=0.7,
          top_p=0.95,
          frequency_penalty=0,
          presence_penalty=0,
          stop=None,
          stream=False
      )

     
      response_text = completion.choices[0].message['content']
      st.write("Response:")
      st.text_area("", response_text, height=200)
  else:
      st.warning("Please enter a question.")
