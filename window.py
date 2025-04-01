from PyQt6 import sip
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QPixmap
from PyQt6 import uic
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl
import sys
import sqlite3


class Main_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("avtovitrina_1.ui", self)
        self.setWindowTitle("Автовитрина")
        self.web_view = QWebEngineView(self)
        self.web_view.setGeometry(0, 430, 1070, 480)
        self.initUI()
        self.data_base()
        self.check_button_cuzov()

    def initUI(self):
        self.pixmap_name = QPixmap("logotip.png")
        self.name.setPixmap(self.pixmap_name)

        self.pixmap_crossover = QPixmap("crossover1.png")
        self.crossover_photo.setPixmap(self.pixmap_crossover)

        self.pixmap_sedan = QPixmap("sedan1.png")
        self.sedan_photo.setPixmap(self.pixmap_sedan)

        self.pixmap_jeep = QPixmap("jeep1.png")
        self.jeep_photo.setPixmap(self.pixmap_jeep)

        self.pixmap_kupe = QPixmap("kupe1.png")
        self.kupe_photo.setPixmap(self.pixmap_kupe)

        self.pixmap_sport = QPixmap("sport1.png")
        self.sport_photo.setPixmap(self.pixmap_sport)

        self.crossover_btn.clicked.connect(self.check_button_cuzov)
        self.kupe_btn.clicked.connect(self.check_button_cuzov)
        self.jeep_btn.clicked.connect(self.check_button_cuzov)
        self.sedan_btn.clicked.connect(self.check_button_cuzov)
        self.sport_btn.clicked.connect(self.check_button_cuzov)
        self.list_btns = [self.crossover_btn,
                          self.jeep_btn,
                          self.sedan_btn, 
                          self.sport_btn,
                          self.kupe_btn
                          ] 
        self.mark_box.currentTextChanged.connect(self.mark_changed)
        self.model_box.currentTextChanged.connect(self.model_changed)
        
        self.dict_of_cars = {
            1: "bmw x6.jpg",
            2: "bmw x8.jpg",
            3: "mercedes 190sl.jpeg",
            4: "mercedes amg gt.jpg",
            5: "toyota aurion.jpg",
            6: "toyota camry.jpg",
            7: "honda horizon.jpg",
            8: "honda nsx.jpg",
            9: "skoda karoq.jpg",
            10: "skoda octavia.jpg",
            11: "jeep renegade.jpg",
            12: "jeep wrangler.jpg",
            13: "volvo xc60.jpg",
            14: "volvo v90.jpg",
            15: "dodge viper.jpg",
            16: "dodge challenger.jpg",
            17: "chevrolet camaro.webp",
            18: "chevrolet impala.jpg",
            19: "ford bronco.jpg",
            20: "ford mustang.webp"
        }

    def data_base(self):
        con = sqlite3.connect("cars_db.sqlite")
        cur = con.cursor()
        result = cur.execute("SELECT name FROM marks").fetchall()
        for i in result:
            for j in i:
                self.mark_box.addItem(j)
        result = cur.execute("SELECT id, name, kuzov, year, drive FROM specifications").fetchall()
        html_table_parent = """
            <tr>
                <td class="photo"><h1>Фото</h1></td>
                <td class="photo"><img src="file://C:\\Users\\Роман\\Projects\\Avtovitrina_pyqt\\#id"></td>
            </tr>
            <tr>
                <td>
                    <h1 class="name">Название</h1>
                </td>
                <td>
                    <h1 class="name">#name1</h1>
                </td>
            </tr>
            <tr>
                <td>
                    <h1 class="kuzov">Кузов</h1>
                </td>
                <td>
                    <h1 class="kuzov">#kuzov1</h1>
                </td>
            </tr>
            <tr>
                <td>
                    <h1 class="year">Год выпуска</h1>
                </td>
                <td>
                    <h1 class="year">#year1</h1>
                </td>
            </tr>
            <tr>
                <td>
                    <h1 class="drive">Привод</h1>
                </td>
                <td>
                    <h1 class="drive">#drive1</h1>
                </td>
            </tr>"""
        html_table_result = ""
        for i in range(len(result)):
            html_table = html_table_parent
            html_table = html_table.replace("#id", self.dict_of_cars[int(str(result[i][0]))])
            html_table = html_table.replace("#name1", str(result[i][1]))
            html_table = html_table.replace("#kuzov1", str(result[i][2]))
            html_table = html_table.replace("#year1", str(result[i][3]))
            html_table = html_table.replace("#drive1", str(result[i][4]))
            html_table_result += html_table
            html_content = """
                <!DOCTYPE html>
                <html lang="ru">
                <head>
                <meta charset="UTF-8">
                </head>
                <body>
                <table style="height:100%;
                            width:100%;
                            position: absolute;
                            top: 0;
                            bottom: 0;
                            left: 0;
                            right: 0">
                        <style> table 
                                    {
                                        background: #1e213e;
                                    }

                                td
                                    {
                                        color: #CAD4D6;
                                    }
                                h1
                                    {
                                        text-align: center;
                                        color: #f2f2f2;
                                    }

                                caption
                                    {
                                        background:#c74343;
                                    }

                                .photo
                                    {
                                        background: #252F48;
                                        text-align: center;
                                    }

                                .name
                                    {
                                        background: #5c84ab;
                                    }

                                .kuzov
                                    {
                                        background: #5c84ab;
                                    }

                                .year
                                    {
                                        background: #5c84ab
                                    }
                                .drive
                                    {
                                        background: #5c84ab
                                    }
                        </style>
                    <caption><h1>Найдено:</h1></caption>""" + html_table_result + """</table>
                </body>
                </html>"""       
        self.web_view.setHtml(html_content, baseUrl=QUrl('file:'))
        con.close()
        
    def mark_changed(self, current_mark):
        if current_mark == "Любая" and current_mark != "":
            con = sqlite3.connect("cars_db.sqlite")
            cur = con.cursor()
            result = cur.execute("SELECT id, name, kuzov, year, drive FROM specifications").fetchall()
            html_table_parent = """
                <tr>
                    <td class="photo"><h1>Фото</h1></td>
                    <td class="photo"><img src="file://C:\\Users\\Роман\\Projects\\Avtovitrina_pyqt\\#id"></td>
                </tr>
                <tr>
                    <td>
                        <h1 class="name">Название</h1>
                    </td>
                    <td>
                        <h1 class="name">#name1</h1>
                    </td>
                </tr>
                <tr>
                    <td>
                        <h1 class="kuzov">Кузов</h1>
                    </td>
                    <td>
                        <h1 class="kuzov">#kuzov1</h1>
                    </td>
                </tr>
                <tr>
                    <td>
                        <h1 class="year">Год выпуска</h1>
                    </td>
                    <td>
                        <h1 class="year">#year1</h1>
                    </td>
                </tr>
                <tr>
                    <td>
                        <h1 class="drive">Привод</h1>
                    </td>
                    <td>
                        <h1 class="drive">#drive1</h1>
                    </td>
                </tr>"""
            html_table_result = ""
            for i in range(len(result)):
                html_table = html_table_parent
                html_table = html_table.replace("#id", self.dict_of_cars[int(str(result[i][0]))])
                html_table = html_table.replace("#name1", str(result[i][1]))
                html_table = html_table.replace("#kuzov1", str(result[i][2]))
                html_table = html_table.replace("#year1", str(result[i][3]))
                html_table = html_table.replace("#drive1", str(result[i][4]))
                html_table_result += html_table
                html_content = """
                    <!DOCTYPE html>
                    <html lang="ru">
                    <head>
                    <meta charset="UTF-8">
                    </head>
                    <body>
                    <table style="height:100%;
                                width:100%;
                                position: absolute;
                                top: 0;
                                bottom: 0;
                                left: 0;
                                right: 0">
                            <style> table 
                                        {
                                            background: #1e213e;
                                        }

                                    td
                                        {
                                            color: #CAD4D6;
                                        }
                                    h1
                                        {
                                            text-align: center;
                                            color: #f2f2f2;
                                        }

                                    caption
                                        {
                                            background:#c74343;
                                        }

                                    .photo
                                        {
                                            background: #252F48;
                                            text-align: center;
                                        }

                                    .name
                                        {
                                            background: #5c84ab;
                                        }

                                    .kuzov
                                        {
                                            background: #5c84ab;
                                        }

                                    .year
                                        {
                                            background: #5c84ab
                                        }
                                    .drive
                                        {
                                            background: #5c84ab
                                        }
                            </style>
                        <caption><h1>Найдено:</h1></caption>""" + html_table_result + """</table>
                    </body>
                    </html>"""       
                self.web_view.setHtml(html_content, baseUrl=QUrl('file:'))
            con.close()

        if current_mark != "Любая" and current_mark != "":
            con = sqlite3.connect("cars_db.sqlite")
            cur = con.cursor()
            result = cur.execute("""SELECT models.name FROM models
                                    LEFT JOIN marks ON marks.id = models.mark
                                    where marks.name = ?""", (current_mark,)).fetchall()
            con.close()
            self.model_box.clear()
            self.model_box.addItem(result[0][0])
            self.model_box.addItem(result[1][0])
            list_check_button = [self.mark_box.currentText(), self.model_box.currentText()]
            con = sqlite3.connect("cars_db.sqlite")
            cur = con.cursor()
            current_mark = list_check_button[0]
            current_model = list_check_button[1]
            if current_mark == "SKODA":
                current_mark = "SHKODA"
            current_mark_and_model = current_mark + " " + current_model
            result = cur.execute("SELECT id, name, kuzov, year, drive FROM specifications WHERE name = ?", (current_mark_and_model,)).fetchall()
            html_table_parent = """
                <tr>
                    <td class="photo"><h1>Фото</h1></td>
                    <td class="photo"><img src="file://C:\\Users\\Роман\\Projects\\Avtovitrina_pyqt\\#id"></td>
                </tr>
                <tr>
                    <td>
                        <h1 class="name">Название</h1>
                    </td>
                    <td>
                        <h1 class="name">#name1</h1>
                    </td>
                </tr>
                <tr>
                    <td>
                        <h1 class="kuzov">Кузов</h1>
                    </td>
                    <td>
                        <h1 class="kuzov">#kuzov1</h1>
                    </td>
                </tr>
                <tr>
                    <td>
                        <h1 class="year">Год выпуска</h1>
                    </td>
                    <td>
                        <h1 class="year">#year1</h1>
                    </td>
                </tr>
                <tr>
                    <td>
                        <h1 class="drive">Привод</h1>
                    </td>
                    <td>
                        <h1 class="drive">#drive1</h1>
                    </td>
                </tr>"""
            html_table_result = ""
            for i in range(len(result)):
                html_table = html_table_parent
                html_table = html_table.replace("#id", self.dict_of_cars[int(str(result[i][0]))])
                html_table = html_table.replace("#name1", str(result[i][1]))
                html_table = html_table.replace("#kuzov1", str(result[i][2]))
                html_table = html_table.replace("#year1", str(result[i][3]))
                html_table = html_table.replace("#drive1", str(result[i][4]))
                html_table_result += html_table
                html_content = """
                    <!DOCTYPE html>
                    <html lang="ru">
                    <head>
                    <meta charset="UTF-8">
                    </head>
                    <body>
                    <table style="height:100%;
                                width:100%;
                                position: absolute;
                                top: 0;
                                bottom: 0;
                                left: 0;
                                right: 0">
                            <style> table 
                                        {
                                            background: #1e213e;
                                        }

                                    td
                                        {
                                            color: #CAD4D6;
                                        }
                                    h1
                                        {
                                            text-align: center;
                                            color: #f2f2f2;
                                        }

                                    caption
                                        {
                                            background:#c74343;
                                        }

                                    .photo
                                        {
                                            background: #252F48;
                                            text-align: center;
                                        }

                                    .name
                                        {
                                            background: #5c84ab;
                                        }

                                    .kuzov
                                        {
                                            background: #5c84ab;
                                        }

                                    .year
                                        {
                                            background: #5c84ab
                                        }
                                    .drive
                                        {
                                            background: #5c84ab
                                        }
                            </style>
                        <caption><h1>Найдено:</h1></caption>""" + html_table_result + """</table>
                    </body>
                    </html>"""       
                self.web_view.setHtml(html_content, baseUrl=QUrl('file:'))
            con.close()
            

    def model_changed(self, current_model):
        con = sqlite3.connect("cars_db.sqlite")
        cur = con.cursor()
        result = cur.execute("""SELECT models.name FROM models
                                LEFT JOIN marks ON marks.id = models.mark
                                where marks.name = ?""", (self.mark_box.currentText(),)).fetchall()
        con.close()
        if current_model != "" and current_model != result[0][0]:
            con = sqlite3.connect("cars_db.sqlite")
            cur = con.cursor()
            result = cur.execute("""SELECT models.name FROM models
                                    LEFT JOIN marks ON marks.id = models.mark
                                    where marks.name = ?""", (self.mark_box.currentText(),)).fetchall()
            list_check_button = [self.mark_box.currentText(), self.model_box.currentText()]
            current_mark = list_check_button[0]
            if current_mark == "SKODA":
                current_mark = "SHKODA"
            current_model = list_check_button[1]
            if current_model == "Challenger":
                current_model = "CHALLENGER"
            current_mark_and_model = current_mark + " " + current_model
            result = cur.execute("SELECT id, name, kuzov, year, drive FROM specifications WHERE name = ?", (current_mark_and_model,)).fetchall()
            html_table_parent = """
                <tr>
                    <td class="photo"><h1>Фото</h1></td>
                    <td class="photo"><img src="file://C:\\Users\\Роман\\Projects\\Avtovitrina_pyqt\\#id"></td>
                </tr>
                <tr>
                    <td>
                        <h1 class="name">Название</h1>
                    </td>
                    <td>
                        <h1 class="name">#name1</h1>
                    </td>
                </tr>
                <tr>
                    <td>
                        <h1 class="kuzov">Кузов</h1>
                    </td>
                    <td>
                        <h1 class="kuzov">#kuzov1</h1>
                    </td>
                </tr>
                <tr>
                    <td>
                        <h1 class="year">Год выпуска</h1>
                    </td>
                    <td>
                        <h1 class="year">#year1</h1>
                    </td>
                </tr>
                <tr>
                    <td>
                        <h1 class="drive">Привод</h1>
                    </td>
                    <td>
                        <h1 class="drive">#drive1</h1>
                    </td>
                </tr>"""
            html_table_result = ""
            for i in range(len(result)):
                html_table = html_table_parent
                html_table = html_table.replace("#id", self.dict_of_cars[int(str(result[i][0]))])
                html_table = html_table.replace("#name1", str(result[i][1]))
                html_table = html_table.replace("#kuzov1", str(result[i][2]))
                html_table = html_table.replace("#year1", str(result[i][3]))
                html_table = html_table.replace("#drive1", str(result[i][4]))
                html_table_result += html_table
            html_content = """
                <!DOCTYPE html>
                    <html lang="ru">
                    <head>
                    <meta charset="UTF-8">
                    </head>
                    <body>
                    <table style="height:100%;
                                width:100%;
                                position: absolute;
                                top: 0;
                                bottom: 0;
                                left: 0;
                                right: 0">
                            <style> table 
                                        {
                                            background: #1e213e;
                                        }

                                    td
                                        {
                                            color: #CAD4D6;
                                        }
                                    h1
                                        {
                                            text-align: center;
                                            color: #f2f2f2;
                                        }

                                    caption
                                        {
                                            background:#c74343;
                                        }

                                    .photo
                                        {
                                            background: #252F48;
                                            text-align: center;
                                        }

                                    .name
                                        {
                                            background: #5c84ab;
                                        }

                                    .kuzov
                                        {
                                            background: #5c84ab;
                                        }

                                    .year
                                        {
                                            background: #5c84ab
                                        }
                                    .drive
                                        {
                                            background: #5c84ab
                                        }
                            </style>
                        <caption><h1>Найдено:</h1></caption>""" + html_table_result + """</table>
                    </body>
                    </html>"""      
            self.web_view.setHtml(html_content, baseUrl=QUrl('file:'))

    def check_button_cuzov(self):
        for button in self.list_btns:
            if button.isChecked():
                self.mark_box.clear()
                self.model_box.clear()
                self.data_base()
                con = sqlite3.connect("cars_db.sqlite")
                cur = con.cursor()
                btn_text = button.text().lower()
                result = cur.execute("""SELECT id, name, kuzov, year, drive FROM specifications WHERE kuzov = ?""", (btn_text,)).fetchall()
                html_table_parent = """
                    <tr>
                        <td class="photo"><h1>Фото</h1></td>
                        <td class="photo"><img src="file://C:\\Users\\Роман\\Projects\\Avtovitrina_pyqt\\#id"></td>
                    </tr>
                    <tr>
                        <td>
                            <h1 class="name">Название</h1>
                        </td>
                        <td>
                            <h1 class="name">#name1</h1>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <h1 class="kuzov">Кузов</h1>
                        </td>
                        <td>
                            <h1 class="kuzov">#kuzov1</h1>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <h1 class="year">Год выпуска</h1>
                        </td>
                        <td>
                            <h1 class="year">#year1</h1>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <h1 class="drive">Привод</h1>
                        </td>
                        <td>
                            <h1 class="drive">#drive1</h1>
                        </td>
                    </tr>"""
                html_table_result = ""
                for i in range(len(result)):
                    html_table = html_table_parent
                    html_table = html_table.replace("#id", self.dict_of_cars[int(str(result[i][0]))])
                    html_table = html_table.replace("#name1", str(result[i][1]))
                    html_table = html_table.replace("#kuzov1", str(result[i][2]))
                    html_table = html_table.replace("#year1", str(result[i][3]))
                    html_table = html_table.replace("#drive1", str(result[i][4]))
                    html_table_result += html_table
                html_content = """
                    <!DOCTYPE html>
                    <html lang="ru">
                    <head>
                    <meta charset="UTF-8">
                    </head>
                    <body>
                    <table style="height:100%;
                                width:100%;
                                position: absolute;
                                top: 0;
                                bottom: 0;
                                left: 0;
                                right: 0">
                            <style> table 
                                        {
                                            background: #1e213e;
                                        }

                                    td
                                        {
                                            color: #CAD4D6;
                                        }
                                    h1
                                        {
                                            text-align: center;
                                            color: #f2f2f2;
                                        }

                                    caption
                                        {
                                            background:#c74343;
                                        }

                                    .photo
                                        {
                                            background: #252F48;
                                            text-align: center;
                                        }

                                    .name
                                        {
                                            background: #5c84ab;
                                        }

                                    .kuzov
                                        {
                                            background: #5c84ab;
                                        }

                                    .year
                                        {
                                            background: #5c84ab
                                        }
                                    .drive
                                        {
                                            background: #5c84ab
                                        }
                            </style>
                        <caption><h1>Найдено:</h1></caption>""" + html_table_result + """</table>
                    </body>
                    </html>"""
                self.web_view.setHtml(html_content, baseUrl=QUrl('file:'))
                break