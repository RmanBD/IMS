import ctypes
import customtkinter
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import resource.db as db

ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)


# database instance
db = db.InventoryDatabase('resource/Products.db')


# ------------------------------------------------------------
imsapp = customtkinter.CTk()
imsapp.title('Simple Inventory Management System')
imsapp.geometry('800x580+100+50')
imsapp.iconbitmap('resource/icon.ico')
imsapp.config(bg='#ffffff')
imsapp.resizable(False,False)

font1 = ('Arial',25,'bold')
font2 = ('Arial',18,'bold')
font22 = ('Arial',15,'bold')
font3 = ('Arial',13,'bold')
cwinClolor = ('#e6e6e6')
black = ('#141414')
# ------------------------------------------------------------


# ------------------------------------------------------------
def insert():
    id = idEntry.get()
    if not id.startswith('#'):
        id = '#' + id
    name = nameEntry.get()
    quantity = quantityEntry.get()
    if not (id and name and quantity):
        if id == '':
            id = '  [empty]'
            messagebox.showerror('Error',f'Requre ID: fields to insert an item.\n ID = {id}')
        if name == '':
            name = '  [empty]'
            messagebox.showerror('Error',f'Requre Name: fields to insert an item.\n Name = {name}')
        if quantity == '':
            quantity = '  [empty]'
            messagebox.showerror('Error',f'Requre Quantity: fields to insert an item.\nquantity = {quantity}')
        # messagebox.showerror('Error',f'Requre all fields to insert an item.\n\nID: {id}\nName: {name}\nQuantity: {quantity}')
    elif db.id_exists(id):
        messagebox.showerror('Error',f'-> {id} <-\nID already exists.')
    else:
        try:
            db.insert_product(id,name,int(quantity))
            addToTreeview()
            clear()
            createChart()
            # messagebox.showinfo('Sucess',f'Data has been inserted.')
        except ValueError:
            messagebox.showerror('Error',f'Quantity should be an integer.')

def clear(*clicked):
    if clicked:
        tree.selection_remove(tree.focus())
        tree.focus('')
    idEntry.delete(0,END)
    nameEntry.delete(0,END)
    quantityEntry.delete(0,END)
    # idEntry._placeholder_text = '#1'
    # nameEntry._placeholder_text = 'Honey Nuts'
    # quantityEntry._placeholder_text = '10'

def addToTreeview():
    products = db.fetch_products()
    tree.delete(*tree.get_children())
    for Product in products:
        tree.insert('',END,values=Product)

def displayData(event):
    selectedItem = tree.focus()
    if selectedItem:
        row = tree.item(selectedItem)['values']
        clear()
        idEntry.insert(0,row[0])
        nameEntry.insert(0,row[1])
        quantityEntry.insert(0,row[2])
    else:
        pass

def update():
    selectedItem = tree.focus()
    if not selectedItem:
        messagebox.showerror('Error',f'Choose a product to update.')
    else:
        id = idEntry.get()
        name = nameEntry.get()
        quantity = quantityEntry.get()
        db.update_product(name,quantity,id)
        addToTreeview()
        clear()
        createChart()
        messagebox.showinfo('Sucess',f'Data has been update.')


def delete():
    selectedItem = tree.focus()
    if not selectedItem:
        messagebox.showerror('Error',f'Chosse a product to delete.')
    else:
        id = idEntry.get()
        db.delete_product(id)
        addToTreeview()
        clear()
        createChart()
        messagebox.showinfo('Sucess',f'Data has been deleted.')

def createChart():
    productDetails = db.fetch_products()
    productNames = [product[1] for product in productDetails]
    quantity_values = [product[2] for product in productDetails]

    figure = Figure(figsize=(6.2,4), dpi=80,facecolor='#ffffff')
    ax = figure.add_subplot(111)
    ax.bar(productNames,quantity_values,width=0.9,color='#078f00')
    ax.set_xlabel('Product Name',color=black,fontsize=10)
    ax.set_ylabel('quantity Value',color=black,fontsize=10)
    ax.set_title('Product quantity Levels',color=black,fontsize=14)
    ax.tick_params(axis='x',labelcolor=black,labelsize=10)

    canvas = FigureCanvasTkAgg(figure)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0,column=0,padx=0,pady=380)
# ------------------------------------------------------------


