import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

database = mysql.connector.connect(host="localhost", user="root", password="", database="stock")
connect = database.cursor()


def refresh_table():
    # Query the database to fetch the latest data
    connect.execute("SELECT * FROM Clients")
    data = connect.fetchall()

    # Clear the existing table data
    table.delete(*table.get_children())

    # Populate the table with the latest data
    for row in data:
        table.insert("", tk.END, values=row)


def ajouter():
    nom_client = nom_client_entry.get()
    adresse_client = adresse_client_entry.get()
    numero_telephone = numero_telephone_entry.get()

    if len(nom_client) > 0:
        try:
            sql = "INSERT INTO Clients (nom_client, adresse_client, numero_telephone) VALUES (%s, %s, %s)"
            val = (nom_client, adresse_client, numero_telephone)
            connect.execute(sql, val)
            database.commit()
            refresh_table()
            clear_inputs()
            messagebox.showinfo("Succès", "Le client a été ajouté avec succès.")
        except Exception as e:
            print(e)
            database.rollback()
            messagebox.showerror("Erreur", "Erreur lors de l'ajout du client.")
    else:
        messagebox.showerror("Erreur", "Veuillez entrer le nom du client.")


def modifier():
    client_id = client_id_entry.get()
    nom_client = nom_client_entry.get()
    adresse_client = adresse_client_entry.get()
    numero_telephone = numero_telephone_entry.get()

    if len(client_id) > 0:
        try:
            sql = "UPDATE Clients SET nom_client = %s, adresse_client = %s, numero_telephone = %s WHERE client_id = %s"
            val = (nom_client, adresse_client, numero_telephone, client_id)
            connect.execute(sql, val)
            database.commit()
            refresh_table()
            clear_inputs()
            messagebox.showinfo("Succès", "Le client a été modifié avec succès.")
        except Exception as e:
            print(e)
            database.rollback()
            messagebox.showerror("Erreur", "Erreur lors de la modification du client.")
    else:
        messagebox.showerror("Erreur", "Veuillez entrer l'ID du client à modifier.")


def supprimer():
    client_id = client_id_entry.get()
    if len(client_id) > 0:
        try:
            sql = "DELETE FROM Clients WHERE client_id = %s"
            val = (client_id,)
            connect.execute(sql, val)
            database.commit()
            refresh_table()
            clear_inputs()
            messagebox.showinfo("Succès", "Le client a été supprimé avec succès.")
        except Exception as e:
            print(e)
            database.rollback()
            messagebox.showerror("Erreur", "Erreur lors de la suppression du client.")
    else:
        messagebox.showerror("Erreur", "Veuillez entrer l'ID du client à supprimer.")


def clear_inputs():
    nom_client_entry.delete(0, tk.END)
    adresse_client_entry.delete(0, tk.END)
    numero_telephone_entry.delete(0, tk.END)
    client_id_entry.delete(0, tk.END)

def search_by_id():
    client_id = client_id_entry.get()
    if len(client_id) > 0:
        try:
            sql = "SELECT * FROM Clients WHERE client_id = %s"
            val = (client_id,)
            connect.execute(sql, val)
            data = connect.fetchall()
            table.delete(*table.get_children())
            for row in data:
                table.insert("", tk.END, values=row)
        except Exception as e:
            print(e)
            messagebox.showerror("Erreur", "Erreur lors de la recherche du client.")
    else:
        messagebox.showerror("Erreur", "Veuillez entrer l'ID du client à rechercher.")

def clear_search():
    client_id_entry.delete(0, tk.END)
    refresh_table()


root = tk.Tk()
root.title("Gestion des clients")
root.geometry("800x600")
root.resizable(True, True)

# Title
title_label = tk.Label(root, text="Gestion des clients", font=("Arial", 20), padx=10, pady=10)
title_label.pack()

# Table
table_frame = ttk.Frame(root)
table_frame.pack(pady=10)

scrollbar = ttk.Scrollbar(table_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

table = ttk.Treeview(table_frame, columns=("client_id", "nom_client", "adresse_client", "numero_telephone"),
                     show="headings", yscrollcommand=scrollbar.set)

table.heading("client_id", text="ID")
table.heading("nom_client", text="Nom Client")
table.heading("adresse_client", text="Adresse")
table.heading("numero_telephone", text="Numéro de téléphone")

table.column("client_id", width=50)
table.column("nom_client", width=150)
table.column("adresse_client", width=150)
table.column("numero_telephone", width=100)

table.pack(side=tk.LEFT, fill=tk.BOTH)

scrollbar.config(command=table.yview)

# Form
form_frame = ttk.Frame(root)
form_frame.pack(pady=10)

nom_client_label = ttk.Label(form_frame, text="Nom Client:")
nom_client_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)

nom_client_entry = ttk.Entry(form_frame)
nom_client_entry.grid(row=0, column=1, padx=5, pady=5)

adresse_client_label = ttk.Label(form_frame, text="Adresse:")
adresse_client_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)

adresse_client_entry = ttk.Entry(form_frame)
adresse_client_entry.grid(row=1, column=1, padx=5, pady=5)

numero_telephone_label = ttk.Label(form_frame, text="Numéro de téléphone:")
numero_telephone_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)

numero_telephone_entry = ttk.Entry(form_frame)
numero_telephone_entry.grid(row=2, column=1, padx=5, pady=5)

client_id_label = ttk.Label(form_frame, text="ID du client (modify/delete/search):")
client_id_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)

client_id_entry = ttk.Entry(form_frame)
client_id_entry.grid(row=3, column=1, padx=5, pady=5)

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
