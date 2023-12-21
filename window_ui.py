#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-
'''Clase dedicada al manejo de ventanas'''

from cgitb import text
from ctypes import sizeof
from multiprocessing.sharedctypes import Value
from optparse import Values
import socket
import threading
import sys
from tkinter import ttk
import tkinter
from tkinter.ttk import Combobox
from turtle import position, width

from click import command, style
import pygame
from bot import Bot
from tkinter import *
from tkinter import messagebox
from graphic_rep import Graphic_game
from protocol import *
from piece import WHITE_PIECE, BLACK_PIECE


GAME_SERVER_END = ('',9999)
PASSWORD = "*******************"


def get_game_list_from_socket_repr(game_socket_repr):
    '''Dado la representación de un socket devuelve la lista de partidas'''
    code = game_socket_repr[IDENTIFIER_BEGIN : IDENTIFIER_END]
    game_socket_repr = game_socket_repr[IDENTIFIER_END : ]
    if code == REPLY_GAME_LIST:
        game_list = game_socket_repr.split(PROTOCOL_SEPARATOR)
        return game_list[:-1]
    else:
        return [] # Error in reply


class login_ui(object):
    '''Clase dedicada a la ventana de login'''

    def __init__(self):
        self.login_window = None
        self.user_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


    def run(self):
        '''Crea la ventana de login'''

        self.login_window = Tk()
        self.login_window.title('Login')
        self.login_window.configure(width = 300, height = 270)
        self.login_window.configure(bg = '#fecc9c')
        self.login_window.eval('tk::PlaceWindow . center')
        self.login_window.resizable(False, False)

        s = ttk.Style()
        s.configure("MyButton.TButton", background="#fecc9c")

        deco0lbl = Label(self.login_window, text = "", background = "#8e5637")
        deco0lbl.place_configure(x = 5, y = 0, width = 5, height = 163, anchor = "n")

        deco1lbl = Label(self.login_window, text = "", background = "#8e5637")
        deco1lbl.place_configure(x = 5, y = 60, width = 20, height = 5, anchor = "w")

        deco2lbl = Label(self.login_window, text = "", background = "#8e5637")
        deco2lbl.place_configure(x = 5, y = 110, width = 20, height = 5, anchor = "w")

        deco3lbl = Label(self.login_window, text = "", background = "#8e5637")
        deco3lbl.place_configure(x = 5, y = 160, width = 20, height = 5, anchor = "w")

        deco4lbl = Label(self.login_window, text = "", background = "#8e5637")
        deco4lbl.place_configure(x = 75, y = 225, width = 5, height = 75, anchor = "n")

        deco5lbl = Label(self.login_window, text = "", background = "#8e5637")
        deco5lbl.place_configure(x = 225, y = 225, width = 5, height = 75, anchor = "n")

        deco6lbl = Label(self.login_window, text = "", background = "#8e5637")
        deco6lbl.place_configure(x = 150, y = 225, width = 150, height = 5, anchor = "center")

        deco7lbl = Label(self.login_window, text = "", background = "#8e5637")
        deco7lbl.place_configure(x = 125, y = 0, width = 5, height = 160, anchor = "n")

        deco8lbl = Label(self.login_window, text = "", background = "#8e5637")
        deco8lbl.place_configure(x = 280, y = 0, width = 5, height = 160, anchor = "n")


        emailTB = Entry(self.login_window)
        emailTB.place(x=120, y=50)

        emailLB = Label(self.login_window,text="E-Mail:", background = "#fecc9c")
        emailLB.place(x=20, y=50)

        usernameTB = Entry(self.login_window)
        usernameTB.place(x=120, y=100)

        usernameLB = Label(self.login_window,text="Usuario:", background = "#fecc9c")
        usernameLB.place(x=20, y=100)

        passwordTB = Entry(self.login_window, show="*")
        passwordTB.place(x=120, y=150)

        passwordLB = Label(self.login_window,text="Contraseña:", background = "#fecc9c")
        passwordLB.place(x=20, y=150)

        registerBT = ttk.Button(self.login_window, text="Registrarse", command=lambda: self.registerButton(), style = "MyButton.TButton")
        registerBT.place(x=75, y=225, width = 100, height = 25, anchor = "center")

        loginBT = ttk.Button(self.login_window, text="Iniciar sesión", command=lambda: self.loginButton(usernameTB.get(), passwordTB.get(), emailTB.get()), style = "MyButton.TButton")
        loginBT.place(x=225, y=225, width = 100, height = 25, anchor = "center")
        self.login_window.mainloop()


    def registerButton(self):
        self.login_window.destroy()
        init_forms_window = forms_ui(self.user_socket)
        init_forms_window.run()


    def loginButton(self, username, password, email):
        if(username == '' or password == '' or email == ''):
            messagebox.showwarning(title="Credenciales incorrectas", message="Rellene todos los campos.")
            return

        self.user_socket.sendto((REQUEST_LOGIN + username + '-' + password + '-' + email).encode(), GAME_SERVER_END)
        result, server = self.user_socket.recvfrom(1024)
        code = result.decode()
        if(code==REPLY_LOGIN):
            self.login_window.destroy()
            init_main_window = main_window_ui(username, password, email, self.user_socket)
            init_main_window.run()
        elif(code==ERROR_LOGIN):
            messagebox.showwarning(title="Credenciales incorrectas", message="Las credenciales son incorrectas.")
        else:
            raise Exception()


