import customtkinter as ctk
import modules.app as appa
import modules.button_functions as btn_func
from PIL import Image

verify_registration_btn = ctk.CTkButton(
    master = appa.main_app.REGISTRATION_FRAME, 
    text = "Підтвердити",
    width = 200, 
    height = 50, 
    corner_radius = 20, 
    border_width = 3, 
    border_color = "#911CEE",
    command = btn_func.verify_registration, 
    font = ctk.CTkFont("Arial", 30),
    fg_color = "#343638",
    hover_color = "#29292a"
)

verify_authorization_btn = ctk.CTkButton(
    master = appa.main_app.AUTHORIZATION_FRAME, 
    text = "Підтвердити",
    width = 250, 
    height = 100, 
    corner_radius = 20, 
    border_width = 3, 
    command = btn_func.verify_authorization, 
    font = ctk.CTkFont("Arial", 30),
    border_color = "#911CEE",
    fg_color = "#343638",
    hover_color = "#29292a"
)

auth_btn = ctk.CTkButton(
    master = appa.main_app.REGISTRATION_FRAME, 
    text = "Авторизуватися",
    width = 200, 
    height = 50, 
    corner_radius = 20, 
    border_width = 3, 
    command = btn_func.auth_tab, 
    font = ctk.CTkFont("Arial", 24),
    border_color = "#911CEE",
    fg_color = "#343638",
    hover_color = "#29292a"
)

reg_btn = ctk.CTkButton(
    master = appa.main_app.AUTHORIZATION_FRAME, 
    text = "Зареєструватися",
    width = 250, 
    height = 100, 
    corner_radius = 20, 
    border_width = 3, 
    command = btn_func.register_tab, 
    font = ctk.CTkFont("Arial", 25),
    border_color = "#911CEE",
    fg_color = "#343638",
    hover_color = "#29292a"
)

bg_color_btn = ctk.CTkButton(
    master = appa.main_app.APP_FRAME,
    text = "Оберiть колiр фону",
    width = 480,
    height = 70,
    corner_radius = 20,
    border_width = 3,
    border_color = "#911CEE",
    fg_color = "#343638",
    hover_color = "#29292a",
    image = ctk.CTkImage(light_image = Image.open("+.png"), size = (10, 10)),
    compound = "right",
    command = btn_func.bg_color
)

img_color_btn = ctk.CTkButton(
    master = appa.main_app.APP_FRAME,
    text = "Оберiть колiр зображення",
    width = 480,
    height = 70,
    corner_radius = 20,
    border_width = 3,
    border_color = "#911CEE",
    fg_color = "#343638",
    hover_color = "#29292a",
    image = ctk.CTkImage(light_image = Image.open("+.png"), size = (10, 10)),
    compound = "right",
    command=btn_func.image_color
)

logo_qr_code_btn = ctk.CTkButton(
    master = appa.main_app.APP_FRAME,
    text = "Додати логотип до QR коду",
    width = 480,
    height = 70,
    corner_radius = 20,
    border_width = 3,
    border_color = "#911CEE",
    fg_color = "#343638",
    hover_color = "#29292a",
    image = ctk.CTkImage(light_image = Image.open("+.png"), size = (10, 10)),
    compound = "right",
    command = btn_func.logo
)
#
design_img_qr_code_btn = ctk.CTkButton(
    master = appa.main_app.APP_FRAME,
    text = "Оберіть дизайн зображення QR коду",
    width = 480,
    height = 70,
    corner_radius = 20,
    border_width = 3,
    border_color = "#911CEE",
    fg_color = "#343638",
    hover_color = "#29292a",
    image = ctk.CTkImage(light_image = Image.open("+.png"), size = (10, 10)),
    compound = "right",
    command=btn_func.design
)

qr_code_btn = ctk.CTkButton(
    master = appa.main_app.APP_FRAME,
    text = "Створити QR код",
    width = 480,
    height = 70,
    corner_radius = 20,
    border_width = 3,
    border_color = "#911CEE",
    fg_color = "#343638",
    hover_color = "#29292a",
    command = btn_func.make_qrcode
)

history_btn = ctk.CTkButton(
    master = appa.main_app.APP_FRAME,
    text = "Історія",
    width = 280,
    height = 70,
    corner_radius = 20,
    border_width = 3,
    border_color = "#911CEE",
    fg_color = "#343638",
    hover_color = "#29292a",
    command = btn_func.history
)

back_btn = ctk.CTkButton(
    master = appa.main_app.HISTORY_FRAME,
    text = "Назад",
    width = 280,
    height = 70,
    corner_radius = 20,
    border_width = 3,
    border_color = "#911CEE",
    fg_color = "#343638",
    hover_color = "#29292a",
    command = btn_func.back
)

avatar_btn = ctk.CTkButton(
    master = appa.main_app.APP_FRAME,
    text = "Аватар",
    width = 80,
    height = 50,
    corner_radius = 20,
    border_width = 3,
    border_color = "#911CEE",
    fg_color = "#343638",
    hover_color = "#29292a",
    command = btn_func.avatar
    )

verify_registration_btn.place(x = 440, y = 540)
verify_authorization_btn.place(x = 430, y = 490)
auth_btn.place(x = 440, y = 600)
reg_btn.place(x = 430, y = 600)
bg_color_btn.place(x = 20, y = 170)
img_color_btn.place(x = 20, y = 280)
logo_qr_code_btn.place(x = 20, y = 390)
design_img_qr_code_btn.place(x = 20, y = 500)
qr_code_btn.place(x = 20, y = 610)
history_btn.place(x = 700, y = 610)
back_btn.place(x = 400, y = 50)
avatar_btn.place(x = 780, y = 20)