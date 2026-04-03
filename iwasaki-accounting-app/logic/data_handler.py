import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import streamlit as st

# 1. スプレッドシートへの接続設定
def get_spreadsheet():
    # Streamlitのsecretsから認証情報を取得
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scopes)
    client = gspread.authorize(creds)
    # スプレッドシートIDを指定して開く
    return client.open_by_key("1lTRGsGvPTdaBRhs-vaEecpkdb3oh-IIel_Ai2Hfijkk")

# 2. 【最重要】分割入金データの正規化（UNION処理）
def get_all_payment_plans():
    sh = get_spreadsheet()
    all_sheets = sh.worksheets()
    
    combined_data = []
    
    # 「分割：」で始まるシートをすべてループして統合する
    for ws in all_sheets:
        if ws.title.startswith("分割："):
            customer_name = ws.title.replace("分割：", "")
            data = ws.get_all_records() # 各行を辞書形式で取得
            
            for row in data:
                # 顧客名をカラムとして追加（これがDBの外部キー相当になる）
                row["customer_name"] = customer_name
                combined_data.append(row)
    
    # 後のNext.js移行を考え、Pandasでこねた後、辞書のリスト（JSON形式）で返す
    df = pd.DataFrame(combined_data)
    return df.to_dict(orient="records")

# 3. 月次PLデータの取得
def get_pl_summary(target_month: str) -> dict:
    sh = get_spreadsheet()
    # 損益計算書シートを特定（名前はRFPに合わせて調整）
    ws = sh.worksheet("（第6期）2025/10~2026/09")
    data = ws.get_all_records()
    df = pd.DataFrame(data)
    
    # 特定の月の列を抽出するロジック
    # Next.jsのAPIが返すJSONレスポンスを意識した構造にする
    summary = {
        "month": target_month,
        "sales": df.loc[df['項目名'] == '売上合計', target_month].values[0],
        "costs": df.loc[df['項目名'] == '費用合計', target_month].values[0],
        "profit": 0, # 計算ロジックを入れる
        "details": df.to_dict(orient="records")
    }
    summary["profit"] = summary["sales"] - summary["costs"]
    
    return summary