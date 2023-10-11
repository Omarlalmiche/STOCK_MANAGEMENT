import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

database = mysql.connector.connect(host="localhost", user="root", password="", database="stock")
connect = database.cursor()


def refresh_table():
    # Query the database to fetch the latest data
    connect.execute("SELECT * FROM Articles")
    data = connect.fetchall()

    # Clear the existing table data
    table.delete(*table.get_children())

    # Populate the table with the latest data
    for row in data:
        table.insert("", tk.END, values=row)


def ajouter():
    nom_produit = nom_produit_entry.get()
    code_produit = code_produit_entry.get()
    description = description_entry.get()
    cout = cout_entry.get()
    prix_vente = prix_vente_entry.get()
    quantite_stock = quantite_stock_entry.get()
    date_expiration = date_expiration_entry.get()
    categorie_id = categorie_id_entry.get()

    if len(nom_produit) > 0 and len(code_produit) > 0:
        try:
            sql = "INSERT INTO Articles (nom_produit, code_produit, description, cout, prix_vente, quantite_stock, date_expiration, categorie_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            val = (nom_produit, code_produit, description, cout, prix_vente, quantite_stock, date_expiration, categorie_id)
            connect.execute(sql, val)
            database.commit()
            refresh_table()
            clear_inputs()
            messagebox.showinfo("Succès", "L'article a été ajouté avec succès.")
        except Exception as e:
            print(e)
            database.rollback()
            messagebox.showerror("Erreur", "Erreur lors de l'ajout de l'article.")
    else:
        messagebox.showerror("Erreur", "Veuillez entrer le nom et le code du produit.")


def modifier():
    article_id = article_id_entry.get()
    nom_produit = nom_produit_entry.get()
    code_produit = code_produit_entry.get()
    description = description_entry.get()
    cout = cout_entry.get()
    prix_vente = prix_vente_entry.get()
    quantite_stock = quantite_stock_entry.get()
    date_expiration = date_expiration_entry.get()
    categorie_id = categorie_id_entry.get()

    if len(article_id) > 0:
        try:
            sql = "UPDATE Articles SET nom_produit = %s, code_produit = %s, description = %s, cout = %s, prix_vente = %s, quantite_stock = %s, date_expiration = %s, categorie_id = %s WHERE article_id = %s"
            val = (nom_produit, code_produit, description, cout, prix_vente, quantite_stock, date_expiration, categorie_id, article_id)
            connect.execute(sql, val)
            database.commit()
            refresh_table()
            clear_inputs()
            messagebox.showinfo("Succès", "L'article a été modifié avec succès.")
        except Exception as e:
            print(e)
            database.rollback()
            messagebox.showerror("Erreur", "Erreur lors de la modification de l'article.")
    else:
        messagebox.showerror("Erreur", "Veuillez entrer l'ID de l'article à modifier.")


def supprimer():
    article_id = article_id_entry.get()
    if len(article_id) > 0:
        try:
            sql = "DELETE FROM Articles WHERE article_id = %s"
            val = (article_id,)
            connect.execute(sql, val)
            database.commit()
            refresh_table()
            clear_inputs()
            messagebox.showinfo("Succès", "L'article a été supprimé avec succès.")
        except Exception as e:
            print(e)
            database.rollback()
            messagebox.showerror("Erreur", "Erreur lors de la suppression de l'article.")
    else:
        messagebox.showerror("Erreur", "Veuillez entrer l'ID de l'article à supprimer.")


def clear_inputs():
    nom_produit_entry.delete(0, tk.END)
    code_produit_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    cout_entry.delete(0, tk.END)
    prix_vente_entry.delete(0, tk.END)
    quantite_stock_entry.delete(0, tk.END)
    date_expiration_entry.delete(0, tk.END)
    categorie_id_entry.delete(0, tk.END)
    article_id_entry.delete(0, tk.END)


#### search

def search_by_id():
    article_id = article_id_entry.get()
    if len(article_id) > 0:
        try:
            sql = "SELECT * FROM Articles WHERE article_id = %s"
            val = (article_id,)
            connect.execute(sql, val)
            data = connect.fetchall()
            table.delete(*table.get_children())
            for row in data:
                table.insert("", tk.END, values=row)
        except Exception as e:
            print(e)
            messagebox.showerror("Erreur", "Erreur lors de la recherche de l'article.")
    else:
        messagebox.showerror("Erreur", "Veuillez entrer l'ID de l'article à rechercher.")

def clear_search():
    article_id_entry.delete(0, tk.END)
    refresh_table()


#### se


root = tk.Tk()
root.title("Gestion des articles")
root.geometry("800x600")
root.resizable(True, True)

