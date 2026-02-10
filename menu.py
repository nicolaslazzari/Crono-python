from course import Course
from tkinter import *
from functools import partial

class MenuGen :

	def CreerMenu(self, fenetre, liste_course) :

		def creerCourse(nom_course):
			course = Course()
			course.main(nom_course)

		menubar = Menu(fenetre)
		menu1 = Menu(menubar, tearoff=0)
		for i in liste_course :
			menu1.add_command(label=i, command=partial(creerCourse, i))
		menubar.add_cascade(label="Courses", menu=menu1)



		fenetre.configure(menu=menubar)