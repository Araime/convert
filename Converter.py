import os
import sys
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

import requests

START_AMOUNT = 1000
WORK_PATH = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))


def exchange(event):
    entry_usd.delete(0, END)
    entry_eur.delete(0, END)
    entry_cny.delete(0, END)
    try:
        entry_usd.insert(0, "%.2f" % (float(entry_rur.get()) / USD["Value"]))
        entry_eur.insert(0, "%.2f" % (float(entry_rur.get()) / EUR["Value"]))
        entry_cny.insert(0, "%.2f" % (float(entry_rur.get()) / CNY["Value"]))
    except ValueError:
        messagebox.showwarning("Warning", "Проверьте введенную сумму")


if __name__ == "__main__":

    url = "https://www.cbr-xml-daily.ru/daily_json.js"

    root = Tk()
    root.title("Конвертер валют")
    root.geometry("350x212+700+300")
    root.resizable(False, False)
    iconbit = os.path.join(WORK_PATH, "73.ico")
    root.iconbitmap(iconbit)
    root.bind("<Return>", exchange)

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()["Valute"]
        USD = data["USD"]
        EUR = data["EUR"]
        CNY = data["CNY"]
    except requests.exceptions.ConnectionError:
        messagebox.showerror("Error", "Ошибка получения курсов валют")
        root.destroy()

    # Header Frame
    header_frame = Frame(root)
    header_frame.pack(fill=X)
    header_frame.grid_columnconfigure(0, weight=1)
    header_frame.grid_columnconfigure(1, weight=1)
    header_frame.grid_columnconfigure(2, weight=1)

    # Header
    header_currency = Label(header_frame, text="Валюта", bg="#ccc", font="Arial 12 bold")
    header_currency.grid(row=0, column=0, sticky=EW)
    header_buy = Label(header_frame, text="Продажа", bg="#ccc", font="Arial 12 bold")
    header_buy.grid(row=0, column=1, sticky=EW)
    header_changes = Label(header_frame, text="Изменение", bg="#ccc", font="Arial 12 bold")
    header_changes.grid(row=0, column=2, sticky=EW)

    # USD course
    usd_currency = Label(header_frame, text="USD", font="Arial 10")
    usd_currency.grid(row=1, column=0, sticky=EW)
    usd_sale = Label(header_frame, text=("%.2f" % USD["Value"]), font="Arial 10")
    usd_sale.grid(row=1, column=1, sticky=EW)

    usd_difference = "%.2f" % (USD["Value"] - USD["Previous"])
    if "-" in usd_difference:
        usd_changes = Label(header_frame, text=usd_difference, fg="green", font="Arial 10")
    elif usd_difference == 0:
        usd_changes = Label(header_frame, text=usd_difference, font="Arial 10")
    else:
        usd_changes = Label(header_frame, text=f"+{usd_difference}", fg="red", font="Arial 10")

    usd_changes.grid(row=1, column=2, sticky=EW)

    # EUR course
    eur_currency = Label(header_frame, text="EUR", bg="#ccc", font="Arial 10")
    eur_currency.grid(row=2, column=0, sticky=EW)
    eur_sale = Label(header_frame, text=("%.2f" % EUR["Value"]), bg="#ccc", font="Arial 10")
    eur_sale.grid(row=2, column=1, sticky=EW)

    eur_difference = "%.2f" % (EUR["Value"] - EUR["Previous"])
    if "-" in eur_difference:
        eur_changes = Label(header_frame, text=eur_difference, bg="#ccc", fg="green", font="Arial 10")
    elif eur_difference == 0:
        eur_changes = Label(header_frame, text=eur_difference, bg="#ccc", font="Arial 10")
    else:
        eur_changes = Label(header_frame, text=f"+{eur_difference}", bg="#ccc", fg="red", font="Arial 10")

    eur_changes.grid(row=2, column=2, sticky=EW)

    # CNY course
    cny_currency = Label(header_frame, text="CNY", font="Arial 10")
    cny_currency.grid(row=3, column=0, sticky=EW)
    cny_sale = Label(header_frame, text=("%.2f" % CNY["Value"]), font="Arial 10")
    cny_sale.grid(row=3, column=1, sticky=EW)

    cny_difference = "%.2f" % (CNY["Value"] - CNY["Previous"])
    if "-" in cny_difference:
        cny_changes = Label(header_frame, text=cny_difference, fg="green", font="Arial 10")
    elif cny_difference == 0:
        cny_changes = Label(header_frame, text=cny_difference, font="Arial 10")
    else:
        cny_changes = Label(header_frame, text=f"+{cny_difference}", fg="red", font="Arial 10")

    cny_changes.grid(row=3, column=2, sticky=EW)

    # Calc frame
    calc_frame = Frame(root, bg="#fff")
    calc_frame.pack(expand=1, fill=BOTH)
    calc_frame.grid_columnconfigure(1, weight=1)

    # RUR
    label_rur = Label(calc_frame, text="Рубли:", bg="#fff", font="Arial 10 bold")
    label_rur.grid(row=0, column=0, padx=10)
    entry_rur = ttk.Entry(calc_frame, justify=CENTER, font="Arial 10")
    entry_rur.grid(row=0, column=1, columnspan=2, pady=10, padx=10, sticky=EW)
    entry_rur.insert(0, START_AMOUNT)
    entry_rur.focus()

    # Result Frame
    res_frame = Frame(root)
    res_frame.pack(expand=1, fill=BOTH, pady=5)
    res_frame.grid_columnconfigure(1, weight=1)

    # USD
    label_usd = Label(res_frame, text="USD:", font="Arial 10 bold")
    label_usd.grid(row=2, column=0)
    entry_usd = ttk.Entry(res_frame, justify=CENTER, font="Arial 10")
    entry_usd.grid(row=2, column=1, columnspan=2, padx=10, sticky=EW)
    entry_usd.insert(0, "%.2f" % (START_AMOUNT / USD["Value"]))

    # EUR
    label_eur = Label(res_frame, text="EUR:", font="Arial 10 bold")
    label_eur.grid(row=3, column=0)
    entry_eur = ttk.Entry(res_frame, justify=CENTER, font="Arial 10")
    entry_eur.grid(row=3, column=1, columnspan=2, padx=10, sticky=EW)
    entry_eur.insert(0, "%.2f" % (START_AMOUNT / EUR["Value"]))

    # CNY
    label_cny = Label(res_frame, text="CNY:", font="Arial 10 bold")
    label_cny.grid(row=4, column=0)
    entry_cny = ttk.Entry(res_frame, justify=CENTER, font="Arial 10")
    entry_cny.grid(row=4, column=1, columnspan=2, padx=10, sticky=EW)
    entry_cny.insert(0, "%.2f" % (START_AMOUNT / CNY["Value"]))

    root.mainloop()