# Title
title_label = tk.Label(root, text="Gestion des articles", font=("Arial", 20), padx=10, pady=10)
title_label.pack()

# Table
table_frame = ttk.Frame(root)
table_frame.pack(pady=10)

scrollbar = ttk.Scrollbar(table_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

table = ttk.Treeview(table_frame, columns=("article_id", "nom_produit", "code_produit", "description", "cout", "prix_vente", "quantite_stock", "date_expiration", "categorie_id"),
                     show="headings", yscrollcommand=scrollbar.set)

table.heading("article_id", text="ID")
table.heading("nom_produit", text="Nom Produit")
table.heading("code_produit", text="Code Produit")
table.heading("description", text="Description")
table.heading("cout", text="Coût")
table.heading("prix_vente", text="Prix de vente")
table.heading("quantite_stock", text="Quantité en stock")
table.heading("date_expiration", text="Date d'expiration")
table.heading("categorie_id", text="ID de catégorie")

table.column("article_id", width=50)
table.column("nom_produit", width=150)
table.column("code_produit", width=150)
table.column("description", width=200)
table.column("cout", width=80)
table.column("prix_vente", width=100)
table.column("quantite_stock", width=120)
table.column("date_expiration", width=120)
table.column("categorie_id", width=100)

table.pack(side=tk.LEFT, fill=tk.BOTH)

scrollbar.config(command=table.yview)

# Form
form_frame = ttk.Frame(root)
form_frame.pack(pady=10)

nom_produit_label = ttk.Label(form_frame, text="Nom Produit:")
nom_produit_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)

nom_produit_entry = ttk.Entry(form_frame)
nom_produit_entry.grid(row=0, column=1, padx=5, pady=5)

code_produit_label = ttk.Label(form_frame, text="Code Produit:")
code_produit_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)

code_produit_entry = ttk.Entry(form_frame)
code_produit_entry.grid(row=1, column=1, padx=5, pady=5)

description_label = ttk.Label(form_frame, text="Description:")
description_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)

description_entry = ttk.Entry(form_frame)
description_entry.grid(row=2, column=1, padx=5, pady=5)

cout_label = ttk.Label(form_frame, text="Coût:")
cout_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)

cout_entry = ttk.Entry(form_frame)
cout_entry.grid(row=3, column=1, padx=5, pady=5)

prix_vente_label = ttk.Label(form_frame, text="Prix de vente:")
prix_vente_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)

prix_vente_entry = ttk.Entry(form_frame)
prix_vente_entry.grid(row=4, column=1, padx=5, pady=5)

quantite_stock_label = ttk.Label(form_frame, text="Quantité en stock:")
quantite_stock_label.grid(row=5, column=0, padx=5, pady=5, sticky=tk.E)

quantite_stock_entry = ttk.Entry(form_frame)
quantite_stock_entry.grid(row=5, column=1, padx=5, pady=5)

date_expiration_label = ttk.Label(form_frame, text="Date d'expiration:")
date_expiration_label.grid(row=6, column=0, padx=5, pady=5, sticky=tk.E)

date_expiration_entry = ttk.Entry(form_frame)
date_expiration_entry.grid(row=6, column=1, padx=5, pady=5)

categorie_id_label = ttk.Label(form_frame, text="ID de catégorie:")
categorie_id_label.grid(row=7, column=0, padx=5, pady=5, sticky=tk.E)

categorie_id_entry = ttk.Entry(form_frame)
categorie_id_entry.grid(row=7, column=1, padx=5, pady=5)

article_id_label = ttk.Label(form_frame, text="ID de l'article (modify/delete/search):")
article_id_label.grid(row=8, column=0, padx=5, pady=5, sticky=tk.E)

article_id_entry = ttk.Entry(form_frame)
article_id_entry.grid(row=8, column=1, padx=5, pady=5)

# Buttons
button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

ajouter_button = ttk.Button(button_frame, text="Ajouter", command=ajouter)
ajouter_button.grid(row=0, column=0, padx=5)

modifier_button = ttk.Button(button_frame, text="Modifier", command=modifier)
modifier_button.grid(row=0, column=1, padx=5)

supprimer_button = ttk.Button(button_frame, text="Supprimer", command=supprimer)
supprimer_button.grid(row=0, column=2, padx=5)

#### search

search_button = ttk.Button(button_frame, text="Rechercher par ID", command=search_by_id)
search_button.grid(row=0, column=3, padx=5)

clear_search_button = ttk.Button(button_frame, text="Effacer recherche", command=clear_search)
clear_search_button.grid(row=0, column=4, padx=5)

refresh_button = ttk.Button(button_frame, text="Actualiser", command=refresh_table)
refresh_button.grid(row=0, column=5, padx=5)


# search

# Populate table with initial data
refresh_table()

root.mainloop()
