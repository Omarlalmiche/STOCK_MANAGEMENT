import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

database = mysql.connector.connect(host="localhost", user="root", password="", database="stock")
connect = database.cursor()


def refresh_table():
    # Query the database to fetch the latest data
    connect.execute("SELECT * FROM Emplacements")
    data = connect.fetchall()

    # Clear the existing table data
    table.delete(*table.get_children())

    # Populate the table with the latest data
    for row in data:
        table.insert("", tk.END, values=row)


def ajouter():
    nom_emplacement = nom_emplacement_entry.get()
    description = description_entry.get()
    capacite_stockage = capacite_stockage_entry.get()

    if len(nom_emplacement) > 0:
        try:
            sql = "INSERT INTO Emplacements (nom_emplacement, description, capacite_stockage) VALUES (%s, %s, %s)"
            val = (nom_emplacement, description, capacite_stockage)
            connect.execute(sql, val)
            database.commit()
            refresh_table()
            clear_inputs()
            messagebox.showinfo("Succès", "L'emplacement a été ajouté avec succès.")
        except Exception as e:
            print(e)
            database.rollback()
            messagebox.showerror("Erreur", "Erreur lors de l'ajout de l'emplacement.")
    else:
        messagebox.showerror("Erreur", "Veuillez entrer le nom de l'emplacement.")


def modifier():
    emplacement_id = emplacement_id_entry.get()
    nom_emplacement = nom_emplacement_entry.get()
    description = description_entry.get()
    capacite_stockage = capacite_stockage_entry.get()

    if len(emplacement_id) > 0:
        try:
            sql = "UPDATE Emplacements SET nom_emplacement = %s, description = %s, capacite_stockage = %s WHERE emplacement_id = %s"
            val = (nom_emplacement, description, capacite_stockage, emplacement_id)
            connect.execute(sql, val)
            database.commit()
            refresh_table()
            clear_inputs()
            messagebox.showinfo("Succès", "L'emplacement a été modifié avec succès.")
        except Exception as e:
            print(e)
            database.rollback()
            messagebox.showerror("Erreur", "Erreur lors de la modification de l'emplacement.")
    else:
        messagebox.showerror("Erreur", "Veuillez entrer l'ID de l'emplacement à modifier.")


def supprimer():
    emplacement_id = emplacement_id_entry.get()
    if len(emplacement_id) > 0:
        try:
            sql = "DELETE FROM Emplacements WHERE emplacement_id = %s"
            val = (emplacement_id,)
            connect.execute(sql, val)
            database.commit()
            refresh_table()
            clear_inputs()
            messagebox.showinfo("Succès", "L'emplacement a été supprimé avec succès.")
        except Exception as e:
            print(e)
            database.rollback()
            messagebox.showerror("Erreur", "Erreur lors de la suppression de l'emplacement.")
    else:
        messagebox.showerror("Erreur", "Veuillez entrer l'ID de l'emplacement à supprimer.")


def clear_inputs():
    nom_emplacement_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    capacite_stockage_entry.delete(0, tk.END)
    emplacement_id_entry.delete(0, tk.END)


def search_by_id():
    emplacement_id = emplacement_id_entry.get()
    if len(emplacement_id) > 0:
        try:
            sql = "SELECT * FROM Emplacements WHERE emplacement_id = %s"
            val = (emplacement_id,)
            connect.execute(sql, val)
            data = connect.fetchall()
            table.delete(*table.get_children())
            for row in data:
                table.insert("", tk.END, values=row)
        except Exception as e:
            print(e)
            messagebox.showerror("Erreur", "Erreur lors de la recherche de l'emplacement.")
    else:
        messagebox.showerror("Erreur", "Veuillez entrer l'ID de l'emplacement à rechercher.")


def clear_search():
    emplacement_id_entry.delete(0, tk.END)
    refresh_table()


root = tk.Tk()
root.title("Gestion des emplacements")
root.geometry("800x600")
root.resizable(True, True)

# Title
title_label = tk.Label(root, text="Gestion des emplacements", font=("Arial", 20), padx=10, pady=10)
title_label.pack()

# Table
table_frame = ttk.Frame(root)
table_frame.pack(pady=10)

scrollbar = ttk.Scrollbar(table_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

table = ttk.Treeview(table_frame, columns=("emplacement_id", "nom_emplacement", "description", "capacite_stockage"),
                     show="headings", yscrollcommand=scrollbar.set)

table.heading("emplacement_id", text="ID")
table.heading("nom_emplacement", text="Nom Emplacement")
table.heading("description", text="Description")
table.heading("capacite_stockage", text="Capacité de stockage")

table.column("emplacement_id", width=50)
table.column("nom_emplacement", width=150)
table.column("description", width=300)
table.column("capacite_stockage", width=150)

table.pack(side=tk.LEFT, fill=tk.BOTH)

scrollbar.config(command=table.yview)

# Form
form_frame = ttk.Frame(root)
form_frame.pack(pady=10)

nom_emplacement_label = ttk.Label(form_frame, text="Nom Emplacement:")
nom_emplacement_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)

nom_emplacement_entry = ttk.Entry(form_frame)
nom_emplacement_entry.grid(row=0, column=1, padx=5, pady=5)

description_label = ttk.Label(form_frame, text="Description:")
description_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)

description_entry = ttk.Entry(form_frame)
description_entry.grid(row=1, column=1, padx=5, pady=5)

capacite_stockage_label = ttk.Label(form_frame, text="Capacité de stockage:")
capacite_stockage_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)

capacite_stockage_entry = ttk.Entry(form_frame)
capacite_stockage_entry.grid(row=2, column=1, padx=5, pady=5)

emplacement_id_label = ttk.Label(form_frame, text="ID de l'emplacement (modify/delete/search):")
emplacement_id_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)

emplacement_id_entry = ttk.Entry(form_frame)
emplacement_id_entry.grid(row=3, column=1, padx=5, pady=5)

# Buttons
button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

ajouter_button = ttk.Button(button_frame, text="Ajouter", command=ajouter)
ajouter_button.grid(row=0, column=0, padx=5)

modifier_button = ttk.Button(button_frame, text="Modifier", command=modifier)
modifier_button.grid(row=0, column=1, padx=5)

supprimer_button = ttk.Button(button_frame, text="Supprimer", command=supprimer)
supprimer_button.grid(row=0, column=2, padx=5)

search_button = ttk.Button(button_frame, text="Rechercher par ID", command=search_by_id)
search_button.grid(row=0, column=3, padx=5)

clear_search_button = ttk.Button(button_frame, text="Effacer recherche", command=clear_search)
clear_search_button.grid(row=0, column=4, padx=5)

refresh_button = ttk.Button(button_frame, text="Actualiser", command=refresh_table)
refresh_button.grid(row=0, column=5, padx=5)

# Populate table with initial data
refresh_table()

root.mainloop()
