import customtkinter as ctk
import sqlite3 
import tkinter as tk
from PIL import Image


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("TriangleMonkey")
        self.geometry("1080x720+0+0")
        self.resizable(False, False)
        self.DATABASE_CONNECTION = sqlite3.connect("database.db")
        self.CURSOR = self.DATABASE_CONNECTION.cursor()
        self.USERS = '''
            CREATE TABLE IF NOT EXISTS Users (id integer PRIMARY KEY, username TEXT, password TEXT, email TEXT)
        '''
        self.iconbitmap("icon.ico")
        

        self.CURSOR.execute(self.USERS)
        self.REGISTRATION_FRAME = ctk.CTkFrame(master = self, width = 1070, height = 710, corner_radius = 20, border_width = 3, border_color = "#911CEE")
        # self.REGISTRATION_FRAME.place(x = 5, y = 5)
        self.REGISTRATION_FRAME.place(x = 5, y = 5)
        
        self.REGISTRATION_LABEL = ctk.CTkLabel(master = self.REGISTRATION_FRAME, text = "Реєстрація", font = ctk.CTkFont(family = "Arial", size = 30))
        self.REGISTRATION_LABEL.place(x = 475, y = 10)

        self.ENTRY_LOGIN = ctk.CTkEntry(master = self.REGISTRATION_FRAME, width = 500, height = 75, textvariable = ctk.StringVar(), border_color = "#911CEE", font = ctk.CTkFont("Arial", 30))
        self.ENTRY_EMAIL = ctk.CTkEntry(master = self.REGISTRATION_FRAME, width = 500, height = 75, textvariable = ctk.StringVar(), border_color = "#911CEE", font = ctk.CTkFont("Arial", 30))
        self.ENTRY_PASSWORD = ctk.CTkEntry(master = self.REGISTRATION_FRAME, width = 500, height = 75, textvariable = ctk.StringVar(), border_color = "#911CEE", font = ctk.CTkFont("Arial", 30))
        self.ENTRY_REPEAT = ctk.CTkEntry(master = self.REGISTRATION_FRAME, width = 500, height = 75, textvariable = ctk.StringVar(), border_color = "#911CEE", font = ctk.CTkFont("Arial", 30))

        self.ENTRY_LOGIN.place(x = 300, y = 80)
        self.ENTRY_EMAIL.place(x = 300, y = 190)
        self.ENTRY_PASSWORD.place(x = 300, y = 300)
        self.ENTRY_REPEAT.place(x = 300, y = 410)
        


        self.AUTHORIZATION_FRAME = ctk.CTkFrame(master = self, width = 1070, height = 710, corner_radius = 20, border_width = 3, border_color = "#911CEE")
        
        self.ENTRY_USERNAME_AUTH = ctk.CTkEntry(master = self.AUTHORIZATION_FRAME, width = 500, height = 100, textvariable = ctk.StringVar(), border_color = "#911CEE", font = ctk.CTkFont("Arial", 30))
        self.ENTRY_PASSWORD_AUTH = ctk.CTkEntry(master = self.AUTHORIZATION_FRAME, width = 500, height = 100, textvariable = ctk.StringVar(), border_color = "#911CEE", font = ctk.CTkFont("Arial", 30))
        
        self.AUTHORIZAION_LABEL = ctk.CTkLabel(master = self.AUTHORIZATION_FRAME, text = "Авторизацiя", font = ctk.CTkFont(family = "Arial", size = 30))
        self.AUTHORIZAION_LABEL.place(x = 470, y = 10)

        self.ENTRY_USERNAME_AUTH.place(x = 300, y = 160)
        self.ENTRY_PASSWORD_AUTH.place(x = 300, y = 310)

        # self.AUTHORIZATION_FRAME.place(x = 5, y = 5)

        self.LABEL_USERNAME_AUTH = ctk.CTkLabel(master = self.AUTHORIZATION_FRAME, text = "Нікнейм:", font = ctk.CTkFont("Arial", 20))
        self.LABEL_USERNAME_AUTH.place(x = 512, y = 130)
        self.LABEL_PASSWORD_AUTH = ctk.CTkLabel(master = self.AUTHORIZATION_FRAME, text = "Пароль:", font = ctk.CTkFont("Arial", 20))
        self.LABEL_PASSWORD_AUTH.place(x = 513, y = 275)

        self.LABEL_LOGIN_REG = ctk.CTkLabel(master = self.REGISTRATION_FRAME, text = "Нiкнейм:", font = ctk.CTkFont("Arial", 20))
        self.LABEL_EMAIL_REG = ctk.CTkLabel(master = self.REGISTRATION_FRAME, text = "Пошта:", font = ctk.CTkFont("Arial", 20))
        self.LABEL_PASSWORD_REG = ctk.CTkLabel(master = self.REGISTRATION_FRAME, text = "Пароль:", font = ctk.CTkFont("Arial", 20))
        self.LABEL_REPEAT_REG = ctk.CTkLabel(master = self.REGISTRATION_FRAME, text = "Повторення паролю:", font = ctk.CTkFont("Arial", 20))

        # а никалай у нас бигимот
        self.LABEL_LOGIN_REG.place(x = 512, y = 50)
        self.LABEL_EMAIL_REG.place(x = 515, y = 160)
        self.LABEL_PASSWORD_REG.place(x = 513, y = 270)
        self.LABEL_REPEAT_REG.place(x = 460, y = 380)

        self.APP_FRAME = ctk.CTkFrame(master = self, width = 1070, height = 710, corner_radius = 20, border_width = 3, border_color = "#911CEE")
        

        self.LABEL_GEN_PROKUROR_QR_CODE = ctk.CTkLabel(master = self.APP_FRAME, text = "Генератор QR - code", font = ctk.CTkFont("Arial", 20))
        self.LABEL_GEN_PROKUROR_QR_CODE.place(x = 400, y = 10)

        self.URL_ENTRY = ctk.CTkEntry(
            master = self.APP_FRAME,
            width = 480,
            height = 70,
            corner_radius = 20,
            border_width = 3,
            border_color = "#911CEE",
            textvariable= ctk.StringVar(),
            placeholder_text = "Задайте URL"
        )
        self.URL_ENTRY.place(x = 20, y = 60)

        self.QR_CODE_FRAME = ctk.CTkFrame(master = self.APP_FRAME, width = 280, height = 280, corner_radius = 20, border_width = 3, border_color = "#911CEE")
        self.QR_CODE_FRAME.place(x = 700, y = 280)
        
        self.HISTORY_FRAME = ctk.CTkFrame(
            master = self,
            width = 1070,
            height = 710, 
            corner_radius = 20,
            border_width = 3,
            border_color = "#911CEE"
        )

        self.SCROLLABLE_FRAME = ctk.CTkScrollableFrame(
            master = self.HISTORY_FRAME,
            width = 1015, 
            height = 520,
            corner_radius = 20,
            border_width = 3
        )
        
        self.SCROLLABLE_FRAME.place(x = 10, y = 130)

        self.HISTORY_LABEL = ctk.CTkLabel(master = self.HISTORY_FRAME, text = "Історія QR-кодів", font = ctk.CTkFont("Arial", 30))
        self.HISTORY_LABEL.place(x = 420, y = 10)
        
        self.AVATAR_FRAME = ctk.CTkFrame(
            master = self.APP_FRAME, 
            width = 150, 
            height = 150, 
            corner_radius = 20,
            border_width = 3,
            border_color = "#911CEE",
            fg_color = "#343638"
        )
        self.AVATAR_FRAME.place(x = 880, y = 20)

        # self.AVATAR_IMAGE = ctk.CTkImage(light_image = Image.open(f"users/{self.ENTRY_USERNAME_AUTH._textvariable.get()}/avatar.png"))

        self.AVATAR_IMAGE = None
        self.AVATAR_LABEL = None


        # print("ексепт")

        self.IMAGE_LABEL = None
        self.BG_COLOR = (0, 0, 0)
        self.IMAGE_COLOR = (255, 255, 255)
        self.LOGO = None
        self.GRADIENT = None
        self.MODULE_DRAWER = None

main_app = App()