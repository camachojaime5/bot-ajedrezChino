''' Module that implements the user entity '''

from tkinter import *

''' Main window creation '''

window = Tk()
window.title('Chinese Chess App')
window.configure(width = 1080, height = 720)
window.configure(bg = 'lightgray')
window.eval('tk::PlaceWindow . center')
window.resizable(False, False)

''' Game listbox '''

game_listbox = Listbox()
game_listbox.place_configure(x = 290, y = 200, width = 500)


''' Main window buttons '''

play_button = Button(text = 'Play!')
play_button.place_configure(x = 500, y = 500)

window.mainloop()