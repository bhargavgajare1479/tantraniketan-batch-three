import torch
from PIL import Image
import requests
from io import BytesIO
from diffusers import StableDiffusionImg2ImgPipeline
import tkinter as tk
from tkinter import filedialog, messagebox

import torchvision.transforms as T

# You need to install diffusers, transformers, and torch
# pip install diffusers transformers torch


def ghibli_artify(input_image_path, output_image_path):
    # Load the pre-trained Stable Diffusion model (or a Ghibli fine-tuned checkpoint if available)
    model_id = "runwayml/stable-diffusion-v1-5"
    pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")

    # Load and preprocess the input image
    init_image = Image.open(input_image_path).convert("RGB")
    transform = T.Compose([
        T.Resize((512, 512)),
        T.CenterCrop(512),
    ])
    init_image = transform(init_image)

    # Ghibli-style prompt
    prompt = "a portrait in the style of Studio Ghibli animation, highly detailed, vibrant colors"

    # Generate the Ghibli art
    result = pipe(prompt=prompt, image=init_image, strength=0.75, guidance_scale=7.5)
    ghibli_image = result.images[0]
    ghibli_image.save(output_image_path)
    print(f"Ghibli art saved to {output_image_path}")

if __name__ == "__main__":
    input_path = input("Enter the path to your image: ")
    output_path = input("Enter the output path for Ghibli art: ")
    def select_input_file():
        file_path = filedialog.askopenfilename(
            title="Select Input Image",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.webp")]
        )
        if file_path:
            input_entry.delete(0, tk.END)
            input_entry.insert(0, file_path)

    def select_output_file():
        file_path = filedialog.asksaveasfilename(
            title="Save Ghibli Art As",
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png")]
        )
        if file_path:
            output_entry.delete(0, tk.END)
            output_entry.insert(0, file_path)

    def run_ghibli_artify():
        input_path = input_entry.get()
        output_path = output_entry.get()
        if not input_path or not output_path:
            messagebox.showerror("Error", "Please select both input and output paths.")
            return
        try:
            ghibli_artify(input_path, output_path)
            messagebox.showinfo("Success", f"Ghibli art saved to {output_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    root = tk.Tk()
    root.title("Ghibli Artifier")

    tk.Label(root, text="Input Image:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    input_entry = tk.Entry(root, width=40)
    input_entry.grid(row=0, column=1, padx=5, pady=5)
    tk.Button(root, text="Browse...", command=select_input_file).grid(row=0, column=2, padx=5, pady=5)

    tk.Label(root, text="Output Image:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    output_entry = tk.Entry(root, width=40)
    output_entry.grid(row=1, column=1, padx=5, pady=5)
    tk.Button(root, text="Browse...", command=select_output_file).grid(row=1, column=2, padx=5, pady=5)

    tk.Button(root, text="Artify!", command=run_ghibli_artify, width=20).grid(row=2, column=0, columnspan=3, pady=10)

    root.mainloop()