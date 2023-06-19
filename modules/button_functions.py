import customtkinter as ctk
import verify_email
import modules.app as app
import os
import qrcode
import ssl
import smtplib
import threading
from email.message import EmailMessage
from qrcode.image.styledpil import StyledPilImage
from PIL import Image

from qrcode.image.styles.moduledrawers import RoundedModuleDrawer, GappedSquareModuleDrawer, CircleModuleDrawer, VerticalBarsDrawer, HorizontalBarsDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask, SquareGradiantColorMask, HorizontalGradiantColorMask, VerticalGradiantColorMask, ImageColorMask

counter = 0
reg = None
email_check = False
username_check = False


def verify_registration():
    global email_check
    global username_check
    global reg

    if app.main_app.ENTRY_LOGIN._textvariable.get() and app.main_app.ENTRY_EMAIL._textvariable.get() and app.main_app.ENTRY_PASSWORD._textvariable.get() and app.main_app.ENTRY_REPEAT._textvariable.get():
        verification_email = verify_email.verify_email(app.main_app.ENTRY_EMAIL._textvariable.get())
        if verification_email == True:
            if app.main_app.ENTRY_PASSWORD._textvariable.get() == app.main_app.ENTRY_REPEAT._textvariable.get():
                username_data = app.main_app.CURSOR.execute("SELECT username FROM Users").fetchall()
                username_check = False
                email_check = False
                print(username_data)
                for client in username_data:
                    if client[0] != app.main_app.ENTRY_LOGIN._textvariable.get():
                        continue
                    else:
                        username_check = True

                if username_check == False:
                    email_data = app.main_app.CURSOR.execute("SELECT email FROM Users").fetchall()
                    for email in email_data:
                        if email[0] != app.main_app.ENTRY_EMAIL._textvariable.get():
                            continue
                        else:
                            email_check = True

                    if email_check == False:
                        app.main_app.CURSOR.execute("INSERT INTO Users (username, password, email) VALUES (?, ?, ?)", (app.main_app.ENTRY_LOGIN._textvariable.get(), app.main_app.ENTRY_PASSWORD._textvariable.get(), app.main_app.ENTRY_EMAIL._textvariable.get()))
                        app.main_app.DATABASE_CONNECTION.commit()
                        
                        try:
                            os.mkdir(f"users/{app.main_app.ENTRY_LOGIN._textvariable.get()}")
                            reg = True
                            win = ctk.CTkToplevel()
                            win.title("Реєстрація")
                            win.resizable(False, False)
                            win.geometry(f"{250}x{100}")
                            win.attributes("-topmost", True)
                            label = ctk.CTkLabel(master = win, text = "Вас успішно зареєстровано!", font = ctk.CTkFont("Arial", 17))
                            label.place(x = 5, y = 40)
                            win.mainloop()


                            email_sender = "qrcodeapppractice@gmail.com"
                            email_password = "hdrbysjdwauhxkqt"
                            email_receiver = app.main_app.ENTRY_EMAIL._textvariable.get()
                            email_subject = "Реєстрація у TriangleMonkey"
                            email_body = "Вітаю! Ви зареєструвалися у базі даних TriangleMonkey!"
                            email = EmailMessage()
                            email["From"] = email_sender
                            email["To"] = email_receiver
                            email["Subject"] = email_subject
                            email.set_content(email_body)
                            context = ssl.create_default_context()
                            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context = context) as smtp:
                                smtp.login(email_sender, email_password)
                                smtp.sendmail(email_sender, email_receiver, email.as_string())
                        except:
                            pass


                    else:
                        win = ctk.CTkToplevel()
                        win.title("Помилка")
                        win.resizable(False, False)
                        win.geometry(f"{535}x{160}")
                        win.attributes("-topmost", True)
                        label = ctk.CTkLabel(master = win, text = "Такий нік або e-mail вже зареєстровано!", font = ctk.CTkFont("Arial", 20), text_color = "red")
                        label.place(x = 75, y = 60)
                        
                else:
                    win = ctk.CTkToplevel()
                    win.title("Помилка")
                    win.resizable(False, False)
                    win.geometry(f"{535}x{160}")
                    win.attributes("-topmost", True)
                    label = ctk.CTkLabel(master = win, text = "Такий нік або e-mail вже зареєстровано!", font = ctk.CTkFont("Arial", 20), text_color = "red")
                    label.place(x = 75, y = 60)


