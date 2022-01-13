# Trade APP
This app is a REST backend to add/get trade details in the trades app.
Get operation can be performed based on trade id and filters based on other fields

# Install dependencies
###
Recommend to run the following in a virtual environment.
###
pip install -r requirements.txt

# Run the app
uvicorn main:app --reload

# Access application
Go to following link
http://localhost:8000/docs

# Test Input
###
Click on POST request, Enter the following input data:
###
###
{
  "assetClass": "as1",
  "counterparty": "cp1",
  "instrumentId": "i1",
  "instrumentName": "iname1",
  "tradeDateTime": "2022-01-13T07:06:13.045Z",
  "tradeDetails": {
    "buySellIndicator": "BUY",
    "price": 100,
    "quantity": 4
  },
  "tradeId": "t001",
  "trader": "vinod"
}
###
