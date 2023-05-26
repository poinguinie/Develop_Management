'''
    Download Link
        http://poinguinie.dothome.co.kr/data/work_tool.zip
'''

import sys
import os
import urllib.request
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget
from Crawler import Crawler
from StlCrawler import Crawler as sc

class MainWindow(QMainWindow):
    # 생성자
    def __init__(self, debug = False) -> None:
        super().__init__()
        self.initVariable(debug)
        self.initFont()
        self.initUI()

    # 변수 초기화 메서드
    def initVariable(self, debug):
        self.lang_hash = {
            "C++" : "cpp",
            "C" : "c",
            "C#" : "cs",
            "Java" : "java",
            "JavaScript" :"javascript",
            "Python" : "python"
        }
        self.extention = {
            "cpp": "cc",
            "c": "c",
            "cs": "cs",
            "java": "java",
            "javascript": "js",
            "python": "py"
        }
        self.selectedLanguage = "cpp"
        self.DEBUG = debug
        self.crawler = None
        self.status = None
        self.isCalled = False
        self.currentTabIdx = 0
        self.maxTabIdx = 4
        self.stl_selected = "vector"
        self.stl_clawler = sc()
        self.stl_clawler.connect(self.stl_selected)
        self.links = []

    # 폰트 설정 메서드
    def initFont(self):
        self.fontDB = QFontDatabase()

        fonts = os.listdir("fonts")
        # 0 : black, 1 : bold, 2 : light, 3 : medium, 4 : regular, 5 : thin
        fonts_title = ["Black", "Bold", "Light" ,"Medium", "Regular", "Thin"]
        self.fonts = {}
        for i, font in enumerate(fonts):
            self.fontDB.addApplicationFont("./fonts/%s" % font)
            self.fonts[fonts_title[i]] = font
        # fontDB.addApplicationFont("./fonts/NotoSansKR-Regular.otf")

    # 전체 UI 생성 메서드
    def initUI(self):
        # MenuBar 설정
        self.initMenuBar()

        self.tabs = QTabWidget()

        # UI 설정
        self.initMainUI()
        self.initFakerUI()
        self.initFaker2UI()
        # self.initFaker3UI()
        
        # Tabs 설정
        self.initTabs()        
        
        self.setCentralWidget(self.tabs)

        # self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Set Genaral Infomation (Title, Size, Position, Icon)
        self.setWindowTitle("Programmers Tool")
        self.setGeometry(100, 100, 1580, 800)
        self.setWindowIcon(QIcon("./images/program.ico"))

        self.show()

    # Tabs 정보 초기화 메서드
    def initTabs(self):
        self.tabs.addTab(self.faker_main_widget, "Data Type")
        self.tabs.addTab(self.faker_main_2_widget, "STL")
        # self.tabs.addTab(self.faker_main_3_widget, "Shell Script")
        self.tabs.addTab(self.main_widget, "Setting")

        tabsChangedAction = QAction("Tab Change Event", self)
        tabsChangedAction.setShortcut("tab")
        tabsChangedAction.triggered.connect(self.tabEvent)

        # self.tabs.setCurrentIndex(self.currentTabIdx)
        self .tabs.addAction(tabsChangedAction)

    # Tabs 이벤트 (tab 클릭) 메서드
    def tabEvent(self):
        self.currentTabIdx += 1
        if self.currentTabIdx == 3:
            self.currentTabIdx = 0
        self.tabs.setCurrentIndex(self.currentTabIdx)

    # 메뉴바 초기화 메서드
    def initMenuBar(self):
        # 메뉴바 변수 정의
        self.menubar = self.menuBar()
        self.menubar.setNativeMenuBar(False)

        # 메뉴 정의
        filemenu = self.menubar.addMenu("&File")
        helpmenu = self.menubar.addMenu("&Help")

        # Label, Layout Widget Reset Action 정의
        settingResetAction = QAction('Setting Reset', self)
        settingResetAction.setShortcut('Ctrl+R')
        settingResetAction.triggered.connect(self.initLabel)

        # Output 폴더 생성 Action 정의
        openFolderAction = QAction('Open Folder', self)
        openFolderAction.setShortcut('Ctrl+O')
        openFolderAction.triggered.connect(lambda : os.startfile(os.getcwd() + "/output/"))

        # Exit Action 정의
        exitAction = QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(qApp.exit)

        # Action 추가 (File Menu)
        filemenu.addAction(settingResetAction)
        filemenu.addAction(openFolderAction)
        filemenu.addAction(exitAction)

        # 릴리즈 노트 페이지 Action 정의
        releaseNoteAction = QAction('Release Note', self)
        shortCutAction = QAction('Short Cut List', self)

        # Action 추가 (Help Menu)
        helpmenu.addAction(releaseNoteAction)      
        helpmenu.addAction(shortCutAction)  

    # 메인 UI 생성 메서드
    def initMainUI(self):
        self.main_widget = QWidget()

        # Main Layout
        self.main_layout = QVBoxLayout(self.main_widget)

        # URL AREA
        self.url_area = QHBoxLayout()

        url_area_height = 30

        self.language_label = QLabel("언어 : ")

        self.language_comboBox = QComboBox()
        self.language_comboBox.addItems(["C++", "C", "C#", "Java" ,"JavaScript", "Python"])

        self.language_comboBox.currentTextChanged.connect(self.selectLang)
        self.language_comboBox.setFixedWidth(120)
        self.language_comboBox.setFixedHeight(url_area_height - 4)

        self.url_edit = QLineEdit(self)
        self.url_edit.setMaximumWidth(450)
        self.url_edit.setFixedWidth(500)
        self.url_edit.setFixedHeight(url_area_height)
        self.url_edit.setPlaceholderText("Enter the URL...")

        if self.DEBUG:
            self.url_edit.setText("https://school.programmers.co.kr/learn/courses/30/lessons/181186")

        self.url_btn = QPushButton("검색")
        self.url_btn.setCheckable(True)
        self.url_btn.setFixedWidth(120)
        self.url_btn.setFixedHeight(url_area_height)

        self.url_btn.clicked.connect(self.getUrlInfo)

        self.url_area.addStretch(3)
        self.url_area.addWidget(self.language_label)
        self.url_area.addWidget(self.language_comboBox)

        self.url_area.addStretch(1)
        self.url_area.addWidget(self.setSeparatorVLine())
        self.url_area.addStretch(1)

        self.url_area.addWidget(self.url_edit)
        self.url_area.addStretch(1)
        self.url_area.addWidget(self.url_btn)
        self.url_area.addStretch(3)

        self.main_layout.addLayout(self.url_area)

        # Content Area
        self.content_area = QVBoxLayout()

        ## Result Area
        self.result_area = QHBoxLayout()

        ### Information Area
        self.info_area = QScrollArea()
        '''
            문제 제목
            문제 설명
            제한 사항
            예제 입출력 (자세히 보기 버튼)
        '''
        self.scroll_info_area = QScrollArea()
        self.info_group_box = QGroupBox()

        self.info_layout = QFormLayout()

        self.title_t = QLabel("문제 제목")
        self.title_t.setFont(QFont(self.fonts["Bold"], 10))
        self.title = QLabel()
        
        self.desc_t = QLabel("\n문제 설명")
        self.desc_t.setFont(QFont(self.fonts["Bold"], 10))
        self.desc = QVBoxLayout()

        self.restrictions_t = QLabel("\n제한 사항")
        self.restrictions_t.setFont(QFont(self.fonts["Bold"], 10))
        self.restrictions = QVBoxLayout()

        self.io_examples_t = QLabel("\n입출력 예제")
        self.io_examples_t.setFont(QFont(self.fonts["Bold"], 10))
        self.io_examples = QGridLayout()

        self.io_examples_desc_t = QLabel("\n입출력 예제 설명")
        self.io_examples_desc_t.setFont(QFont(self.fonts["Bold"], 10))
        self.io_examples_desc = QVBoxLayout()

        # 문제 제목
        self.info_layout.addRow(self.title_t)
        self.info_layout.addRow(self.setSeparatorHLine())
        self.info_layout.addRow(self.title)

        # 문제 설명
        self.info_layout.addRow(self.desc_t)
        self.info_layout.addRow(self.setSeparatorHLine())
        self.info_layout.addRow(self.desc)

        # 제한 사항
        self.info_layout.addRow(self.restrictions_t)
        self.info_layout.addRow(self.setSeparatorHLine())
        self.info_layout.addRow(self.restrictions)

        # 예제 입출력
        self.info_layout.addRow(self.io_examples_t)
        self.info_layout.addRow(self.setSeparatorHLine())
        self.info_layout.addRow(self.io_examples)

        # 예제 입출력 설명
        self.info_layout.addRow(self.io_examples_desc_t)
        self.info_layout.addRow(self.setSeparatorHLine())
        self.info_layout.addRow(self.io_examples_desc)

        # 정보 Group Box, Scroll Area 레이아웃 설정
        self.info_group_box.setLayout(self.info_layout)
        self.scroll_info_area.setWidget(self.info_group_box)
        self.scroll_info_area.setWidgetResizable(True)        

        ### Code Area
        # self.code_scroll_area = QScrollArea()
        self.code_area = QVBoxLayout()

        self.code_label = QLabel("코드")

        self.code_text_area = QTextEdit()
        self.code_text_area.setFixedWidth(600)

        self.code_area.addWidget(self.code_label)
        self.code_area.addWidget(self.code_text_area)

        # self.code_scroll_area.setLayout(self.code_area)

        ## Download Button Area
        self.download_btn_area = QHBoxLayout()

        buttonWeight = 300
        buttonHeight = 40

        self.btn1 = QPushButton("문제 설명 다운로드 ( .txt )")
        self.btn2 = QPushButton("문제 설명 다운로드 ( .md  )")
        self.btn3 = QPushButton("문제 코드 다운로드")

        self.btn1.clicked.connect(self.download2txt)
        self.btn2.clicked.connect(self.download2md)
        self.btn3.clicked.connect(self.download2code)

        # 버튼 크기 조정 (300, 40)
        self.btn1.setFixedWidth(buttonWeight)
        self.btn2.setFixedWidth(buttonWeight)
        self.btn3.setFixedWidth(buttonWeight)

        self.btn1.setFixedHeight(buttonHeight)
        self.btn2.setFixedHeight(buttonHeight)
        self.btn3.setFixedHeight(buttonHeight)

        # 다운로드 버튼 레이아웃 설정
        self.download_btn_area.addStretch(4)
        self.download_btn_area.addWidget(self.btn1)
        self.download_btn_area.addStretch(1)
        self.download_btn_area.addWidget(self.btn2)
        self.download_btn_area.addStretch(1)
        self.download_btn_area.addWidget(self.btn3)
        self.download_btn_area.addStretch(4)

        # 전체 레이아웃 설정        
        self.result_area.addWidget(self.scroll_info_area)
        self.result_area.addWidget(self.setSeparatorVLine())
        # self.result_area.addWidget(self.code_scroll_area)
        self.result_area.addLayout(self.code_area)

        self.content_area.addLayout(self.result_area)
        self.content_area.addWidget(self.setSeparatorHLine())
        self.content_area.addLayout(self.download_btn_area)

        self.main_layout.addWidget(self.setSeparatorHLine())

        self.main_layout.addLayout(self.content_area)

        # self.setLayout(self.main_layout)

    # Faker UI 생성 메서드 (Type Define)
    def initFakerUI(self):
        self.faker_main_widget = QWidget()

        self.faker_main_layout = QVBoxLayout()

        self.scroll_box = QScrollArea()

        # self.type_group_box = QGroupBox()        

        self.type_table_layout = QGridLayout()

        type_def = [
            ["구분", "자료형", "크기", "범위"],
            ["문자형", "(signed) char", "1 Byte", "-128 ~ 127"],
            ["문자형", "unsigned char",	"1 Byte", "0 ~ 255"],
            ["문자형", "wchar_t", "2 Byte", "0 ~ 65,535"],
            ["정수형", "bool", "1 Byte", "0 ~ 1"],
            ["정수형", "(signed) short (int)", "2 Byte", "-32,768 ~ 32,767"],
            ["정수형", "unsigned short (int)", "4 Byte", "0 ~ 65,535"],
            ["정수형", "(signed) int", "4 Byte", "-2,147,483,648 ~ 2,147,483,647"],
            ["정수형", "unsigned int", "4 Byte", "0 ~ 4,294,967,295"],
            ["정수형", "(signed) long (int)", "4 Byte", "-2,147,483,648 ~ 2,147,483,647"],
            ["정수형", "unsigned long (int)", "4 Byte", "0 ~ 4,294,967,295"],
            ["정수형", "__int8", "1 Byte", "-128 ~ 127"],
            ["정수형", "__int16", "2 Byte", "-32,768 ~ 32,767"],
            ["정수형", "__int32", "4 Byte", "-2,147,483,648 ~ 2,147,483,647"],
            ["정수형", "__int64", "8 Byte", "-9,223,372,036,854,775,808 ~ 9,223,372,036,854,775,807"],
            ["실수형", "float", "4 Byte", "3.4E-38(-3.4*10^38) ~ 3.4E+38(3.4*10^38) (7digits)"],
            ["실수형", "(long) double", "8 Byte", "1.79E-308(-1.79*10^308) ~ 1.79E+308(1.79*10^308) (15digits)"]
        ]

        for i, t in enumerate(type_def):
            for j, item in enumerate(t):
                if i == 0:
                    label = QLabel(item)
                    label.setFixedHeight(30)
                    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    label.setFont(QFont(self.fonts["Bold"], 11))
                else:
                    if j == 3:
                        label = QLineEdit()
                        label.setText(item)
                        label.setFixedWidth(600)
                    else:
                        label = QLabel(item)
                        label.setFont(QFont(self.fonts["Regular"], 10))
                    label.setFixedHeight(25)
                self.type_table_layout.addWidget(label, i, j)

        # self.type_group_box.setLayout(self.type_table_layout)
        self.scroll_box.setLayout(self.type_table_layout)
        self.scroll_box.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.faker_main_layout.addWidget(self.scroll_box)

        self.faker_main_widget.setLayout(self.faker_main_layout)

    # Faker UI 생성 메서드 (STL)
    def initFaker2UI(self):
        self.faker_main_2_widget = QWidget()

        self.faker_main_2_layout = QVBoxLayout()

        self.stl_top_layout = QHBoxLayout()
        
        self.stl_comboBox = QComboBox()
        self.stl_comboBox.setFixedSize(300, 40)
        self.stl_comboBox.addItems([
            "Vector",
            "Array",
            "Queue",
            "Stack",
            "Deque",
            "Set",
            "Map",
        ])
        
        self.stl_comboBox.currentTextChanged.connect(self.stl_selected_event)

        self.stl_info_reset_btn = QPushButton("Information Reset")
        self.stl_info_reset_btn.setFixedSize(200, 45)

        self.stl_info_reset_btn.clicked.connect(lambda: self.clearStlInfo())

        self.stl_top_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.stl_top_layout.addSpacing(10)
        self.stl_top_layout.addWidget(self.stl_comboBox)
        self.stl_top_layout.addStretch(1)
        self.stl_top_layout.addWidget(self.stl_info_reset_btn)
        self.stl_top_layout.addSpacing(10)
        
        self.stl_info_group_box = QGroupBox("Vector")

        self.stl_info_layout = QHBoxLayout()

        # Information Layout (Left) -> Scroll Area
        ## Method List
        self.stl_info_left_scroll_area = QScrollArea()
        self.stl_info_left_scroll_area.setFixedWidth(400)
        self.stl_info_left_scroll_area.setAlignment(Qt.AlignmentFlag.AlignHCenter or Qt.AlignmentFlag.AlignTop)
        self.stl_info_left_scroll_area.setWidgetResizable(True)
        self.stl_info_left_group_box = QGroupBox()
        self.stl_info_left_group_box.setFixedWidth(350)
        self.stl_info_left_layout = QVBoxLayout()
        self.stl_info_left_layout.setAlignment(Qt.AlignmentFlag.AlignCenter or Qt.AlignmentFlag.AlignTop)

        self.setUI_Stl()

        self.stl_info_left_group_box.setLayout(self.stl_info_left_layout)

        self.stl_info_left_scroll_area.setWidget(self.stl_info_left_group_box)

        # Information Layout (Right) -> Scroll Area
        ## Method Detail Information
        # self.stl_info_right_info_layout = QVBoxLayout()
        # self.stl_info_right_info_layout.
        self.stl_info_right_info_scroll_area = QScrollArea()
        self.stl_info_right_info_scroll_area.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))

        self.stl_info_right_group_box = QGroupBox()
        self.stl_info_right_group_layout = QFormLayout()

        # self.stl_info_right_group_box.setFixedSize(600, 600)
        ## Right Information Area Widget
        self.stl_info_right_title_t = QLabel("Title")
        self.changeFontSize(self.stl_info_right_title_t, 12)
        self.stl_info_right_title = QLabel()

        self.stl_info_right_desc_t = QLabel("Description")
        self.changeFontSize(self.stl_info_right_desc_t, 12)
        self.stl_info_right_desc = QLabel()

        self.stl_info_right_param_t = QLabel("Parameters")
        self.changeFontSize(self.stl_info_right_param_t, 12)
        self.stl_info_right_param = QLabel()

        self.stl_info_right_return_t = QLabel("Return Value")
        self.changeFontSize(self.stl_info_right_return_t, 12)
        self.stl_info_right_return = QLabel()

        self.stl_info_right_code_t = QLabel("Example Code")
        self.changeFontSize(self.stl_info_right_code_t, 12)
        self.stl_info_right_code = QLabel()

        self.stl_info_right_output_t = QLabel("Output")
        self.changeFontSize(self.stl_info_right_output_t, 12)
        self.stl_info_right_output = QLabel()

        ## AddWidget
        self.stl_info_right_group_layout.addRow(self.stl_info_right_title_t)
        self.stl_info_right_group_layout.addRow(self.setSeparatorHLine())
        self.stl_info_right_group_layout.addRow(self.stl_info_right_title)
        self.stl_info_right_group_layout.addRow(QLabel("\n"))

        self.stl_info_right_group_layout.addRow(self.stl_info_right_desc_t)
        self.stl_info_right_group_layout.addRow(self.setSeparatorHLine())
        self.stl_info_right_group_layout.addRow(self.stl_info_right_desc)
        self.stl_info_right_group_layout.addRow(QLabel("\n"))

        self.stl_info_right_group_layout.addRow(self.stl_info_right_param_t)
        self.stl_info_right_group_layout.addRow(self.setSeparatorHLine())
        self.stl_info_right_group_layout.addRow(self.stl_info_right_param)
        self.stl_info_right_group_layout.addRow(QLabel("\n"))

        self.stl_info_right_group_layout.addRow(self.stl_info_right_return_t)
        self.stl_info_right_group_layout.addRow(self.setSeparatorHLine())
        self.stl_info_right_group_layout.addRow(self.stl_info_right_return)
        self.stl_info_right_group_layout.addRow(QLabel("\n"))

        self.stl_info_right_group_layout.addRow(self.stl_info_right_code_t)
        self.stl_info_right_group_layout.addRow(self.setSeparatorHLine())
        self.stl_info_right_group_layout.addRow(self.stl_info_right_code)
        self.stl_info_right_group_layout.addRow(QLabel("\n"))

        self.stl_info_right_group_layout.addRow(self.stl_info_right_output_t)
        self.stl_info_right_group_layout.addRow(self.setSeparatorHLine())
        self.stl_info_right_group_layout.addRow(self.stl_info_right_output)
        self.stl_info_right_group_layout.addRow(QLabel("\n"))

        self.stl_info_right_group_box.setLayout(self.stl_info_right_group_layout)

        # self.stl_info_right_group_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        # self.stl_info_right_group_box.setFixedWidth(1000)

        self.stl_info_right_info_scroll_area.setWidget(self.stl_info_right_group_box)
        self.stl_info_right_info_scroll_area.setWidgetResizable(True)
        # self.stl_info_right_info_scroll_area.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))

        
        # print(self.stl_info_right_group_box.sizePolicy().setHorizontalPolicy(QSizePolicy.Policy.Expanding))    

        # Add Widget in Layout (Full)
        self.stl_info_layout.addWidget(self.stl_info_left_scroll_area)
        self.stl_info_layout.addWidget(self.setSeparatorVLine())
        self.stl_info_layout.addWidget(self.stl_info_right_info_scroll_area)

        # Add Layout in Group Box (Information)
        self.stl_info_group_box.setLayout(self.stl_info_layout)

        # Main Layout Setting
        self.faker_main_2_layout.addLayout(self.stl_top_layout)
        self.faker_main_2_layout.addWidget(self.stl_info_group_box)

        self.faker_main_2_widget.setLayout(self.faker_main_2_layout)

    # STL ComboBox 선택 이벤트 메서드
    def stl_selected_event(self, selected):
        self.stl_selected = selected.lower()
        self.stl_info_group_box.setTitle(selected)

        self.stl_clawler.connect(selected)

        self.clearLayout(self.stl_info_left_layout)
        
        self.setUI_Stl()

    # STL UI 설정 메서드
    def setUI_Stl(self):
        self.links.clear()
        for i, function in enumerate(self.stl_clawler.functions_data):
            #   print(function["link"])
            link = function["link"]
            # print(link)
            # print(link)
            self.links.append(link)
            item = QPushButton(str(i+1) + "." + function["title"])
            # item.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
            
            # item = QPushButton(function["title"])
            item.setFixedSize(320, 80)
            # item.clicked.connect(self.clickedFunction(parse.urlencode(function["link"])))
            item.pressed.connect(self.clickedFunction)

            self.stl_info_left_layout.addWidget(item)

    # Function QPushButton 클릭 이벤트 메서드
    def clickedFunction(self):
        btn = self.sender()
        idx = int(btn.text().split(".")[0]) - 1
        url = self.links[idx]
        self.stl_clawler.connect(self.stl_selected, url)
        # print(self.stl_clawler.detail_data)
        # Title, Description, Parameters, Return_Value, Example_code, Example_output
        self.stl_info_right_title.setText(self.stl_clawler.detail_data["title"])
        self.stl_info_right_desc.setText(self.stl_clawler.detail_data["description"])
        self.stl_info_right_param.setText(self.stl_clawler.detail_data["parameters"])
        self.stl_info_right_return.setText(self.stl_clawler.detail_data["return_value"])
        self.stl_info_right_code.setText(self.stl_clawler.detail_data["example_code"])
        self.stl_info_right_output.setText(self.stl_clawler.detail_data["example_output"])

    # STL Information Area Clear 메서드
    def clearStlInfo(self):
        self.stl_info_right_title.setText("")
        self.stl_info_right_desc.setText("")
        self.stl_info_right_param.setText("")
        self.stl_info_right_return.setText("")
        self.stl_info_right_code.setText("")
        self.stl_info_right_output.setText("")

    # Faker UI 생성 메서드 (Shell Script)
    def initFaker3UI(self):
        self.faker_main_3_widget = QWidget()

    # 언어 변경 메서드
    def selectLang(self, item):
        self.selectedLanguage = self.lang_hash[item]
        # print(self.selectedLanguage)

    # URL Crawling 실행 메서드
    def getUrlInfo(self):
        # URL 검사
        if self.url_edit.text() == "":
            QMessageBox.warning(self, "오류" ,"URL을 입력해주세요")
            return False
        if self.url_edit.text().find("https://school.programmers.co.kr/learn/") == -1:
            QMessageBox.warning(self, "오류" ,"잘못된 URL 형식입니다.")
            return False

        # 현재 호환 언어 : C++
        if self.selectedLanguage != "cpp":
            QMessageBox.warning(self, "오류" ,"해당 언어는 현재 호환되지 않습니다.")
            return False        
        
        # 각 라벨 초기화
        self.initLabel()

        self.isCalled = True
        
        # Crawler 객체 생성
        self.crawler = Crawler(self.url_edit.text(), self.selectedLanguage)

        self.status = self.crawler.status_code
        # 네트워크 접속 실패
        if self.status != 200:
            QMessageBox.warning(self, "오류" ,"해당 문제를 불러오는 데 실패했습니다.")
            return False
        
        reponse = self.crawler.setMainFunction()

        if reponse == False:
            QMessageBox.warning(self, "오류" ,"지원하지 않는 언어입니다.")
            return False
        
        # 정보 출력
        ## 문제 제목 출력
        self.title.setText(self.crawler.title)

        ## 문제 설명 출력
        for problem_desc in self.crawler.problem_desc:
            if problem_desc.find("image_url:") == -1:
                self.desc.addWidget(QLabel(problem_desc))
            else:
                # 이미지 출력
                self.desc.addWidget(self.drawImage(problem_desc))                

        ## 제한 사항 출력
        for restriction in self.crawler.restrictions:
            self.restrictions.addWidget(QLabel(restriction))

        ## 입출력 예제 출력
        ioExample_title = self.crawler.ioExample_list[0]
        ioExamples = self.crawler.ioExample_list[1:]

        ### 입출력 예제 변수명 출력
        for i in range(len(ioExample_title)):
            self.io_examples.addWidget(QLabel(ioExample_title[i]), 0, i)

        ### 입출력 예제 요소 출력
        for i in range(len(ioExamples)):
            for j in range(len(ioExamples[i])):
                btn = QLabel(ioExamples[i][j])
                btn.setFixedSize(60, 20)
                self.io_examples.addWidget(btn, i + 1, j)

        ## 입출력 예제 설명 출력
        for desc in self.crawler.example_desc:
            if desc.find("입출력 예 #") != -1:
                label = QLabel(desc)
                label.setFont(QFont(self.fonts["Bold"], 10))
                self.io_examples_desc.addWidget(label)
            elif desc.find("image_url") != -1:
                # 이미지 출력
                self.io_examples_desc.addWidget(self.drawImage(desc))
            else:
                self.io_examples_desc.addWidget(QLabel(desc))
        
        ## 코드 출력
        self.code_text_area.setText(self.crawler.code.strip())

    # 문제 정보 Clear 메서드
    def initLabel(self):
        if self.isCalled == False:
            return False
        self.title.setText("")
        self.clearLayout(self.desc)
        self.clearLayout(self.restrictions)
        self.clearLayout(self.io_examples)
        self.clearLayout(self.io_examples_desc)
        self.code_text_area.setText("")

    # 레이아웃 내 요소 삭제 메서드
    def clearLayout(self, layout):
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().deleteLater()

    # PyQT5 윈도우에 이미지 그리는 메서드
    def drawImage(self, desc):
        url = desc[10:]
        data = urllib.request.urlopen(url).read()
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        pixmap.scaledToHeight(500)
        label = QLabel()
        label.setPixmap(pixmap.scaled(label.width(), label.height(), Qt.KeepAspectRatio))
        return label

    # 수평 구분선 메서드
    def setSeparatorHLine(self):
        separatorLine = QFrame()
        separatorLine.setFrameShape(QFrame.HLine)
        separatorLine.setFrameShadow(QFrame.Sunken)

        return separatorLine
    
    # 수직 구분선 메서드
    def setSeparatorVLine(self):
        separatorLine = QFrame()
        separatorLine.setFrameShape(QFrame.VLine)
        separatorLine.setFrameShadow(QFrame.Sunken)

        return separatorLine

    # txt 파일 다운로드 메서드
    def download2txt(self):
        if self.saveWarning() == False:
            return False
        
        FileSave = QFileDialog.getSaveFileName(self, 'Save file', './output/', "Text File(*.txt)")

        f = open(FileSave[0], "w", encoding="utf-8")
        f.write("문제 제목\n")
        f.write(self.crawler.title + "\n")
        f.write("\n문제 설명\n")
        for problem_desc in self.crawler.problem_desc:
            if problem_desc.find("image_url:") == -1:
                f.write(problem_desc + "\n")

        f.write("\n제한 사항\n")
        for restriction in self.crawler.restrictions:
            f.write(restriction + "\n")

        f.write("\n입출력 예제\n")

        for row in self.crawler.ioExample_list:
            for col in row:
                f.write(col + " ")
            f.write("\n")
        
        f.write("\n입출력 예제 설명\n")
        for desc in self.crawler.example_desc:
            if desc.find("image_url") == -1:
                f.write(desc + "\n")
        f.close()
        QMessageBox.information(self, "저장" ,"저장이 완료되었습니다.")
        self.openFolder(FileSave[0])

    # 마크다운 파일 다운로드 메서드
    def download2md(self):
        if self.saveWarning() == False:
            return False
        
        FileSave = QFileDialog.getSaveFileName(self, 'Save file', './output/', "MarkDown File(*.md)")
        f = open(FileSave[0], "w", encoding="utf-8")

        # 문제 제목 출력
        f.write("# %s\n\n" % self.crawler.title)

        # 문제 설명 출력
        f.write("## 문제 설명\n")
        for desc in self.crawler.problem_desc:
            if desc.find("image_url:") == -1:
                f.write("%s\n\n" % desc)
            else:
                # 이미지 출력
                f.write("![Img](%s)\n\n" % desc[10:])

        # 제한 사항 출력
        f.write("\n<br>\n\n## 제한 사항\n")
        for restriction in self.crawler.restrictions:
            f.write("- %s\n" % restriction)
        f.write("\n\n<br>\n\n")

        # 입출력 예 출력
        ioExample_title = self.crawler.ioExample_list[0]
        ioExamples = self.crawler.ioExample_list[1:]
        f.write("## 입출력 예\n")
        
        ### 입출력 예제 변수명 출력
        title = ""
        sep = ""
        for t in ioExample_title:
            title += "|%s" % t
            sep += "|" + "-" * (len(title) - 1)
        title += "|\n"
        sep += "|\n"

        f.write(title)
        f.write(sep)

        ### 입출력 예제 요소 출력
        for example in ioExamples:
            for item in example:
                f.write("|%s" % item)
            f.write("|\n")
        f.write("\n\n<br>\n\n")

        # 입출력 예 설명
        f.write("## 입출력 예 설명\n")
        for desc in self.crawler.example_desc:
            if desc.find("입출력 예 #") != -1:
                f.write("### %s\n" % desc)
            elif desc.find("image_url") != -1:
                # 이미지 출력
                f.write("![Img](%s)\n\n" % desc[10:])
            else:
                f.write("%s\n\n" % desc)

        f.close()

        QMessageBox.information(self, "저장" ,"저장이 완료되었습니다.")
        self.openFolder(FileSave[0])

    # 소스 코드 다운로드 메서드
    def download2code(self):
        if self.saveWarning() == False:
            return False
        
        ext = "Program File(*.%s)" % (self.extention[self.selectedLanguage])
        FileSave = QFileDialog.getSaveFileName(self, 'Save file', './output/', ext)

        f = open(FileSave[0], "w", encoding="utf-8")
        f.write(self.crawler.code)
        f.close()

        QMessageBox.information(self, "저장" ,"저장이 완료되었습니다.")
        self.openFolder(FileSave[0])

    # 저장할 정보 없을 시 경고 창 띄우는 메서드
    def saveWarning(self):
        if self.crawler == None or self.status != 200:
            QMessageBox.warning(self, "오류" ,"저장할 정보가 없습니다.")
            return False

    # Path의 폴더 오픈 메서드
    def openFolder(self, path):
        path = "/".join(path.split("/")[0:-1])
        os.startfile(path)

    # 라벨의 폰트 사이즈 변경 메서드
    def changeFontSize(self, label, size):
        font = QFont()
        font.setPointSize(size)
        label.setFont(font)


# 실행 코드
if __name__ == "__main__":
    app = QApplication(sys.argv)

    if len(sys.argv) > 1:
        # Debug 모드
        if sys.argv[1] == "1":
            window = MainWindow(True)
        else:
            window = MainWindow()
    else:
        window = MainWindow()
        
    app.exec_()