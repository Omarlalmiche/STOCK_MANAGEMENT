import mysql.connector
import tkinter as tk
from tkinter import ttk

# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="stock"
)

# Create a cursor object to interact with the database
cursor = db.cursor()

# Execute the SQL queries to calculate the statistics
cursor.execute("SELECT COUNT(*) FROM Articles WHERE quantite_stock > 0")
sales_count = cursor.fetchone()[0]

cursor.execute("SELECT AVG(DATEDIFF(CURRENT_DATE(), date_expiration)) FROM Articles WHERE quantite_stock > 0")
average_stock_rotation = cursor.fetchone()[0]


cursor.execute("SELECT (COUNT(*) / SUM(quantite_commandee)) * 100 FROM Details_commande")
stockout_rate = cursor.fetchone()[0]

cursor.execute("SELECT AVG(cout_unitaire) FROM Details_commande")
average_cost_per_sale = cursor.fetchone()[0]

cursor.execute("SELECT AVG(quantite_stock) FROM Articles")
average_stock_level = cursor.fetchone()[0]

cursor.execute("SELECT SUM(quantite_commandee) / AVG(quantite_stock) FROM Details_commande INNER JOIN Articles ON Details_commande.produit_id = Articles.article_id")
stock_turnover_rate = cursor.fetchone()[0]

cursor.execute("SELECT AVG(quantite_stock * cout_unitaire) FROM Articles INNER JOIN Details_commande ON Articles.article_id = Details_commande.produit_id")
average_stock_cost = cursor.fetchone()[0]

cursor.execute("SELECT (COUNT(*) - SUM(CASE WHEN statut_commande = 'En attente' THEN 1 ELSE 0 END)) / COUNT(*) * 100 FROM Commandes")
order_fulfillment_rate = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM Commandes WHERE date_livraison_prevue < CURRENT_DATE() AND statut_commande = 'En attente'")
late_orders_count = cursor.fetchone()[0]

cursor.execute("SELECT SUM(prix_vente * quantite_commandee) FROM Articles INNER JOIN Details_commande ON Articles.article_id = Details_commande.produit_id")
stockout_cost = cursor.fetchone()[0]

# Close the database connection
db.close()

# Create the Tkinter GUI window
window = tk.Tk()
window.title("Stock Statistics")

# Create a table to display the statistics
table = ttk.Treeview(window)
table["columns"] = ("Statistique", "Valeur")
table.column("#0", width=0, stretch=tk.NO)
table.column("Statistique", anchor=tk.CENTER, width=300)
table.column("Valeur", anchor=tk.CENTER, width=300)
table.heading("Statistique", text="Statistique")
table.heading("Valeur", text="Valeur")

# Insert the statistics into the table
table.insert("", tk.END, values=["Taux de vente", f"{sales_count:.2f}%"])
table.insert("", tk.END, values=["Temps moyen de rotation des stocks", f"{average_stock_rotation:.2f} jours"])
table.insert("", tk.END, values=["Taux de rupture de stock", f"{stockout_rate:.2f}%"])
table.insert("", tk.END, values=["Coût moyen par article vendu", f"${average_cost_per_sale:.2f}"])
table.insert("", tk.END, values=["Niveau de stock moyen", f"{average_stock_level:.2f}"])
table.insert("", tk.END, values=["Taux de rotation des stocks", f"{stock_turnover_rate:.2f}"])
table.insert("", tk.END, values=["Coût moyen des stocks", f"${average_stock_cost:.2f}"])
table.insert("", tk.END, values=["Taux de satisfaction des commandes", f"{order_fulfillment_rate:.2f}%"])
table.insert("", tk.END, values=["Niveau de commandes en retard", late_orders_count])
table.insert("", tk.END, values=["Coût de la rupture de stock", f"${stockout_cost:.2f}"])

# Pack the table into the window
table.pack()

# Start the Tkinter event loop
window.mainloop()
