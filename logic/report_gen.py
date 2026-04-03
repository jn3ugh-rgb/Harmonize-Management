def generate_report_text(target_month: str) -> str:
    """
    指定された月の報告メッセージを生成する（プロトタイプ版）
    """
    # ここに将来的にPLデータなどを組み込む
    report = f"【{target_month}度 業務報告書】\n\n"
    report += "今月の収支状況を報告いたします。\n"
    report += "詳細はダッシュボードをご確認ください。\n\n"
    report += "※このメッセージはシステムで自動生成されました。"
    
    return report