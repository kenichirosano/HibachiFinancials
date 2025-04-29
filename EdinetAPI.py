import requests
import pandas as pd

# APIのエンドポイント
url = 'https://disclosure.edinet-fsa.go.jp/api/v2/documents.json'

# パラメータの設定（例: 2024年5月17日の書類を取得）
params = {
    'date': '2024-05-17',
    'type': 2,  # 2は有価証券報告書などの決算書類
    "Subscription-Key":"0b23b5dde3214e7c9e8ad15011c55a55"
}

# APIリクエストを送信
response = requests.get(url, params=params)

# レスポンスのJSONデータを取得
data = response.json()

# データフレームに変換
documents = data['results']
df = pd.DataFrame(documents)

# 特定のカラムだけを選択
df_filtered = df[['docID', 'secCode','edinetCode', 'filerName', 'docDescription', 'submitDateTime']]

# 決算情報のみをフィルタリング
df_financial = df_filtered[df_filtered['docDescription'].str.contains('有価証券報告書', na=False)]
df_financial

