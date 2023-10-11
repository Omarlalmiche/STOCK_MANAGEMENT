import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

database = mysql.connector.connect(host="localhost", user="root", password="", database="stock")
connect = database.cursor()

def refresh_table():
    # Query the database to fetch the latest data
    connect.execute("SELECT * FROM Commandes")
    data = connect.fetchall()

    # Clear the existing table data
    table.delete(*table.get_children())

    # Populate the table with the latest data
    for row in data:
        table.insert("", tk.END, values=row)

def ajouter():
    date_commande = date_commande_entry.get()
    date_livraison_prevue = date_livraison_prevue_entry.get()
    statut_commande = statut_commande_entry.get()
    fournisseur_id = fournisseur_id_entry.get()

    if len(date_commande) > 0 and len(date_livraison_prevue) > 0 and len(statut_commande) > 0 and len(fournisseur_id) > 0:
        try:
            sql = "INSERT INTO Commandes (date_commande, date_livraison_prevue, statut_commande, fournisseur_id) VALUES (%s, %s, %s, %s)"
            val = (date_commande, date_livraison_prevue, statut_commande, fournisseur_id)
            connect.execute(sql, val)
            database.commit()
            refresh_table()
            clear_inputs()
            messagebox.showinfo("Succès", "La commande a été ajoutée avec succès.")
        except Exception as e:
            print(e)
            database.rollback()
            messagebox.showerror("Erreur", "Erreur lors de l'ajout de la commande.")
    else:
        messagebox.showerror("Erreur", "Veuillez remplir tous les champs de la commande.")

def modifier():
    commande_id = commande_id_entry.get()
    date_commande = date_commande_entry.get()
    date_livraison_prevue = date_livraison_prevue_entry.get()
    statut_commande = statut_commande_entry.get()
    fournisseur_id = fournisseur_id_entry.get()

    if len(commande_id) > 0 and len(date_commande) > 0 and len(date_livraison_prevue) > 0 and len(statut_commande) > 0 and len(fournisseur_id) > 0:
        try:
            sql = "UPDATE Commandes SET date_commande = %s, date_livraison_prevue = %s, statut_commande = %s, fournisseur_id = %s WHERE commande_id = %s"
            val = (date_commande, date_livraison_prevue, statut_commande, fournisseur_id, commande_id)
            connect.execute(sql, val)
            database.commit()
            refresh_table()
            clear_inputs()
            messagebox.showinfo("Succès", "La commande a été modifiée avec succès.")
        except Exception as e:
            print(e)
            database.rollback()
            messagebox.showerror("Erreur", "Erreur lors de la modification de la commande.")
    else:
        messagebox.showerror("Erreur", "Veuillez remplir tous les champs de la commande et spécifier l'ID de la commande à modifier.")

def supprimer():
    commande_id = commande_id_entry.get()
    if len(commande_id) > 0:
        try:
            sql = "DELETE FROM Commandes WHERE commande_id = %s"
            val = (commande_id,)
            connect.execute(sql, val)
            database.commit()
            refresh_table()
            clear_inputs()
            messagebox.showinfo("Succès", "La commande a été supprimée avec succès.")
        except Exception as e:
            print(e)
            database.rollback()
            messagebox.showerror("Erreur", "Erreur lors de la suppression de la commande.")
    else:
        messagebox.showerror("Erreur", "Veuillez spécifier l'ID de la commande à supprimer.")

def clear_inputs():
    commande_id_entry.delete(0, tk.END)
    date_commande_entry.delete(0, tk.END)
    date_livraison_prevue_entry.delete(0, tk.END)
    statut_commande_entry.delete(0, tk.END)
    fournisseur_id_entry.delete(0, tk.END)

def search_by_id():
    commande_id = commande_id_entry.get()
    if len(commande_id) > 0:
        try:
            sql = "SELECT * FROM Commandes WHERE commande_id = %s"
            val = (commande_id,)
            connect.execute(sql, val)
            data = connect.fetchall()
            table.delete(*table.get_children())
            for row in data:
                table.insert("", tk.END, values=row)
        except Exception as e:
            print(e)
            messagebox.showerror("Erreur", "Erreur lors de la recherche de la commande.")
    else:
        messagebox.showerror("Erreur", "Veuillez entrer l'ID de la commande à rechercher.")

def clear_search():
    refresh_table()

root = tk.Tk()
root.title("Gestion des commandes")
root.geometry("800x600")
root.resizable(True, True)

# Title
title_label = tk.Label(root, text="Gestion des commandes", font=("Arial", 20), padx=10, pady=10)
title_label.pack()

# Table
table_frame = ttk.Frame(root)
table_frame.pack(pady=10)

scrollbar = ttk.Scrollbar(table_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

table = ttk.Treeview(table_frame, columns=("commande_id", "date_commande", "date_livraison_prevue", "statut_commande", "fournisseur_id"),
                     show="headings", yscrollcommand=scrollbar.set)

table.heading("commande_id", text="ID")
table.heading("date_commande", text="Date de commande")
table.heading("date_livraison_prevue", text="Date de livraison prévue")
table.heading("statut_commande", text="Statut de commande")
table.heading("fournisseur_id", text="ID du fournisseur")

table.column("commande_id", width=50)
table.column("date_commande", width=150)
table.column("date_livraison_prevue", width=150)
table.column("statut_commande", width=150)
table.column("fournisseur_id", width=100)

table.pack(side=tk.LEFT, fill=tk.BOTH)

scrollbar.config(command=table.yview)

# Form
form_frame = ttk.Frame(root)
form_frame.pack(pady=10)

date_commande_label = ttk.Label(form_frame, text="Date de commande:")
date_commande_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)

date_commande_entry = ttk.Entry(form_frame)
date_commande_entry.grid(row=0, column=1, padx=5, pady=5)

date_livraison_prevue_label = ttk.Label(form_frame, text="Date de livraison prévue:")
date_livraison_prevue_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)

date_livraison_prevue_entry = ttk.Entry(form_frame)
date_livraison_prevue_entry.grid(row=1, column=1, padx=5, pady=5)

statut_commande_label = ttk.Label(form_frame, text="Statut de commande:")
statut_commande_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)

statut_commande_entry = ttk.Entry(form_frame)
statut_commande_entry.grid(row=2, column=1, padx=5, pady=5)

fournisseur_id_label = ttk.Label(form_frame, text="ID du fournisseur:")
fournisseur_id_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)

fournisseur_id_entry = ttk.Entry(form_frame)
fournisseur_id_entry.grid(row=3, column=1, padx=5, pady=5)

commande_id_label = ttk.Label(form_frame, text="ID de la commande (modify/delete/search):")
commande_id_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)

commande_id_entry = ttk.Entry(form_frame)
commande_id_entry.grid(row=4, column=1, padx=5, pady=5)

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
