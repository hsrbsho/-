import requests
import pandas as pd
import time


def fetch_bond_data():
    url = "https://www.chinamoney.com.cn/ags/ms/cm-u-bond-md/BondMarketInfoListEN"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.chinamoney.com.cn/english/bdInfo/",
        "X-Requested-With": "XMLHttpRequest"
    }

    all_records = []
    for page in range(1, 15):
        payload = {
            "pageNo": str(page),
            "pageSize": "15",
            "issueYear": "2023",
            "bondType": "100001",
            "isNew": "1"
        }
        try:
            print(f"正在抓取第 {page} 页...")
            res = requests.post(url, data=payload, headers=headers, timeout=20)
            data_list = res.json().get("data", {}).get("resultList", [])

            if not data_list:
                break

            # --- 调试代码：仅在第一页打印第一条数据的结构，帮你彻底揪出 Issuer 标签 ---
            if page == 1:
                print("\n[系统检查] 第一条数据的原始字段如下，请检查哪个是 Ministry of Finance:")
                print(data_list[0])
                print("-" * 50)

            for r in data_list:
                # 修正后的字段映射：
                # Issuer -> 优先尝试 entyFullNameEN (英文全称)
                issuer = r.get("entyFullNameEN") or r.get("entyFullName") or r.get(
                    "entCorShortName") or "Ministry of Finance"

                # Issue Date -> 优先尝试 issueStartDateEN 或 issueStartDate
                issue_date = r.get("issueStartDate") or r.get("objPgAgDate") or r.get("issueStartDateEN")

                all_records.append({
                    "ISIN": r.get("isin"),
                    "Bond Code": r.get("bondCode"),
                    "Issuer": issuer,
                    "Bond Type": r.get("bondType"),
                    "Issue Date": issue_date,
                    "Latest Rating": r.get("rtgCpOutl")
                })

            if len(data_list) < 15: break
            time.sleep(1)

        except Exception as e:
            print(f"抓取异常: {e}")
            break

    if all_records:
        df = pd.DataFrame(all_records).drop_duplicates(subset=['Bond Code'])
        cols = ["ISIN", "Bond Code", "Issuer", "Bond Type", "Issue Date", "Latest Rating"]
        df = df[cols]

        try:
            filename = "ChinaMoney_Bonds_Final_Fixed.csv"
            df.to_csv(filename, index=False, encoding="utf-8-sig")
            print(f"\n✅ 抓取完成！共计 {len(df)} 条。")
            print("\n--- 数据前几行预览 ---")
            print(df[['Bond Code', 'Issuer', 'Issue Date']].head(5))
        except PermissionError:
            print("\n❌ 错误：请关闭 Excel 后重试！")
    else:
        print("未获取到数据。")


if __name__ == "__main__":
    fetch_bond_data()