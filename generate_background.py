import requests
import os

# --------------------------------------------------------------------------------------------------
# Generate Background for Image 
# --------------------------------------------------------------------------------------------------

def generate_background(bg_prompt, api_key, base64_string, save_name):
    url = "https://engine.prod.bria-api.com/v2/image/edit/replace_background"
    headers = {"Content-Type": "application/json", "api_token": api_key}
    payload = {"image": base64_string, "prompt": bg_prompt, "sync": True}

    if base64_string:
        print("Base64 String made it to generate_background function")

    try:
        response = requests.post(url, json=payload, headers=headers)
        result = response.json()

        image_url = result["result"]["image_url"]

        project_dir = os.path.dirname(os.path.abspath(__file__))
        save_path = os.path.join(project_dir, save_name)

        response = requests.get(image_url)
        if response.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(response.content)

        else:
            print(f"Failed to save image. Status code: {response.status_code}")

        return {
            "save_path": save_path,
        }

    except (KeyError, IndexError, TypeError) as e:
        print("Error processing API response:", str(e))

        return result
