import re


def reg_search(text, regex_list):
    # --- 内部清洗功能：统一日期格式 ---
    def clean_format(val):
        # 匹配文本中是否含有类似 "2023 年 6 月 1 日" 的结构
        date_parts = re.findall(r'\d+', str(val))
        if '年' in str(val) and len(date_parts) >= 3:
            return f"{date_parts[0]}-{date_parts[1].zfill(2)}-{date_parts[2].zfill(2)}"
        return val

    # --- 预定义的规则库（应对原题或常见场景） ---
    # 只要 key 匹配上，就会自动调用这里的正则
    library = {
        '标的证券': r'股票代码：([\w\.]+)',
        '换股期限': r'(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日)'
    }

    final_output = []

    for task in regex_list:
        entry = {}
        for key, pattern in task.items():
            # 逻辑：如果 pattern 是自定义或空的，去规则库找；否则用用户手写的
            actual_rule = library.get(key) if (pattern == '*自定义*' or not pattern) else pattern

            if not actual_rule:
                entry[key] = None
                continue

            # 开始匹配
            matches = re.findall(actual_rule, text)

            if matches:
                # 清洗数据并处理输出（单项直接出，多项出列表）
                cleaned = [clean_format(m) for m in matches]
                entry[key] = cleaned[0] if len(cleaned) == 1 else cleaned
            else:
                entry[key] = None

        final_output.append(entry)

    return final_output


# ==========================================
# 场景一：跑通原题（使用预设规则）
# ==========================================
text_finance = "股票代码：600900.SH，时间：2023 年 6 月 2日至 2027 年 6 月 1 日"
rules_finance = [{'标的证券': '*自定义*', '换股期限': '*自定义*'}]
print("原题结果：", reg_search(text_finance, rules_finance))

# ==========================================
# 场景二：处理新文本（手动输入规则）
# ==========================================
text_order = "我的订单号是：TX12345，快递单号是：SF98765"
# 此时库里没有“订单”，我们需要手动输入规则
rules_order = [{'订单号': r'订单号是：(\w+)'}]
print("订单结果：", reg_search(text_order, rules_order))