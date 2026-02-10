from tkinter import *
from tkinter import ttk
import sqlite3
import pandas as pad
from tkinter import filedialog

class ExportResult :


	def main(self) :

		def export() :
			res_file_path = filedialog.askdirectory(title= "Dossier de dépot des résultats", initialdir= '::{20D04FE0-3AEA-1069-A2D8-08002B30309D}',mustexist=True)
			course = listeCombo.get()
			cur.execute(f"SELECT i.numdos, i.nom, i.prenom, i.cat, i.sex, i.club, r.temp_lis FROM {course} as i JOIN {course}_res as r on i.numdos = r.numdos ORDER BY r.temp_brut;")
			resultat_course = cur.fetchall()
			cur.execute(f"SELECT cat FROM {course} GROUP BY cat")
			categories = cur.fetchall() 
			dic_cat_m = {x[0]: 0 for x in categories}
			dic_cat_f = dic_cat_m
			for i in range(len(resultat_course)) :
				res = resultat_course[i]
				cat = res[3]
				sexe = res[4]
				if sexe == 'F' :
					dic_cat_f[cat] = dic_cat_f[cat]+1
					resultat_course[i] = resultat_course[i] + (dic_cat_f[cat],)
				elif sexe == 'M':
					dic_cat_m[cat] = dic_cat_m[cat]+1
					resultat_course[i] = resultat_course[i] + (dic_cat_m[cat],)
			res_file_path = res_file_path + "\\Resultat_" + course + ".xlsx"
			classement = range(1, len(resultat_course)+1)
			colonnes = ["Dossard", "Nom", "Prénom", "Catégorie", "Sexe", "Club", "Temps", "Classement Catégorie"]
			df = pad.DataFrame(resultat_course, columns=colonnes,index=classement)

			writer = pad.ExcelWriter(res_file_path, engine = 'xlsxwriter')
			df.to_excel(writer, merge_cells=False, index_label ="Classement", sheet_name='Classement')

			ind = []
			res_course_cat = []
			for c in categories :
				catego = c[0]
				cur.execute(f"SELECT i.numdos, i.nom, i.prenom, i.club, r.temp_lis FROM {course} as i JOIN {course}_res as r on i.numdos = r.numdos WHERE i.cat = '{catego}' AND i.sex = 'M' ORDER BY r.temp_brut;")
				res_m = cur.fetchall()
				cur.execute(f"SELECT i.numdos, i.nom, i.prenom, i.club, r.temp_lis FROM {course} as i JOIN {course}_res as r on i.numdos = r.numdos WHERE i.cat = '{catego}' AND i.sex = 'F' ORDER BY r.temp_brut;")
				res_f = cur.fetchall()
				res_course_cat.append((catego, 'M'))
				ind.append('')
				i=1
				for x in res_m :
					res_course_cat.append(x)
					ind.append(i)
					i+=1
				res_course_cat.append((catego, 'F'))
				ind.append('')
				i=1
				for x in res_f :
					res_course_cat.append(x)
					ind.append(i)
					i+=1

			df_cat = pad.DataFrame(res_course_cat,index=ind)
			df_cat.to_excel(writer, merge_cells=False, header=False, sheet_name='Categories')

			writer.close()

			






		db = sqlite3.connect('db_donnees.sqlite')
		cur = db.cursor()
		cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name like '%_res';")#'%_res'
		liste_course = [x[0][:-4] for x in cur.fetchall()]

		fenetre = Tk("Export des resultats")
		fenetre.geometry("400x300")
		label_inv1 = Label(fenetre, text= "", font=("Arial", 20)).pack()
		label = Label(fenetre, text= "Choisir la course", font=("Arial", 18), pady=30).pack()
		listeCombo = ttk.Combobox(fenetre, values=liste_course)
		listeCombo.current(0)
		listeCombo.pack()
		label_inv2 = Label(fenetre, text= "", font=("Arial", 10)).pack()
		bouton_export = Button(fenetre, text= "Exporter resultats", command=export, anchor= CENTER).pack()

		fenetre.mainloop()
