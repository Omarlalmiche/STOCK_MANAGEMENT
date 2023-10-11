import tkinter as tk
from tkinter import ttk
import mysql.connector

database = mysql.connector.connect(host="localhost", user="root", password="", database="stock")
connect = database.cursor()


def refresh_table(table, query):
    # Query the database to fetch the latest data
    connect.execute(query)
    data = connect.fetchall()

    # Clear the existing table data
    table.delete(*table.get_children())

    # Populate the table with the latest data
    for row in data:
        table.insert("", tk.END, values=row)


root = tk.Tk()
root.title("Gestion de stock")
root.geometry("800x600")
root.resizable(True, True)

# Create a notebook (tabbed interface) to display tables
notebook = ttk.Notebook(root)
notebook.pack(pady=10)

# Create tabs for each table

# Table 1: Articles
articles_tab = ttk.Frame(notebook)
notebook.add(articles_tab, text="Articles")

# Table 2: Categories_articles
categories_tab = ttk.Frame(notebook)
notebook.add(categories_tab, text="Categories_articles")

# Table 3: Emplacements
emplacements_tab = ttk.Frame(notebook)
notebook.add(emplacements_tab, text="Emplacements")

# Populate tables with initial data

# Table 1: Articles
articles_table_frame = ttk.Frame(articles_tab)
articles_table_frame.pack(pady=10)

articles_scrollbar = ttk.Scrollbar(articles_table_frame)
articles_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

articles_table = ttk.Treeview(articles_table_frame, columns=("article_id", "nom_produit", "code_produit", "description",
                                                             "cout", "prix_vente", "quantite_stock", "date_expiration",
                                                             "categorie_id"),
                              show="headings", yscrollcommand=articles_scrollbar.set)

articles_table.heading("article_id", text="ID")
articles_table.heading("nom_produit", text="Nom Produit")
articles_table.heading("code_produit", text="Code Produit")
articles_table.heading("description", text="Description")
articles_table.heading("cout", text="Coût")
articles_table.heading("prix_vente", text="Prix de vente")
articles_table.heading("quantite_stock", text="Quantité en stock")
articles_table.heading("date_expiration", text="Date d'expiration")
articles_table.heading("categorie_id", text="ID Catégorie")

articles_table.column("article_id", width=50)
articles_table.column("nom_produit", width=150)
articles_table.column("code_produit", width=150)
articles_table.column("description", width=200)
articles_table.column("cout", width=100)
articles_table.column("prix_vente", width=100)
articles_table.column("quantite_stock", width=120)
articles_table.column("date_expiration", width=120)
articles_table.column("categorie_id", width=80)

articles_table.pack(side=tk.LEFT, fill=tk.BOTH)

articles_scrollbar.config(command=articles_table.yview)

# Table 2: Categories_articles
categories_table_frame = ttk.Frame(categories_tab)
categories_table_frame.pack(pady=10)

categories_scrollbar = ttk.Scrollbar(categories_table_frame)
categories_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

categories_table = ttk.Treeview(categories_table_frame, columns=("categorie_id", "nom_categorie", "description"),
                                show="headings", yscrollcommand=categories_scrollbar.set)

categories_table.heading("categorie_id", text="ID")
categories_table.heading("nom_categorie", text="Nom Catégorie")
categories_table.heading("description", text="Description")

categories_table.column("categorie_id", width=50)
categories_table.column("nom_categorie", width=150)
categories_table.column("description", width=500)

categories_table.pack(side=tk.LEFT, fill=tk.BOTH)

categories_scrollbar.config(command=categories_table.yview)

# Table 3: Emplacements
emplacements_table_frame = ttk.Frame(emplacements_tab)
emplacements_table_frame.pack(pady=10)

emplacements_scrollbar = ttk.Scrollbar(emplacements_table_frame)
emplacements_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

emplacements_table = ttk.Treeview(emplacements_table_frame, columns=("emplacement_id", "nom_emplacement", "description",
                                                                     "capacite_stockage"),
                                  show="headings", yscrollcommand=emplacements_scrollbar.set)

emplacements_table.heading("emplacement_id", text="ID")
emplacements_table.heading("nom_emplacement", text="Nom Emplacement")
emplacements_table.heading("description", text="Description")
emplacements_table.heading("capacite_stockage", text="Capacité de stockage")

emplacements_table.column("emplacement_id", width=50)
emplacements_table.column("nom_emplacement", width=150)
emplacements_table.column("description", width=200)
emplacements_table.column("capacite_stockage", width=150)

emplacements_table.pack(side=tk.LEFT, fill=tk.BOTH)

emplacements_scrollbar.config(command=emplacements_table.yview)

# Populate tables with initial data

# Table 1: Articles
refresh_table(articles_table, "SELECT * FROM Articles")

# Table 2: Categories_articles
refresh_table(categories_table, "SELECT * FROM Categories_articles")

# Table 3: Emplacements
refresh_table(emplacements_table, "SELECT * FROM Emplacements")

root.mainloop()