def verify_authorization():
    global reg
    if app.main_app.ENTRY_USERNAME_AUTH._textvariable.get() and app.main_app.ENTRY_PASSWORD_AUTH._textvariable.get():
        data = app.main_app.CURSOR.execute("SELECT password, username FROM Users").fetchall()
        if (app.main_app.ENTRY_PASSWORD_AUTH._textvariable.get(), app.main_app.ENTRY_USERNAME_AUTH._textvariable.get()) in data:
            # print("Тут має фрейм перемикатися, але не")
            app.main_app.APP_FRAME.place(x = 5, y = 5)
            reg = False
            
            try:
                app.main_app.AVATAR_IMAGE = ctk.CTkImage(light_image = Image.open(f"users/{app.main_app.ENTRY_USERNAME_AUTH._textvariable.get()}/avatar.png"), size = (115, 115))
                app.main_app.AVATAR_LABEL = ctk.CTkLabel(master = app.main_app.AVATAR_FRAME, text = "", image = app.main_app.AVATAR_IMAGE)
                app.main_app.AVATAR_LABEL.place(x = 17, y = 17)
            except:
                pass

def auth_tab():
    app.main_app.REGISTRATION_FRAME.place_forget()
    app.main_app.AUTHORIZATION_FRAME.place(x = 5, y = 5)
    

def register_tab():
    app.main_app.AUTHORIZATION_FRAME.place_forget()
    app.main_app.REGISTRATION_FRAME.place(x = 5, y = 5)


def make_qrcode():
    if app.main_app.URL_ENTRY._textvariable.get():
        win1 = ctk.CTkToplevel(app.main_app)
        win1.resizable(False, False)
        win1.geometry(f"{535}x{260}+{0}+{0}")
        win1.title("Збереження")
        win1.attributes("-topmost", True)
        entry = ctk.CTkEntry(
            master = win1, 
            width = 400, height = 150, 
            textvariable = ctk.StringVar(), 
            border_color = "#911CEE", 
            font = ctk.CTkFont("Arial", 30),
            corner_radius=20
        )
        
        entry.place(x = 67, y = 10)
        
        def onButtonPressed():
            if entry._textvariable.get():
                QRCode = qrcode.QRCode(
                    version = 1,
                    error_correction = qrcode.constants.ERROR_CORRECT_L,
                    box_size = 10
                )
                # try:
                QRCode.add_data(app.main_app.URL_ENTRY._textvariable.get())
                QRCode.make(True)
                if app.main_app.GRADIENT:
                    if app.main_app.LOGO:
                        file = QRCode.make_image(
                            back_color = app.main_app.IMAGE_COLOR, 
                            fill_color = app.main_app.BG_COLOR,
                            image_factory = StyledPilImage,
                            color_mask = ImageColorMask(color_mask_image = app.main_app.LOGO),

                        )                           
                    else:
                        file = QRCode.make_image(
                            back_color = app.main_app.IMAGE_COLOR, 
                            fill_color = app.main_app.BG_COLOR, 
                            image_factory = StyledPilImage,
                            color_mask = app.main_app.GRADIENT
                        )
                if app.main_app.MODULE_DRAWER:
                    if app.main_app.LOGO:
                        file = QRCode.make_image(
                            back_color = app.main_app.IMAGE_COLOR, 
                            fill_color = app.main_app.BG_COLOR,
                            image_factory = StyledPilImage,
                            color_mask = ImageColorMask(color_mask_image =  app.main_app.LOGO)
                        )
                    else:
                        file = QRCode.make_image(
                            back_color = app.main_app.IMAGE_COLOR, 
                            fill_color = app.main_app.BG_COLOR, 
                            module_drawer = app.main_app.MODULE_DRAWER, 
                            image_factory = StyledPilImage
                        )
                if not app.main_app.MODULE_DRAWER and not app.main_app.GRADIENT:
                    if app.main_app.LOGO:
                        print(app.main_app.LOGO)

                        file = QRCode.make_image(
                            back_color = app.main_app.IMAGE_COLOR, 
                            fill_color = app.main_app.BG_COLOR,
                            image_factory = StyledPilImage,
                            color_mask = ImageColorMask(color_mask_image = app.main_app.LOGO)
                        )


                    else:
                        file = QRCode.make_image(
                            back_color = app.main_app.IMAGE_COLOR,
                            fill_color = app.main_app.BG_COLOR
                        )
                
                if reg == True:
                    file.save(f"users/{app.main_app.ENTRY_LOGIN._textvariable.get()}/{entry._textvariable.get()}")
                    app.main_app.IMAGE_LABEL = ctk.CTkLabel(
                        master = app.main_app.QR_CODE_FRAME, 
                        text = "", 
                        image = ctk.CTkImage(light_image = Image.open(f"users/{app.main_app.ENTRY_LOGIN._textvariable.get()}/{entry._textvariable.get()}"), size = (280, 280))
                    )
                if reg == False:
                    file.save(f"users/{app.main_app.ENTRY_USERNAME_AUTH._textvariable.get()}/{entry._textvariable.get()}")
                    app.main_app.IMAGE_LABEL = ctk.CTkLabel(
                        master = app.main_app.QR_CODE_FRAME, 
                        text = "", 
                        image = ctk.CTkImage(light_image = Image.open(f"users/{app.main_app.ENTRY_USERNAME_AUTH._textvariable.get()}/{entry._textvariable.get()}"), size = (280, 280))
                    )

                app.main_app.IMAGE_LABEL.place(x = 0, y = 0)
                app.main_app.MODULE_DRAWER = None
                app.main_app.GRADIENT = None
                app.main_app.BG_COLOR = (0, 0, 0)
                app.main_app.IMAGE_COLOR = (255, 255, 255)
                app.main_app.LOGO = None
                win1.destroy()

                # except:
                #     print("Помилка")
        
        button = ctk.CTkButton(
            master = win1,
            width = 100,
            height = 75,
            corner_radius = 20,
            border_width = 3,
            border_color = "#911CEE",
            fg_color = "#343638",
            hover_color = "#29292a",
            text = "Пiдтвердити",
            command = onButtonPressed
        )

        button.place(x = 217, y = 170)

        

