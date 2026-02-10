import time
from tkinter import *
from tkinter import filedialog 
from functools import partial
import sqlite3
import datetime

class Course:

	def main(self,nom_course) :

		db = sqlite3.connect('db_donnees.sqlite')
		cur = db.cursor()

		stopchrono = TRUE

		def start(j):
			nonlocal stopchrono
			nonlocal demarrer_chrono
			sc = time.time()
			if (demarrer_chrono == 0) :
				demarrer_chrono = sc
				# On garde pour plus tard, c'est genre des restes
				if (j > 0):
					diff = int(sc - demarrer_chrono)
					mins = diff//60
					diff = diff - mins*60
					if(diff<10):
						diff = f"0{diff}"
					if(mins<10):
						mins = f"0{mins}"
					text_chrono.insert(INSERT, f"Vague {j+1} démarrée après {mins}m{diff}s")
				else :
					date = datetime.datetime.fromtimestamp(sc).strftime('%d/%m%Y à %H:%M:%S')
					text_chrono.insert(INSERT, f"Chrono Démarré le {date}")
			if (stopchrono) :
				stopchrono = FALSE
				

		#############################################
		#											#
		#	Fonction de mise en forme du temps		#
		#											#
		#############################################
		# def cent2tps(cs) :
		# 	heure = cs//360000
		# 	minute = cs//6000 - heure*60
		# 	secondes = cs//100 - minute*60 - heure*3600
		# 	centsec=cs- minute*6000 - heure*360000 - secondes*100
		# 	if(secondes<10):
		# 		secondes = f"0{secondes}"
		# 	if(minute<10):
		# 		minute = f"0{minute}"
		# 	if(heure<10):
		# 		heure = f"0{heure}"
		# 	return(f"{heure}h{minute}m{secondes}s{centsec}cs")



		def stop():
			nonlocal stopchrono
			if not stopchrono :
				stopchrono = TRUE
				text_chrono.delete('1.0', END)
				text_chrono.insert(INSERT, "Chrono Arrêté")

		def dossard(i,j):
			nonlocal stopchrono
			if not stopchrono :
				write_res(True, i, j)
				Button(frame_num_dos, text=(i+1)+k*j,width=5, command= partial(write_res, False, i, j), bg = 'RED').grid(row=j, column=i)

		def write_res (b, i, j) :
			nonlocal demarrer_chrono
			stop_chrono = time.time()
			file = open("Memoire_" + nom_course + "_" + timestaamp_today + ".txt",'a')
			temp = stop_chrono - demarrer_chrono
			temp_brut = int(temp) 
			temp_lis = str(datetime.timedelta(seconds=temp_brut))
			doss = (i+1)+k*j
			file.write(f"Dossard : {doss}, Temps : {temp_lis}\n")
			file.close()
			if b :
				cur.execute(f"INSERT INTO {nom_table_res} (numdos, temp_brut, temp_lis) values (?, ?, ?)", (doss, temp_brut, temp_lis))
				db.commit()

		timestaamp_today = str(datetime.datetime.today().strftime('%d%m%Y'))
		nom_table = "Course_" + nom_course + "_" + timestaamp_today # récup nombre inscrit
		cur.execute(f"SELECT count(*), min(numdos) FROM {nom_table}")
		nb_concu, num_min_dos = cur.fetchall()[0]
		num_min_dos-=1

		nom_table_res = nom_table + "_res"

		command = f"""DROP TABLE IF EXISTS {nom_table_res};
			CREATE TABLE {nom_table_res} (
			numdos INTEGER,
			temp_brut INTEGER,
			temp_lis CHAR,
			PRIMARY KEY (numdos));"""
		cur.executescript(command)
		db.commit()

		demarrer_chrono = 0

		fenetre = Tk()
		fenetre.geometry("1800x700")
		fenetre.title("Course " + nom_course)

		frame_tps = LabelFrame(fenetre)
		frame_tps.grid(row=2, column=0, columnspan=1, sticky='W', ipadx=130, ipady=25)
		# for i in range(0, nb_vagues) :
		bouton_start = Button(frame_tps, text="Démarrer le chrono", command=partial(start, 0)).grid(row=0, column=5)
		text_chrono = Text(fenetre, height= 1, width=40)
		text_chrono.grid(row= 1, column=0)
		bouton_stop = Button(frame_tps, text= "Stopper temps", command=stop).grid(row=1, column=5)
		frame_num_dos = LabelFrame(fenetre,width=125)
		frame_num_dos.grid(row=2, column=20, columnspan=20, sticky='W', padx=100, pady=5, ipadx=130, ipady=25)

		k=25
		k_q = nb_concu//k
		k_r = nb_concu%k


		for j in range (k_q+1):
			if j < k_q :
				for i in range(k) :
					Button(frame_num_dos, text=num_min_dos+(i+1)+k*j,width=5, command= partial(dossard, i, j)).grid(row=j, column=i)
			else :
				for i in range(k_r) :
					Button(frame_num_dos, text=num_min_dos+(i+1)+k*j,width=5, command= partial(dossard, i, j)).grid(row=j, column=i)


		fenetre.mainloop()

##Catégories: MP, PO, PU, BE, MI, CA, JU, SX, VX where X ∈ ℕ
