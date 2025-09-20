import os
import time
import requests
from requests.exceptions import RequestException, SSLError

def multiple_expand_9(payload, api_token, save_name, max_retries=3):

    url = "https://engine.prod.bria-api.com/v2/image/edit/expand"
    headers = {"Content-Type": "application/json", "api_token": api_token}

    try:

        response = requests.post(url, json=payload, headers=headers, timeout=60)
        result = response.json()


        if "result" not in result or "image_url" not in result["result"]:
            print(f"API did not return a valid result for {save_name}. Full response: {result}")
            return None

        image_url = result["result"]["image_url"]

        project_dir = os.path.dirname(os.path.abspath(__file__))
        save_path = os.path.join(project_dir, save_name)

        for attempt in range(1, max_retries + 1):
            try:
                img_response = requests.get(image_url, timeout=60, stream=True)
                img_response.raise_for_status()

                with open(save_path, "wb") as f:
                    for chunk in img_response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)

                return {"save_path": save_path}  

            except (RequestException, SSLError) as e:
                print(f"Attempt {attempt} failed for {save_name}: {e}")
                if attempt < max_retries:
                    time.sleep(2)  
                else:
                    print(f"Failed to download {save_name} after {max_retries} attempts")
                    return None

    except requests.exceptions.Timeout:
        print(f"POST request timed out for {save_name}. Skipping this image.")
        return None
    except Exception as e:
        print(f"Unexpected error for {save_name}: {str(e)}")
        return None