def bg_color():
    win = ctk.CTkToplevel()
    win.resizable(False, False)
    win.geometry(f"{545}x{270}+{0}+{0}")
    win.title("Колір фону")
    win.attributes("-topmost", True)
    
    frame = ctk.CTkFrame(
        master = win, 
        width = 535, 
        height = 260,
        corner_radius = 20,
        border_width = 3,
        border_color = "#911CEE"
    )

    def change_bg_color():
        app.main_app.BG_COLOR = (int(bg_color_entry_r._textvariable.get()), int(bg_color_entry_g._textvariable.get()), int(bg_color_entry_b._textvariable.get()))
        frame.place_forget()
        win.destroy()

    bg_color_entry_r = ctk.CTkEntry(
        master = frame, 
        width = 50, 
        height = 50, 
        # corner_radius = 20, 
        # border_width = 3, 
        # border_color = "#911CEE", 
        textvariable = ctk.StringVar(),
    )
    bg_color_entry_g = ctk.CTkEntry(
        master = frame, 
        width = 50, 
        height = 50, 
        # corner_radius = 20, 
        # border_width = 3, 
        # border_color = "#911CEE", 
        textvariable = ctk.StringVar(),
    )
    bg_color_entry_b = ctk.CTkEntry(
        master = frame, 
        width = 50, 
        height = 50, 
        # corner_radius = 20, 
        # border_width = 3, 
        # border_color = "#911CEE", 
        textvariable = ctk.StringVar(),
    )
    
    confirm_button = ctk.CTkButton(
        master = frame, 
        width = 235, 
        height = 100, 
        corner_radius = 20, 
        border_width = 3, 
        border_color = "#911CEE",
        fg_color = "#343638",
        hover_color = "#29292a",
        text = "Підтвердити",
        command = change_bg_color
    )

    r_label = ctk.CTkLabel(master = frame, font = ("Arial", 20), text = "R:")
    g_label = ctk.CTkLabel(master = frame, font = ("Arial", 20), text = "G:")
    b_label = ctk.CTkLabel(master = frame, font = ("Arial", 20), text = "B:")

    bg_color_entry_r.place(x = 180, y = 50)
    bg_color_entry_g.place(x = 240, y = 50)
    bg_color_entry_b.place(x = 300, y = 50)
    confirm_button.place(x = 150, y = 120)
    r_label.place(x = 180, y = 20)
    g_label.place(x = 240, y = 20)
    b_label.place(x = 300, y = 20)

    frame.place(x = 5, y = 5)


