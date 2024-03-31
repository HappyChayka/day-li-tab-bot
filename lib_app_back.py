import sqlite3 as sql3
import config


def ConnectData():
    connection = sql3.connect(config.LIBRARY_DB)
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS library (
    id INTEGER PRIMARY KEY,
    fna text,
    sna text,
    BkID text,
    Bkt text,
    Atr text,
    DBo text,
    Ddu text,
    sPr text,
    DoD text
    )""")
    connection.commit()
    connection.close()


def add_data_rec(fna, sna, BkID, Bkt, Atr, DBo, Ddu, sPr, DoD):
    connection = sql3.connect(config.LIBRARY_DB)
    cursor = connection.cursor()
    cursor.execute("""INSERT INTO library VALUES 
    (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (fna, sna,
                                           BkID, Bkt, Atr,
                                           DBo, Ddu, sPr, DoD))
    connection.commit()
    connection.close()


def view_data():
    connection = sql3.connect(config.LIBRARY_DB)
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM library""")
    rows = cursor.fetchall()
    connection.close()
    return rows


def delete_data_rec(id):
    connection = sql3.connect(config.LIBRARY_DB)
    cursor = connection.cursor()
    cursor.execute("""DELETE FROM library WHERE id=?""", (id, ))
    connection.commit()
    connection.close()


def update_data_rec(id, fna="", sna="", BkID="",
                    Bkt="", Atr="", DBo="",
                    Ddu="", sPr="", DoD=""):
    connection = sql3.connect(config.LIBRARY_DB)
    cursor = connection.cursor()
    cursor.execute("""UPDATE library SET 
    fna=?, sna=?, BkID=?, 
    Bkt=?, Atr=?, DBo=?, 
    Ddu=?, sPr=?, DoD=?
    WHERE id = ?""",
    (fna, sna, BkID,
                Bkt, Atr, DBo,
                Ddu, sPr, DoD, id))
    connection.commit()
    connection.close()


def search_data_rec(fna="", sna="", BkID="",
                    Bkt="", Atr="", DBo="",
                    Ddu="", sPr="", DoD=""):
    connection = sql3.connect(config.LIBRARY_DB)
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM library WHERE 
                    fna LIKE ? OR sna LIKE ? OR BkID LIKE ? OR
                    Bkt LIKE ? OR Atr LIKE ? OR DBo LIKE ? OR
                    Ddu LIKE ? OR sPr LIKE ? OR DoD LIKE?""",
                   (fna, sna, BkID,
                    Bkt, Atr, DBo,
                    Ddu, sPr, DoD))
    rows = cursor.fetchall()
    connection.close()
    return rows

ConnectData()