class forms_ui(object):
    '''Clase dedicada al formulario de registro'''
    
    def __init__(self, user_socket):
        self.forms_window = None
        self.user_socket = user_socket


    def run(self):
        self.forms_window = Tk()
        self.forms_window.title('Registrar usuario')
        self.forms_window.configure(width = 300, height = 220)
        self.forms_window.configure(bg = '#fecc9c')
        self.forms_window.eval('tk::PlaceWindow . center')
        self.forms_window.resizable(False, False)

        s = ttk.Style()
        s.configure("MyButton.TButton", background="#fecc9c")

        deco0lbl = Label(self.forms_window, text = "", background = "#8e5637")
        deco0lbl.place_configure(x = 300/2, y = 200, width = 300, height = 5, anchor = "center")

        deco1lbl = Label(self.forms_window, text = "", background = "#8e5637")
        deco1lbl.place_configure(x = 35, y = 0, width = 5, height = 15, anchor = "n")

        emailTB = Entry(self.forms_window)
        emailTB.place(x=120, y=50)

        emailLB = Label(self.forms_window,text="E-Mail:", background = "#fecc9c")
        emailLB.place(x=20, y=50)

        userTB = Entry(self.forms_window)
        userTB.place(x=120, y=100)

        userLB = Label(self.forms_window,text="Username:", background = "#fecc9c")
        userLB.place(x=20, y=100)

        passwordTB = Entry(self.forms_window, show="*")
        passwordTB.place(x=120, y=150)

        passwordLB = Label(self.forms_window,text="Password:", background = "#fecc9c")
        passwordLB.place(x=20, y=150)

        createUserBT = ttk.Button(self.forms_window, text="Crear nuevo usuario", command=lambda: self.createUserButton(emailTB.get(), userTB.get(), passwordTB.get()), style = "MyButton.TButton")
        createUserBT.place(x=300/2, y=200, anchor = "center")

        backBT = ttk.Button(self.forms_window, text="Atrás", command=lambda: self.backButton(), style = "MyButton.TButton")
        backBT.place(x=35, y=22.5, width = 50, height = 25, anchor = "center")
        self.forms_window.mainloop()


    def createUserButton(self, email, username, password):
        if(username == '' or password == '' or email == ''):
            messagebox.showwarning(title="Credenciales incorrectas", message="Rellene todos los campos.")
            return
        
        self.user_socket.sendto((REQUEST_ADD_USER + username + '-' + password + '-' + email).encode(), GAME_SERVER_END)
        result, server = self.user_socket.recvfrom(1024)
        code = result.decode()
        if(code==REPLY_ADD_USER):
            self.forms_window.destroy()
            init_main_window = main_window_ui(username, password, email, self.user_socket)
            init_main_window.run()
        elif(code==ERROR_ADDING_USER):
            messagebox.showwarning(title="Error registro", message="Ha ocurrido un error creando el usuario.")
        else:
            raise Exception()
        

    def backButton(self):
        self.forms_window.destroy()
        init_login_window = login_ui()
        init_login_window.run()


