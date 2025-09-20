import requests
import os
from dotenv import load_dotenv

load_dotenv()
bria_api_key = os.getenv("BRIA_API_KEY")

def remove_background(base64_string): 
    url = "https://engine.prod.bria-api.com/v2/image/edit/remove_background"
    headers = {"Content-Type": "application/json", "api_token": bria_api_key}
    payload = {"image": base64_string, "sync": True}

    if base64_string:
        print("Base64 String made it to remove_background function")

    try:
        response = requests.post(url, json=payload, headers=headers)

        try: 
            result = response.json()
        except Exception:
            print("Error: Failed to Parse JSON Response:", response.text)
            return None

        image_url = result["result"]["image_url"]
        
        project_dir = os.path.dirname(os.path.abspath(__file__))
        save_path_rmbk = os.path.join(project_dir, "seed_rmbk.png")

        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            with open(save_path_rmbk, "wb") as f:
                f.write(image_response.content)
            print(f"Image saved to {save_path_rmbk}")
        else:
            print(f"Failed to save image. Status code: {image_response.status_code}")

        print("Save Path:", save_path_rmbk)
        return {
            "save_path_rmbk": save_path_rmbk,
        }
    
    except Exception as e:
        print("Error processing API response:", str(e))
        return None
