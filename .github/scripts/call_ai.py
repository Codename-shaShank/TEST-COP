#!/usr/bin/env python3
import json
import urllib.request
import os
import sys

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 call_ai.py <prompt_file> <output_file>")
        sys.exit(1)

    prompt_file = sys.argv[1]
    output_file = sys.argv[2]
    
    token = os.environ.get("GH_TOKEN")
    if not token:
        print("Error: GH_TOKEN environment variable not set.")
        sys.exit(1)

    try:
        with open(prompt_file, 'r', encoding='utf-8') as f:
            prompt_text = f.read()
    except Exception as e:
        print(f"Error reading prompt file: {e}")
        sys.exit(1)

    url = "https://models.inference.ai.azure.com/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    data = {
        "model": "gpt-4o",
        "messages": [
            {"role": "user", "content": prompt_text}
        ],
        "temperature": 0.2
    }
    
    req = urllib.request.Request(
        url, 
        data=json.dumps(data).encode('utf-8'), 
        headers=headers
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            output_text = result['choices'][0]['message']['content']
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(output_text)
                
            print(f"Successfully called AI and saved response to {output_file}")
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")
        error_body = e.read().decode('utf-8')
        print(f"Error details: {error_body}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
