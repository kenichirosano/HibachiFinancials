import requests
import pandas as pd
# Import the get_api_key function from the api_key module
from api_key import get_api_key

# API's URL
url = 'https://disclosure.edinet-fsa.go.jp/api/v2/documents.json'

# Set the parameters for the API request and send the request
api_key = get_api_key()
params = {
    'date': '2025-05-01',
    'type': 2,  # 2は有価証券報告書などの決算書類
    "Subscription-Key": api_key,
}
response = requests.get(url, params=params)

# Convert the response JSON to a DataFrame 
data = response.json()
documents = data['results']
df = pd.DataFrame(documents)

# Save 
df.head()

# 特定のカラムだけを選択
df_filtered = df[['docID', 'secCode','edinetCode', 'filerName', 'docDescription', 'submitDateTime']]

# 決算情報のみをフィルタリング
df_financial = df_filtered[df_filtered['docDescription'].str.contains('有価証券報告書', na=False)]
df_financial