def image_color():
    win = ctk.CTkToplevel()
    win.resizable(False, False)
    win.geometry(f"{545}x{270}+{0}+{0}")
    win.title("Колір зображення")
    win.attributes("-topmost", True)

    frame = ctk.CTkFrame(
        master = win, 
        width = 535, 
        height = 260,
        corner_radius = 20,
        border_width = 3,
        border_color = "#911CEE"
    )

    def change_image_color():
        app.main_app.IMAGE_COLOR = (int(image_color_entry_r._textvariable.get()), int(image_color_entry_g._textvariable.get()), int(image_color_entry_b._textvariable.get()))
        frame.place_forget()
        win.destroy()

    image_color_entry_r = ctk.CTkEntry(
        master = frame, 
        width = 50, 
        height = 50, 
        # corner_radius = 20, 
        # border_width = 3, 
        # border_color = "#911CEE", 
        textvariable = ctk.StringVar(),
    )
    image_color_entry_g = ctk.CTkEntry(
        master = frame, 
        width = 50, 
        height = 50, 
        # corner_radius = 20, 
        # border_width = 3, 
        # border_color = "#911CEE", 
        textvariable = ctk.StringVar(),
    )
    image_color_entry_b = ctk.CTkEntry(
        master = frame, 
        width = 50, 
        height = 50, 
        # corner_radius = 20, 
        # border_width = 3, 
        # border_color = "#911CEE", 
        textvariable = ctk.StringVar(),
    )
    confirm_button = ctk.CTkButton(
        master = frame, 
        width = 235, 
        height = 100, 
        corner_radius = 20, 
        border_width = 3, 
        border_color = "#911CEE",
        fg_color = "#343638",
        hover_color = "#29292a",
        text = "Підтвердити",
        command = change_image_color,
    )

    r_label = ctk.CTkLabel(master = frame, font = ("Arial", 20), text = "R:")
    g_label = ctk.CTkLabel(master = frame, font = ("Arial", 20), text = "G:")
    b_label = ctk.CTkLabel(master = frame, font = ("Arial", 20), text = "B:")

    image_color_entry_r.place(x = 180, y = 50)
    image_color_entry_g.place(x = 240, y = 50)
    image_color_entry_b.place(x = 300, y = 50)
    confirm_button.place(x = 150, y = 120)
    r_label.place(x = 180, y = 20)
    g_label.place(x = 240, y = 20)
    b_label.place(x = 300, y = 20)

    frame.place(x = 5, y = 5)

def logo():
    win = ctk.CTkToplevel()
    win.resizable(False, False)
    win.geometry(f"{545}x{270}")
    win.title("Логотип")
    win.attributes("-topmost", True)
    
    # win.focus_force()
    # win.grab_set()
    # win.grab_release()

    def find_path():
        filename = ctk.filedialog.askopenfilename(filetypes = [("PNG", ".png"), ("JPEG", ".jpg .jpeg"), ("SVG", ".svg")])
        app.main_app.LOGO = Image.open(filename)    

        frame.place_forget()
        win.destroy()

    frame = ctk.CTkFrame(
        master = win, 
        width = 535, 
        height = 260,
        corner_radius = 20,
        border_width = 3,
        border_color = "#911CEE" 
    )
    
    find_path_btn = ctk.CTkButton(
        master = frame, 
        width = 335,
        height = 100,
        corner_radius = 20,
        border_width = 3,
        border_color = "#911CEE",
        fg_color = "#343638",
        hover_color = "#29292a",
        command = find_path,
        text = "Обрати картинку"
        
    )
    
    find_path_btn.place(x = 100, y = 80)

    frame.place(x = 5, y = 5)
    # app.main_app.LOGO = 


