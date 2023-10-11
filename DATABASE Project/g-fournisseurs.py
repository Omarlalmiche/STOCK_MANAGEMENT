import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

database = mysql.connector.connect(host="localhost", user="root", password="", database="stock")
connect = database.cursor()


def refresh_table():
    # Query the database to fetch the latest data
    connect.execute("SELECT * FROM Fournisseurs")
    data = connect.fetchall()

    # Clear the existing table data
    table.delete(*table.get_children())

    # Populate the table with the latest data
    for row in data:
        table.insert("", tk.END, values=row)


def ajouter():
    nom_entreprise = nom_entreprise_entry.get()
    adresse = adresse_entry.get()
    numero_telephone = numero_telephone_entry.get()
    numero_fax = numero_fax_entry.get()
    courriel = courriel_entry.get()
    contact_principal = contact_principal_entry.get()

    if len(nom_entreprise) > 0:
        try:
            sql = "INSERT INTO Fournisseurs (nom_entreprise, adresse, numero_telephone, numero_fax, courriel, contact_principal) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (nom_entreprise, adresse, numero_telephone, numero_fax, courriel, contact_principal)
            connect.execute(sql, val)
            database.commit()
            refresh_table()
            clear_inputs()
            messagebox.showinfo("Succès", "Le fournisseur a été ajouté avec succès.")
        except Exception as e:
            print(e)
            database.rollback()
            messagebox.showerror("Erreur", "Erreur lors de l'ajout du fournisseur.")
    else:
        messagebox.showerror("Erreur", "Veuillez entrer le nom de l'entreprise du fournisseur.")


def modifier():
    fournisseur_id = fournisseur_id_entry.get()
    nom_entreprise = nom_entreprise_entry.get()
    adresse = adresse_entry.get()
    numero_telephone = numero_telephone_entry.get()
    numero_fax = numero_fax_entry.get()
    courriel = courriel_entry.get()
    contact_principal = contact_principal_entry.get()

    if len(fournisseur_id) > 0:
        try:
            sql = "UPDATE Fournisseurs SET nom_entreprise = %s, adresse = %s, numero_telephone = %s, numero_fax = %s, courriel = %s, contact_principal = %s WHERE fournisseur_id = %s"
            val = (nom_entreprise, adresse, numero_telephone, numero_fax, courriel, contact_principal, fournisseur_id)
            connect.execute(sql, val)
            database.commit()
            refresh_table()
            clear_inputs()
            messagebox.showinfo("Succès", "Le fournisseur a été modifié avec succès.")
        except Exception as e:
            print(e)
            database.rollback()
            messagebox.showerror("Erreur", "Erreur lors de la modification du fournisseur.")
    else:
        messagebox.showerror("Erreur", "Veuillez entrer l'ID du fournisseur à modifier.")


def supprimer():
    fournisseur_id = fournisseur_id_entry.get()
    if len(fournisseur_id) > 0:
        try:
            sql = "DELETE FROM Fournisseurs WHERE fournisseur_id = %s"
            val = (fournisseur_id,)
            connect.execute(sql, val)
            database.commit()
            refresh_table()
            clear_inputs()
            messagebox.showinfo("Succès", "Le fournisseur a été supprimé avec succès.")
        except Exception as e:
            print(e)
            database.rollback()
            messagebox.showerror("Erreur", "Erreur lors de la suppression du fournisseur.")
    else:
        messagebox.showerror("Erreur", "Veuillez entrer l'ID du fournisseur à supprimer.")


def clear_inputs():
    nom_entreprise_entry.delete(0, tk.END)
    adresse_entry.delete(0, tk.END)
    numero_telephone_entry.delete(0, tk.END)
    numero_fax_entry.delete(0, tk.END)
    courriel_entry.delete(0, tk.END)
    contact_principal_entry.delete(0, tk.END)
    fournisseur_id_entry.delete(0, tk.END)


