import requests
import json
from collections import defaultdict
import socket

def tokenize(log_line, delimiter=None):
    if delimiter:
        return log_line.strip().split(delimiter)
    else:
        return log_line.strip().split()

def identify_template(log_lines, min_freq=0.6):
    tokenized_logs = [tokenize(line) for line in log_lines]
    max_tokens = max(len(tokens) for tokens in tokenized_logs)
    
    position_token_freq = [defaultdict(int) for _ in range(max_tokens)]
    
    for tokens in tokenized_logs:
        for i in range(max_tokens):
            if i < len(tokens):
                position_token_freq[i][tokens[i]] += 1
            else:
                position_token_freq[i]["<MISSING>"] += 1
    
    template = []
    total_lines = len(log_lines)
    
    for pos in range(max_tokens):
        token_counts = position_token_freq[pos]
        most_common_token, count = max(token_counts.items(), key=lambda x: x[1])
        freq = count / total_lines
        
        if freq >= min_freq and most_common_token != "<MISSING>":
            template.append(most_common_token)
        else:
            template.append("<*>")
    return template

def parse_log(log_line, template):
    tokens = tokenize(log_line)
    parsed = {}
    
    if len(tokens) >= 3:
        timestamp = tokens[0] + " " + tokens[1]
        level = tokens[2]
        message = " ".join(tokens[3:]) if len(tokens) > 3 else ""
    else:
        timestamp = None
        level = None
        message = log_line
    if level!=None and level.upper()=="ERROR":
        parsed.update({
            "timestamp": timestamp,
            "level": level,
            "message": message,
            "host": socket.gethostname(),        # Update with your hostname if desired
            "service": "WinREAgent",  # Update with your service name
            "log.source": "read-log-file_python_kk"
        })
    
    return parsed

def send_logs_to_dynatrace(log_entries, dynatrace_url, api_token):
    print(f'log_entries.... {log_entries}')
    headers = {
        "Authorization": f"Api-Token {api_token}",
        "Content-Type": "application/json; charset=utf-8"
    }
    
    response = requests.post(dynatrace_url, headers=headers, data=json.dumps(log_entries))
    print(f"Sent {len(log_entries)} logs to Dynatrace")
    print("Response status code:", response.status_code)
    print("Response body:", response.text)

def parse_and_send_from_file(log_file_path, dynatrace_url, api_token, max_sample_lines=100):
    # Read some lines for template detection (limited to max_sample_lines)
    sample_lines = []
    with open(log_file_path, 'r') as f:
        for i, line in enumerate(f):
            if line.strip():
                sample_lines.append(line.strip())
            if i + 1 >= max_sample_lines:
                break

    if not sample_lines:
        print("Log file is empty or no valid lines found.")
        return

    print("Identifying log template based on sample lines...")
    template = identify_template(sample_lines)
    print("Identified template tokens:", template)

    # Parse entire file now and collect parsed logs
    parsed_logs = []
    with open(log_file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
  
            parsed = parse_log(line, template)
            if len(parse_log(line, template))!=0:
                parsed_logs.append(parsed)

    print(f"Parsed {len(parsed_logs)} log entries, sending to Dynatrace...")
    send_logs_to_dynatrace(parsed_logs, dynatrace_url, api_token)

if __name__ == "__main__":

    log_file_path = "C:\\Windows\\PFRO.log"  # Path to your log file
    log_file_path ="C:\Windows\Logs\WinREAgent\\setupact.log"
    dynatrace_endpoint = "https://lsm93412.live.dynatrace.com/api/v2/logs/ingest"  # Your Dynatrace environment URL
    api_token = "dt0c01.7EDLZFZ33DVD55XOQRJI6Z4L.BWK5LRASW3XNDY5X3V66XAGQKSAZJFXJPCJL5DGLZEUC5WUMZQ66MON5ITVAHX5R"  # Your Dynatrace API token with logs.ingest scope

    parse_and_send_from_file(log_file_path, dynatrace_endpoint, api_token)
