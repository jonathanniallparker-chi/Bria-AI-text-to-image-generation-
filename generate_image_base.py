import requests
import os

# # --------------------------------------------------------------------------------------------------
# # Generate Base from Bria AI 
# # --------------------------------------------------------------------------------------------------

def generate_image_base(prompt, api_key):
    url = "https://engine.prod.bria-api.com/v1/text-to-image/base/3.2"
    headers = {"Content-Type": "application/json", "api_token": api_key}
    payload = {"prompt": prompt, "num_results": 1, "sync": True}

    try:
        response = requests.post(url, json=payload, headers=headers)
        result = response.json()

        image_url = result["result"][0]["urls"][0]
        seed = result["result"][0]["seed"]

        project_dir = os.path.dirname(os.path.abspath(__file__))
        save_path = os.path.join(project_dir, f"seed_{seed}.png")

        response = requests.get(image_url)
        if response.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(response.content)

        else:
            print(f"Failed to save image. Status code: {response.status_code}")

        return {
            "generated_image_seed": seed,
            "save_path": save_path,
        }

    except (KeyError, IndexError, TypeError) as e:
        print("Error processing API response:", str(e))

        return result

    