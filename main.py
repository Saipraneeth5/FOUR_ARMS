import requests
import base64
import os
import tkinter as tk
from tkinter import filedialog


# Function to open a file dialog and let the user select an image
def select_image(title="Select an Image"):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(title=title, filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    return file_path


# Function to convert an image file to base64
def image_file_to_base64(image_path):
    with open(image_path, 'rb') as f:
        image_data = f.read()
    return base64.b64encode(image_data).decode('utf-8')


# Function to save base64 image to a file
def save_base64_image(base64_string, output_path):
    image_data = base64.b64decode(base64_string)
    with open(output_path, 'wb') as f:
        f.write(image_data)
    print(f"Image saved at: {output_path}")


# Function to open the saved image (Windows only)
def open_image(file_path):
    try:
        os.startfile(file_path)  # Windows-specific
    except Exception as e:
        print(f"Could not open image: {e}")


# Load API key (secure approach)
api_key = "SG_993575f05b1d50b4"
url = "https://api.segmind.com/v1/try-on-diffusion"

# Ask user to select images
print("Please select the model image...")
model_image_path = select_image("Select Model Image")
print("Please select the clothing image...")
cloth_image_path = select_image("Select Clothing Image")

# Validate if user selected valid files
if not model_image_path or not os.path.exists(model_image_path):
    print("Error: No valid model image selected.")
    exit()
if not cloth_image_path or not os.path.exists(cloth_image_path):
    print("Error: No valid clothing image selected.")
    exit()

# Request payload
data = {
    "model_image": image_file_to_base64(model_image_path),
    "cloth_image": image_file_to_base64(cloth_image_path),
    "category": "Upper body",
    "num_inference_steps": 35,
    "guidance_scale": 2,
    "seed": 12467,
    "base64": True  # Ensuring response is in base64 format
}

headers = {'x-api-key': api_key}

response = requests.post(url, json=data, headers=headers)

if response.status_code == 200:
    result = response.json()
    image_base64 = result.get("image", "")

    if image_base64:
        output_path = os.path.join(os.getcwd(), "generated_tryon.png")  # Save in PyCharm workspace
        save_base64_image(image_base64, output_path)
        open_image(output_path)  # Automatically open the saved image
    else:
        print("Error: No image data received from API")
else:
    print("API Error:", response.status_code, response.text)
