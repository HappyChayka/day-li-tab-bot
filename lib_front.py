import config
import tkinter.messagebox
import lib_app_back as lab
from tkinter import *


class Library:

    def __init__(self, root):
        self.root = root
        self.root.title("Система Управления Базой Данных Библиотеки")
        self.root.geometry("1350x580+0+0")

        fna = StringVar()  # Firstname
        sna = StringVar()  # Surname
        BkID = StringVar()  # Book ID
        Bkt = StringVar()  # Book Title
        Atr = StringVar()  # Author
        DBo = StringVar()  # Date Borrowed
        Ddu = StringVar()  # Date Due
        sPr = StringVar()  # Days on Loan
        DoD = StringVar()  # Date OverDue

        # ==========================Function Declaration====================================

        def add_data():
            if len(fna.get()) != 0:
                lab.add_data_rec(fna.get(), sna.get(), BkID.get(),
                                 Bkt.get(), Atr.get(), DBo.get(),
                                 Ddu.get(), sPr.get(), DoD.get())
                booklist.delete(0, END)
                booklist.insert(END, fna.get(), sna.get(), BkID.get(),
                                Bkt.get(), Atr.get(), DBo.get(),
                                Ddu.get(), sPr.get(), DoD.get())

        def display_data():
            booklist.delete(0, END)
            for row in lab.view_data():
                booklist.insert(END, row)

        def clear_data():
            self.txtFName.delete(0, END)
            self.txtSName.delete(0, END)
            self.txtBkID.delete(0, END)
            self.txtBkNa.delete(0, END)
            self.txtAtr.delete(0, END)
            self.txtDaBo.delete(0, END)
            self.txtDaDue.delete(0, END)
            self.txtDOL.delete(0, END)
            self.txtDOD.delete(0, END)

        def delete_data():
            if len(fna.get()) != 0:
                lab.delete_data_rec(sb[0])
                clear_data()
                display_data()

        def update_data():
            if len(fna.get()) != 0:
                lab.update_data_rec(sb[0], fna.get(), sna.get(), BkID.get(),
                                    Bkt.get(), Atr.get(), DBo.get(),
                                    Ddu.get(), sPr.get(), DoD.get())

        def search_data():
            booklist.delete(0, END)
            for row in lab.search_data_rec(fna.get(), sna.get(), BkID.get(),
                                           Bkt.get(), Atr.get(), DBo.get(),
                                           Ddu.get(), sPr.get(), DoD.get()):
                booklist.insert(END, row)

        def i_exit():
            shouldexit = tkinter.messagebox.askyesno("СУБДБ", "Вы точно хотите выйти?")
            if shouldexit > 0:
                root.destroy()
                return

        def selected_book(event):
            global sb
            search_book = booklist.curselection()[0]
            sb = booklist.get(search_book)

            self.txtFName.delete(0, END)
            self.txtFName.insert(0, sb[1])
            self.txtSName.delete(0, END)
            self.txtSName.insert(0, sb[2])
            self.txtBkID.delete(0, END)
            self.txtBkID.insert(0, sb[3])
            self.txtBkNa.delete(0, END)
            self.txtBkNa.insert(0, sb[4])
            self.txtAtr.delete(0, END)
            self.txtAtr.insert(0, sb[5])
            self.txtDaBo.delete(0, END)
            self.txtDaBo.insert(0, sb[6])
            self.txtDaDue.delete(0, END)
            self.txtDaDue.insert(0, sb[7])
            self.txtDOL.delete(0, END)
            self.txtDOL.insert(0, sb[8])
            self.txtDOD.delete(0, END)
            self.txtDOD.insert(0, sb[9])

        # ======================================Frames====================================

        c1, c2, c3, c4, c5 = config.COLOR_PALETTE
        tit_fnt = config.TITLE_FONT
        nml_fnt = config.NORMAL_FONT
        btn_fnt = config.BUTTON_FONT

        main_frame = Frame(self.root, bg=c1)
        main_frame.grid()

        tit_frame = Frame(main_frame, bd=2, padx=40, pady=8, bg=c2, relief=RIDGE)
        tit_frame.pack(side=TOP)

        self.lblTit = Label(tit_frame, font=tit_fnt,
                            text="Система Управления Базой Данных Библиотеки", bg=c1)
        self.lblTit.grid(sticky=W)

        button_frame = Frame(main_frame, bd=2, width=1350, height=100, padx=20, pady=20, bg=c2, relief=RIDGE)
        button_frame.pack(side=BOTTOM)

        frame_detail = Frame(main_frame, bd=0, width=1350, height=50, padx=20, bg=c1, relief=RIDGE)
        frame_detail.pack(side=BOTTOM)

        data_frame = Frame(main_frame, bd=1, width=1350, height=400, padx=20, pady=20, bg=c3, relief=RIDGE)
        data_frame.pack(side=BOTTOM)

        data_frame_left = LabelFrame(data_frame, bd=1, width=800, height=300, padx=20, relief=RIDGE,
                                     font=nml_fnt, text="Введите данные", bg=c2)
        data_frame_left.pack(side=LEFT)

        data_frame_right = LabelFrame(data_frame, bd=1, width=450, height=300, padx=20, pady=3, relief=RIDGE,
                                      font=nml_fnt, text="Информация о книге", bg=c2)
        data_frame_right.pack(side=RIGHT)

        # ====================================Labels and Entries====================================

        self.lblFirstName = Label(data_frame_left, font=nml_fnt, text="Имя", padx=2, pady=2, bg=c2)
        self.lblFirstName.grid(row=0, column=0, sticky=W)
        self.txtFName = Entry(data_frame_left, font=nml_fnt, textvariable=fna, width=25, bg=c4)
        self.txtFName.grid(row=0, column=1)

        self.lblSurname = Label(data_frame_left, font=nml_fnt, text="Фамилия", padx=2, pady=2, bg=c2)
        self.lblSurname.grid(row=1, column=0, sticky=W)
        self.txtSName = Entry(data_frame_left, font=nml_fnt, textvariable=sna, width=25, bg=c4)
        self.txtSName.grid(row=1, column=1)

        self.lblBookID = Label(data_frame_left, font=nml_fnt, text="ID Книги", padx=2, pady=2, bg=c2)
        self.lblBookID.grid(row=2, column=0, sticky=W)
        self.txtBkID = Entry(data_frame_left, font=nml_fnt, textvariable=BkID, width=25, bg=c4)
        self.txtBkID.grid(row=2, column=1)

        self.lblBookName = Label(data_frame_left, font=nml_fnt, text="Назвние", padx=2, pady=2, bg=c2)
        self.lblBookName.grid(row=3, column=0, sticky=W)
        self.txtBkNa = Entry(data_frame_left, font=nml_fnt, textvariable=Bkt, width=25, bg=c4)
        self.txtBkNa.grid(row=3, column=1)

        self.lblAuthor = Label(data_frame_left, font=nml_fnt, text="Автор", padx=2, pady=2, bg=c2)
        self.lblAuthor.grid(row=4, column=0, sticky=W)
        self.txtAtr = Entry(data_frame_left, font=nml_fnt, textvariable=Atr, width=25, bg=c4)
        self.txtAtr.grid(row=4, column=1)

        self.lblDateBorrowed = Label(data_frame_left, font=nml_fnt, text="Взято", padx=2, pady=2, bg=c2)
        self.lblDateBorrowed.grid(row=0, column=3, sticky=W)
        self.txtDaBo = Entry(data_frame_left, font=nml_fnt, textvariable=DBo, width=25, bg=c4)
        self.txtDaBo.grid(row=0, column=4)

        self.lblDateDue = Label(data_frame_left, font=nml_fnt, text="Д/б сдано", padx=2, pady=2, bg=c2)
        self.lblDateDue.grid(row=1, column=3, sticky=W)
        self.txtDaDue = Entry(data_frame_left, font=nml_fnt, textvariable=Ddu, width=25, bg=c4)
        self.txtDaDue.grid(row=1, column=4)

        self.lblDaysOnLoan = Label(data_frame_left, font=nml_fnt, text="Дней с взятия", padx=2, pady=2, bg=c2)
        self.lblDaysOnLoan.grid(row=2, column=3, sticky=W)
        self.txtDOL = Entry(data_frame_left, font=nml_fnt, textvariable=sPr, width=25, bg=c4)
        self.txtDOL.grid(row=2, column=4)

        self.lblDateOverDue = Label(data_frame_left, font=nml_fnt, text="Сдано вовремя?", padx=2, pady=2, bg=c2)
        self.lblDateOverDue.grid(row=3, column=3, sticky=W)
        self.txtDOD = Entry(data_frame_left, font=nml_fnt, textvariable=DoD, width=25, bg=c4)
        self.txtDOD.grid(row=3, column=4)

        # ====================================Listbox and Scrollbar====================================

        scrollbar = Scrollbar(data_frame_right)
        scrollbar.grid(row=0, column=1, sticky="ns")

        booklist = Listbox(data_frame_right, width=45, height=12, font=nml_fnt,
                           yscrollcommand=scrollbar.set)
        booklist.bind("<<ListboxSelect>>", selected_book)
        booklist.grid(row=0, column=0, padx=8)
        scrollbar.config(command=booklist.yview)

        # ====================================Buttons and Widgets====================================

        self.btnAddData = Button(button_frame, bg=c4, text="Добавить", font=btn_fnt, height=2, width=13, bd=4,
                                 command=add_data)
        self.btnAddData.grid(row=0, column=1)

        self.btnDisplayData = Button(button_frame, bg=c4, text="Показать", font=btn_fnt, height=2, width=13, bd=4,
                                     command=display_data)
        self.btnDisplayData.grid(row=0, column=2)

        self.btnClearData = Button(button_frame, bg=c4, text="Очистить", font=btn_fnt, height=2, width=13, bd=4,
                                   command=clear_data)
        self.btnClearData.grid(row=0, column=3)

        self.btnDeleteData = Button(button_frame, bg=c4, text="Удалить", font=btn_fnt, height=2, width=13, bd=4,
                                    command=delete_data)
        self.btnDeleteData.grid(row=0, column=4)

        self.btnUpdateData = Button(button_frame, bg=c4, text="Обновить", font=btn_fnt, height=2, width=13, bd=4,
                                    command=update_data)
        self.btnUpdateData.grid(row=0, column=5)

        self.btnSearchData = Button(button_frame, bg=c4, text="Найти", font=btn_fnt, height=2, width=13, bd=4,
                                    command=search_data)
        self.btnSearchData.grid(row=0, column=6)

        self.btnExitData = Button(button_frame, bg=c4, text="Закрыть", font=btn_fnt, height=2, width=13, bd=4,
                                  command=i_exit)
        self.btnExitData.grid(row=0, column=7)


if __name__ == "__main__":
    root = Tk()
    application = Library(root)
    root.mainloop()
