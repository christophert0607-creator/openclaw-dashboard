import subprocess
import json
import sys
import time

def run_command(cmd):
    # print(f"Executing: {cmd}") # Debug
    while True:
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        if result.returncode != 0:
            if "rateLimitExceeded" in result.stderr or "403" in result.stderr or "quota" in result.stderr.lower():
                with open("error.log", "a") as f:
                    f.write(f"Rate limit hit, sleeping 10s...\n")
                time.sleep(10)
                continue
            with open("error.log", "a") as f:
                f.write(f"Error running command: {cmd}\n{result.stderr}\n")
            return None
        return result.stdout

def process_promotions(account):
    total_processed = 0
    while True:
        with open("status.log", "a") as f:
            f.write(f"Searching for promotions in {account}...\n")
        output = run_command(f'gog gmail search "label:INBOX category:promotions" --account {account} --json --limit 500')
        if not output:
            break
        
        try:
            data = json.loads(output)
            threads = data.get('threads', [])
            if not threads:
                with open("status.log", "a") as f:
                    f.write(f"No more promotions found for {account}.\n")
                break
            
            thread_ids = [t['id'] for t in threads]
            with open("status.log", "a") as f:
                f.write(f"Archiving {len(thread_ids)} threads from {account}...\n")
            
            for i in range(0, len(thread_ids), 50):
                batch_ids = thread_ids[i:i+50]
                id_list = " ".join(batch_ids)
                modify_cmd = f'gog gmail batch modify {id_list} --remove INBOX --account {account}'
                run_command(modify_cmd)
            
            total_processed += len(thread_ids)
            with open("status.log", "a") as f:
                f.write(f"Processed {total_processed} so far for {account}...\n")
            
            if len(thread_ids) < 500:
                break
        except Exception as e:
            with open("status.log", "a") as f:
                f.write(f"Error parsing JSON: {e}\n")
            break
    return total_processed

def process_finance(account):
    keywords = ["statement", "bill", "invoice", "settlement", "結單", "賬單", "收據", "futu", "mox", "ant bank"]
    query = " OR ".join([f'"{k}"' for k in keywords])
    total_processed = 0
    
    while True:
        with open("status.log", "a") as f:
            f.write(f"Searching for finance emails in {account}...\n")
        # Exclude those already labeled
        search_query = f'({query}) -label:Finance -label:Bills'
        output = run_command(f'gog gmail search "{search_query}" --account {account} --json --limit 500')
        if not output:
            break
            
        try:
            data = json.loads(output)
            threads = data.get('threads', [])
            if not threads:
                with open("status.log", "a") as f:
                    f.write(f"No more finance emails found for {account}.\n")
                break
            
            thread_ids = [t['id'] for t in threads]
            with open("status.log", "a") as f:
                f.write(f"Labeling {len(thread_ids)} threads as Finance/Bills in {account}...\n")
            
            for i in range(0, len(thread_ids), 50):
                batch_ids = thread_ids[i:i+50]
                id_list = " ".join(batch_ids)
                modify_cmd = f'gog gmail batch modify {id_list} --add Finance,Bills --account {account}'
                run_command(modify_cmd)
            
            total_processed += len(thread_ids)
            with open("status.log", "a") as f:
                f.write(f"Processed {total_processed} finance emails for {account}...\n")
            
            if len(thread_ids) < 500:
                break
        except Exception as e:
            with open("status.log", "a") as f:
                f.write(f"Error parsing JSON: {e}\n")
            break
    return total_processed

if __name__ == "__main__":
    accounts = ["christophert0607@gmail.com", "ahchung0607@gmail.com"]
    report = {}
    
    for acc in accounts:
        promo_count = process_promotions(acc)
        finance_count = process_finance(acc)
        report[acc] = {"promotions_archived": promo_count, "finance_labeled": finance_count}
    
    with open("status.log", "a") as f:
        f.write("\n=== FINAL REPORT ===\n")
        f.write(json.dumps(report, indent=2))
        f.write("\nDONE\n")
