import os
from tkinter import Label
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image


def slice_image(filepath):
    try:
        img = Image.open(filepath)
        width, height = img.size

        if width % 2 != 0:
            status_label.config(text="❌ Image width must be even!", fg="red")
            return

        mid = width // 2
        left = img.crop((0, 0, mid, height))
        right = img.crop((mid, 0, width, height))

        base, ext = os.path.splitext(filepath)
        left_path = base + "_left" + ext
        right_path = base + "_right" + ext

        left.save(left_path)
        right.save(right_path)

        # Update status without popup
        status_label.config(text="✅ Split saved!", fg="green")
        root.bell()  # <-- comment if you dont like sound i guess

    except Exception as e:
        status_label.config(text=f"❌ Error: {e}", fg="red")


def drop(event):
    filepath = event.data.strip("{}")
    if os.path.isfile(filepath):
        slice_image(filepath)
    else:
        status_label.config(text="❌ Invalid file dropped", fg="red")


# --- GUI Setup ---
root = TkinterDnD.Tk()
root.title("Image Splitter (Drag & Drop)")
root.geometry("400x250")

label = Label(root, text="Drag & Drop an image file here", width=40, height=10, bg="lightgray")
label.pack(padx=20, pady=20)

status_label = Label(root, text="Waiting for image...", fg="gray")
status_label.pack(pady=10)

label.drop_target_register(DND_FILES)
label.dnd_bind('<<Drop>>', drop)

root.mainloop()
