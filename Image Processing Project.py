import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, Scale
from PIL import Image, ImageTk

class SpeckleNoiseRemoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Speckle Noise")
        
        # Image display
        self.original_image_label = tk.Label(self.root, text="Original Image")
        self.original_image_label.grid(row=0, column=0, padx=10, pady=10)
        
        self.processed_image_label = tk.Label(self.root, text="Processed Image")
        self.processed_image_label.grid(row=0, column=1, padx=10, pady=10)
        
        # Buttons
        self.choose_image_button = tk.Button(self.root, text="Choose Image", command=self.choose_image)
        self.choose_image_button.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
        
        self.add_noise_button = tk.Button(self.root, text="Add Noise", command=self.add_noise)
        self.add_noise_button.grid(row=2, column=0, padx=10, pady=5)
        
        self.remove_noise_button = tk.Button(self.root, text="Remove Noise", command=self.remove_noise)
        self.remove_noise_button.grid(row=2, column=1, padx=10, pady=5)
        
        self.save_original_button = tk.Button(self.root, text="Save Original Image", command=self.save_original_image)
        self.save_original_button.grid(row=3, column=0, padx=10, pady=5)
        
        self.save_processed_button = tk.Button(self.root, text="Save Processed Image", command=self.save_processed_image)
        self.save_processed_button.grid(row=3, column=1, padx=10, pady=5)
        
        # Noise filter strength scales
        self.add_noise_strength_label = tk.Label(self.root, text="Add Noise Strength:")
        self.add_noise_strength_label.grid(row=4, column=0, padx=10, pady=5, sticky=tk.E)
        
        self.add_noise_strength_scale = Scale(self.root, from_=0, to=200, orient=tk.HORIZONTAL)
        self.add_noise_strength_scale.set(100)
        self.add_noise_strength_scale.grid(row=4, column=1, columnspan=2, padx=10, pady=5, sticky=tk.W+tk.E)

        self.remove_noise_strength_label = tk.Label(self.root, text="Remove Noise Strength:")
        self.remove_noise_strength_label.grid(row=5, column=0, padx=10, pady=5, sticky=tk.E)
        
        self.remove_noise_strength_scale = Scale(self.root, from_=0, to=200, orient=tk.HORIZONTAL)
        self.remove_noise_strength_scale.set(100)
        self.remove_noise_strength_scale.grid(row=5, column=1, columnspan=2, padx=10, pady=5, sticky=tk.W+tk.E)
        
        # Image variables
        self.original_image = None
        self.noisy_image = None
        self.processed_image = None

    def choose_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.original_image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            self.display_image(self.original_image, self.original_image_label)

    def display_image(self, image, label):
        image = Image.fromarray(image)
        image = image.resize((500, 500), Image.BILINEAR)
        image = ImageTk.PhotoImage(image)
        label.config(image=image)
        label.image = image

    def add_noise(self):
        if self.original_image is not None:
            add_noise_strength = self.add_noise_strength_scale.get() / 100
            self.noisy_image = self.add_speckle_noise(self.original_image, strength=add_noise_strength)
            self.display_image(self.noisy_image, self.processed_image_label)
        else:
            messagebox.showerror("Error", "No image selected.")

    def remove_noise(self):
        if self.original_image is not None:
            if self.noisy_image is not None:
                remove_noise_strength = self.remove_noise_strength_scale.get() / 100
                self.processed_image = self.remove_speckle_noise(self.noisy_image, strength=remove_noise_strength)
            else:
                remove_noise_strength = self.remove_noise_strength_scale.get() / 100
                self.processed_image = self.remove_speckle_noise(self.original_image, strength=remove_noise_strength)
                
            self.display_image(self.processed_image, self.processed_image_label)
        else:
            messagebox.showerror("Error", "No image selected.")

    def save_original_image(self):
        if self.original_image is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
            if file_path:
                cv2.imwrite(file_path, self.original_image)
                messagebox.showinfo("Save Original Image", "Original image saved successfully.")
        else:
            messagebox.showerror("Error", "No original image to save.")

    def save_processed_image(self):
        if self.processed_image is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
            if file_path:
                cv2.imwrite(file_path, self.processed_image)
                messagebox.showinfo("Save Processed Image", "Processed image saved successfully.")
        else:
            messagebox.showerror("Error", "No processed image to save.")

    def add_speckle_noise(self, image, mean=0, sigma=0.1, strength=0.5):
        noise = np.random.normal(mean, sigma, image.shape)
        noisy_image = image + image * noise * strength
        noisy_image = np.clip(noisy_image, 0, 255).astype(np.uint8)
        return noisy_image

    def remove_speckle_noise(self, image, d=9, sigma_color=50, sigma_space=50, strength=0.5):
        d = int(d * strength)
        sigma_color = int(sigma_color * strength)
        sigma_space = int(sigma_space * strength)
        return cv2.bilateralFilter(image, d, sigma_color, sigma_space)

def main():
    root = tk.Tk()
    root.title("Speckle Noise")
    root.resizable(False, False)
    app = SpeckleNoiseRemoverApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()