class main_window_ui(object):
    '''Clase para gestionar el menú principal'''

    def __init__(self, username, password, email, user_socket):
        self.main_window = None
        self.email = email
        self.username = username
        self.password = password
        self.user_socket = user_socket


    def run(self):
        ancho = 350
        alto = 240

        self.main_window = Tk()
        self.main_window.title('Menú principal')
        self.main_window.configure(width = ancho, height = alto)
        #self.main_window.configure(bg = 'lightgray')
        #   #fecc9c
        self.main_window.configure(bg = '#fecc9c')
        self.main_window.eval('tk::PlaceWindow . center')
        self.main_window.resizable(False, False)

        s = ttk.Style()
        s.configure("MyButton.TButton", background="#fecc9c")

        deco0lbl = Label(self.main_window, text = "", background = "#8e5637")
        deco0lbl.place_configure(x = 270, y = 0, width = 5, height = 20)

        deco1lbl = Label(self.main_window, text = "", background = "#8e5637")
        deco1lbl.place_configure(x = ancho/2, y = alto/2, width = ancho, height = 5, anchor = "center")

        deco2lbl = Label(self.main_window, text = "", background = "#8e5637")
        deco2lbl.place_configure(x = ancho/2, y = alto*3/4, width = ancho, height = 5, anchor = "center")

        deco3lbl = Label(self.main_window, text = "", background = "#8e5637")
        deco3lbl.place_configure(x = ancho*1/4, y = alto/2, width = 5, height = alto/2, anchor = "n")

        deco4lbl = Label(self.main_window, text = "", background = "#8e5637")
        deco4lbl.place_configure(x = ancho*3/4, y = alto/2, width = 5, height = alto/2, anchor = "n")

        gestionarCuentaBT = ttk.Button(self.main_window, text="Gestionar cuenta", comman=lambda: self.gestionarCuentaButton(), style = "MyButton.TButton")
        gestionarCuentaBT.place_configure(x = 200, y = 10, width = 140, height = 25)

        createGameBT = ttk.Button(self.main_window, text="Crear partida", comman=lambda: self.createGameButton(), style = "MyButton.TButton")
        createGameBT.place_configure(x = ancho*1/4, y = alto/2, width = 140, height = 25, anchor = "center")

        joinGameBT = ttk.Button(self.main_window, text="Buscar partida", comman=lambda: self.joinGameButton(), style = "MyButton.TButton")
        joinGameBT.place_configure(x = ancho*3/4, y = alto/2, width = 140, height = 25, anchor = "center")

        singlePlayerBT = ttk.Button(self.main_window, text="Jugador Vs. Bot", comman=lambda: self.singlePlayerButton(), style = "MyButton.TButton")
        singlePlayerBT.place_configure(x = ancho*1/4, y = alto*3/4, width = 140, height = 25, anchor = "center")

        spectateBT = ttk.Button(self.main_window, text="Bot Vs. Bot", comman=lambda: self.spectateButton(), style = "MyButton.TButton")
        spectateBT.place_configure(x = ancho*3/4, y = alto*3/4, width = 140, height = 25, anchor = "center")



    def createGameButton(self):
        self.user_socket.sendto((REQUEST_ADD_GAME + 'Partida de ' + self.username + PROTOCOL_SEPARATOR + \
            self.username).encode(), GAME_SERVER_END)
        result, server = self.user_socket.recvfrom(1024)
        code = result.decode()

        if(code == REPLY_ADD_GAME):
            self.main_window.withdraw()
            game = Graphic_game(self.user_socket, WHITE_PIECE)
            game.run()
            self.main_window.deiconify()

        elif(code == ERROR_ADDING_GAME):
            messagebox.showwarning(title="Error", message="No se ha podido crear una partida.")

        else:
            raise Exception()


    def joinGameButton(self):
        self.main_window.destroy()
        init_lobby_window = lobby_ui(self.username, self.password, self.email, self.user_socket)
        init_lobby_window.run()


    def singlePlayerButton(self):
        '''Genera una partida contra un bot'''
        self.main_window.withdraw()

        self.user_socket.sendto((REQUEST_ADD_GAME + 'Partida1' + PROTOCOL_SEPARATOR + \
            self.username).encode(), GAME_SERVER_END)
        result, server = self.user_socket.recvfrom(1024)
        code = result.decode()

        if(code == REPLY_ADD_GAME):
            bot_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            bot_socket.sendto((REQUEST_ADD_PLAYER_TO_GAME + \
                'Partida1' + PROTOCOL_SEPARATOR + 'BOT1').encode(),GAME_SERVER_END)
            result, server = bot_socket.recvfrom(1024)

            game_player = Graphic_game(self.user_socket,
                WHITE_PIECE, vs_bot=True)
            thr = threading.Thread(target=game_player.run, args=tuple())
            thr.start()

            game_bot = Bot(BLACK_PIECE, bot_socket)
            game_bot.run()
            thr.join()

        elif(code == ERROR_ADDING_GAME):
            messagebox.showwarning(title="Error", message="No se ha podido crear una partida.")

        else:
            raise Exception()

        self.main_window.deiconify()


    def spectateButton(self):
        '''Genera una partida entre bots'''
        self.main_window.withdraw()

        bot1_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        bot1_socket.sendto((REQUEST_ADD_GAME + 'Partida1' + PROTOCOL_SEPARATOR + \
            'BOT1').encode(), GAME_SERVER_END)
        result, server = bot1_socket.recvfrom(1024)
        code = result.decode()
        if(code == REPLY_ADD_GAME):
            bot2_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            bot2_socket.sendto((REQUEST_ADD_PLAYER_TO_GAME + \
                'Partida1' + PROTOCOL_SEPARATOR + 'BOT2').encode(),GAME_SERVER_END)
            result, server = bot2_socket.recvfrom(1024)
            code = result.decode()

            if(code == REPLY_ADD_PLAYER_TO_GAME):
                game_player = Graphic_game(bot1_socket,
                    WHITE_PIECE, bot=True, vs_bot=True)
                thr = threading.Thread(target=game_player.run, args=tuple())
                thr.start()

                game_bot = Bot(BLACK_PIECE, bot2_socket)
                game_bot.run()
                thr.join()

            elif(code == ERROR_ADDING_PLAYER_TO_GAME):
                messagebox.showwarning(title="Error", message="No se ha podido crear una partida.")

            else:
                raise Exception()
        elif(code == ERROR_ADDING_GAME):
            messagebox.showwarning(title="Error", message="No se ha podido crear una partida.")

        else:
            raise Exception()
        
        self.main_window.deiconify()


    def gestionarCuentaButton(self):
        self.main_window.destroy()
        init_gestion_window = gestion_cuenta_ui(self.email, self.username, self.password, self.user_socket)
        init_gestion_window.run()


