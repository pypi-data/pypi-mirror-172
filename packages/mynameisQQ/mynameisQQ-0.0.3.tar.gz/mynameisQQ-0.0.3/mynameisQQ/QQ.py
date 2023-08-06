import random
class PongsuraQQ:
	"""
	this class has the information about QQ 
	including the name
	the age
	and bla bla bla

	Example
	#----------------
	QQ = PongsuraQQ()
	QQ.show_name()
	QQ.show_youtube()
	QQ.about()
	QQ.show_art()
	QQ.dice()
	#----------------
	"""
	def __init__(self):
		self.name = 'QQ'
		self.page = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'

	def show_name(self):
		print(f'Hi my name is {self.name}')	

	def show_youtube(self):
		print('https://www.youtube.com/watch?v=xvFZjo5PgG0')	

	def about(self):
		text = """
		-----------------------
		Hi my name is QQ
		A Brawl Stars player
		Currenty #1 Thailand
		-----------------------"""
		print(text)

	def show_art(self):
		text = """
		⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡤⠒⠒⠲⣄⡠⠤⠤⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
		⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠚⢹⠀⠀⠀⠀⠸⡀⠀⠀⠈⡷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
		⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⠀⠸⡄⠀⠀⠀⢸⠁⠀⠀⢠⣧⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
		⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡳⠤⠚⠒⠂⠀⠙⠒⠒⠤⢿⡁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
		⠀⠀⠀⠀⢀⡀⣀⡤⣄⠀⠀⠀⠀⠀⠀⢀⡴⠚⠁⢀⠀⠀⠀⠀⠀⠀⠀⠱⠀⠀⠈⠳⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
		⠀⠀⠀⠀⣿⠀⡇⠀⡼⠋⢙⠆⠀⠀⣠⠊⣀⡀⠀⡜⠀⣀⡤⢤⣀⠀⠀⠀⢣⠀⠀⠀⣼⢛⣿⠆⠀⠀⠀⠀⠀⠀⠀
		⠀⠀⢠⣤⣼⠛⠧⠼⡤⠤⣎⠀⢀⣰⠃⡾⠉⢻⢀⠃⣼⠋⠀⠀⠙⣧⠀⠀⠈⡆⠀⠀⠈⠉⢳⠀⠀⠀⠀⠀⠀⠀⠀
		⠀⣀⣈⣿⢫⢤⣤⢸⡇⠀⢿⡿⢻⠇⠰⡇⢀⠎⠸⠀⠹⣄⠀⠀⣠⡟⠀⠀⠀⡇⠀⠀⠀⠀⠀⣇⠀⠀⠀⠀⠀⠀⠀
		⢸⡟⡹⢿⡀⠓⠛⢙⡇⠀⢠⣧⡾⠀⠀⢩⣿⣦⣤⣠⣤⣌⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⢀⡠⠤⠚⢦⠀⠀⠀⠀⠀⠀
		⠈⢿⡅⠀⠙⠦⠄⣰⠧⠄⢚⣿⡇⠀⠀⣿⠀⠀⠉⠁⠀⢹⠄⠀⠀⠀⠀⠀⢀⣠⠶⠊⠉⢀⡤⠂⢼⡂⠀⠀⠀⠀⠀
		⠀⠈⢧⠀⠀⠀⠀⠀⠀⠀⡸⣸⡇⠀⠀⠘⢦⣀⠀⣀⡠⠋⠀⠀⠀⠀⢀⣴⠟⠁⠀⠀⢀⠎⠀⠀⠀⠙⢦⡀⠀⡀⠀
		⠀⠀⠀⠳⢄⡀⠀⠀⣀⣰⡇⡇⡇⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⢠⡿⠁⠀⠀⠀⠀⣎⠀⠀⠀⠀⠀⠀⠹⣭⠋⠀
		⠀⠀⠀⠀⠀⠈⠉⠉⠀⢰⣿⠀⡇⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⣾⠁⢸⡉⢳⡲⣼⠉⡇⠀⠀⠀⠀⠀⠀⠘⣦⣄
		⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠀⢠⠀⠀⠀⠀⠀⠇⠀⠀⠀⠀⠀⠀⢻⡄⢾⣳⡀⣻⠁⢇⡰⠀⠀⠀⠀⠀⠀⠀⢹⡅
		⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⡄⣾⣦⣤⣀⠀⠀⠸⠀⠀⠀⠀⠀⠀⠈⣷⡄⠀⠉⠁⠀⠀⡇⠀⢀⡄⠀⠀⠀⠀⠀⣇
		⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠿⡄⠈⠉⠛⠻⣦⣤⡾⠿⠯⠿⠟⠛⠛⠙⢦⣀⠀⠀⢸⠀⠀⢸⣀⡀⠀⠀⠀⠀⢸
		⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⠦⣀⣀⠀⠈⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢉⡹⡞⢇⣀⣸⠋⠀⢀⡴⠁⢠⠏
		⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠧⠄⠀⠉⠉⠉⠉⠐⠲⢄⡀⠀⣀⡠⠴⠒⠁⠀⡇⠀⠈⠑⠶⣈⣁⠤⠒⠁⠀
		⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡞⠀⠀⠀⠀⠀⠀⠀⠀⢀⡇⢠⠋⠉⠉⠁⠀⠀⠀⠀⢹⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
		⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠁⠒⠒⠒⠒⠒⠒⠈⠉⠀⠈⠓⠒⠀⠀⠒⠒⠒⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
				""" 	
		print(text)			




	def	dice(self):
		dice_list = ['A','B','C','D','E','F']
		first = random.choice(dice_list)
		second = random.choice(dice_list)
		print(f' you got {first, second}')

if __name__ == '__main__':
	QQ = PongsuraQQ()
	QQ.show_name()
	QQ.show_youtube()
	QQ.about()
	QQ.show_art()
	QQ.dice()
