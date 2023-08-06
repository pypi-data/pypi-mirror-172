import os, sys
import re, requests
from bs4 import BeautifulSoup
import bs4
import threading
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *


background_image_stylesheet = '''
MyFlixerWidget {
    border-image: url("bg.jpg");
    background-repeat: no-repeat; 
    background-position: center;
}
'''

# https://myflixer.pw/genre/horror?page=1
# https://myflixer.pw/genre/horror?page=27

default_genre_or_tag = 'horror'
base_url_ = 'https://myflixer.pw'
base_url = base_url_ + '/genre/horror?page='
default_parser = 'html.parser'
initial_page = 50
max_pages = 250


def resize_screen_ratio(object, screenw, screenh, posx_ratio=1/2, posy_ratio=1/2, w_ratio=1/6, h_ratio=0, delta=60):
    """
    screen_geometry = PyQt5.QtWidgets.QDesktopWidget().screenGeometry(-1)
    screenw, screenh = screen_geometry.width(), screen_geometry.height()
    resize_screen_ratio(w1, screenw, screenh, 1/4, 1/5)
    resize_screen_ratio(w2, screenw, screenh, 3/4, 1/5)
    object, screenw, screenh, posx_ratio=1/2, posy_ratio=1/2, w_ratio=1/6, h_ratio=0, delta=60

    object hrs punya method resize dan move.
    """
    if h_ratio <= 0:
        h_ratio = w_ratio
    if posy_ratio <= 0:
        posy_ratio = posx_ratio
    lebar, tinggi = int(screenw*w_ratio), int(screenh*h_ratio)
    object.resize(lebar, tinggi)
    posx = int((screenw-lebar)*posx_ratio)
    posy = int((screenh-tinggi)*posy_ratio) - delta
    object.move(posx, posy)


def get_imdb(url, results):
    soup = BeautifulSoup(requests.get(url).content, default_parser)
    imdb = soup.find('button', class_='btn-imdb').text.strip()
    if imdb:
        imdb = imdb.removeprefix('IMDB: ').strip()
        if url in results:
            results[url]['imdb'] = imdb


def get_data_myflixer(prefix_url = base_url_, code = f'{default_genre_or_tag} {initial_page}', results={}, refresh_result=True):
    """
    qt.so 2
    qt.so python 5
    qt.so rust
    """
    # if refresh_result:
    #     results = {} # supaya gak makin banyak...
    so_url = f'{prefix_url}/genre/__TAG__?page=__PAGE__'
    m = re.match(r'([A-Za-z]+)?\s*(\d+)?', code).groups()
    if m[0] or m[1]:
        so_url = so_url.replace('__TAG__', m[0])
        so_url = so_url.replace('__PAGE__', m[1])
    print(f"[get_data_myflixer] fetching {so_url}", len(results))
    isi = requests.get(so_url).content
    soup = BeautifulSoup(isi, default_parser)
    blocks = soup.findAll('div', class_='flw-item')
    threads = []
    for block in blocks:
        poster_img = block.find('img', class_="film-poster-img")
        poster = poster_img.attrs.get('data-src', '')
        name_link_h2 = block.find('h2', class_='film-name')
        name_link_a = name_link_h2.select_one('a')
        film_name = name_link_a.text.strip()
        url = base_url_ + '/' + name_link_a.attrs.get('href', '')
        year = block.find('span', class_='fdi-item').text.strip()
        #print(f"{film_name} ({year}), {url} => {poster}\n")
        entry = {
            'title': film_name,
            'year': year,
            'url': url,
            'poster': poster,
        }
        if not url in results:
            results[url] = entry
        else:
            results[url].update(entry)
        t = threading.Thread(target=get_imdb, args=(url, results))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
    print(f"[get_data_myflixer] returning from {so_url}", len(results))


class BrowserWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(BrowserWindow, self).__init__(*args, **kwargs)
        self.tabs = QTabWidget()
        self.urls = []
        self.default_url = 'http://www.google.com'        
        self.tabs.setDocumentMode(True)  # making document mode true		
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)  # adding action when double clicked		
        self.tabs.currentChanged.connect(self.current_tab_changed)  # adding action when tab is changed		
        self.tabs.setTabsClosable(True)  # making tabs closeable		
        self.tabs.tabCloseRequested.connect(self.close_current_tab)  # adding action when tab close is requested		
        self.setCentralWidget(self.tabs)  # making tabs as central widget
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        navtb = QToolBar("Navigation")  # creating a tool bar for navigation		
        self.addToolBar(navtb)  # adding tool bar tot he main window		
        back_btn = QAction("Back", self)
        back_btn.setStatusTip("Back to previous page")
        # adding action to back button
        # making current tab to go back
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        navtb.addAction(back_btn)
        next_btn = QAction("Forward", self)
        next_btn.setStatusTip("Forward to next page")
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navtb.addAction(next_btn)

        # similarly adding reload button
        reload_btn = QAction("Reload", self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navtb.addAction(reload_btn)
        # creating home action
        home_btn = QAction("Home", self)
        home_btn.setStatusTip("Go home")
        # adding action to home button
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)
        # adding a separator
        navtb.addSeparator()
        # creating a line edit widget for URL
        self.urlbar = QLineEdit()
        # adding action to line edit when return key is pressed
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        # adding line edit to tool bar
        navtb.addWidget(self.urlbar)
        # similarly adding stop action
        stop_btn = QAction("Stop", self)
        stop_btn.setStatusTip("Stop loading current page")
        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
        navtb.addAction(stop_btn)
        # creating first tab
        self.add_new_tab(self.default_url, 'Homepage')
        
        self.setWindowTitle("My Browser")
        self.hide()

    def new_url(self, alamat):
        self.add_new_tab(alamat, alamat.removeprefix('https://'))

    def add_new_tab(self, qurl = None, label ="Blank"):
        if qurl is None:
            qurl = self.default_url
        if qurl in self.urls:
            self.tabs.setCurrentIndex(self.urls.index(qurl))
            return
        self.urls.append(qurl)
        qurl = QUrl(qurl)
        browser = QWebEngineView()
        browser.setZoomFactor(1.5)
        browser.setUrl(qurl)  # setting url to browser        
        i = self.tabs.addTab(browser, label)  # setting tab index
        self.tabs.setCurrentIndex(i)
        # adding action to the browser when url is changed
        # update the url
        browser.urlChanged.connect(lambda qurl, browser = browser: self.update_urlbar(qurl, browser))
        # adding action to the browser when loading is finished
        # set the tab title
        browser.loadFinished.connect(lambda _, i = i, browser = browser: self.tabs.setTabText(i, browser.page().title()))

    # when double clicked is pressed on tabs
    def tab_open_doubleclick(self, i):
        # checking index i.e
        # No tab under the click
        if i == -1:
            # creating a new tab
            self.add_new_tab()

    # when tab is changed
    def current_tab_changed(self, i):
        # get the curl
        qurl = self.tabs.currentWidget().url()
        # update the url
        self.update_urlbar(qurl, self.tabs.currentWidget())
        # update the title
        self.update_title(self.tabs.currentWidget())

    # when tab is closed
    def close_current_tab(self, i):
        # if there is only one tab
        if self.tabs.count() < 2:
            # do nothing
            return
        # else remove the tab
        self.tabs.removeTab(i)

    # method for updating the title
    def update_title(self, browser):
        # if signal is not from the current tab
        if browser != self.tabs.currentWidget():
            # do nothing
            return
        # get the page title
        title = self.tabs.currentWidget().page().title()
        # set the window title
        self.setWindowTitle("% s - Geek PyQt5" % title)

    # action to go to home
    def navigate_home(self):
        # go to google
        self.tabs.currentWidget().setUrl(QUrl(self.default_url))

    # method for navigate to url
    def navigate_to_url(self):
        # get the line edit text
        # convert it to QUrl object
        q = QUrl(self.urlbar.text())
        # if scheme is blank
        if q.scheme() == "":
            # set scheme
            q.setScheme("http")
        # set the url
        self.tabs.currentWidget().setUrl(q)

    # method to update the url
    def update_urlbar(self, q, browser = None):
        # If this signal is not from the current tab, ignore
        if browser != self.tabs.currentWidget():
            return
        # set text to the url bar
        self.urlbar.setText(q.toString())
        # set cursor position
        self.urlbar.setCursorPosition(0)


