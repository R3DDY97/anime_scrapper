#!/usr/bin/env python3

from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QApplication,
                             QTextEdit, QComboBox, QLineEdit,QCheckBox,
                             QGridLayout, qApp, QFileDialog)
import sys, os, csv

class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.anime()

    def anime(self):

        grid = QGridLayout()
        grid.setSpacing(20)

        btns = ["Check for Episodes", "Open", "Download selected \nEpisodes"]
        options = ["One Episode", "Few Episodes", "All Episodes"]
        labels = ["Enter anime series  url having all episodes list ",
                  "Select folder to save downoladed episodes ",
                  "Hang on takes time to parse and get all Episodes Download Links",
                  "Enter episode numbers to download"]
        self.urlLE = QLineEdit()
        self.one = QComboBox()
        self.someLE = QLineEdit()
        self.anime_labls = [QLabel(i) for i in labels]
        self.anime_btns = [QPushButton(i) for i in btns]
        self.dl_options = [QCheckBox(i) for i in options]
        self.anime_btns[0].clicked.connect(self.get_info)
        self.anime_btns[1].clicked.connect(self.selectfolder)

        self.setLayout(grid)
        self.setWindowTitle("Anime scrapper")
        # self.setGeometry(300,100,300,300)
        grid.addWidget(self.anime_labls[0],0,1)
        grid.addWidget(self.anime_labls[1],3,1)
        grid.addWidget(self.anime_labls[2],2,1)
        grid.addWidget(self.anime_labls[3],4,1)

        grid.addWidget(self.urlLE,1,1)
        grid.addWidget(self.one,4,3)
        grid.addWidget(self.someLE,5,3)

        for i in range(len(self.anime_btns)):
            grid.addWidget(self.anime_btns[0],1,2)
            grid.addWidget(self.anime_btns[1],3,2)
            grid.addWidget(self.anime_btns[2],8,2)
        for i in range(len(self.dl_options)):
            grid.addWidget(self.dl_options[i],i+4,2)

        self.show()

    def get_info(self):

        self.path = os.path.dirname(__file__)
        os.chdir(self.path)
        seriesurl = self.urlLE.text()
        print("Selected anime series url is {}".format(seriesurl))
        os.system("python3 get_epi_filelist.py {}".format(seriesurl) )
        self.anime_labls[2].setText("HANG 0N Parsing site and making Downloads R3ADY")
        with open("Episode_Download_Links.csv", "r") as epis:
            Info = csv.reader(epis)
            self.episode_no_urls = list(Info)
        self.epi_no_urls = [[int(i),j] for i,j in self.episode_no_urls]
        self.epi_no_urls.sort()
        self.epi_urls = [i[1] for i in self.epi_no_urls]
        print(self.epi_urls)
        self.epi_nos = [i[0] for i in self.epi_no_urls]
        print(self.epi_nos)
        self.anime_labls[2].setText("Total Episodes are {}".format(len(self.epi_nos)))

    def selectfolder(self):

        self.dldir = QFileDialog.getExistingDirectory(self, "Select Folder to save episodes", os.getenv(self.path))

        for i in self.epi_nos:
            self.one.addItem(i)

        self.dl_options[0].stateChanged.connect(self.dl_one)
        self.dl_options[1].stateChanged.connect(self.dl_few)
        self.dl_options[2].stateChanged.connect(self.dl_all)

    def dl_one(self):
        one_Epi = self.one.currentText()
        print(one_Epi)
        if one_Epi in self.epi_nos:
            for_GUI.download_episode(self.dldir, self.epi_urls[int(one_Epi)-1])

    def dl_few(self):
        few_list = self.someLE.text().split(",")
        print(few_list)
        for i in few_list:
            for_GUI.download_episode(self.dldir, self.epi_urls[int(i)-1])


    def dl_all(self):
        all_list = [i for i in range(1,len(self.epi_urls))]
        print(all_list)
        print("Takes lot of time and data to Download all Episodes ..HANG ON ...")
        for i in self.epiurls:
            for_GUI.download_episode(self.dldir, i)


app = QApplication(sys.argv)
tickets = Window()
sys.exit(app.exec_())
