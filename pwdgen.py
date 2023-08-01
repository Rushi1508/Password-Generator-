import string
import random
from tkinter import *
from tkinter import messagebox
import sqlite3
from PIL import ImageTk, Image

with sqlite3.connect("data.db") as db:
    cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users(Username TEXT NOT NULL, GeneratedPassword TEXT NOT NULL);")
cursor.execute("SELECT * FROM users")
db.commit()
db.close()


class GUI():
    def __init__(self, master: object) -> object:
        self.master = master
        self.username = StringVar()
        self.passwordlen = IntVar()
        self.generatedpassword = StringVar()
        self.n_username = StringVar()
        self.n_generatedpassword = StringVar()
        self.n_passwordlen = IntVar()

        root.title('Password Generator')
        root.geometry('800x800')
        root.resizable(False, False)

        self.bg_image = ImageTk.PhotoImage(Image.open("pwdgen.jpg"))

        # Create a label to display the background image
        self.background_label = Label(root, image=self.bg_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.label = Label(text="Password Generator", fg='darkblue',bg="white", font='Times 30 bold underline',bd=4, relief='ridge')
        self.label.grid(row=0, column=1)

        self.blank_label1 = Label(text="")
        self.blank_label1.grid(row=1, column=0, columnspan=2)

        self.blank_label2 = Label(text="")
        self.blank_label2.grid(row=2, column=0, columnspan=2)

        self.blank_label2 = Label(text="")
        self.blank_label2.grid(row=3, column=0, columnspan=2)

        self.user = Label(text="Enter user name: ", font='times 20', bd=2, relief='solid')
        self.user.grid(row=4, column=0)

        self.textfield = Entry(textvariable=self.n_username, font='Times 16', bd=4, relief='ridge')
        self.textfield.grid(row=4, column=1)
        self.textfield.focus_set()

        self.blank_label3 = Label(text="")
        self.blank_label3.grid(row=5, column=0)

        self.length = Label(text="Enter password length: ", font='times 20', bd=2, relief='solid')
        self.length.grid(row=6, column=0)

        self.length_textfield = Entry(textvariable=self.n_passwordlen, font='times 16', bd=6, relief='ridge')
        self.length_textfield.grid(row=6, column=1)

        self.blank_label4 = Label(text="")
        self.blank_label4.grid(row=7, column=0)

        self.generated_password = Label(text="Generated password: ", font='times 20', bd=2, relief='solid')
        self.generated_password.grid(row=8, column=0)

        self.generated_password_textfield = Entry(textvariable=self.n_generatedpassword, font='times 16', bd=6,
                                                  relief='ridge', fg='darkblue')
        self.generated_password_textfield.grid(row=8, column=1)

        self.blank_label5 = Label(text="")
        self.blank_label5.grid(row=9, column=0)

        self.blank_label6 = Label(text="")
        self.blank_label6.grid(row=10, column=0)

        self.generate = Button(text="GENERATE PASSWORD", bd=3, relief='solid', padx=1, pady=1, font='times 18 bold',
                               fg='white', bg='darkblue', command=self.generate_pass)
        self.generate.grid(row=11, column=1)

        self.blank_label5 = Label(text="")
        self.blank_label5.grid(row=12, column=0)

        self.accept = Button(text="ACCEPT", bd=3, relief='solid', padx=1, pady=1, font='times 18', fg='darkblue',
                             bg='white', command=self.accept_fields)
        self.accept.grid(row=13, column=1)

        self.blank_label1 = Label(text="")
        self.blank_label1.grid(row=14, column=1)

        self.reset = Button(text="RESET", bd=3, relief='solid', padx=1, pady=1, font='times 18', fg='darkblue',
                            bg='white', command=self.reset_fields)
        self.reset.grid(row=15, column=1)

    def generate_pass(self):
        upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        lower = "abcdefghijklmnopqrstuvwxyz"
        chars = "@#%&()\"?!"
        numbers = "1234567890"
        upper = list(upper)
        lower = list(lower)
        chars = list(chars)
        numbers = list(numbers)
        name = self.textfield.get()
        leng = self.length_textfield.get()

        with sqlite3.connect("users.db") as db:
            cursor = db.cursor()

        if name == "":
            messagebox.showerror("Error", "PLEASE ENTER THE NAME")
            return

        if name.isalpha() == False:
            messagebox.showerror("Error", "NAME SYNTAX IS INVALID")
            self.textfield.delete(0, 25)
            return

        length = int(leng)

        if length < 4:
            messagebox.showerror("Error", "PASSWORD LENGTH SHOULD BE AT LEAST 4")
            self.textfield.configure(text="")
            return
        else:
            self.blank_label1.configure(text="")

        self.generated_password_textfield.delete(0, length)

        u = random.randint(1, length - 3)
        l = random.randint(1, length - 2 - u)
        c = random.randint(1, length - 1 - u - l)
        n = length - u - l - c

        password = random.sample(upper, u) + random.sample(lower, l) + random.sample(chars, c) + random.sample(numbers,
                                                                                                               n)
        random.shuffle(password)
        gen_passwd = "".join(password)
        n_generatedpassword = self.generated_password_textfield.insert(0, gen_passwd)

    def accept_fields(self):
        with sqlite3.connect("data.db") as db:
            cursor = db.cursor()
            find_user = ("SELECT * FROM users WHERE Username = ?")
            cursor.execute(find_user, [(self.n_username.get())])

            if cursor.fetchall():
                messagebox.showerror("This username already exists!", "Please use an another username")
            else:
                insert = str("INSERT INTO users(Username, GeneratedPassword) VALUES(\'%s\', \'%s\');" % (self.n_username.get(), self.n_generatedpassword.get()))
                cursor.execute(insert)
                db.commit()
                messagebox.showinfo("Success!", "PASSWORD GENERATED")

    def reset_fields(self):
        self.textfield.delete(0, 25)
        self.length_textfield.delete(0, 25)
        self.generated_password_textfield.delete(0, 25)


if __name__ == '__main__':
    root = Tk()
    pass_gen = GUI(root)
    root.mainloop()