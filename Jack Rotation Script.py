import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import tkinter as tk
import PIL
from PIL import Image, ImageTk
from tkinter.filedialog import asksaveasfile, askopenfilename

#Create tkinter window
root=tk.Tk()
root.geometry('800x600')
root.title("NIfTI Rotation Tool")

#Create file types
files = [('All Files','*.*'),
        ('NIfTI files','*.nii')]

#Initialize variables
orig_data= ""
data = ""
ax_slices = 0
cor_slices = 0
sag_slices = 0
file_loaded = False

#Open file
def open_file():
    global orig_data, data, ax_slices, cor_slices, sag_slices, file_loaded
    
    #Pause redrawing
    file_loaded = False

    #Open file
    filename = askopenfilename(initialdir = "/", title = "Select File to Open", filetypes = files)
    img = nib.load(filename)
    orig_data = img.get_fdata()


    #Normalize
    max_pix = np.max(orig_data)
    min_pix = np.min(orig_data)
    data = (orig_data-min_pix) * 255 // (max_pix-min_pix)
    
    #Collect size information
    ax_slices = data.shape[2]
    cor_slices = data.shape[1]
    sag_slices = data.shape[0]

    #Signal file loaded
    file_loaded = True

    #Reconfig sliders
    ax_slicer.config(from_=0, to=ax_slices-1)
    cor_slicer.config(from_=0, to=cor_slices-1)
    sag_slicer.config(from_=0, to=sag_slices-1)

    root.update()
    root.update_idletasks()

#Track rotation state
rot_state = []

#Create save function
def save_as():
    file = asksaveasfile(filetypes = files, defaultextension = files)

#Define rotate commands
def rot_left():
    global data, rot_state
    if plane.get() == "axial":
        data = np.rot90(data,1,(0,1))
        rot_state = rot_state + [1]
    if plane.get() == "coronal":
        data = np.rot90(data,1,(0,2))
        rot_state = rot_state + [2]
    if plane.get() == "sagittal":
        data = np.rot90(data,1,(1,2))
        rot_state = rot_state + [3]

    #Collect size information
    ax_slices = data.shape[2]
    cor_slices = data.shape[1]
    sag_slices = data.shape[0]

    #Reconfig sliders
    ax_slicer.config(from_=0, to=ax_slices-1)
    cor_slicer.config(from_=0, to=cor_slices-1)
    sag_slicer.config(from_=0, to=sag_slices-1)

def rot_right():
    global data, rot_state
    if plane.get() == "axial":
        data = np.rot90(data,-1,(0,1))
        rot_state = rot_state + [-1]
    if plane.get() == "coronal":
        data = np.rot90(data,-1,(0,2))
        rot_state = rot_state + [-2]
    if plane.get() == "sagittal":
        data = np.rot90(data,-1,(1,2))
        rot_state = rot_state + [-3]

    #Collect size information
    ax_slices = data.shape[2]
    cor_slices = data.shape[1]
    sag_slices = data.shape[0]
    
    #Reconfig sliders
    ax_slicer.config(from_=0, to=ax_slices-1)
    cor_slicer.config(from_=0, to=cor_slices-1)
    sag_slicer.config(from_=0, to=sag_slices-1)

#Create control panel
sidepanel = tk.Frame(root)
sidepanel.pack(side="left", fill="y")

#Open file button
openbutton = tk.Button(sidepanel,text = "Open File", command = open_file)
openbutton.pack(pady=5)

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

left = tk.Button(frame1, text = "Left", command = rot_left)
left.pack(side="left",padx=10)

right = tk.Button(frame1, text = "Right", command = rot_right)
right.pack(side="left",padx=10)

#Create canvas
C = tk.Canvas(root,bg = "black")
C.pack(padx = 5, pady = 5, fill= tk.BOTH, expand=True)

#Create save button
savebutton = tk.Button(sidepanel,text = "Save As", command = save_as)
savebutton.pack(pady=5)


def showslice():
    if file_loaded == True:
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
    root.update()
    root.update_idletasks()


#Display image
showslice()

root.mainloop()
