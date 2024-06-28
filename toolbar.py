import os
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
from PyQt5.QtCore import Qt
import speak


class Toolbar:
    def __init__(self,parent,toolbar_layout:qtw.QWidget,other_controls_widget:qtw.QWidget,text_box:qtw.QTextEdit) -> None:
        # some variables
        self.parent = parent
        self.main_widget = toolbar_layout
        self.other_controls_widget = other_controls_widget
        self.editor = text_box 
        self.style_str = f'''QTextEdit{r'{'} {'type: user-defined;'}{r'}'}'''

        # working with font selector box
        font_selector = self.main_widget.findChild(qtw.QFontComboBox,"fontSelector")
        font_selector.currentFontChanged.connect(self.set_selected_font)

        # working with font size selector box
        font_size_selector = self.main_widget.findChild(qtw.QSpinBox,"fontSizeSelector")
        font_size_selector.valueChanged.connect(self.set_selected_font_size)

        # bold button
        bold = self.main_widget.findChild(qtw.QPushButton,"boldButton")
        bold.clicked.connect(lambda:self.set_font("bold"))

        # italic button
        italic = self.main_widget.findChild(qtw.QPushButton,"italicButton")
        italic.clicked.connect(lambda:self.set_font("italic"))

        # underline button
        underline = self.main_widget.findChild(qtw.QPushButton,"underlineButton")
        underline.clicked.connect(lambda:self.set_font("underline"))

        # reset button
        reset = self.main_widget.findChild(qtw.QPushButton,"resetButton")
        reset.clicked.connect(lambda:self.set_font("reset"))

        # upper_to_lower button
        upper_to_lower = self.main_widget.findChild(qtw.QPushButton,"upperToLowerButton")
        upper_to_lower.clicked.connect(lambda:self.set_font("utl"))

        # lower_to_upper button
        lower_to_upper = self.main_widget.findChild(qtw.QPushButton,"lowerToUpperButton")
        lower_to_upper.clicked.connect(lambda:self.set_font("ltu"))
        # small_caps button
        small_caps_btn = self.main_widget.findChild(qtw.QPushButton,"smallCapsButton")
        small_caps_btn.clicked.connect(lambda:self.set_font("small_caps"))
        # capitalization  button
        capitalization_btn = self.main_widget.findChild(qtw.QPushButton,"capitalizationButton")
        capitalization_btn.clicked.connect(lambda:self.set_font("capitalize"))


        # copy button
        copy_text_btn = self.main_widget.findChild(qtw.QPushButton,"copyText")
        copy_text_btn.clicked.connect(self.copy_all)

        # insert Image button
        insert_image_text_btn = self.main_widget.findChild(qtw.QPushButton,"insertImage")
        insert_image_text_btn.clicked.connect(self.insert_image)


        # insert bulleted list
        bulleted_list_btn = self.main_widget.findChild(qtw.QPushButton,"bulletedListButton")
        bulleted_list_btn.clicked.connect(self.insert_bulleted_list)
        bulleted_styles_actions = {
            "Disc":lambda:self.insert_bulleted_list("disc"),
            "Circle":lambda:self.insert_bulleted_list("circle"),
            "Square":lambda:self.insert_bulleted_list("square"),
            "Decimal":lambda:self.insert_bulleted_list("decimal"),
            "Lower Alpha":lambda:self.insert_bulleted_list("lalpha"),
            "Upper Alpha":lambda:self.insert_bulleted_list("ualpha"),
            "Lower Roman":lambda:self.insert_bulleted_list("lroman"),
            "Upper Roman":lambda:self.insert_bulleted_list("uroman")
        }

        # adding the actions to actions list
        for name,action in bulleted_styles_actions.items():
            temp_action = qtw.QAction(name,bulleted_list_btn)
            temp_action.triggered.connect(action)
            bulleted_list_btn.addAction(temp_action)

        # insert table button
        table_button = self.main_widget.findChild(qtw.QPushButton,"tableButton")
        table_button.clicked.connect(self.insert_table)




        # Initialize The Speak Object
        speak.Speaker(self.parent,self.other_controls_widget,self.editor)


    def set_selected_font(self,e):
        self.editor.setFontFamily(qtg.QFont(e).family())

    def set_selected_font_size(self,e):
        self.editor.setFontPointSize(float(e))

    def set_font(self,flag):
        self.format = None


        current_font = self.editor.font().family()
        current_size = self.editor.font().pointSize()
        

        if flag == "bold":
            self.editor.setFont(qtg.QFont(current_font,current_size,qtg.QFont.Weight.Bold)) 
        elif flag == "italic":
            self.editor.setFont(qtg.QFont(current_font,current_size,qtg.QFont.Weight.Normal,True)) 
        elif flag == "underline":
            underlined_font =qtg.QFont(current_font,current_size,qtg.QFont.Weight.Normal)
            underlined_font.setUnderline(True)
            self.editor.setFont(underlined_font)
        elif flag == "reset":
            reset_font = qtg.QFont(current_font,current_size,qtg.QFont.Weight.Normal,False)
            self.editor.setFont(reset_font)
        elif flag == "utl":
            self.format = self.editor.textCursor().charFormat()
            self.format.setFontCapitalization(qtg.QFont.Capitalization.AllLowercase)
            self.editor.setCurrentCharFormat(self.format)
        elif flag == "ltu":
            self.format = self.editor.textCursor().charFormat()
            self.format.setFontCapitalization(qtg.QFont.Capitalization.AllUppercase)
            self.editor.setCurrentCharFormat(self.format)

        elif flag == "small_caps":
            self.format = self.editor.textCursor().charFormat()
            self.format.setFontCapitalization(qtg.QFont.Capitalization.SmallCaps)
            self.editor.setCurrentCharFormat(self.format)
        elif flag == "capitalize":
            self.format = self.editor.textCursor().charFormat()
            self.format.setFontCapitalization(qtg.QFont.Capitalization.Capitalize)
            self.editor.setCurrentCharFormat(self.format)


    def insert_bulleted_list(self,name):
        
        '''
            ListDisc = ... # type: QTextListFormat.Style
            ListCircle = ... # type: QTextListFormat.Style
            ListSquare = ... # type: QTextListFormat.Style
            ListDecimal = ... # type: QTextListFormat.Style
            ListLowerAlpha = ... # type: QTextListFormat.Style
            ListUpperAlpha = ... # type: QTextListFormat.Style
            ListLowerRoman = ... # type: QTextListFormat.Style
            ListUpperRoman 
        '''
        cursor = self.editor.textCursor()
        indentation = 2
        list_format = None

        if name == 'disc':
            list_format = qtg.QTextListFormat()
            list_format.setIndent(indentation)
            list_format.setStyle(qtg.QTextListFormat.Style.ListDisc)
            cursor.insertList(list_format)

        elif name == "circle":
            list_format = qtg.QTextListFormat()
            list_format.setIndent(indentation)
            list_format.setStyle(qtg.QTextListFormat.Style.ListCircle)
            cursor.insertList(list_format)

        elif name == "square":
            list_format = qtg.QTextListFormat()
            list_format.setIndent(indentation)
            list_format.setStyle(qtg.QTextListFormat.Style.ListSquare)
            cursor.insertList(list_format)

        elif name == "decimal":
            list_format = qtg.QTextListFormat()
            list_format.setIndent(indentation)
            list_format.setStyle(qtg.QTextListFormat.Style.ListDecimal)
            cursor.insertList(list_format)

        elif name == "lalpha":
            list_format = qtg.QTextListFormat()
            list_format.setIndent(indentation)
            list_format.setStyle(qtg.QTextListFormat.Style.ListLowerAlpha)
            cursor.insertList(list_format)

        elif name == "ualpha":
            list_format = qtg.QTextListFormat()
            list_format.setIndent(indentation)
            list_format.setStyle(qtg.QTextListFormat.Style.ListUpperAlpha)
            cursor.insertList(list_format)

        elif name == "lroman":
            list_format = qtg.QTextListFormat()
            list_format.setIndent(indentation)
            list_format.setStyle(qtg.QTextListFormat.Style.ListLowerRoman)
            cursor.insertList(list_format)

        elif name == "uroman":
            list_format = qtg.QTextListFormat()
            list_format.setIndent(indentation)
            list_format.setStyle(qtg.QTextListFormat.Style.ListUpperRoman)
            cursor.insertList(list_format)
            
            

    def insert_table(self):
        cursor = self.editor.textCursor()
        table = qtg.QTextTableFormat()
        table.setCellSpacing(1.5)
        table.setCellPadding(6)
        table.setLeftMargin(15)
        cursor.insertTable(3,3,table)

    def copy_all(self):
        self.editor.selectAll()
        self.editor.copy()

    def insert_image(self):
        filters = "All Images (*.*)"
        image_path,_ = qtw.QFileDialog.getOpenFileName(self.parent,"Insert Image",os.getcwd(),filters)
        if image_path:
            self.editor.textCursor().insertImage(image_path)