class MyflixerInternal(QWidget):

    url_signal = pyqtSignal(str)
    show_hide_state = pyqtSignal(bool)
    toggle_table_signal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.bold_font = QFont("Roman times", 12, QFont.Bold)
        self.data = {}
        get_data_myflixer(results=self.data)
        self.initUI()

    def setContent(self):

        self.content.setRowCount(len(self.data))
        self.content.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        # https://stackoverflow.com/questions/38098763/pyside-pyqt-how-to-make-set-qtablewidget-column-width-as-proportion-of-the-a
        for i, (k,v) in enumerate(reversed(self.data.items())):
            # ['Title', 'Year', 'IMDB', 'URL', 'Poster']
            # for j in enumerate(self.column_labels):
            #     self.content.setItem(i, j, current_item)
            # current_item = QTableWidgetItem(isi)
            self.content.setItem(i, 0, QTableWidgetItem(v['title']))
            self.content.setItem(i, 1, QTableWidgetItem(v['year']))
            if not 'imdb' in v:
                imdb_score = 'N/A'
            else:
                imdb_score = v['imdb']
            imdb_item = QTableWidgetItem(imdb_score)
            try:
                if float(imdb_score) > 7.0:
                    # imdb_item.setStyleSheet('background-color: gold; color: indigo;')
                    imdb_item.setBackground(QColor('gold'))
                    imdb_item.setFont(QFont("Roman times", 16, QFont.Bold))
                    imdb_item.setForeground(QColor('indigo'))
                elif float(imdb_score) > 6.5:
                    imdb_item.setBackground(QColor('chartreuse'))
            except ValueError:
                pass
            self.content.setItem(i, 2, imdb_item)
            self.content.setItem(i, 3, QTableWidgetItem(v['url']))
            self.content.setItem(i, 4, QTableWidgetItem(v['poster']))

    def load_so(self):
        prefix = self.combo0.currentText()
        tag = self.edit_tag.text()
        page = self.page.value()
        print(f"""
        prefix      = {prefix}
        tag         = {tag}
        page        = {page}
        """)

        get_data_myflixer(prefix_url=prefix, code=f'{tag} {page}', results=self.data)
        # https://stackoverflow.com/questions/15848086/how-to-delete-all-rows-from-qtablewidget
        self.content.setRowCount(0)
        self.setContent()

    def toggle_table(self, state):
        self.toggle_table_signal.emit(state)
        self.content.setHidden(state)
        if self.toggle_table_button.isChecked():
            self.toggle_table_button.setText('Show table')
        else:
            self.toggle_table_button.setText('Hide table')

    def toggle_browser(self, state):
        self.show_hide_state.emit(state)
        if self.toggle_browser_button.isChecked():
            self.toggle_browser_button.setText('Show browser')
        else:
            self.toggle_browser_button.setText('Hide browser')

    def combo_change_index(self, index):
        print(index)
        self.edit_tag.setText('')

    def next_page(self):
        curpage = self.page.value()
        if curpage >= max_pages:
            return
        self.page.setValue(curpage+1)
        self.load_so()

    def prev_page(self):
        curpage = self.page.value()
        if curpage <= 1:
            return
        self.page.setValue(curpage-1)
        self.load_so()

    def setToolbar(self):
        self.tool_layout = QHBoxLayout()
        self.combo0 = QComboBox(self)
        self.combo0.addItems([
            base_url_
        ])
        self.combo0.currentTextChanged.connect(lambda value: print(value))
        self.combo0.setStyleSheet('height: 32px; background-color: bisque; font-family: Consolas; font-size: 16px;')
        self.combo0.currentIndexChanged.connect(self.combo_change_index)
        # combo0.textChanged.connect(lambda value: print(value))
        self.tool_layout.addWidget(self.combo0)
        lbl1 = QLabel("Tag")

        self.tool_layout.addWidget(lbl1)
        self.edit_tag = QLineEdit(default_genre_or_tag)
        self.edit_tag.setStyleSheet('height: 32px; background-color: bisque; font-family: Consolas; font-size: 16px;')
        self.edit_tag.returnPressed.connect(self.load_so)
        self.tool_layout.addWidget(self.edit_tag)

        lbl3 = QLabel("Page")
        self.tool_layout.addWidget(lbl3)
        self.page = QSpinBox()
        self.page.setRange(1, max_pages)
        self.page.setValue(initial_page)
        # self.page.valueChanged.connect(lambda value: print('val:', value))
        # spin4.textChanged.connect(lambda value: print('text:', value))
        self.tool_layout.addWidget(self.page)

        lefticon = QApplication.style().standardIcon(QStyle.SP_ArrowLeft)
        righticon = QApplication.style().standardIcon(QStyle.SP_ArrowRight)
        left = QPushButton(lefticon, "")
        right = QPushButton(righticon, "")
        left.setStyleSheet('padding: 5px; background-color: chocolate; font-family: Consolas; font-size: 16px;')
        right.setStyleSheet('padding: 5px; background-color: chocolate; font-family: Consolas; font-size: 16px;')
        left.clicked.connect(self.prev_page)
        right.clicked.connect(self.next_page)
        self.tool_layout.addWidget(left)        
        self.tool_layout.addWidget(right)

        self.tool_layout.addStretch(1)

        self.toggle_table_button = QPushButton("Toggle table")
        self.toggle_table_button.setCheckable(True)
        self.toggle_table_button.setChecked(True)
        self.toggle_table_button.setStyleSheet("""
            QPushButton {background:rgb(66, 66, 66); color: white;} 
            QPushButton::checked {background:rgb(255, 255, 0); color: blue;}
        """)
        self.tool_layout.addWidget(self.toggle_table_button)
        self.toggle_table_button.toggled.connect(lambda state: self.toggle_table(state))

        self.use_system_browser = QCheckBox("Use system browser")
        self.use_system_browser.stateChanged.connect(lambda state: print('use system browser' if state==Qt.Checked else 'use internal browser'))
        self.tool_layout.addWidget(self.use_system_browser)

        self.toggle_browser_button = QPushButton("Toggle browser")
        self.toggle_browser_button.setCheckable(True)
        self.toggle_browser_button.setChecked(True)
        self.toggle_browser_button.setStyleSheet("""
            QPushButton {background:rgb(66, 66, 66); color: white;} 
            QPushButton::checked {background:rgb(255, 255, 0); color: blue;}
        """)
        self.tool_layout.addWidget(self.toggle_browser_button)
        self.toggle_browser_button.toggled.connect(lambda state: self.toggle_browser(state))

        load_button = QPushButton("load")
        load_button.clicked.connect(self.load_so)
        self.tool_layout.addWidget(load_button)
        self.stackoverflow_layout.addLayout(self.tool_layout)

    def initUI(self):
        self.resize(1200, 800)
        self.stackoverflow_layout = QVBoxLayout()

        self.content = QTableWidget(self)
        self.setToolbar()

        self.column_labels = ['Title', 'Year', 'IMDB', 'URL', 'Poster']
        self.content.setColumnCount(len(self.column_labels))
        for i in range(1,len(self.column_labels)+1):
            item = QTableWidgetItem()
            self.content.setHorizontalHeaderItem(i, item)
        self.content.setHorizontalHeaderLabels(self.column_labels)
        self.stackoverflow_layout.addWidget(self.content)
        self.setContent()
        self.content.itemClicked.connect(self.onClicked)

        self.setLayout(self.stackoverflow_layout)
        self.setWindowTitle('Myflixer')

    @pyqtSlot(QTableWidgetItem)
    def onClicked(self, it):
        # ['Title', 'Year', 'IMDB', 'URL', 'Poster']
        #   0        1       2       3      4
        if it.column()==3:  # URL
            alamat = it.text()
            if self.use_system_browser.isChecked():
                import webbrowser
                webbrowser.open_new(alamat)
            else:
                self.url_signal.emit(alamat)


