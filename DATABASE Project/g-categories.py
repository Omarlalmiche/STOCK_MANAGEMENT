import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

database = mysql.connector.connect(host="localhost", user="root", password="", database="stock")
connect = database.cursor()


def refresh_table():
    # Query the database to fetch the latest data
    connect.execute("SELECT * FROM Categories_articles")
    data = connect.fetchall()

    # Clear the existing table data
    table.delete(*table.get_children())

    # Populate the table with the latest data
    for row in data:
        table.insert("", tk.END, values=row)


def ajouter():
    nom_categorie = nom_categorie_entry.get()
    description = description_entry.get()

    if len(nom_categorie) > 0:
        try:
            sql = "INSERT INTO Categories_articles (nom_categorie, description) VALUES (%s, %s)"
            val = (nom_categorie, description)
            connect.execute(sql, val)
            database.commit()
            refresh_table()
            clear_inputs()
            messagebox.showinfo("Succès", "La catégorie d'article a été ajoutée avec succès.")
        except Exception as e:
            print(e)
            database.rollback()
            messagebox.showerror("Erreur", "Erreur lors de l'ajout de la catégorie d'article.")
    else:
        messagebox.showerror("Erreur", "Veuillez entrer le nom de la catégorie d'article.")


def modifier():
    categorie_id = categorie_id_entry.get()
    nom_categorie = nom_categorie_entry.get()
    description = description_entry.get()

    if len(categorie_id) > 0:
        try:
            sql = "UPDATE Categories_articles SET nom_categorie = %s, description = %s WHERE categorie_id = %s"
            val = (nom_categorie, description, categorie_id)
            connect.execute(sql, val)
            database.commit()
            refresh_table()
            clear_inputs()
            messagebox.showinfo("Succès", "La catégorie d'article a été modifiée avec succès.")
        except Exception as e:
            print(e)
            database.rollback()
            messagebox.showerror("Erreur", "Erreur lors de la modification de la catégorie d'article.")
    else:
        messagebox.showerror("Erreur", "Veuillez entrer l'ID de la catégorie d'article à modifier.")


def supprimer():
    categorie_id = categorie_id_entry.get()
    if len(categorie_id) > 0:
        try:
            sql = "DELETE FROM Categories_articles WHERE categorie_id = %s"
            val = (categorie_id,)
            connect.execute(sql, val)
            database.commit()
            refresh_table()
            clear_inputs()
            messagebox.showinfo("Succès", "La catégorie d'article a été supprimée avec succès.")
        except Exception as e:
            print(e)
            database.rollback()
            messagebox.showerror("Erreur", "Erreur lors de la suppression de la catégorie d'article.")
    else:
        messagebox.showerror("Erreur", "Veuillez entrer l'ID de la catégorie d'article à supprimer.")


def clear_inputs():
    nom_categorie_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    categorie_id_entry.delete(0, tk.END)

def search_by_id():
    categorie_id = categorie_id_entry.get()
    if len(categorie_id) > 0:
        try:
            sql = "SELECT * FROM Categories_articles WHERE categorie_id = %s"
            val = (categorie_id,)
            connect.execute(sql, val)
            data = connect.fetchall()
            table.delete(*table.get_children())
            for row in data:
                table.insert("", tk.END, values=row)
        except Exception as e:
            print(e)
            messagebox.showerror("Erreur", "Erreur lors de la recherche de la catégorie d'article.")
    else:
        messagebox.showerror("Erreur", "Veuillez entrer l'ID de la catégorie d'article à rechercher.")

def clear_search():
    categorie_id_entry.delete(0, tk.END)
    refresh_table()

root = tk.Tk()
root.title("Gestion des catégories d'articles")
root.geometry("800x600")
root.resizable(True, True)

# Title
title_label = tk.Label(root, text="Gestion des catégories d'articles", font=("Arial", 20), padx=10, pady=10)
title_label.pack()

# Table
table_frame = ttk.Frame(root)
table_frame.pack(pady=10)

scrollbar = ttk.Scrollbar(table_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

table = ttk.Treeview(table_frame, columns=("categorie_id", "nom_categorie", "description"),
                     show="headings", yscrollcommand=scrollbar.set)

table.heading("categorie_id", text="ID")
table.heading("nom_categorie", text="Nom Catégorie")
table.heading("description", text="Description")

table.column("categorie_id", width=50)
table.column("nom_categorie", width=150)
table.column("description", width=500)

table.pack(side=tk.LEFT, fill=tk.BOTH)

scrollbar.config(command=table.yview)

# Form
form_frame = ttk.Frame(root)
form_frame.pack(pady=10)

nom_categorie_label = ttk.Label(form_frame, text="Nom Catégorie:")
nom_categorie_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)

nom_categorie_entry = ttk.Entry(form_frame)
nom_categorie_entry.grid(row=0, column=1, padx=5, pady=5)

description_label = ttk.Label(form_frame, text="Description:")
description_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)

description_entry = ttk.Entry(form_frame)
description_entry.grid(row=1, column=1, padx=5, pady=5)

categorie_id_label = ttk.Label(form_frame, text="ID de la catégorie (modify/delete/search):")
categorie_id_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)

categorie_id_entry = ttk.Entry(form_frame)
categorie_id_entry.grid(row=2, column=1, padx=5, pady=5)

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
