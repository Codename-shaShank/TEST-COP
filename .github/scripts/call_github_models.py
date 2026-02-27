#!/usr/bin/env python3
"""
GitHub Models API client for calling AI models
Authenticates using GITHUB_TOKEN (from GitHub Actions) and calls GitHub Models
"""

import os
import sys
import json
import urllib.request
import urllib.error

def call_github_models(prompt_text, model="openai/gpt-4o"):
    """
    Call GitHub Models API using the correct endpoint and authentication.

    Args:
        prompt_text: The prompt to send to the model
        model: Default model name (can be overridden via MODEL_NAME env)

    Returns:
        The model's response text, or an error message if failed.
    """

    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token:
        return "Error: GITHUB_TOKEN environment variable not set"

    # Allow override from env (so your workflow can set MODEL_NAME)
    env_model = os.environ.get("MODEL_NAME")
    if env_model:
        model = env_model

    # Optional: normalize a few short aliases
    model_map = {
        "gpt-4o": "openai/gpt-4o",
        "gpt-4o-mini": "openai/gpt-4o-mini",
        "openai/gpt-4o-mini": "openai/gpt-4o-mini",
        "openai/gpt-4o": "openai/gpt-4o",
    }
    model = model_map.get(model, model)

    # GitHub Models API endpoint (NOT the Azure endpoint)
    api_endpoint = "https://models.github.ai/inference/chat/completions"

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You are an expert Ruby on Rails developer. Provide concise, actionable fixes.",
            },
            {
                "role": "user",
                "content": prompt_text,
            },
        ],
        "temperature": 1,
        "top_p": 1,
        "max_tokens": 4096,
    }

    headers = {
        "Authorization": f"Bearer {github_token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        # GitHub Models requires this header
        "X-GitHub-Api-Version": "2022-11-28",
    }

    try:
        request = urllib.request.Request(
            api_endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )

        with urllib.request.urlopen(request, timeout=30) as response:
            response_data = json.loads(response.read().decode("utf-8"))

        if "choices" in response_data and response_data["choices"]:
            message = response_data["choices"][0]["message"]["content"]
            return message
        else:
            return f"Error: Unexpected API response format: {response_data}"

    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        try:
            error_json = json.loads(error_body)
            error_msg = error_json.get("error", {}).get("message", str(error_json))
        except Exception:
            error_msg = error_body
        return f"Error: HTTP {e.code} - {error_msg}"
    except urllib.error.URLError as e:
        return f"Error: Network error - {e.reason}"
    except json.JSONDecodeError as e:
        return f"Error: Invalid JSON response - {e}"
    except Exception as e:
        return f"Error: {type(e).__name__}: {e}"

def main():
    """Read prompt from stdin and call GitHub Models API"""

    if not sys.stdin.isatty():
        prompt_text = sys.stdin.read()
    else:
        if len(sys.argv) > 1:
            prompt_text = " ".join(sys.argv[1:])
        else:
            print("Usage: python call_github_models.py < prompt.txt", file=sys.stderr)
            print("Or: echo 'prompt' | python call_github_models.py", file=sys.stderr)
            sys.exit(1)

    if not prompt_text.strip():
        print("Error: Empty prompt", file=sys.stderr)
        sys.exit(1)

    response = call_github_models(prompt_text)
    print(response)

    if response.strip().startswith("Error:"):
        sys.exit(1)

    sys.exit(0)

if __name__ == "__main__":
    main()
