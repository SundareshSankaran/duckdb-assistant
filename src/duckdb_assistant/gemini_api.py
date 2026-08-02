def generate_duckdb_query(system_prompt: str,user_prompt: str, explain_results: bool) -> dict:
    """This function generates DuckDB SQL based on a given user prompt using the Gemini API."""
    import os
    import json
    import time
    import random
    import re 
    from google import genai
    from google.genai import errors
    from dotenv import load_dotenv
    load_dotenv()  # Load environment variables from .env file

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    FALLBACK_MODELS = ["gemini-3.6-flash", "gemini-3.5-flash-lite", "gemini-3.5-flash", "gemini-3.1-pro-preview","gemini-3.1-flash-lite", "gemini-2.5-flash"]

    for model in FALLBACK_MODELS:
        try:
           response = client.models.generate_content(
               model=model,
               contents=system_prompt + "\n\n" + user_prompt 
               )
           break
        except Exception as e:
            print(errors)
            print(f"Error with model {model}: {e}")
            time_delay = random.uniform(1, 3)  # Random delay between 1 and 3 seconds
            print(f"Retrying with next model after {time_delay:.2f} seconds...")
            time.sleep(time_delay)
            continue

    response_text = response.text
    pattern = r"```(?:sql)?\s*\n(.*?)\n```"
    m = re.search(pattern, response_text, re.DOTALL | re.IGNORECASE)

    if m:
        duckdb_query = m.group(1).strip()
        response_dict = {"query": duckdb_query, "response_text": response_text}
    else:
        response_dict = {"query": "", "response_text": response_text}
    return response_dict