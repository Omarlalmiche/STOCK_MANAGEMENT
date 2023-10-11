import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

database = mysql.connector.connect(host="localhost", user="root", password="", database="stock")
connect = database.cursor()

def refresh_table():
    # Query the database to fetch the latest data
    connect.execute("SELECT * FROM Livraisons")
    data = connect.fetchall()

    # Clear the existing table data
    table.delete(*table.get_children())

    # Populate the table with the latest data
    for row in data:
        table.insert("", tk.END, values=row)

def ajouter():
    numero_livraison = numero_livraison_entry.get()
    date_livraison = date_livraison_entry.get()
    fournisseur_id = fournisseur_id_entry.get()

    if len(numero_livraison) > 0:
        try:
            sql = "INSERT INTO Livraisons (numero_livraison, date_livraison, fournisseur_id) VALUES (%s, %s, %s)"
            val = (numero_livraison, date_livraison, fournisseur_id)
            connect.execute(sql, val)
            database.commit()
            refresh_table()
            clear_inputs()
            messagebox.showinfo("Succès", "La livraison a été ajoutée avec succès.")
        except Exception as e:
            print(e)
            database.rollback()
            messagebox.showerror("Erreur", "Erreur lors de l'ajout de la livraison.")
    else:
        messagebox.showerror("Erreur", "Veuillez entrer le numéro de livraison.")

def modifier():
    numero_livraison = numero_livraison_entry.get()
    date_livraison = date_livraison_entry.get()
    fournisseur_id = fournisseur_id_entry.get()

    if len(numero_livraison) > 0:
        try:
            sql = "UPDATE Livraisons SET date_livraison = %s, fournisseur_id = %s WHERE numero_livraison = %s"
            val = (date_livraison, fournisseur_id, numero_livraison)
            connect.execute(sql, val)
            database.commit()
            refresh_table()
            clear_inputs()
            messagebox.showinfo("Succès", "La livraison a été modifiée avec succès.")
        except Exception as e:
            print(e)
            database.rollback()
            messagebox.showerror("Erreur", "Erreur lors de la modification de la livraison.")
    else:
        messagebox.showerror("Erreur", "Veuillez entrer le numéro de livraison à modifier.")

def supprimer():
    numero_livraison = numero_livraison_entry.get()
    if len(numero_livraison) > 0:
        try:
            sql = "DELETE FROM Livraisons WHERE numero_livraison = %s"
            val = (numero_livraison,)
            connect.execute(sql, val)
            database.commit()
            refresh_table()
            clear_inputs()
            messagebox.showinfo("Succès", "La livraison a été supprimée avec succès.")
        except Exception as e:
            print(e)
            database.rollback()
            messagebox.showerror("Erreur", "Erreur lors de la suppression de la livraison.")
    else:
        messagebox.showerror("Erreur", "Veuillez entrer le numéro de livraison à supprimer.")

def clear_inputs():
    numero_livraison_entry.delete(0, tk.END)
    date_livraison_entry.delete(0, tk.END)
    fournisseur_id_entry.delete(0, tk.END)

def search_by_id():
    numero_liv = numero_livraison_entry.get()
    if len(numero_liv) > 0:
        try:
            sql = "SELECT * FROM Livraisons WHERE numero_livraison = %s"
            val = (numero_liv,)
            connect.execute(sql, val)
            data = connect.fetchall()
            table.delete(*table.get_children())
            for row in data:
                table.insert("", tk.END, values=row)
        except Exception as e:
            print(e)
            messagebox.showerror("Erreur", "Erreur lors de la recherche du livraison.")
    else:
        messagebox.showerror("Erreur", "Veuillez entrer le numero du LIVRAISON à rechercher.")

def clear_search():
    numero_livraison_entry.delete(0, tk.END)
    refresh_table()

root = tk.Tk()
root.title("Gestion des livraisons")
root.geometry("800x600")
root.resizable(True, True)

# Create a frame
frame = tk.Frame(root)
frame.pack(pady=20)

# Create a treeview
table = ttk.Treeview(frame, columns=(1, 2, 3), show="headings", height=10)
table.pack(side=tk.LEFT, padx=20)

# Add column headings
table.heading(1, text="Numéro de livraison")
table.heading(2, text="Date de livraison")
table.heading(3, text="Fournisseur ID")

# Add scrollbars
scroll_y = tk.Scrollbar(frame, orient=tk.VERTICAL, command=table.yview)
scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

# Configure the treeview to use the scrollbar
table.configure(yscrollcommand=scroll_y.set)

# Add entry fields and labels
numero_livraison_label = tk.Label(root, text="Numéro de livraison:")
numero_livraison_label.place(x=200, y=300)
numero_livraison_entry = tk.Entry(root)
numero_livraison_entry.place(x=350, y=300)

date_livraison_label = tk.Label(root, text="Date de livraison:")
date_livraison_label.place(x=200, y=330)
date_livraison_entry = tk.Entry(root)
date_livraison_entry.place(x=350, y=330)

fournisseur_id_label = tk.Label(root, text="Fournisseur ID:")
fournisseur_id_label.place(x=200, y=360)
fournisseur_id_entry = tk.Entry(root)
fournisseur_id_entry.place(x=350, y=360)

# Add buttons
ajouter_button = tk.Button(root, text="Ajouter", command=ajouter)
ajouter_button.place(x=250, y=400)

modifier_button = tk.Button(root, text="Modifier", command=modifier)
modifier_button.place(x=350, y=400)

supprimer_button = tk.Button(root, text="Supprimer", command=supprimer)
supprimer_button.place(x=450, y=400)

# Create a button frame
button_frame = tk.Frame(root)
button_frame.pack(pady=20)

# Add search, clear, and refresh buttons
search_button = ttk.Button(button_frame, text="Rechercher par NUM", command=search_by_id)
search_button.grid(row=0, column=3, padx=5)

clear_search_button = ttk.Button(button_frame, text="Effacer recherche", command=clear_search)
clear_search_button.grid(row=0, column=4, padx=5)

refresh_button = ttk.Button(button_frame, text="Actualiser", command=refresh_table)
refresh_button.grid(row=0, column=5, padx=5)

# Refresh the table with the latest data
refresh_table()

root.mainloop()
