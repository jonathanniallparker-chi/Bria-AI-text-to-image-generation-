from generate_image_base import generate_image_base
from dotenv import load_dotenv
import os
from image_to_base64 import image_to_base64
from remove_background import remove_background 
from generate_background import generate_background
from nine_multiple_expand import multiple_expand_9
from create_grid import create_image_grid

# --------------------------------------------------------------------------------------------------
# 1. ADD AN API KEY TO THE .ENV FILE
# ---------------------------------------------ß-----------------------------------------------------

# --------------------------------------------------------------------------------------------------
# 2. THERE ARE 2 PLACES WITH PROMPTS BELOW IN generate_image_base() AND generate_background()
# ---------------------------------------------ß-----------------------------------------------------

# --------------------------------------------------------------------------------------------------
# 3. This Python script, generates a base image (prompt #1), remvoes the background, adds 3 
# backgrounds (Prompt #2) creating 3 seed_images. 
# The script then loops over each base image + background combo (3x), and creates 9 photos of 
# # 3 objects on 3 backgrounds with the object being in 3 positions. 
# These 9 photos are then added to a 3x3 grid.
# ---------------------------------------------ß-----------------------------------------------------

# ---------------------------------------------ß-----------------------------------------------------
# 4. I created this project in VS Studio, with Python 3, .VENV, and saved images in my directory. 
# ---------------------------------------------ß-----------------------------------------------------

# ---------------------------------------------ß-----------------------------------------------------
# 5. To run script, enter into terminal "python3 main1.py"
# ---------------------------------------------ß-----------------------------------------------------


load_dotenv()
api_key = os.getenv("BRIA_API_KEY")

# --------------------------------------------------------------------------------------------------
# Generate Text to Image, Save to Directory, Return Seed String
# ---------------------------------------------ß-----------------------------------------------------
#Prompt #1
prompt = "a silhouette of dragon's body, wings, legs, head, and tail, flying through the air, photorealistic"
print("Generating Image Base...")

result = generate_image_base(prompt, api_key)
print("Save Path:", result["save_path"])
save_path = result["save_path"]

seed_label = f"seed_{result['generated_image_seed']}"
print("Seed Label:", seed_label)

# --------------------------------------------------------------------------------------------------
# Base64 string for Generated Image
# --------------------------------------------------------------------------------------------------

base64_string = image_to_base64(result["save_path"])

# --------------------------------------------------------------------------------------------------
# Remove Background
# --------------------------------------------------------------------------------------------------

bg_removed = remove_background(base64_string)

# --------------------------------------------------------------------------------------------------
# Base64 string for Background Removed Image
# --------------------------------------------------------------------------------------------------

base64_string = image_to_base64(bg_removed["save_path_rmbk"])

# --------------------------------------------------------------------------------------------------
# Generate Background 
# --------------------------------------------------------------------------------------------------

# Prompts #2 
bg_prompts = [
    "in the sky with lightening, photorealistic style",
    "over a mountain range, photorealistic style",
    "dead sea valley at sunset, photorealistic style",
]

save_paths = []

for i, bg_prompt in enumerate(bg_prompts):
    save_name = f"{seed_label}_background_temp_{i}.png"
    bg_added = generate_background(bg_prompt, api_key, base64_string, save_name)

    project_dir = os.path.dirname(os.path.abspath(__file__))
    save_path_bg = os.path.join(project_dir, f"{seed_label}_background_generated_{i}.png")
    os.rename(bg_added["save_path"], save_path_bg)

    save_paths.append(save_path_bg)

print("All Backgrounds Generated and Saved:")
print(save_paths[0]) 
print(save_paths[1])  
print(save_paths[2]) 
    


# --------------------------------------------------------------------------------------------------
# 9x Expand
# --------------------------------------------------------------------------------------------------

saved_paths = [save_paths[0], save_paths[1], save_paths[2]]

variation_offsets = [
    {"location": [500, 1000], "size": [800, 800]},
    {"location": [1000, 1500], "size": [800, 800]},
    {"location": [1300, 2000], "size": [800, 800]},
]

expand_payloads = {}

for img_idx, base_path in enumerate(saved_paths, start=1):  
    base64_string = image_to_base64(base_path)
    
    for var_idx, var in enumerate(variation_offsets, start=1):  
        key = f"image_{img_idx}.{var_idx}"  
        payload = {
            "image": base64_string,
            "sync": True,
            "canvas_size": [2000, 3000],
            "original_image_location": var["location"],
            "original_image_size": var["size"],
        }
        expand_payloads[key] = payload

expand_save_paths = []  

for key, payload in expand_payloads.items():
    save_name = f"{key}_expanded.png" 
    result = multiple_expand_9(payload, api_key, save_name=save_name)
    if result and "save_path" in result:
        expand_save_paths.append(result["save_path"])
        print(f"Saved and returned: {result['save_path']}")

print("\nAll expanded save paths (list):")
print(expand_save_paths[i])

# --------------------------------------------------------------------------------------------------
# Create 3x3 Grid of Images
# --------------------------------------------------------------------------------------------------

image_files = [
    "/Users/jonathanniallparker/Desktop/briaAssignment/image_1.1_expanded.png",
    "/Users/jonathanniallparker/Desktop/briaAssignment/image_1.2_expanded.png",
    "/Users/jonathanniallparker/Desktop/briaAssignment/image_1.3_expanded.png",
    "/Users/jonathanniallparker/Desktop/briaAssignment/image_2.1_expanded.png",
    "/Users/jonathanniallparker/Desktop/briaAssignment/image_2.2_expanded.png",
    "/Users/jonathanniallparker/Desktop/briaAssignment/image_2.3_expanded.png",
    "/Users/jonathanniallparker/Desktop/briaAssignment/image_3.1_expanded.png",
    "/Users/jonathanniallparker/Desktop/briaAssignment/image_3.2_expanded.png",
    "/Users/jonathanniallparker/Desktop/briaAssignment/image_3.3_expanded.png"
]
create_image_grid(image_files, 3, 3)
