#!/usr/bin/env python3

from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QApplication,QRadioButton,
                             QTextEdit, QComboBox, QLineEdit,QCheckBox,
                             QGridLayout, qApp, QFileDialog)
import sys, os, csv, requests
from tqdm import tqdm


class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.anime()


    def anime(self):

        grid = QGridLayout()
        grid.setSpacing(20)

        btns = ["Check for Episodes", "Open"]
        # btns = ["Check for Episodes", "Open", "Download selected \nEpisodes"]
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
        #self.dl_options = [QCheckBox(i) for i in options]
        self.dl_options = [QRadioButton(i) for i in options]
        self.anime_btns[0].clicked.connect(self.get_info)
        self.anime_btns[1].clicked.connect(self.selectfolder)
        # self.anime_btns[2].clicked.connect(self.download_episode)

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
            # grid.addWidget(self.anime_btns[2],8,2)
        for i in range(len(self.dl_options)):
            grid.addWidget(self.dl_options[i],i+4,2)

        self.show()


    def download_episode(self,path,url):
        episode_no = url.split('--')[1]
        print("Downloading episode no {}".format(episode_no))
        name = "{}/Episode-{}.mp4".format(path,episode_no)
        try:
            response = requests.get(url, stream=True)
        except requests.RequestException:
            print(requests.RequestException)
            sys.exit(1)

        scale_factor = 1
        chunk_size = 1024 * 1024 * scale_factor
        total_size = int(response.headers.get('content-length', 0))
        total = round(total_size / chunk_size)
        with open(name, 'wb') as episode_file:
            for data in tqdm(response.iter_content(chunk_size), total=total, unit=' MB'):
                episode_file.write(data)

    def get_info(self):
        self.anime_labls[2].setText("HANG 0N Parsing site and making Downloads R3ADY")
        self.path = os.path.dirname(os.path.abspath('__file__'))
        os.chdir(self.path)
        print(self.path)
        seriesurl = self.urlLE.text()
        os.system("python3 get_epi_filelist.py {}".format(seriesurl))

        print("Selected anime series url is {}".format(seriesurl))

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
        print("Selected folder for downloaded episode(s) is {} ".format(self.dldir))

        for i in self.epi_nos:
            self.one.addItem(str(i))

        # self.dl_options[0].stateChanged.connect(self.dl_one)
        # self.dl_options[1].stateChanged.connect(self.dl_few)
        # self.dl_options[2].stateChanged.connect(self.dl_all)


        self.dl_options[0].toggled.connect(lambda:self.dl_one(self.dl_options[0]))
        self.dl_options[1].toggled.connect(lambda:self.dl_few(self.dl_options[1]))
        self.dl_options[2].toggled.connect(lambda:self.dl_all(self.dl_options[2]))

    def dl_one(self,check):
        if check.isChecked():
            one_Epi = int(self.one.currentText())
            print(one_Epi)
            if one_Epi in self.epi_nos:
                self.download_episode(self.dldir, self.epi_urls[one_Epi-1])

    def dl_few(self,check):
        if check.isChecked():
            few_list = self.someLE.text().split(",")
            print("Selected Episodes are {}".format(few_list))
            for i in few_list:
                self.download_episode(self.dldir, self.epi_urls[int(i)-1])


    def dl_all(self,check):
        if check.isChecked():
            all_list = [i for i in range(1,len(self.epi_urls))]
            print("Takes lot of time and data to Download all Episodes ..HANG ON ...")
            for i in self.epi_urls:
                self.download_episode(self.dldir, i)


app = QApplication(sys.argv)
tickets = Window()
sys.exit(app.exec_())
