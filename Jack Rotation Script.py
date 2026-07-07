import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import tkinter as tk
import PIL
from PIL import Image, ImageTk

def load_nifti(file_path):
    img = nib.load(file_path)
    data = img.get_fdata()
    return data

def rotate_nifti(data, angle, axes):
    rotated_data = np.rot90(data, k=angle, axes = axes)
    return rotated_data

def rot_left(data):
    if plane == "axial":
        data = np.rot90(data,1,(0,1))
    if plane == "coronal":
        data = np.rot90(data,1,(0,2))
    if plane == "sagittal":
        data = np.rot90(data,1,(1,2))

def rot_right(data):
    if plane == "axial":
        data = np.rot90(data,-1,(0,1))
    if plane == "coronal":
        data = np.rot90(data,-1,(0,2))
    if plane == "sagittal":
        data = np.rot90(data,-1,(1,2))

#Create tkinter window
root=tk.Tk()
root.geometry('800x600')
root.title("NiFTI Rotation Tool")

#Load data
data = load_nifti(r"C:\Users\mall88\Documents\Temp folder\BA001.1.nii")

#Normalize
max_pix = np.max(data)
min_pix = np.min(data)
data = (data-min_pix) * 255 // (max_pix-min_pix)

#Collect size information
ax_slices = data.shape[2]
cor_slices = data.shape[1]
sag_slices = data.shape[0]

#Create control panel
sidepanel = tk.Frame(root)
sidepanel.pack(side="left", fill="y")

#Create plane label
planelabel = tk.Label(sidepanel,text = "Selected Plane")
planelabel.pack(pady=5)

#Initialize plane variable
plane = tk.StringVar(root,"coronal")

#Create frame and fill with radiobuttons for plane select
frame2 = tk.Frame(sidepanel)
frame2.pack(pady=5)

axial = tk.Radiobutton(frame2, text = "Axial", variable = plane, value = "axial")
axial.pack(side="left")

coronal = tk.Radiobutton(frame2, text = "Coronal", variable = plane, value = "coronal")
coronal.pack(side="left")

sagittal = tk.Radiobutton(frame2, text = "Sagittal", variable = plane, value = "sagittal")
sagittal.pack(side="left")

#Create crosshairs option
crosshair = tk.BooleanVar(root,True)
crosshairbutton = tk.Checkbutton(sidepanel, text="Show Crosshair", variable = crosshair)
crosshairbutton.pack(pady = 5)

#Initializ slice select
ax_slice = tk.IntVar(root, 0)
cor_slice = tk.IntVar(root, 0)
sag_slice = tk.IntVar(root, 0)

#Create slice select sliders
ax_slicer = tk.Scale(sidepanel, from_=0, to=ax_slices-1, orient="horizontal", label="Axial Slice", variable= ax_slice)
ax_slicer.pack(pady=5)

cor_slicer = tk.Scale(sidepanel, from_=0, to=cor_slices-1, orient="horizontal", label="Coronal Slice", variable= cor_slice)
cor_slicer.pack(pady=5)

sag_slicer = tk.Scale(sidepanel, from_=0, to=sag_slices-1, orient="horizontal", label="Sagittal Slice", variable= sag_slice)
sag_slicer.pack(pady=5)

#Create rotate label
lbl2 = tk.Label(sidepanel, text = "Rotate")
lbl2.pack()

#Create frame and rotate left and right buttons
frame1 = tk.Frame(sidepanel)
frame1.pack(pady=10)

left = tk.Button(frame1, text = "Left", command = rot_left(data))
left.pack(side="left",padx=10)

right = tk.Button(frame1, text = "Right", command = rot_right(data))
right.pack(side="left",padx=10)

#Create canvas
C = tk.Canvas(root,bg = "black")
C.pack(padx = 5, pady = 5, fill= tk.BOTH, expand=True)

def showslice():
    #Clear Canvas
    C.delete("all")
    
    #Get canvas size
    w = C.winfo_width()
    h = C.winfo_height()

    #Redraw backgroud
    C.create_rectangle(0,0,w,h,fill = "black")

    #Check which plane currently selected and gather slice data
    if plane.get() == "axial":
        cur_slice_mtx = data[:,:,ax_slice.get()]
    if plane.get() == "coronal":
        cur_slice_mtx = data[:,cor_slice.get(),:] 
    if plane.get() == "sagittal":
        cur_slice_mtx = data[sag_slice.get(),:,:]
    
    img = Image.fromarray(cur_slice_mtx)
    photo = ImageTk.PhotoImage(img)
    C.create_image(w/2, h/2, anchor = 'center', image = photo)
    C.image = photo

    #Display Crosshair
    if crosshair.get() == True:
        if plane.get() == "axial":
            C.create_line(0,sag_slice.get()+(h-sag_slices)/2,w,sag_slice.get()+(h-sag_slices)/2, fill = "yellow")
            C.create_line(cor_slice.get()+(w-cor_slices)/2,0,cor_slice.get()+(w-cor_slices)/2,h, fill = "yellow")
        if plane.get() == "coronal":
            C.create_line(0,sag_slice.get()+(h-sag_slices)/2,w,sag_slice.get()+(h-sag_slices)/2, fill = "yellow")
            C.create_line(ax_slice.get()+(w-ax_slices)/2,0,ax_slice.get()+(w-ax_slices)/2,h, fill = "yellow")
        if plane.get() == "sagittal":
            C.create_line(0,cor_slice.get()+(h-cor_slices)/2,w,cor_slice.get()+(h-cor_slices)/2, fill = "yellow")
            C.create_line(ax_slice.get()+(w-ax_slices)/2,0,ax_slice.get()+(w-ax_slices)/2,h, fill = "yellow")
    
    #Refresh Display
    root.after(16,showslice)


#Display image
showslice()

root.mainloop()
