import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import openai
from src.sample_data import ALL_ALERTS, TEST_ALERTS
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
load_dotenv()

def run():
    # Initialize the embedding model (adjust model name as needed)
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Sample historical alerts with trade details and supervisor comments
    # historical_alerts = [
    #     {"alert_id": "1", "trade_details": "Buy 10M bonds at 99.5; low risk, normal PnL", "comment": "Legitimate trade; no action required."},
    #     {"alert_id": "2", "trade_details": "Sell 5M bonds at 100.2; high volatility, slight negative PnL", "comment": "Potential spoofing; monitor trader activity."},
    #     # ... add more historical alerts
    # ]

    historical_alerts = ALL_ALERTS

    # Compute embeddings for the trade details of historical alerts
    trade_texts = [alert["trade_details"] for alert in historical_alerts]
    embeddings = model.encode(trade_texts)

    # Create a FAISS index using L2 (Euclidean) distancerun
    d = embeddings.shape[1]  # Dimension of the embeddings
    index = faiss.IndexFlatL2(d)
    index.add(np.array(embeddings))

    # Test New alert that triggers comment suggestion
    for new_alert in TEST_ALERTS:
        new_embedding = model.encode([new_alert["trade_details"]])

        # Retrieve the top 3 similar historical alerts
        k = 2
        distances, indices = index.search(np.array(new_embedding), k)
        retrieved_alerts = [historical_alerts[i] for i in indices[0]]

        # Build the context from similar alerts
        context = ""
        for alert in retrieved_alerts:
            context += f"Trade details: {alert['trade_details']}\nComment: {alert['comment']}\n---\n"

        # Construct the prompt for the LLM
        prompt = f"""
        Given the following historical trade alerts and their supervisor comments:
        {context}
        For a new alert with these details:
        Trade details: {new_alert['trade_details']}
        Instrument: {new_alert['instrument']}
        Generate a brief comment on behalf of Trading Supervisor with reference trade details in alert for this alert without providing references to historical trades or alerts.
        Per AI Overview: State if it is a legitimate trade or if any action is required as system reported it as {new_alert['alert_type']}.
        """
        print('********************LLM Prompt: Start **************************')
        print(prompt)
        print('********************LLM Prompt: End ****************************\n')

        # # Call the LLM to generate a comment suggestion
        MODEL = "llama-3.1-8b-instant"
        llm = ChatGroq(model=MODEL, temperature=0)

        messages = [
        ("system", "You are a financial supervisor."),
        ("human", prompt)
        ]

        res = llm.invoke(messages)
        print('********************LLM Response: Start ************************\n')
        print(res.content)
        print('********************LLM Response: End **************************\n\n')

        # Load the OpenAI API key from the environment variable
        # openai_api_key = os.getenv("OPENAI_API_KEY")
        # if not openai_api_key:
        #     raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")

        # client = openai.OpenAI(api_key=openai_api_key)  # Ensure you have the latest OpenAI library

        # response = client.chat.completions.create(
        #     model="gpt-4o",  # Use "gpt-4" if needed
        #     messages=[{"role": "system", "content": "You are a financial supervisor."},
        #               {"role": "user", "content": prompt}],
        #     max_tokens=100
        # )

        # suggested_comment = response.choices[0].message.content

        # print("Suggested comment:", suggested_comment)