frame = customtkinter.CTkFrame(imsapp,border_width=0,fg_color=cwinClolor,bg_color='#ffffff',corner_radius=4,width=375,height=280)
frame.place(x=15,y=15)

image1 = PhotoImage(file='resource/img.PNG')
image1 = image1.subsample(image1.width()//70, image1.height()//70)
imgLabel = Label(frame,image=image1,bg=cwinClolor)
# imgLabel.place(x=20,y=5)
imgLabel.grid(row=0,column=0,columnspan=1,pady=20)



titleLabel = customtkinter.CTkLabel(frame,font=font1,text='Product Details',text_color=black)
titleLabel.grid(row=0,column=1,columnspan=3,padx=20)

'''id row'''
idLabel = customtkinter.CTkLabel(frame,font=font2,text='Item ID :',text_color=black)
idLabel.grid(row=1,column=0,columnspan=1,pady=5,padx=20,sticky='w')

idEntry = customtkinter.CTkEntry(frame,font=font2,text_color=black,fg_color='#fff',border_color='#B2016C',border_width=2,width=160,placeholder_text='#1')
idEntry.grid(row=1,column=1,columnspan=3)


'''name row'''
nameLabel = customtkinter.CTkLabel(frame,font=font2,text='Item Name :',text_color=black)
nameLabel.grid(row=2,column=0,columnspan=1,pady=5,padx=20,sticky='w')

nameEntry = customtkinter.CTkEntry(frame,font=font2,text_color=black,fg_color='#fff',border_color='#B2016C',border_width=2,width=160,placeholder_text='Honey Nuts')
nameEntry.grid(row=2,column=1,columnspan=3)


'''quantity row'''
quantityLabel = customtkinter.CTkLabel(frame,font=font2,text='Item Quantity :',text_color=black)
quantityLabel.grid(row=3,column=0,columnspan=1,pady=5,padx=20,sticky='w')

quantityEntry = customtkinter.CTkEntry(frame,font=font2,text_color=black,fg_color='#fff',border_color='#B2016C',border_width=2,width=160,placeholder_text='20')
quantityEntry.grid(row=3,column=1,columnspan=3)


'''Button frame'''
frame2 = customtkinter.CTkFrame(frame,corner_radius=10,border_width=0,fg_color=cwinClolor,width=375,height=280)
frame2.grid(row=4,column=0,columnspan=3,padx=20,pady=20)


'''add Button'''
addButton = customtkinter.CTkButton(frame2,command=insert,font=font22,text_color='#fff',text='Add',fg_color='#047E43',hover_color='#025B30',cursor='hand2',corner_radius=8,width=75)
addButton.grid(row=4,column=0,padx=5)

'''clear Button'''
clearButton = customtkinter.CTkButton(frame2,command=lambda:clear(True),font=font22,text_color='#fff',text='New',fg_color='#79a6d2',hover_color='#b3cce6',cursor='hand2',corner_radius=8,width=75)
clearButton.grid(row=4,column=1,padx=5)

'''Update Button'''
updateButton = customtkinter.CTkButton(frame2,command=update,font=font22,text_color='#fff',text='Update',fg_color='#33cc33',hover_color='#70db70',cursor='hand2',corner_radius=8,width=75)
updateButton.grid(row=4,column=2,padx=5)

'''Delete Button'''
deleteButton = customtkinter.CTkButton(frame2,command=delete,font=font22,text_color='#fff',text='Delete',fg_color='#cc0000',hover_color='#ff1a1a',cursor='hand2',corner_radius=8,width=75)
deleteButton.grid(row=4,column=3,padx=5)




style = ttk.Style(imsapp)

style.theme_use(themename='clam')
style.configure('Treeviewe',font=font3)
style.map('Treeview',background=[('selected','#aa04a7')])

tree = ttk.Treeview(imsapp,height=31)
tree['columns'] = ('ID','Name','quantity')

tree.column('#0',width=0,stretch=tk.NO)
tree.column('ID',anchor=tk.CENTER,width=155)
tree.column('Name',anchor=tk.CENTER,width=155)
tree.column('quantity',anchor=tk.CENTER,width=155)

tree.heading('ID',text='Item ID')
tree.heading('Name',text='Item Name')
tree.heading('quantity',text='Quantity')

tree.place(x=500,y=20)

tree.bind('<ButtonRelease>',displayData)
addToTreeview()
createChart()
imsapp.mainloop()

