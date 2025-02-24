import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import openai
from src.sample_data import ALL_ALERTS

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

    # Create a FAISS index using L2 (Euclidean) distance
    d = embeddings.shape[1]  # Dimension of the embeddings
    index = faiss.IndexFlatL2(d)
    index.add(np.array(embeddings))

    # New alert that triggers comment suggestion
    new_alert = {
        "alert_id": "6",
        "instrument": "vanilla IR swaps",
        "alert_type": "Wash",
        "trade_details": "Related orders: [Order ID: D400, Size: 50M, Price: Swap rate 2.1%, Order Type: Market, Status: Executed, PnL: 100K, Volatility: Low], [Order ID: D401, Size: 50M, Price: Swap rate 2.1%, Order Type: Market, Status: Executed, PnL: 100K, Volatility: Low]",
    }
    new_embedding = model.encode([new_alert["trade_details"]])

    # Retrieve the top 3 similar historical alerts
    k = 3
    distances, indices = index.search(np.array(new_embedding), k)
    retrieved_alerts = [historical_alerts[i] for i in indices[0]]

    # Build the context from similar alerts
    context = ""
    for alert in retrieved_alerts:
        context += f"Trade details: {alert['trade_details']}\nComment: {alert['comment']}\n---\n"

    print (context)

    # # Construct the prompt for the LLM
    # prompt = f"""
    # Given the following historical trade alerts and their supervisor comments:
    # {context}
    # For a new alert with these details:
    # Trade details: {new_alert['trade_details']}
    # Risk profile: {new_alert['risk']}
    # PnL impact: {new_alert['pnl']}
    # Generate a concise supervisor comment for this alert.
    # """

    # # Call the LLM to generate a comment suggestion
    # client = openai.OpenAI(api_key="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")  # Ensure you have the latest OpenAI library

    # response = client.chat.completions.create(
    #     model="gpt-4o",  # Use "gpt-4" if needed
    #     messages=[{"role": "system", "content": "You are a financial supervisor."},
    #               {"role": "user", "content": prompt}],
    #     max_tokens=100
    # )

    # suggested_comment = response.choices[0].message.content

    # print("Suggested comment:", suggested_comment)
