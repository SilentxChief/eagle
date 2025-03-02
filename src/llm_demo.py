import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from src.sample_data import ALL_ALERTS, TEST_ALERTS
from tabulate import tabulate

load_dotenv()

#This is naga's code
def format_alert_for_embedding(alert):
    # Emphasize the alert type by repeating it
    alert_type_str = f"ALERT TYPE: {alert['alert_type']} " * 3
    details = "; ".join(
        ", ".join(f"{k}: {v}" for k, v in order.items())
        for order in alert["trade_details"]
    )
    return f"{alert_type_str}; Instrument: {alert['instrument']}; Trade Details: {details}"

def format_trade_details_for_print(alert):
    # Format trade_details for readable print in tabular format
    headers = alert["trade_details"][0].keys()
    rows = [order.values() for order in alert["trade_details"]]
    return tabulate(rows, headers, tablefmt="grid")

def run():
    # Initialize the embedding model (adjust model name as needed)
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Sample historical alerts with trade details and supervisor comments
    historical_alerts = ALL_ALERTS

    # Compute embeddings for the trade details of historical alerts using structured format
    trade_texts = [format_alert_for_embedding(alert) for alert in historical_alerts]
    embeddings = model.encode(trade_texts)

    # No normalization step – using raw embeddings for Euclidean (L2) distance
    # Create an IVF index
    nlist = 100  # Number of clusters
    d = embeddings.shape[1]  # Dimension of the embeddings
    quantizer = faiss.IndexFlatL2(d)  # Quantizer using L2 (Euclidean) distance
    index = faiss.IndexIVFFlat(quantizer, d, nlist, faiss.METRIC_L2)

    # Train the index
    index.train(np.array(embeddings))

    # Add embeddings to the index
    index.add(np.array(embeddings))

    # Test new alert that triggers comment suggestion
    for new_alert in TEST_ALERTS:
        new_trade_text = [format_alert_for_embedding(new_alert)]
        new_embedding = model.encode(new_trade_text)

        # Retrieve the top 2 similar historical alerts
        k = 2
        distances, indices = index.search(np.array(new_embedding), k)
        retrieved_alerts = [historical_alerts[i] for i in indices[0]]

        # Build the context from similar alerts
        context = ""
        for alert in retrieved_alerts:
            context += (
                "--------------------------------------------------\n"
                f"Trade details:\n{format_trade_details_for_print(alert)}\n"
                f"Alert Type: {alert['alert_type']}\n"
                f"Comment: {alert['comment']}\n"
            )
        context += "--------------------------------------------------\n"

        # Construct the prompt for the LLM
        prompt = (
            "Given the following historical trade alerts and their supervisor comments:\n"
            f"{context}\n"
            "For a new alert with these details:\n"
            f"Trade details:\n{format_trade_details_for_print(new_alert)}\n"
            f"Instrument: {new_alert['instrument']}\n\n"
            "Generate a brief functional comment on behalf of a Trading Supervisor, "
            "with reference to the trade details above, without mentioning historical trades or alerts.\n"
            f"Per AI Overview: State if it is a legitimate trade or if any action is required as the system reported it as {new_alert['alert_type']}.\n"
        )

        # Print the constructed prompt in a readable format
        print("\n" + "="*100)
        print("LLM Prompt: Start")
        print("="*100)
        print(prompt)
        print("="*100)
        print("LLM Prompt: End")
        print("\n" + "="*100)

        # Call the LLM to generate a comment suggestion
        MODEL = "llama-3.1-8b-instant"
        llm = ChatGroq(model=MODEL, temperature=0)
        messages = [
            ("system", "You are a financial supervisor."),
            ("human", prompt)
        ]
        res = llm.invoke(messages)
        
        # Print the LLM response neatly formatted
        print("\n" + "#"*100)
        print("LLM Response: Start")
        print("#"*100)
        print(res.content)
        print("#"*100)
        print("LLM Response: End")
        print("\n" + "#"*100)

if __name__ == "__main__":
    run()