def design():
    # Дiма альо
    win = ctk.CTkToplevel(app.main_app)
    win.resizable(False, False)
    win.geometry(f"{545}x{270}+{0}+{0}")
    win.title("Логотип")
    win.attributes("-topmost", True)
    
    def gradient():
        button_module_drawer.place_forget()
        button_gradient.place_forget()

        def radial_gradient():
            app.main_app.GRADIENT = RadialGradiantColorMask()
            frame.place_forget()
            win.destroy()

        def square_gradient():
            app.main_app.GRADIENT = SquareGradiantColorMask()
            frame.place_forget()
            win.destroy()

        def horizontal_gradient():
            app.main_app.GRADIENT = HorizontalGradiantColorMask()
            frame.place_forget()
            win.destroy()

        def vertical_gradient():
            app.main_app.GRADIENT = VerticalGradiantColorMask()
            frame.place_forget()
            win.destroy()

        # def image_color_mask():
        #     app.main_app.GRADIENT = ImageColorMask()
        #     frame.place_forget()
        #     win.destroy()

        button_radial_gradient = ctk.CTkButton(
            master = frame, 
            width = 335, 
            height = 40, 
            corner_radius = 20,
            border_width = 3,
            border_color = "#911CEE",
            fg_color = "#343638",
            hover_color = "#29292a",
            text =  "Radial Gradient",
            command = radial_gradient
        )

        button_square_gradient = ctk.CTkButton(
            master = frame, 
            width = 335, 
            height = 40, 
            corner_radius = 20,
            border_width = 3,
            border_color = "#911CEE",
            fg_color = "#343638",
            hover_color = "#29292a",
            text =  "Square Gradient",
            command = square_gradient
        )

        button_horizontal_gradient = ctk.CTkButton(
            master = frame, 
            width = 335, 
            height = 40, 
            corner_radius = 20,
            border_width = 3,
            border_color = "#911CEE",
            fg_color = "#343638",
            hover_color = "#29292a",
            text =  "Horizontal Gradient",
            command = horizontal_gradient
        )

        button_vertical_gradient = ctk.CTkButton(
            master = frame, 
            width = 335, 
            height = 40, 
            corner_radius = 20,
            border_width = 3,
            border_color = "#911CEE",
            fg_color = "#343638",
            hover_color = "#29292a",
            text =  "Vertical Gradient",
            command = vertical_gradient
        )

        # button_image_color_mask = ctk.CTkButton(
        #     master = frame, 
        #     width = 335, 
        #     height = 40, 
        #     corner_radius = 20,
        #     border_width = 3,
        #     border_color = "#911CEE",
        #     fg_color = "#343638",
        #     hover_color = "#29292a",
        #     text =  "Image Color Mask",
        #     command = image_color_mask
        # )

        button_radial_gradient.place(x = 10,y = 10)
        button_square_gradient.place(x = 10,y = 60)
        button_horizontal_gradient.place(x = 10,y = 100)
        button_vertical_gradient.place(x = 10,y = 140)
        # button_image_color_mask.place(x = 10,y = 180)     

    def module_drawer():
        button_module_drawer.place_forget()
        button_gradient.place_forget()

        def gapped_square():
            app.main_app.MODULE_DRAWER = GappedSquareModuleDrawer()
            frame.place_forget()
            win.destroy()
        
        def circle_module():
            app.main_app.MODULE_DRAWER = CircleModuleDrawer()
            frame.place_forget()
            win.destroy()

        def rounded():
            app.main_app.MODULE_DRAWER = RoundedModuleDrawer()
            frame.place_forget()
            win.destroy()
        
        def vertical_bars():
            app.main_app.MODULE_DRAWER = VerticalBarsDrawer()
            frame.place_forget()
            win.destroy()

        def horizontal_bars():
            app.main_app.MODULE_DRAWER = HorizontalBarsDrawer()
            frame.place_forget()
            win.destroy()

        button_gapped_square = ctk.CTkButton(
            master = frame, 
            width = 335, 
            height = 40, 
            corner_radius = 20,
            border_width = 3,
            border_color = "#911CEE",
            fg_color = "#343638",
            hover_color = "#29292a",
            text =  "Gapped Square",
            command = gapped_square
        )
        
        button_circle = ctk.CTkButton(
            master = frame, 
            width = 335, 
            height = 40, 
            corner_radius = 20,
            border_width = 3,
            border_color = "#911CEE",
            fg_color = "#343638",
            hover_color = "#29292a",
            text =  "Circle",
            command = circle_module
        )

        button_rounded = ctk.CTkButton(
            master = frame, 
            width = 335, 
            height = 40, 
            corner_radius = 20,
            border_width = 3,
            border_color = "#911CEE",
            fg_color = "#343638",
            hover_color = "#29292a",
            text =  "Rounded",
            command = rounded
        )

        button_vertical_bars = ctk.CTkButton(
            master = frame, 
            width = 335, 
            height = 40, 
            corner_radius = 20,
            border_width = 3,
            border_color = "#911CEE",
            fg_color = "#343638",
            hover_color = "#29292a",
            text =  "Vertical Bars",
            command = vertical_bars
        )

        button_horizontal_bars = ctk.CTkButton(
            master = frame, 
            width = 335, 
            height = 40, 
            corner_radius = 20,
            border_width = 3,
            border_color = "#911CEE",
            fg_color = "#343638",
            hover_color = "#29292a",
            text =  "Horizontal Bars",
            command = horizontal_bars
        )

        button_gapped_square.place(x = 10, y = 10)
        button_circle.place(x = 10, y = 60)
        button_rounded.place(x = 10, y =100)
        button_vertical_bars.place(x = 10, y = 140)
        button_horizontal_bars.place(x = 10, y = 180)
    
    frame = ctk.CTkFrame(
        master= win, 
        width = 535, 
        height = 260, 
        corner_radius=20, 
        border_width = 3,
        border_color = "#911CEE"
    )

    button_module_drawer = ctk.CTkButton(
        master = frame, 
        width = 335, 
        height = 100, 
        corner_radius = 20,
        border_width = 3,
        border_color = "#911CEE",
        fg_color = "#343638",
        hover_color = "#29292a",
        text =  "Фільтри",
        command = module_drawer
    )

    button_gradient = ctk.CTkButton(
        master=frame, 
        width = 335, 
        height = 100, 
        corner_radius = 20,
        border_width = 3,
        border_color = "#911CEE",
        fg_color = "#343638",
        hover_color = "#29292a",
        text="Градiент",
        command= gradient
    )

    frame.place(x = 5, y = 5)
    

    button_module_drawer.place(x = 10, y = 30)
    button_gradient.place(x = 10, y = 140)