class gestion_cuenta_ui(object):
    '''Clase dedicada a la ventana de gestion de usuario'''

    def __init__(self, email, username, password, user_socket):
        self.gestion_window = None
        self.email = email
        self.username = username
        self.password = password
        self.user_socket = user_socket

        self.userPass = None

    
    def run(self):
        ancho = 400
        alto = 245

        self.gestion_window = Tk()
        self.gestion_window.title('Gestionar cuenta')
        self.gestion_window.configure(width=ancho, height=alto)
        self.gestion_window.configure(bg = '#fecc9c')
        self.gestion_window.eval('tk::PlaceWindow . center')
        self.gestion_window.resizable(False, False)

        s = ttk.Style()
        s.configure("MyButton.TButton", background="#fecc9c")

        s2 = ttk.Style()
        s2.configure("MyLabel.TLabel", background="#fecc9c")

        for xyz in range(alto):
            if xyz==alto-(alto-17) or xyz==50 or xyz==80 or xyz==110 or xyz==230:
                labellabel = Label(self.gestion_window, text = "", background = "#8e5637")
                labellabel.place_configure(x = ancho/2, y = xyz, width = 400, height = 5, anchor = "center")
        
        selec = Combobox(values=["Cambiar contraseña, Cambiar username"])

        password1_Lbl = ttk.Label(self.gestion_window, text="Introduzca su contraseña:", style="MyLabel.TLabel")
        password1_Lbl.place_forget()
        
        password1_Entry = Entry(self.gestion_window, show="*")
        password1_Entry.place_forget()

        password2_Lbl = ttk.Label(self.gestion_window, text="Repita su contraseña:", style="MyLabel.TLabel")
        password2_Lbl.place_forget()

        password2_Entry = Entry(self.gestion_window, show="*")
        password2_Entry.place_forget()

        nickAux_Lbl = ttk.Label(self.gestion_window, text="Introduzca nuevo username:", style="MyLabel.TLabel")
        nickAux_Lbl.place_forget()

        newNick_Entry = Entry(self.gestion_window, show="")
        newNick_Entry.place_forget()

        password_Lbl = ttk.Label(self.gestion_window, text="Introduzca nueva contraseña:", style="MyLabel.TLabel")
        password_Lbl.place_forget()

        newPassword_Entry = Entry(self.gestion_window, show="*")
        newPassword_Entry.place_forget()

        change_Button = ttk.Button(self.gestion_window, text="Cambiar", style="MyButton.TButton", command = lambda : self.changeBtn(self.password, password1_Entry.get(), password2_Entry.get(), selec.get(), newNick_Entry.get(), newPassword_Entry.get()))
        change_Button.place_forget()

        hidens = [password1_Lbl, password1_Entry, password2_Lbl, password2_Entry, nickAux_Lbl, password_Lbl, newNick_Entry, newPassword_Entry, change_Button]


        lblDeco0 = Label(self.gestion_window, text = "", background = "#fecc9c")
        lblDeco0.place_configure(x = ancho/2, y = 50, width = 150, height =25, anchor = "center")

        lblDeco1 = Label(self.gestion_window, text = "", background = "#fecc9c")
        lblDeco1.place_configure(x = ancho*1/4, y = 110, width = 150, height =25, anchor = "center")

        lblDeco2 = Label(self.gestion_window, text = "", background = "#fecc9c")
        lblDeco2.place_configure(x = ancho*1/4, y = 80, width = 150, height =25, anchor = "center")

        back_Button = ttk.Button(self.gestion_window, text="Atrás", style="MyButton.TButton", command= self.open_back)
        back_Button.place_configure(x = ancho-(ancho-5), y = alto-(alto-5), width = 65, height = 25)

        email_Lbl = ttk.Label(self.gestion_window, text = self.email, style = "MyLabel.TLabel")
        email_Lbl.place(x = ancho/2, y = 50, height = 25, anchor = "center")

        nickLbl = ttk.Label(self.gestion_window, text=self.username, style="MyLabel.TLabel")
        nickLbl.place(x = ancho*1/4, y = 80, anchor="center")

        changeNick_button = ttk.Button(self.gestion_window, text="Cambiar username", style="MyButton.TButton", command=lambda : self.changeNickBtn(hidens, ancho, alto, selec))
        changeNick_button.place_configure(x = ancho*3/4, y = 80, width = 150, height = 25, anchor="center")

        password_Lbl = ttk.Label(self.gestion_window, text=PASSWORD[0:len(self.password)], style="MyLabel.TLabel")
        password_Lbl.place(x = ancho*1/4, y = 110, anchor="center")

        changePassword_button = ttk.Button(self.gestion_window, text="Cambiar contraseña", style="MyButton.TButton", command = lambda : self.changePasswordBtn(hidens, ancho, alto, selec))
        changePassword_button.place_configure(x = ancho*3/4, y = 110, width = 150, height = 25, anchor="center")


    def open_back(self):

        main_window = main_window_ui(self.username, self.password, self.email, self.user_socket)
        self.gestion_window.destroy()
        main_window.run()


    def changeNickBtn(self, Objects, ancho, alto, selec):
        selec.set("Cambiar username")
        Objects[0].place_configure(x = ancho*1/4, y = 140, anchor="center")
        Objects[1].place_configure(x = ancho*3/4, y = 140, anchor="center")
        Objects[2].place_configure(x = ancho*1/4, y = 170, anchor="center")
        Objects[3].place_configure(x = ancho*3/4, y = 170, anchor="center")
        Objects[4].place_configure(x = ancho*1/4, y = 200, anchor="center")
        Objects[5].place_forget()
        Objects[6].place_configure(x = ancho*3/4, y = 200, anchor="center")
        Objects[7].place_forget()
        Objects[8].place_configure(x = ancho/2, y = 230, width = 60, height = 25, anchor="center")


    def changePasswordBtn(self, Objects, ancho, alto, selec):
        selec.set("Cambiar contraseña")
        Objects[0].place_configure(x = ancho*1/4, y = 140, anchor="center")
        Objects[1].place_configure(x = ancho*3/4, y = 140, anchor="center")
        Objects[2].place_configure(x = ancho*1/4, y = 170, anchor="center")
        Objects[3].place_configure(x = ancho*3/4, y = 170, anchor="center")
        Objects[4].place_forget()
        Objects[5].place_configure(x = ancho*1/4, y = 200, anchor="center")
        Objects[6].place_forget()
        Objects[7].place_configure(x = ancho*3/4, y = 200, anchor="center")
        Objects[8].place_configure(x = ancho/2, y = 230, width = 60, height = 25, anchor="center")


    def changeBtn(self, p0, p1, p2, selec, newNick, newPassword):
        if p1==p2 and p1!="" and p2!="":

            if p0==p1 and selec=="Cambiar username":

                self.user_socket.sendto((REQUEST_UPDATE_USER + newNick + '-' + self.password + '-' + self.email).encode(), GAME_SERVER_END)
                result, server = self.user_socket.recvfrom(1024)
                code = result.decode()

                if (code == REPLY_UPDATE_USER):
                    messagebox.showwarning(title="Hecho", message="El nombre de usuario ha sido cambiado.")

                    self.gestion_window.destroy()
                    init_main_window = main_window_ui(newNick, self.password, self.email, self.user_socket)
                    init_main_window.run()
                
                elif (code == ERROR_UPDATING_USER):
                    messagebox.showwarning(title="Error", message="No se ha podido cambiar el nombre de usuario.")

                else:
                    raise Exception()

            elif p0==p1 and selec=="Cambiar contraseña":

                self.user_socket.sendto((REQUEST_UPDATE_USER + self.username + '-' + newPassword + '-' + self.email).encode(), GAME_SERVER_END)
                result, server = self.user_socket.recvfrom(1024)
                code = result.decode()

                if (code == REPLY_UPDATE_USER):
                    messagebox.showwarning(title="Hecho", message="La contraseña ha sido cambiada.")

                    self.gestion_window.destroy()
                    init_main_window = main_window_ui(self.username, newPassword, self.email, self.user_socket)
                    init_main_window.run()
                
                elif (code == ERROR_UPDATING_USER):
                    messagebox.showwarning(title="Error", message="No se ha podido cambiar la contraseña.")

                else:
                    raise Exception()

        elif p1=="" or p2=="":
            messagebox.showwarning(title="Contraseña en blanco", message="Rellene ambas contraseñas.")
            
        else:
            messagebox.showwarning(title="Contraseñas distintas", message="Las constraseñas deben ser iguales.")


