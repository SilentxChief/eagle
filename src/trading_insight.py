import numpy as np
import faiss
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from sentence_transformers import SentenceTransformer

load_dotenv()

# Generate mock market data
def generate_market_data():
    timestamps = [datetime.now() - timedelta(minutes=i*10) for i in range(100)]
    market_prices = {"IR Swaps": [], "Bonds": [], "Bond Future": [], "IR Futures": [], "IR Options": [], "FX Forward": []}
    
    for asset in market_prices.keys():
        base_price = random.uniform(100, 500)
        for _ in timestamps:
            market_prices[asset].append(round(base_price * (1 + random.uniform(-0.02, 0.02)), 2))
    
    return timestamps, market_prices

market_timestamps, market_prices = generate_market_data()

# Compute historical volatility
def compute_volatility(price_series):
    log_returns = np.log(np.array(price_series)[1:] / np.array(price_series)[:-1])
    return round(np.std(log_returns) * np.sqrt(len(price_series)), 2)  # Annualized volatility approximation

# Generate mock trader activity data
def generate_mock_data():
    traders = ["Trader_A", "Trader_B", "Trader_C", "Trader_D", "Trader_E"]
    desks = {"Trader_A": "Rates", "Trader_B": "Rates", "Trader_C": "Credit", "Trader_D": "Credit", "Trader_E": "FX"}
    assets = ["IR Swaps", "Bonds", "Bond Future", "IR Futures", "IR Options", "FX Forward"]
    trade_types = ["BUY", "SELL"]
    
    trader_data = []
    start_time = datetime.now() - timedelta(days=7)
    
    for _ in range(50):  # 50 mock trades
        trader = random.choice(traders)
        asset = random.choice(assets)
        trade_time = start_time + timedelta(minutes=random.randint(1, 10000))
        closest_market_index = min(range(len(market_timestamps)), key=lambda i: abs(market_timestamps[i] - trade_time))
        market_price = market_prices[asset][closest_market_index]
        
        trade = {
            "trader": trader,
            "desk": desks[trader],
            "timestamp": trade_time.strftime("%Y-%m-%d %H:%M:%S"),
            "asset": asset,
            "price": round(market_price * (1 + random.uniform(-0.01, 0.01)), 2),
            "quantity": random.randint(1, 100),
            "trade_type": random.choice(trade_types),
            "market_conditions": {
                "volatility": compute_volatility(market_prices[asset]),
                "bid_ask_spread": round(random.uniform(0.01, 0.5), 2),
                "market_price": market_price
            }
        }
        
        trader_data.append(trade)
    
    return trader_data

trader_activity_data = generate_mock_data()

# Initialize the SentenceTransformer model once
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Convert trader activity into text embeddings using SentenceTransformer
def get_embedding(text):
    return embedding_model.encode(text)

# Prepare embeddings
def prepare_embeddings(trader_data):
    embeddings = []
    texts = []
    for trade in trader_data:
        text_representation = f"Trader: {trade['trader']}, Desk: {trade['desk']}, Asset: {trade['asset']}, Type: {trade['trade_type']}, Price: {trade['price']}, Qty: {trade['quantity']}, Volatility: {trade['market_conditions']['volatility']}, Spread: {trade['market_conditions']['bid_ask_spread']}, Market Price: {trade['market_conditions']['market_price']}"
        embeddings.append(get_embedding(text_representation))
        texts.append(text_representation)
    return np.array(embeddings), texts

embeddings, text_data = prepare_embeddings(trader_activity_data)

# Store embeddings in FAISS
dimension = embeddings.shape[1]  # SentenceTransformer embedding size
t_index = faiss.IndexFlatL2(dimension)
t_index.add(embeddings)

# Function to query trader activity
def query_trader_activity(query_text, k=5):
    query_embedding = get_embedding(query_text)
    D, I = t_index.search(np.array([query_embedding]), k)  # Get top-k matches
    results = [text_data[i] for i in I[0]]
    return results

# Function to get insights from LLM
def get_insights(trader_activities):
    prompt = f"Analyze the following trader activities and provide insights:\n{chr(10).join(trader_activities)}\nInsights:"

    MODEL = "llama-3.1-8b-instant"
    llm = ChatGroq(model=MODEL, temperature=0)
    messages=[{"role": "user", "content": prompt}]

    response = llm.invoke(messages)
    return response.content

# Example query
query = "Find unusual trading patterns in Bonds in the last week"
matching_activities = query_trader_activity(query)
insights = get_insights(matching_activities)

print("Relevant Trades:")
for trade in matching_activities:
    print(trade)
print("\nInsights:")
print(insights)