def history():
    global counter
    app.main_app.APP_FRAME.place_forget()
    app.main_app.HISTORY_FRAME.place(x = 5, y = 5)
    
    for filename in os.listdir(f"users/{app.main_app.ENTRY_USERNAME_AUTH._textvariable.get()}"):
        if filename != "avatar.png":
            label = ctk.CTkLabel(master = app.main_app.SCROLLABLE_FRAME, text = filename, font = ctk.CTkFont("Arial", 30))
            label.grid(row = counter, column = 0)
    
            counter += 1

def back():
    app.main_app.HISTORY_FRAME.place_forget()
    app.main_app.APP_FRAME.place(x = 5, y = 5)



def avatar():
    file = ctk.filedialog.askopenfilename(filetypes = [("PNG", ".png"), ("JPEG", ".jpg .jpeg"), ("SVG", ".svg")])
    image = Image.open(file)
    image.resize((147, 147))
    image = image.save(fp = f"users/{app.main_app.ENTRY_USERNAME_AUTH._textvariable.get()}/avatar.png")
    app.main_app.AVATAR_IMAGE = ctk.CTkImage(light_image = Image.open(f"users/{app.main_app.ENTRY_USERNAME_AUTH._textvariable.get()}/avatar.png"), size = (115, 115))
    if app.main_app.AVATAR_LABEL:
        app.main_app.AVATAR_LABEL.place_forget()
    app.main_app.AVATAR_LABEL = ctk.CTkLabel(master = app.main_app.AVATAR_FRAME, image = app.main_app.AVATAR_IMAGE, text = "")
    app.main_app.AVATAR_LABEL.place(x = 17, y = 17)