class lobby_ui(object):
    '''Clase dedicada a la ventana de lobbies'''

    def __init__(self, username, password, email, user_socket):
        self.lobby_window = None
        self.user_socket = user_socket
        self.listbox = None
        self.username = username
        self.password = password
        self.email = email


    def run(self):
        '''Crea la ventana de lobbies'''
        self.lobby_window = Tk()
        self.lobby_window.title('Lobbies')
        self.lobby_window.configure(width = 550, height = 720)
        self.lobby_window.configure(bg = '#fecc9c')
        self.lobby_window.eval('tk::PlaceWindow . center')
        self.lobby_window.resizable(False, False)

        s = ttk.Style()
        s.configure("MyButton.TButton", background="#fecc9c")

        deco0lbl = Label(self.lobby_window, text = "", background = "#8e5637")
        deco0lbl.place_configure(x = 1080/2, y = 650, width = 1080, height = 5, anchor = "center")

        deco1lbl = Label(self.lobby_window, text = "", background = "#8e5637")
        deco1lbl.place_configure(x = 100, y = 720/2, width = 5, height = 720, anchor = "center")

        deco2lbl = Label(self.lobby_window, text = "", background = "#8e5637")
        deco2lbl.place_configure(x = 450, y = 720/2, width = 5, height = 720, anchor = "center")

        refresh_button = ttk.Button(text = 'Refrescar', command = self.get_games, style = "MyButton.TButton")
        refresh_button.place_configure(x = 100, y = 650, width = 150, height = 100, anchor = "center")

        back_button = ttk.Button(text = 'Atŕas', command = self.open_back, style = "MyButton.TButton")
        back_button.place_configure(x = 275, y = 650, width = 150, height = 100, anchor = "center")

        join_button = ttk.Button(text = 'Unirse', command = self.join_game, style = "MyButton.TButton")
        join_button.place_configure(x = 450, y = 650, width = 150, height = 100, anchor = "center")

        self.listbox = Listbox()
        self.listbox.place_configure(x = 25, y = 30, width = 500, height = 530)

        self.get_games()
        self.lobby_window.mainloop()


    def get_games(self):
        '''Devuelve la lista de partidas'''
        self.user_socket.sendto(REQUEST_GAME_LIST.encode(), GAME_SERVER_END)
        result, server = self.user_socket.recvfrom(1024)
        game_list = get_game_list_from_socket_repr(result.decode())

        self.listbox.delete(0,END)

        for position in range(0,len(game_list)):
            self.listbox.insert(position, str(game_list[position]))

        for i in range(self.listbox.size()):
            if i % 2 == 1:
                self.listbox.itemconfigure(i, bg="#dddddd")


    def open_back(self):
        '''Crea y abre la ventana principal'''

        self.lobby_window.destroy()
        init_main_window = main_window_ui(self.username, self.password, self.email, self.user_socket)
        init_main_window.run()

    def join_game(self):
        '''Se une a una partida'''
        items = self.listbox.curselection()
        if len(items) != 1:
            messagebox.showwarning(title="Selecciona partida", message="Seleccione una partida válida.")
            return
        else:
            nombre_partida = self.listbox.get(items)

        self.user_socket.sendto((REQUEST_ADD_PLAYER_TO_GAME + \
            nombre_partida + PROTOCOL_SEPARATOR + self.username).encode(),GAME_SERVER_END)
        result, server = self.user_socket.recvfrom(1024)
        code = result.decode()
        if(code == REPLY_ADD_PLAYER_TO_GAME):
            self.lobby_window.withdraw()
            game = Graphic_game(self.user_socket, BLACK_PIECE)
            game.run()
            self.lobby_window.destroy()
            init_main_window = main_window_ui(self.username, self.password, self.email, self.user_socket)
            init_main_window.run()
        elif(code == ERROR_ADDING_PLAYER_TO_GAME):
            messagebox.showwarning(title="Error al unirse a la partida", message="Ha ocurrido un error al unirse a la partida.")

init_login_window = login_ui()
init_login_window.run()