import streamlit as st
import pandas as pd
from logic.data_handler import get_all_payment_plans, get_pl_summary
from logic.report_gen import generate_report_text

# ページ設定
st.set_page_config(
    page_title="岩崎経理代行システム | MVP",
    page_icon="📊",
    layout="wide"
)

# サイドメニューの作成
st.sidebar.title("🛠️ 管理メニュー")
menu = st.sidebar.radio(
    "機能を選択してください",
    ["接続テスト", "ダッシュボード", "分割入金管理", "報告メッセージ生成"]
)

# --- 1. 接続テスト（既存のデバッグ用） ---
if menu == "接続テスト":
    st.title("🔗 Google Sheets 接続テスト")
    st.info("スプレッドシートから全顧客の分割データを統合して取得します。")
    
    if st.button("全顧客の分割データを取得"):
        with st.spinner("データを取得中..."):
            try:
                data = get_all_payment_plans()
                st.success(f"取得に成功しました！ 取得件数: {len(data)}件")
                
                # 取得したデータをテーブル形式で表示
                df = pd.DataFrame(data)
                st.subheader("取得データプレビュー（最初の5件）")
                st.table(df.head(5))
                
                # データ構造の確認（エンジニア用）
                with st.expander("生のJSON構造を確認"):
                    st.json(data[:2])
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")

# --- 2. ダッシュボード（PL可視化） ---
elif menu == "ダッシュボード":
    st.title("📊 月次収支サマリー")
    # ここではRFPに合わせ、2026年3月などを選択肢にする想定
    target_month = st.selectbox("対象月を選択", ["2026/03", "2026/02", "2026/01"])
    
    if st.button("サマリーを表示"):
        summary = get_pl_summary(target_month)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("売上合計", f"¥{summary['sales']:,}")
        col2.metric("費用合計", f"¥{summary['costs']:,}")
        col3.metric("当月利益", f"¥{summary['profit']:,}")
        
        st.subheader("収支詳細")
        st.table(pd.DataFrame(summary['details']))

# --- 3. 分割入金管理 ---
elif menu == "分割入金管理":
    st.title("💳 分割入金・消込管理")
    st.write("全顧客の分割支払い状況を横断的に確認できます。")
    
    with st.spinner("最新の支払い状況を読み込み中..."):
        data = get_all_payment_plans()
        df = pd.DataFrame(data)
        
        # 未入金（入金額が0または予定額より少ない）のものを抽出するなどのフィルタも可能
        st.dataframe(df, use_container_width=True)

# --- 4. 報告メッセージ生成 ---
elif menu == "報告メッセージ生成":
    st.title("✉️ 報告メッセージ作成")
    target_month = st.selectbox("報告対象月", ["2026/03", "2026/02"])
    
    if st.button("メッセージを生成"):
        with st.spinner("集計と文章作成を行っています..."):
            report = generate_report_text(target_month)
            st.subheader("生成された文面")
            st.text_area(
                label="このままコピーして報告に使用できます",
                value=report,
                height=400
            )
            st.caption("※現時点ではPDF出力機能はプロトタイプ対象外です。")

# フッター
st.sidebar.markdown("---")
st.sidebar.caption("Powered by Non-chan DX Prototype")