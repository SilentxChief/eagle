base_alerts = [
  {
      "alert_id": "1",
      "instrument": "equity",
      "alert_type": "Wash",
      "trade_details": [
          {"Order ID": "A100", "Size": 1000, "Price": 50.5, "Order Type": "Market", "Status": "Executed", "PnL": "5K", "Volatility": "Low"},
          {"Order ID": "A101", "Size": 1000, "Price": 50.5, "Order Type": "Market", "Status": "Executed", "PnL": "5K", "Volatility": "Low"}
      ],
      "comment": "Potential wash trade detected. Both orders executed at the same price and size, indicating possible self-trading. Further investigation required."
  },
  {
      "alert_id": "2",
      "instrument": "bond futures",
      "alert_type": "Front Running",
      "trade_details": [
          {"Order ID": "B200", "Size": 500, "Price": 101.2, "Order Type": "Limit", "Status": "Placed", "PnL": "10K", "Volatility": "Medium"},
          {"Order ID": "B201", "Size": 500, "Price": 101.5, "Order Type": "Market", "Status": "Executed", "PnL": "15K", "Volatility": "High"}
      ],
      "comment": "Possible front running activity. A limit order placed ahead of a market order raises concerns. Review trader activity for potential misconduct."
  },
  {
      "alert_id": "3",
      "instrument": "FX forwards",
      "alert_type": "Spoofing",
      "trade_details": [
          {"Order ID": "C300", "Size": 200, "Price": 1.305, "Order Type": "Limit", "Status": "Placed", "PnL": "-2K", "Volatility": "High"},
          {"Order ID": "C301", "Size": 200, "Price": 1.306, "Order Type": "Limit", "Status": "Cancelled", "PnL": "0", "Volatility": "Low"}
      ],
      "comment": "Suspected spoofing detected. Large orders were placed and then cancelled quickly. Investigate the intent behind these orders."
  },
  {
      "alert_id": "4",
      "instrument": "bond futures",
      "alert_type": "Front Running",
      "trade_details": [
          {"Order ID": "D400", "Size": 300, "Price": 130.5, "Order Type": "Limit", "Status": "Placed", "PnL": "-3K", "Volatility": "Medium"},
          {"Order ID": "D401", "Size": 300, "Price": 130.6, "Order Type": "Limit", "Status": "Placed", "PnL": "-4K", "Volatility": "High"}
      ],
      "comment": "Front running activity detected. Orders placed just in advance of large market orders suggest potential malpractice. A detailed review is recommended."
  },
  {
      "alert_id": "5",
      "instrument": "vanilla IR swaps",
      "alert_type": "Spoofing",
      "trade_details": [
          {"Order ID": "E500", "Size": 50000000, "Price": "Swap rate 2.1%", "Order Type": "Market", "Status": "Executed", "PnL": "100K", "Volatility": "Low"},
          {"Order ID": "E501", "Size": 50000000, "Price": "Swap rate 2.1%", "Order Type": "Market", "Status": "Executed", "PnL": "100K", "Volatility": "Low"}
      ],
      "comment": "Suspicious spoofing behavior detected. The orders show anomalies in execution timing and pricing. Immediate review is needed."
  },
  {
      "alert_id": "6",
      "instrument": "equity",
      "alert_type": "Spoofing",
      "trade_details": [
          {"Order ID": "F600", "Size": 1000, "Price": 50.5, "Order Type": "Limit", "Status": "Placed", "PnL": "5K", "Volatility": "Low"},
          {"Order ID": "F601", "Size": 1000, "Price": 50.6, "Order Type": "Limit", "Status": "Cancelled", "PnL": "0", "Volatility": "Low"}
      ],
      "comment": "False Positive detected. Orders were cancelled as part of a legitimate trading strategy. No further action needed."
  }
]

