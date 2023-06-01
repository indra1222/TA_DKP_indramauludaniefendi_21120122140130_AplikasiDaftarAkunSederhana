from tkinter import *
import tkinter.messagebox as messageBox
import sqlite3

class AccountApp:
    def __init__(self, root):
        self.root = root
        self.root.title("aplikasi sederhana")

        self.username = StringVar()
        self.password = StringVar()
        self.firstname = StringVar()
        self.lastname = StringVar()

        self.create_table()
        self.login_form()


    def create_table(self):
        conn = sqlite3.connect("db_member.db")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT, password TEXT, firstname TEXT, lastname TEXT)")
        conn.commit()
        conn.close()

    def exit_app(self):
        result = messageBox.askquestion('System', 'Apakah Anda yakin ingin keluar?', icon="warning")
        if result == 'yes':
            self.root.destroy()

    def login_form(self):
        self.LoginFrame = Frame(self.root, bg="red" )
        self.LoginFrame.pack(side=TOP, pady=80)
        lbl_username = Label(self.LoginFrame, text="Username:", font=('arial', 21), bd=18,bg="red" )
        lbl_username.grid(row=1)
        lbl_password = Label(self.LoginFrame, text="Password:", font=('arial', 21), bd=18,bg="red")
        lbl_password.grid(row=2)
        self.lbl_result1 = Label(self.LoginFrame, text="masukan akun nya", font=('arial', 14),bg="red",fg="black")
        self.lbl_result1.grid(row=3, columnspan=2)
        username = Entry(self.LoginFrame, font=('arial', 16), textvariable=self.username, width=15)
        username.grid(row=1, column=1)
        password = Entry(self.LoginFrame, font=('arial', 16), textvariable=self.password, width=15, show="*")
        password.grid(row=2, column=1)
        btn_login = Button(self.LoginFrame, text="Login Member", font=('arial', 14), width=35, command=self.login)
        btn_login.grid(row=4, columnspan=2, pady=20)
        lbl_register = Label(self.LoginFrame, text="Daftar Member", bg="red",fg="blue", font=('arial', 12))
        lbl_register.grid(row=0, sticky=W)
        lbl_register.bind('<Button-1>', self.toggle_to_register)

    def register_form(self):
        self.RegisterFrame = Frame(self.root)
        self.RegisterFrame.pack(side=TOP, pady=40)
        lbl_username = Label(self.RegisterFrame, text="Username:", font=('arial', 18), bd=18)
        lbl_username.grid(row=1)
        lbl_password = Label(self.RegisterFrame, text="Password:", font=('arial', 18), bd=18)
        lbl_password.grid(row=2)
        lbl_firstname = Label(self.RegisterFrame, text="Nama Depan:", font=('arial', 18), bd=18)
        lbl_firstname.grid(row=3)
        lbl_lastname = Label(self.RegisterFrame, text="Nama Belakang:", font=('arial', 18), bd=18)
        lbl_lastname.grid(row=4)
        self.lbl_result2 = Label(self.RegisterFrame, text="", font=('arial', 18))
        self.lbl_result2.grid(row=5, columnspan=2)
        username = Entry(self.RegisterFrame, font=('arial', 20), textvariable=self.username, width=10)
        username.grid(row=1, column=1)
        password = Entry(self.RegisterFrame, font=('arial', 20), textvariable=self.password, width=10, show="*")
        password.grid(row=2, column=1)
        firstname = Entry(self.RegisterFrame, font=('arial', 20), textvariable=self.firstname, width=10)
        firstname.grid(row=3, column=1)
        lastname = Entry(self.RegisterFrame, font=('arial', 20), textvariable=self.lastname, width=10)
        lastname.grid(row=4, column=1)
        btn_register = Button(self.RegisterFrame, text="Register", font=('arial', 14), width=35, command=self.register)
        btn_register.grid(row=6, columnspan=2, pady=20)
        lbl_login = Label(self.RegisterFrame, text="Login", fg="Blue", font=('arial', 14))
        lbl_login.grid(row=0, sticky=W)
        lbl_login.bind('<Button-1>', self.toggle_to_login)

    def toggle_to_login(self, event=None):
        self.RegisterFrame.destroy()
        self.login_form()

    def toggle_to_register(self, event=None):
        self.LoginFrame.destroy()
        self.register_form()

    def register(self):
        if self.username.get() == "" or self.password.get() == "" or self.firstname.get() == "" or self.lastname.get() == "":
            self.lbl_result2.config(text="mohon untuk diisi", fg="red")
        else:
            conn = sqlite3.connect("db_member.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM `member` WHERE `username` = ?", (self.username.get(),))
            if cursor.fetchone() is not None:
                self.lbl_result2.config(text="Username sudah digunakan", fg="red")
            else:
                cursor.execute("INSERT INTO `member` (username, password, firstname, lastname) VALUES(?, ?, ?, ?)", (str(self.username.get()), str(self.password.get()), str(self.firstname.get()), str(self.lastname.get())))
                conn.commit()
                self.username.set("")
                self.password.set("")
                self.firstname.set("")
                self.lastname.set("")
                self.lbl_result2.config(text="Akun member berhasil dibuat! berhasil akun telah terbuat", fg="black")
            cursor.close()
            conn.close()

    def login(self, event=None):
        if self.username.get() == "" or self.password.get() == "":
            self.lbl_result1.config(text="Masukkan Username atau Password", fg="black")
        else:
            conn = sqlite3.connect("db_member.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM `member` WHERE `username` = ? and `password` = ?", (self.username.get(), self.password.get()))
            if cursor.fetchone() is not None:
                self.home_window()
                self.username.set("")
                self.password.set("")
                self.lbl_result2.config(text="")
            else:
                self.lbl_result1.config(text="salah paswordnya", fg="black")
            cursor.close()
            conn.close()

    def home_window(self):
        self.root.withdraw()
        home = Toplevel(self.root)
        home.title("Aplikasi Pembuatan Akun Sederhana")
        width = 635
        height = 465
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        home.geometry("%dx%d+%d+%d" % (width, height, x, y))
        lbl_home = Label(home, text="akun berhasil masuk", font=('arial', 30)).pack()
        btn_logout = Button(home, text="Logout", font=('arial', 14), command=self.logout).pack(pady=25)
        

    def logout(self):
        self.root.deiconify()
        self.root.destroy()
        self.__init__(Tk())

# Membuat loop perulangan
while True:
    root = Tk()
    app = AccountApp(root)
    root.mainloop()

    # Mengecek apakah pengguna ingin keluar dari aplikasi
    result = messageBox.askquestion('System', 'Apakah Anda ingin keluar dari aplikasi?', icon="warning")
    if result != 'yes':
        break

root = Tk()
app = AccountApp(root)
root.mainloop()
