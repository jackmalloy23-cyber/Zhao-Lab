import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import tkinter as tk

def load_nifti(file_path):
    img = nib.load(file_path)
    data = img.get_fdata()
    return data

def rotate_nifti(data, angle, axes):
    rotated_data = np.rot90(data, k=angle, axes = axes)
    return rotated_data

def rot_left():
    angle = 1

def rot_right():
    angle = -1

data = load_nifti(r"C:\Users\mall88\Documents\Temp folder\BA001.1.nii")

ax_slices = data.shape[2]
cor_slices = data.shape[1]
sag_slices = data.shape[0]



root=tk.Tk()

sidepanel = tk.Frame(root)
sidepanel.pack(side="left", fill="y")

lbl1 = tk.Label(sidepanel, text="NIfTI Rotation Tool")
lbl1.pack(pady=10)

frame2 = tk.Frame(sidepanel)
frame2.pack(pady=10)

plane = tk.Variable(root, (0,1))

axial = tk.Radiobutton(frame2, text = "Axial", variable = plane, value = (0,1))
axial.pack(side="left")

coronal = tk.Radiobutton(frame2, text = "Coronal", variable = plane, value = (0,2))
coronal.pack(side="left")

sagittal = tk.Radiobutton(frame2, text = "Sagittal", variable = plane, value = (1,2))
sagittal.pack(side="left")

ax_slice = tk.Scale(sidepanel, from_=0, to=ax_slices, orient="horizontal", label="Axial Slice")
ax_slice.pack(pady=10)

cor_slice = tk.Scale(sidepanel, from_=0, to=cor_slices, orient="horizontal", label="Coronal Slice")
cor_slice.pack(pady=10)

sag_slice = tk.Scale(sidepanel, from_=0, to=sag_slices, orient="horizontal", label="Sagittal Slice")
sag_slice.pack(pady=10)

lbl2 = tk.Label(sidepanel, text = "Rotate")
lbl2.pack()

frame1 = tk.Frame(sidepanel)
frame1.pack(pady=10)

left = tk.Button(frame1, text = "Left", command = rot_left)
left.pack(side="left",padx=10)

right = tk.Button(frame1, text = "Right", command = rot_right)
right.pack(side="left",padx=10)

C = tk.Canvas(root, width=512, height=512)
 



root.mainloop()
