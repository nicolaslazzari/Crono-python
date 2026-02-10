from tkinter import *
from tkinter import filedialog
import pandas as pad
import sqlite3
from datetime import datetime
from menu import MenuGen
from ExportResult import ExportResult

db = sqlite3.connect('db_donnees.sqlite')
cur = db.cursor()

centsec = 0
demarrer_chrono=0

def import_insc():
	file_path = filedialog.askopenfile(title= "Fichiers des inscrits à importer", mode ='r', initialdir= '::{20D04FE0-3AEA-1069-A2D8-08002B30309D}', filetypes =[("Fichiers Excel","*.xlsx"), ("Fichiers OpenDocument","*.ods")])
	f = pad.ExcelFile(file_path.name)
	for i in (f.sheet_names):
		nom_table = "Course_" + i + "_" + str(datetime.today().strftime('%d%m%Y'))
		command = f"""DROP TABLE IF EXISTS {nom_table};
			CREATE TABLE {nom_table} (
			numdos INTEGER,
			nom VARCHAR,
			prenom VARCHAR,
			cat VARCHAR,
			sex VARCHAR,
			club VARCHAR,
			PRIMARY KEY (numdos));"""
		cur.executescript(command)
		db.commit()
		sheet = f.parse(i, header=None)
		for j in range (len(sheet)) :
			cur.execute(f"INSERT INTO {nom_table} (numdos, nom, prenom, cat, sex, club) values (?, ?, ?, ?, ?, ?)", (int(sheet[0][j]), sheet[1][j], sheet[2][j], sheet[3][j], sheet[4][j], sheet[5][j]))
			db.commit()

	m = MenuGen()
	m.CreerMenu(fenetre, f.sheet_names)



#temporaire (generation fichier result)
def export_insc():
	e = ExportResult()
	e.main()


fenetre = Tk()

fenetre.geometry("500x500")
fenetre.title("Crono")
# fenetre.state('zoomed')


label = Label(fenetre, text= "Importer les inscription\nou\nExporter les resultats", font=("Arial", 18), pady= 75).pack()
bouton_import = Button(fenetre, text="Importer inscrits", command=import_insc).pack()
bouton_export = Button(fenetre, text= "Exporter resultats", command=export_insc).pack()



fenetre.mainloop()







