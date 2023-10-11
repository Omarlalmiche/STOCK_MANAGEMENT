import tkinter as tk
from tkinter import ttk
import subprocess
import sys

def open_articles():
    subprocess.Popen([sys.executable, "g-articles.py"])

def open_commandes():
    subprocess.Popen([sys.executable, "g-commandes.py"])

def open_categories():
    subprocess.Popen([sys.executable, "g-categories.py"])

def open_livraisons():
    subprocess.Popen([sys.executable, "g-livraisons.py"])

def open_clients():
    subprocess.Popen([sys.executable, "g-clients.py"])

def open_fournisseurs():
    subprocess.Popen([sys.executable, "g-fournisseurs.py"])

def open_display_all():
    subprocess.Popen([sys.executable, "g-stock.py"])

def open_statistiques():
    subprocess.Popen([sys.executable, "g-stat.py"])

root = tk.Tk()
root.title("Gestion de Stock - Mohammed Filali & Omar Lalmiche")
root.geometry("800x600")
root.resizable(True, True)

title_label = tk.Label(root, text="Project Base Donnée - Gestion de Stock", font=("Arial", 30), padx=10, pady=10)
title_label.pack(pady=25)

button_frame = ttk.Frame(root)
button_frame.pack(pady=50)

button_style = ttk.Style()
button_style.configure("Custom.TButton", font=("Arial", 18), padding=10)

button1 = ttk.Button(button_frame, text="GESTION DES ARTICLES", command=open_articles, style="Custom.TButton")
button1.grid(row=0, column=0, padx=10, pady=10)

button2 = ttk.Button(button_frame, text="GESTION DES COMMANDES", command=open_commandes, style="Custom.TButton")
button2.grid(row=0, column=1, padx=10, pady=10)

button3 = ttk.Button(button_frame, text="GESTION DES CATÉGORIES", command=open_categories, style="Custom.TButton")
button3.grid(row=1, column=0, padx=10, pady=10)

button4 = ttk.Button(button_frame, text="GESTION DES LIVRAISONS", command=open_livraisons, style="Custom.TButton")
button4.grid(row=1, column=1, padx=10, pady=10)

button5 = ttk.Button(button_frame, text="GESTION DES CLIENTS", command=open_clients, style="Custom.TButton")
button5.grid(row=2, column=0, padx=10, pady=10)

button6 = ttk.Button(button_frame, text="GESTION DES FOURNISSEURS", command=open_fournisseurs, style="Custom.TButton")
button6.grid(row=2, column=1, padx=10, pady=10)

button7 = ttk.Button(button_frame, text="AFFICHER STOCK", command=open_display_all, style="Custom.TButton", width=20)
button7.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

button8 = ttk.Button(button_frame, text="STATISTIQUES DE STOCK", command=open_statistiques, style="Custom.TButton")
button8.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

button_frame.columnconfigure((0, 1), weight=1)
button_frame.rowconfigure((0, 1, 2, 3, 4), weight=1)

root.mainloop()