additional_alerts = [
  {
      "alert_id": str(i),
      "instrument": ["bonds", "cds", "bond futures", "vanilla IR swaps", "fx forwards", "fx futures"][i % 6],
      "alert_type": ["Wash", "Layering", "Spoofing", "Front Running"][i % 4],
      "trade_details": [
          {"Order ID": f"F{i}A", "Size": f"{i % 10 + 1}M", "Price": f"{99 + (i % 5) * 0.1}", "Order Type": "Limit", "Status": "Placed", "PnL": f"{(i % 5) * 10}K", "Volatility": ["Low", "Medium", "High"][i % 3]},
          {"Order ID": f"F{i}B", "Size": f"{i % 10 + 1}M", "Price": f"{99 + (i % 5) * 0.2}", "Order Type": "Cancel", "Status": "Cancelled", "PnL": "0", "Volatility": ["Low", "Medium", "High"][i % 3]}
      ],
      "comment": f"Alert {i}: Signs of {['wash trading', 'layering', 'spoofing', 'front running'][i % 4]} observed. Please verify for potential market misconduct."
  }
  for i in range(7, 2001)
]

ALL_ALERTS = base_alerts + additional_alerts

TEST_ALERTS = [
  {
    "alert_id": "5000",
    "instrument": "vanilla IR swaps",
    "alert_type": "Wash",
    "trade_details": [
        {"Order ID": "G5000", "Size": 50000000, "Price": "Swap rate 2.1%", "Order Type": "Market", "Status": "Executed", "PnL": "100K", "Volatility": "Low"},
        {"Order ID": "G5001", "Size": 50000000, "Price": "Swap rate 2.1%", "Order Type": "Market", "Status": "Executed", "PnL": "100K", "Volatility": "Low"}
    ],
    "comment": "Potential wash trade detected. Both orders executed at the same rate and size, indicating possible self-trading. Further investigation required."
  },
  {
    "alert_id": "5001",
    "instrument": "bond futures",
    "alert_type": "Front Running",
    "trade_details": [
        {"Order ID": "H5000", "Size": 500, "Price": 101.2, "Order Type": "Limit", "Status": "Placed", "PnL": "10K", "Volatility": "Medium"},
        {"Order ID": "H5001", "Size": 500, "Price": 101.5, "Order Type": "Market", "Status": "Executed", "PnL": "15K", "Volatility": "High"}
    ],
    "comment": "Possible front running activity. A limit order placed prior to a market order suggests potential misconduct. Review required."
  },
  {
    "alert_id": "5002",
    "instrument": "FX forwards",
    "alert_type": "Spoofing",
    "trade_details": [
        {"Order ID": "I5000", "Size": 200, "Price": 1.305, "Order Type": "Limit", "Status": "Placed", "PnL": "-2K", "Volatility": "High"},
        {"Order ID": "I5001", "Size": 200, "Price": 1.306, "Order Type": "Limit", "Status": "Cancelled", "PnL": "0", "Volatility": "Low"}
    ],
    "comment": "Suspected spoofing behavior with quick cancellation. Investigate to confirm if this is an attempt to manipulate prices."
  },
  {
    "alert_id": "5003",
    "instrument": "bond futures",
    "alert_type": "Layering",
    "trade_details": [
        {"Order ID": "J5000", "Size": 300, "Price": 130.5, "Order Type": "Limit", "Status": "Placed", "PnL": "-3K", "Volatility": "Medium"},
        {"Order ID": "J5001", "Size": 300, "Price": 130.6, "Order Type": "Limit", "Status": "Placed", "PnL": "-4K", "Volatility": "High"},
        {"Order ID": "J5002", "Size": 300, "Price": 130.7, "Order Type": "Cancel", "Status": "Cancelled", "PnL": "0", "Volatility": "Low"}
    ],
    "comment": "Layering activity observed. Review multiple limit orders for potential manipulation of market pricing."
  },
  {
    "alert_id": "5004",
    "instrument": "equity",
    "alert_type": "Spoofing",
    "trade_details": [
        {"Order ID": "K5000", "Size": 1000, "Price": 50.5, "Order Type": "Limit", "Status": "Placed", "PnL": "5K", "Volatility": "Low"},
        {"Order ID": "K5001", "Size": 1000, "Price": 50.6, "Order Type": "Limit", "Status": "Cancelled", "PnL": "0", "Volatility": "Low"}
    ],
    "comment": "Potential spoofing detected but appears to be a false alarm. The order cancellation was part of a regular risk management process."
  }
]