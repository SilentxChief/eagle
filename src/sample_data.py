base_alerts = [
  {
      "alert_id": "1",
      "instrument": "bonds",
      "trade_details": "Buy 10M bonds at 99.5; low risk, normal PnL",
      "comment": "Legitimate trade; no action required."
  },
  {
      "alert_id": "2",
      "instrument": "bonds",
      "alert_type": "Spoofing",
      "trade_details": "Related orders: [Order ID: A123, Size: 5M, Price: 100.2, Order Type: Limit, Status: Placed, PnL: -50K, Volatility: High], [Order ID: A124, Size: 4.9M, Price: 100.3, Order Type: Cancel, Status: Cancelled, PnL: 0, Volatility: Medium]",
      "comment": "Potential spoofing; monitor trader activity."
  },
  {
      "alert_id": "3",
      "instrument": "cds",
      "alert_type": "Ramping",
      "trade_details": "Related orders: [Order ID: B200, Size: 1M, Price: Par+2, Order Type: Market, Status: Executed, PnL: 20K, Volatility: Medium], [Order ID: B201, Size: 2M, Price: Par+3, Order Type: Market, Status: Executed, PnL: 50K, Volatility: High]",
      "comment": "Check counterparty risk exposure."
  },
  {
      "alert_id": "4",
      "instrument": "bond futures",
      "alert_type": "Layering",
      "trade_details": "Related orders: [Order ID: C300, Size: 10, Price: 130.5, Order Type: Limit, Status: Placed, PnL: -10K, Volatility: Medium], [Order ID: C301, Size: 15, Price: 130.6, Order Type: Limit, Status: Placed, PnL: -15K, Volatility: High], [Order ID: C302, Size: 25, Price: 130.7, Order Type: Cancel, Status: Cancelled, PnL: 0, Volatility: Low]",
      "comment": "Hedging activity confirmed; no action needed."
  },
  {
      "alert_id": "5",
      "instrument": "vanilla IR swaps",
      "alert_type": "Wash",
      "trade_details": "Related orders: [Order ID: D400, Size: 50M, Price: Swap rate 2.1%, Order Type: Market, Status: Executed, PnL: 100K, Volatility: Low], [Order ID: D401, Size: 50M, Price: Swap rate 2.1%, Order Type: Market, Status: Executed, PnL: 100K, Volatility: Low]",
      "comment": "Review rate risk and counterparty."
  }
]

# Generate additional alerts dynamically
additional_alerts = [
  {
      "alert_id": str(i),
      "instrument": ["bonds", "cds", "bond futures", "vanilla IR swaps", "fx forwards", "fx futures"][i % 6],
      "alert_type": ["Ramping", "Layering", "Spoofing", "Off-Market"][i % 4],
      "trade_details": f"Related orders: [Order ID: F{i}A, Size: {i % 10 + 1}M, Price: {99 + (i % 5) * 0.1}, Order Type: Limit, Status: Placed, PnL: {(i % 5) * 10}K, Volatility: {['Low', 'Medium', 'High'][i % 3]}], [Order ID: F{i}B, Size: {i % 10 + 1}M, Price: {99 + (i % 5) * 0.2}, Order Type: Cancel, Status: Cancelled, PnL: 0, Volatility: {['Low', 'Medium', 'High'][i % 3]}]",
      "comment": f"Auto-generated comment {i}"
  }
  for i in range(6, 2001)
]


TEST_ALERTS = [
  {
    "alert_id": "1",
    "instrument": "vanilla IR swaps",
    "alert_type": "Wash",
    "trade_details": "Related orders: [Order ID: D400, Size: 50M, Price: Swap rate 2.1%, Order Type: Market, Status: Executed, PnL: 100K, Volatility: Low], [Order ID: D401, Size: 50M, Price: Swap rate 2.1%, Order Type: Market, Status: Executed, PnL: 100K, Volatility: Low]",
    "comment": "Review rate risk and counterparty."
  },
  {
    "alert_id": "2",
    "instrument": "equity options",
    "alert_type": "Spoofing",
    "trade_details": "Related orders: [Order ID: E500, Size: 10K, Price: $50.00, Order Type: Limit, Status: Canceled, PnL: 0, Volatility: High], [Order ID: E501, Size: 10K, Price: $50.05, Order Type: Market, Status: Executed, PnL: 50K, Volatility: High]",
    "comment": "Investigate potential spoofing activity."
  },
  {
    "alert_id": "3",
    "instrument": "FX forwards",
    "alert_type": "Front Running",
    "trade_details": "Related orders: [Order ID: F600, Size: 5M, Price: 1.2000 EUR/USD, Order Type: Market, Status: Executed, PnL: 20K, Volatility: Medium], [Order ID: F601, Size: 5M, Price: 1.1995 EUR/USD, Order Type: Market, Status: Executed, PnL: 25K, Volatility: Medium]",
    "comment": "Check for front running indicators."
  },
  {
    "alert_id": "4",
    "instrument": "commodity futures",
    "alert_type": "Insider Trading",
    "trade_details": "Related orders: [Order ID: C700, Size: 100 contracts, Price: $70.00, Order Type: Market, Status: Executed, PnL: 150K, Volatility: High], [Order ID: C701, Size: 100 contracts, Price: $71.00, Order Type: Market, Status: Executed, PnL: 140K, Volatility: High]",
    "comment": "Analyze for insider trading signals."
  },
  {
    "alert_id": "5",
    "instrument": "corporate bonds",
    "alert_type": "Marking the Close",
    "trade_details": "Related orders: [Order ID: B800, Size: 2M, Price: 99.50, Order Type: Market, Status: Executed, PnL: 10K, Volatility: Low], [Order ID: B801, Size: 2M, Price: 99.75, Order Type: Market, Status: Executed, PnL: 15K, Volatility: Low]",
    "comment": "Evaluate end-of-day trading patterns."
  }
]

# Combine base alerts with additional alerts
ALL_ALERTS = base_alerts + additional_alerts