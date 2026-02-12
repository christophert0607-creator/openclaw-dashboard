import sys
import json
import re
from datetime import datetime

def extract_mox_data(email_json):
    data = json.loads(email_json)
    body = data.get('body', '')
    subject = data.get('headers', {}).get('subject', '')
    date_str = data.get('headers', {}).get('date', '')
    
    # Try to parse date
    # Thu, 5 Feb 2026 09:37:30 +0000
    try:
        dt = datetime.strptime(re.sub(r' \(.*\)', '', date_str), "%a, %d %b %Y %H:%M:%S %z")
    except:
        dt = datetime.now()

    result = {
        "date": dt.strftime("%Y-%m-%d %H:%M:%S"),
        "month": dt.strftime("%Y-%m"),
        "year": dt.strftime("%Y"),
        "type": "Other",
        "amount": 0.0,
        "description": "",
        "merchant": ""
    }

    # Clean body
    clean_body = re.sub(r'<[^>]+>', ' ', body)
    clean_body = re.sub(r'\s+', ' ', clean_body).strip()

    if "轉數成功" in subject or "轉數成功" in clean_body:
        result["type"] = "Transfer Out"
        match = re.search(r"向(.+?)付款HKD([\d,]+\.\d{2})", clean_body)
        if match:
            result["merchant"] = match.group(1).strip()
            result["amount"] = -float(match.group(2).replace(',', ''))
        result["description"] = "FPS Out"
    elif "收到款項" in subject or "收到款項" in clean_body:
        result["type"] = "Transfer In"
        match = re.search(r"(.+?)已向你付款HKD([\d,]+\.\d{2})", clean_body)
        if match:
            result["merchant"] = match.group(1).strip()
            result["amount"] = float(match.group(2).replace(',', ''))
        result["description"] = "FPS In"
    elif "成功入錢至你在Mox 的戶口" in subject or "成功入錢至你在Mox的戶口" in clean_body:
        result["type"] = "Deposit"
        match = re.search(r"入錢HKD([\d,]+\.\d{2})至你在Mox的戶口", clean_body)
        if match:
            result["amount"] = float(match.group(1).replace(',', ''))
        result["description"] = "Deposit/Add Money"
    elif "交易已完成" in subject or "消費" in clean_body:
        result["type"] = "Payment"
        match = re.search(r"在(.+?)消費HKD([\d,]+\.\d{2})", clean_body)
        if match:
            result["merchant"] = match.group(1).strip()
            result["amount"] = -float(match.group(2).replace(',', ''))
        result["description"] = "Card Payment"
    elif "直接付款成功" in subject:
        result["type"] = "Direct Debit"
        match = re.search(r"向(.+?)支付HKD([\d,]+\.\d{2})", clean_body)
        if match:
            result["merchant"] = match.group(1).strip()
            result["amount"] = -float(match.group(2).replace(',', ''))
        result["description"] = "Direct Debit"
    
    return result

if __name__ == "__main__":
    emails = sys.stdin.read().split('\n--EMAIL_BOUNDARY--\n')
    results = []
    for email in emails:
        if email.strip():
            try:
                results.append(extract_mox_data(email))
            except Exception as e:
                pass
    print(json.dumps(results, indent=2, ensure_ascii=False))
