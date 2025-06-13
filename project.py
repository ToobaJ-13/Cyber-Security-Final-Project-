import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

# Converts a string to binary with 16-bit EOF marker
def text_to_binary(text):
    binary = ''.join(format(ord(char), '08b') for char in text)
    binary += '1111111111111110'  # 16-bit EOF marker
    return binary

# Converts binary to text, stops at 16-bit EOF marker
def binary_to_text(binary):
    eof_index = binary.find('1111111111111110')
    if eof_index != -1:
        binary = binary[:eof_index]
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    text = ''.join(chr(int(char, 2)) for char in chars)
    return text

# Encode message into image
def encode_message():
    image_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.png *.jpg *.bmp")])
    if not image_path:
        return

    # Load and preview image
    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    preview = img.copy()
    preview.thumbnail((200, 200))
    img_tk = ImageTk.PhotoImage(preview)
    image_preview_label.configure(image=img_tk)
    image_preview_label.image = img_tk

    message = entry_message.get("1.0", tk.END).strip()
    if not message:
        messagebox.showerror("Error", "Please enter a message to hide.")
        return

    output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if not output_path:
        return

    binary = text_to_binary(message)
    pixels = img.load()

    width, height = img.size
    idx = 0

    for y in range(height):
        for x in range(width):
            if idx < len(binary):
                r, g, b = pixels[x, y]
                r = (r & ~1) | int(binary[idx])  # modify LSB of red
                pixels[x, y] = (r, g, b)
                idx += 1
            else:
                break

    img.save(output_path)
    messagebox.showinfo("Success", f"Message encoded and saved to:\n{output_path}")

# Decode message from image
def decode_message():
    image_path = filedialog.askopenfilename(title="Select Encoded Image", filetypes=[("Image Files", "*.png *.jpg *.bmp")])
    if not image_path:
        return

    # Load and preview image
    img = Image.open(image_path)
    preview = img.copy()
    preview.thumbnail((200, 200))
    img_tk = ImageTk.PhotoImage(preview)
    image_preview_label.configure(image=img_tk)
    image_preview_label.image = img_tk

    pixels = img.load()
    width, height = img.size
    binary = ""

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            binary += str(r & 1)

    message = binary_to_text(binary)
    messagebox.showinfo("Decoded Message", message)

# GUI setup
root = tk.Tk()
root.title("🕵️ Image Steganography")
root.geometry("600x550")
root.config(bg="#1e1e2f")
root.resizable(False, False)

# Header
header = tk.Label(root, text="🕵️ Image Steganography", font=("Helvetica", 22, "bold"), bg="#1e1e2f", fg="#00FFAB")
header.pack(pady=(20, 5))

separator = tk.Frame(root, height=2, bg="#00FFAB")
separator.pack(fill=tk.X, padx=40, pady=(0, 20))

# Main Frame
frame = tk.Frame(root, bg="#2e2e3f", bd=2, relief=tk.RIDGE)
frame.pack(padx=30, pady=10, fill=tk.BOTH, expand=True)

# Message Label
label_instruction = tk.Label(frame, text="Enter message to hide:", font=("Helvetica", 14), bg="#2e2e3f", fg="white")
label_instruction.pack(pady=(15, 5))

# Text Area
entry_message = tk.Text(frame, height=8, width=60, font=("Courier New", 12), bg="#f0f0f0", wrap=tk.WORD)
entry_message.pack(padx=20, pady=5)

# Buttons Frame
btn_frame = tk.Frame(frame, bg="#2e2e3f")
btn_frame.pack(pady=20)

btn_encode = tk.Button(
    btn_frame, text="🧪 Encode Message", command=encode_message,
    bg="#28a745", fg="white", font=("Helvetica", 12, "bold"), width=25, height=2, relief=tk.FLAT, cursor="hand2"
)
btn_encode.pack(side=tk.LEFT, padx=10)

btn_decode = tk.Button(
    btn_frame, text="🔍 Decode Message", command=decode_message,
    bg="#007bff", fg="white", font=("Helvetica", 12, "bold"), width=25, height=2, relief=tk.FLAT, cursor="hand2"
)
btn_decode.pack(side=tk.LEFT, padx=10)

# Image Preview Label (initially empty)
image_preview_label = tk.Label(root, bg="#1e1e2f")
image_preview_label.pack(pady=10)

# Footer
footer = tk.Label(root, text="Made with ❤️ using Python", font=("Helvetica", 10), bg="#1e1e2f", fg="gray")
footer.pack(side=tk.BOTTOM, pady=10)

root.mainloop()