class Myflixer(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.main_layout = QVBoxLayout()
        stackoverflow_splitter = QSplitter(Qt.Vertical)

        widgetbrowser = BrowserWindow()
        stackoverflow_splitter.addWidget(widgetbrowser)
        stackoverflow_widget = MyflixerInternal()
        stackoverflow_splitter.addWidget(stackoverflow_widget)

        stackoverflow_widget.url_signal.connect(widgetbrowser.new_url)
        stackoverflow_widget.show_hide_state.connect(widgetbrowser.setHidden)
        # https://stackoverflow.com/questions/29537762/pyqt-qsplitter-setsizes-usage
        # stackoverflow_widget.toggle_table_signal.connect(lambda state: stackoverflow_splitter.setStretchFactor(10,1) if state else stackoverflow_splitter.setStretchFactor(5,5))
        stackoverflow_widget.toggle_table_signal.connect(lambda state: stackoverflow_splitter.setSizes([500,100]) if state else stackoverflow_splitter.setSizes([400,400]))

        stackoverflow_splitter.handle(1).setStyleSheet('background: 3px blue;')

        self.main_layout.addWidget(stackoverflow_splitter)
        self.setLayout(self.main_layout)

        # self.resize(800, 600)
        self.setWindowTitle('Myflixer')


class CustomTitleBar(QWidget):

    clickPos = None

    def __init__(self, parent):
        super(CustomTitleBar, self).__init__(parent)
        self.setAutoFillBackground(True)
        
        self.setBackgroundRole(QPalette.Shadow)
        # alternatively:
        # palette = self.palette()
        # palette.setColor(palette.Window, Qt.black)
        # palette.setColor(palette.WindowText, Qt.white)
        # self.setPalette(palette)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(1, 1, 1, 1)
        layout.addStretch()

        self.title = QLabel("My Own Bar", self, alignment=Qt.AlignCenter)
        # if setPalette() was used above, this is not required
        self.title.setForegroundRole(QPalette.Light)

        style = self.style()
        ref_size = self.fontMetrics().height()
        ref_size += style.pixelMetric(style.PM_ButtonMargin) * 2
        self.setMaximumHeight(ref_size + 2)

        btn_size = QSize(ref_size, ref_size)
        for target in ('min', 'normal', 'max', 'close'):
            btn = QToolButton(self, focusPolicy=Qt.NoFocus)
            layout.addWidget(btn)
            btn.setFixedSize(btn_size)

            iconType = getattr(style, 
                'SP_TitleBar{}Button'.format(target.capitalize()))
            btn.setIcon(style.standardIcon(iconType))

            if target == 'close':
                colorNormal = 'red'
                colorHover = 'orangered'
            else:
                colorNormal = 'palette(mid)'
                colorHover = 'palette(light)'
            btn.setStyleSheet('''
                QToolButton {{
                    background-color: {};
                }}
                QToolButton:hover {{
                    background-color: {}
                }}
            '''.format(colorNormal, colorHover))

            signal = getattr(self, target + 'Clicked')
            btn.clicked.connect(signal)

            setattr(self, target + 'Button', btn)

        self.normalButton.hide()

        self.updateTitle(parent.windowTitle())
        parent.windowTitleChanged.connect(self.updateTitle)

        self.gripSize = 16
        grip = QSizeGrip(self) # satu grip akan otomatis di kiri atas
        grip.resize(self.gripSize, self.gripSize)
        # self.grips = []
        # for _ in range(4):
        #     grip = QSizeGrip(self)
        #     grip.resize(self.gripSize, self.gripSize)
        #     self.grips.append(grip)

    def updateTitle(self, title=None):
        if title is None:
            title = self.window().windowTitle()
        width = self.title.width()
        width -= self.style().pixelMetric(QStyle.PM_LayoutHorizontalSpacing) * 2
        self.title.setText(self.fontMetrics().elidedText(
            title, Qt.ElideRight, width))

    def windowStateChanged(self, state):
        self.normalButton.setVisible(state == Qt.WindowMaximized)
        self.maxButton.setVisible(state != Qt.WindowMaximized)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clickPos = event.windowPos().toPoint()

    def mouseMoveEvent(self, event):
        if self.clickPos is not None:
            self.window().move(event.globalPos() - self.clickPos)

    def mouseReleaseEvent(self, QMouseEvent):
        self.clickPos = None

    def closeClicked(self):
        self.window().close()

    def maxClicked(self):
        self.window().showMaximized()

    def normalClicked(self):
        self.window().showNormal()

    def minClicked(self):
        self.window().showMinimized()

    def resizeEvent(self, event):
        self.title.resize(self.minButton.x(), self.height())
        self.updateTitle()


class MyflixerWidgetBase(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setWindowFlags(self.windowFlags() | Qt.CustomizeWindowHint | Qt.FramelessWindowHint)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        # self.titleBar = CustomTitleBar(self)
        # self.setContentsMargins(0, self.titleBar.height(), 0, 0)
        self.grips = []
        self.gripSize = 16
        for _ in range(2): # buat 2 grip utk ditaro di bawah ki-ka
            grip = QSizeGrip(self)
            grip.resize(self.gripSize, self.gripSize)
            self.grips.append(grip)

        self.initUI()

    def initUI(self):

        self.main_layout = QHBoxLayout()
        stackoverflow0 = Myflixer()
        self.main_layout.addWidget(stackoverflow0)
        self.setLayout(self.main_layout)        
        # self.setWindowTitle('Myflixer')
        # self.setStyleSheet(background_image_stylesheet)


class MyFlixerWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setWindowFlags(self.windowFlags() | Qt.CustomizeWindowHint | Qt.FramelessWindowHint)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.titleBar = CustomTitleBar(self)
        self.setContentsMargins(0, self.titleBar.height(), 0, 0)
        self.grips = []
        self.gripSize = 16
        for _ in range(2): # buat 2 grip utk ditaro di bawah ki-ka
            grip = QSizeGrip(self)
            grip.resize(self.gripSize, self.gripSize)
            self.grips.append(grip)

        self.initUI()

    def changeEvent(self, event):
        if event.type() == event.WindowStateChange:
            self.titleBar.windowStateChanged(self.windowState())

    def resizeEvent(self, event):
        self.titleBar.resize(self.width(), self.titleBar.height())

        rect = self.rect()
        # # top right
        # self.grips[0].move(rect.right() - self.gripSize, 0)
        # bottom right
        self.grips[0].move(rect.right() - self.gripSize, rect.bottom() - self.gripSize)
        # bottom left
        self.grips[1].move(0, rect.bottom() - self.gripSize)

    def initUI(self):

        self.main_layout = QHBoxLayout()
        stackoverflow0 = Myflixer()
        self.main_layout.addWidget(stackoverflow0)
        self.setLayout(self.main_layout)        
        self.setWindowTitle('Myflixer')
        self.setStyleSheet(background_image_stylesheet)


def main():
    app = QApplication([])
    ex = MyFlixerWidget()
    QShortcut(QKeySequence("Ctrl+Q"), ex, activated=lambda: qApp.quit())
    screen_geometry = QDesktopWidget().screenGeometry(-1)
    screenw, screenh = screen_geometry.width(), screen_geometry.height()
    resize_screen_ratio(ex, screenw, screenh, w_ratio=0.95, h_ratio=0.9)
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


"""
TODO:
setiap ganti combobox maka tag dikosongkan
krn gak make sense ada tag "python" utk writing stackexchange misalnya.
"""
