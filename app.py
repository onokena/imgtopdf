import tkinter as tk
from tkinter import filedialog
import os
from reportlab.pdfgen import canvas
from PIL import Image

class ImageToPDFConvert:
    def __init__(self, root):
        self.root =  root
        self.image_path = []
        self.output_pdf = tk.StringVar()
        self.selected_images_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)

        self.initialize_ui()

    def initialize_ui(self):
        title_label = tk.Label(self.root, text="Image to PDF Converter.", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)

        select_image_button = tk.Button(self.root, text="Select Image", command=self.select_image_button)
        select_image_button.pack(pady=(0, 10))

        self.selected_images_listbox.pack(pady=(0,10), fill=tk.BOTH, expand=True)

        label = tk.Label(self.root, text="Enter PDF name")
        label.pack()

        pdf_name_entry = tk.Entry(self.root, textvariable=self.output_pdf, width=40, justify="center")
        pdf_name_entry.pack()

        convert_button = tk.Button(self.root, text="Convert Image", command=self.convert_images_pdf)
        convert_button.pack(pady=(20, 40))

    def select_image_button(self):
        self.image_path = filedialog.askopenfilenames(title="Select Image", filetypes=[("Imagefiles", "*.png;*.jpg;*.jpeg;*gif")])
        self.update_selected_images_listbox()
    
    def update_selected_images_listbox(self):
        self.selected_images_listbox.delete(0, tk.END)

        for image_pathz in self.image_path:
            _, image_pathz = os.path.split(image_pathz)
            self.selected_images_listbox.insert(tk.END, image_pathz)

    def convert_images_pdf(self):
        if not self.image_path:
            return
        
        output_pdf_path = self.output_pdf.get() + ".pdf" if self.output_pdf.get() else "output.pdf"

        pdf = canvas.Canvas(output_pdf_path, pagesize=(612, 792))

        for image_pathz in self.image_path:
            img = Image.open(image_pathz)
            available_width = 540
            available_height = 720
            scale_factor = min(available_width / img.width, available_height / img.height)
            new_width = img.width * scale_factor
            new_height = img.height * scale_factor
            x_centered = (612 - new_width) / 2
            y_centered = (792 - new_height) / 2

            pdf.setFillColor("white")
            pdf.rect(0, 0, 612, 792, fill=True)
            pdf.drawInlineImage(img, x_centered, y_centered, width=new_width, height=new_height)
            pdf.showPage()

        pdf.save()

def main():
    root = tk.Tk()
    root.title("Image to PDF")
    converter = ImageToPDFConvert(root)
    root.geometry("400x600")
    root.mainloop()

if __name__ == "__main__":
    main()