def search_by_id():
    fournisseur_id = fournisseur_id_entry.get()
    if len(fournisseur_id) > 0:
        try:
            sql = "SELECT * FROM Fournisseurs WHERE fournisseur_id = %s"
            val = (fournisseur_id,)
            connect.execute(sql, val)
            data = connect.fetchall()
            table.delete(*table.get_children())
            for row in data:
                table.insert("", tk.END, values=row)
        except Exception as e:
            print(e)
            messagebox.showerror("Erreur", "Erreur lors de la recherche du fournisseur.")
    else:
        messagebox.showerror("Erreur", "Veuillez entrer l'ID du fournisseur à rechercher.")


def clear_search():
    fournisseur_id_entry.delete(0, tk.END)
    refresh_table()


root = tk.Tk()
root.title("Gestion des fournisseurs")
root.geometry("800x600")
root.resizable(True, True)

# Title
title_label = tk.Label(root, text="Gestion des fournisseurs", font=("Arial", 20), padx=10, pady=10)
title_label.pack()

# Table
table_frame = ttk.Frame(root)
table_frame.pack(pady=10)

scrollbar = ttk.Scrollbar(table_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

table = ttk.Treeview(table_frame,
                     columns=("fournisseur_id", "nom_entreprise", "adresse", "numero_telephone", "numero_fax", "courriel",
                              "contact_principal"),
                     show="headings", yscrollcommand=scrollbar.set)

table.heading("fournisseur_id", text="ID")
table.heading("nom_entreprise", text="Nom Entreprise")
table.heading("adresse", text="Adresse")
table.heading("numero_telephone", text="Numéro de téléphone")
table.heading("numero_fax", text="Numéro de fax")
table.heading("courriel", text="Courriel")
table.heading("contact_principal", text="Contact Principal")

table.column("fournisseur_id", width=50)
table.column("nom_entreprise", width=150)
table.column("adresse", width=150)
table.column("numero_telephone", width=100)
table.column("numero_fax", width=100)
table.column("courriel", width=150)
table.column("contact_principal", width=150)

table.pack(side=tk.LEFT, fill=tk.BOTH)

scrollbar.config(command=table.yview)

# Form
form_frame = ttk.Frame(root)
form_frame.pack(pady=10)

nom_entreprise_label = ttk.Label(form_frame, text="Nom Entreprise:")
nom_entreprise_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)

nom_entreprise_entry = ttk.Entry(form_frame)
nom_entreprise_entry.grid(row=0, column=1, padx=5, pady=5)

adresse_label = ttk.Label(form_frame, text="Adresse:")
adresse_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)

adresse_entry = ttk.Entry(form_frame)
adresse_entry.grid(row=1, column=1, padx=5, pady=5)

numero_telephone_label = ttk.Label(form_frame, text="Numéro de téléphone:")
numero_telephone_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)

numero_telephone_entry = ttk.Entry(form_frame)
numero_telephone_entry.grid(row=2, column=1, padx=5, pady=5)

numero_fax_label = ttk.Label(form_frame, text="Numéro de fax:")
numero_fax_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)

numero_fax_entry = ttk.Entry(form_frame)
numero_fax_entry.grid(row=3, column=1, padx=5, pady=5)

courriel_label = ttk.Label(form_frame, text="Courriel:")
courriel_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)

courriel_entry = ttk.Entry(form_frame)
courriel_entry.grid(row=4, column=1, padx=5, pady=5)

contact_principal_label = ttk.Label(form_frame, text="Contact Principal:")
contact_principal_label.grid(row=5, column=0, padx=5, pady=5, sticky=tk.E)

contact_principal_entry = ttk.Entry(form_frame)
contact_principal_entry.grid(row=5, column=1, padx=5, pady=5)

fournisseur_id_label = ttk.Label(form_frame, text="ID du fournisseur (modify/delete/search):")
fournisseur_id_label.grid(row=6, column=0, padx=5, pady=5, sticky=tk.E)

fournisseur_id_entry = ttk.Entry(form_frame)
fournisseur_id_entry.grid(row=6, column=1, padx=5, pady=5)

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
