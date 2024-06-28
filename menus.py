from datetime import datetime
import os
import re
import sys
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QRegExp
from PyQt5.QtPrintSupport import QPrinter,QPrintDialog
import webbrowser
import info_dialog
import texts



class MenuDealer:
    def __init__(self,parent,clipboard:qtg.QClipboard) -> None:
        self.parent = parent
        self.editor = self.parent.findChild(qtw.QTextEdit,"editor")
        self.clipboard = clipboard
        # control File Menu
        self.control_file_menu()
        # control Edit Menu
        self.control_edit_menu()
        # control Rich Edit Menu
        self.control_rich_edit_menu()
        # control View Menu
        self.control_view_menu()
        # control View Menu
        self.control_about_menu()

        
    def control_file_menu(self):
        self.file_path = None
        self.current_dir = os.getcwd()
        # Function Called When Action Triggers
        def new_file():
            try:
                file, _ = qtw.QFileDialog.getSaveFileName(self.parent,"New File",self.current_dir)
                if file:
                    self.file_path = file
                    with open(file,"w") as f:
                        pass
            except Exception as e:
                print(e)

                        
        def open_file():
            try:
                file_patterns = " Rich Document (*.doc);;All Files (*.*);;Text File (Simple Text) (*.txt)"
                file, _ = qtw.QFileDialog.getOpenFileName(self.parent,"Open File",self.current_dir,file_patterns)
                self.file_path = file
                if file:
                    self.parent.setWindowTitle(self.file_path)
                    with open(file,"r") as f:
                        if ".doc" in os.path.basename(file):
                            self.editor.clear()
                            self.editor.insertHtml(f.read()) 
                        elif ".txt" in os.path.basename(self.file):
                            self.editor.clear()
                            self.editor.insertPlainText(self.get_raw_text(f.read()))
                            
            except Exception as e:  
                print(e)

        def save_file():
            try:
                if self.file_path:
                    if ".doc" in os.path.basename(self.file_path):
                        with open(self.file_path,"w") as f:
                            f.write(self.editor.toHtml())
                    elif ".txt" in os.path.basename(self.file_path):
                        with open(self.file_path,"w") as f:
                            f.write(self.get_raw_text(self.editor.toPlainText()))

            except Exception as e:
                print(e)
 
        def save_as_file():
            try:
                filters = " Rich Document (*.doc);;All Files (*.*);; Text File (Simple Text) (*.txt)"
                file, _ = qtw.QFileDialog.getSaveFileName(self.parent,"Save As",self.current_dir,filters)
                self.file_path = file
                with open(file,"w") as f:
                    f.write(self.editor.toHtml())

            except Exception as e:
                print(e)
        def close_file():
            try:
                if self.file_path:
                    self.file_path = ""
                    self.parent.setWindowTitle("Richify - A Rich Text Editor")
                    self.editor.clear()
            except Exception as e:
                print(e)

        def print_file():
            try:
                printer = QPrinter(QPrinter.HighResolution)
                printer_dialog = QPrintDialog(printer,self.parent)
                printer_dialog.exec_()
            except Exception as e:
                print(e)

        def create_file_with_folder():
            try:
                # function for creating file and folder
                def create_file_folder(input1,input2):
                    try:
                        folder_name = input1.text()
                        file_name = input2.text()

                        if len(folder_name) > 1 and len(file_name) > 1:
                            folder_path = f"{self.current_dir}\\{folder_name}"
                            file_name = f"{folder_path}\\{file_name}"
                            os.mkdir(folder_path)
                            with open(file_name,"w") as f:
                                pass
                            returnedList[3].destroy()

                    except Exception as e:
                        print(e)

                windowTitle = "Create File & Folder"
                place_holder1 = "Enter The Folder Name"
                place_holder2 = "Enter The File Name"
                returnedList:list = self.create_muliple_input_window(
                    windowTitle,
                    place_holder1,
                    place_holder2,
                    "Create!"
                )    

                input_field1_text = returnedList[0]
                input_field2_text = returnedList[1]

                returnedList[2].clicked.connect(lambda:create_file_folder(input_field1_text,input_field2_text))
                
            except Exception as e:
                print(e)

        def create_folder():
            try:
                folder_dialog = qtw.QInputDialog(self.parent)
                folder_text,_ = folder_dialog.getText(folder_dialog,"Create Folder","Enter Folder Name")
                folder_dialog.setOkButtonText("Create")
                folder_dialog.setMinimumSize(150,100)  

                if  len(folder_text)  > 2:
                    path = f"{os.getcwd()}\\{folder_text}"
                    os.mkdir(path)
            except Exception as e:
                print(e)

        def save_as_pdf():
            try:
                if self.file_path:
                    pdf_file,_ = qtw.QFileDialog.getSaveFileName(self.parent,"Export As PDF",self.current_dir,"PDF Files (*.pdf)")
                    printer = QPrinter(QPrinter.HighResolution)
                    printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
                    printer.setOutputFileName(pdf_file)
                    self.editor.document().print_(printer)
                
            except Exception as e:
                print(e)

        def exit_app():
            sys.exit(self.parent)

        # ----------------- File Menu ----------------- 
        fileMenuWithActions = {
            "actionNew":new_file,
            "actionOpen":open_file,
            "actionSave":save_file,
            "actionSave_As":save_as_file,
            "actionClose":close_file,
            "actionPrint":print_file,
            "actionCreate_File_With_Folder":create_file_with_folder,
            "actionCreate_Folder":create_folder,
            "actionExport_As_PDF":save_as_pdf,
            "actionExit":exit_app,
        }

        # control File Menu
        self.control_submenu(fileMenuWithActions)


    def control_edit_menu(self):
         # Function Called When Action Triggers
        def replace_with():
            # function to replace words
            def replace_words(word:str,toBeReplaced:str,dialog):
                text =  self.editor.toPlainText()
                if len(text) > 1:
                    text = text.replace(word.text(),toBeReplaced.text())
                    self.editor.clear()
                    self.editor.setText(text)
                    
                    dialog.destroy()


            placeholder_1 = "Enter The Word..."
            placeholder_2 = "Enter The Word To Be Replaced..."
            buttonText = "Replace!"
            returnedWidgetsList = self.create_muliple_input_window(
                "Replace",
                placeholder_1,
                placeholder_2,
                buttonText
            )

            word = returnedWidgetsList[0]
            toBeReplaced = returnedWidgetsList[1]
            replace_btn = returnedWidgetsList[2]
            dialog = returnedWidgetsList[3]

            replace_btn.clicked.connect(lambda:replace_words(word,toBeReplaced,dialog))




        # ----------------- Edit Menu ----------------- 
        editMenuWithActions = {
            "actionCopy":lambda:self.editor.copy(),
            "actionPaste":lambda:self.editor.paste(),
            "actionCut":lambda:self.editor.cut(),
            "actionUndo":lambda:self.editor.undo(),
            "actionRedo":lambda:self.editor.redo(),
            "actionReplace":replace_with,
            "actionSelect_All":lambda:self.editor.selectAll(),
            "actionClear_All":lambda:self.editor.clear(),
            "actionDate_Time":lambda:self.editor.insertPlainText(datetime.ctime(datetime.now())),
        }

        # control Edit Menu
        self.control_submenu(editMenuWithActions)

    def control_rich_edit_menu(self):
    
        # RICH - Editing : Function Called When Action Triggers
    
            
        def align(flag:str):
            if flag == "center":
                self.editor.setAlignment(Qt.AlignmentFlag.AlignCenter)
            elif flag == "left":
                self.editor.setAlignment(Qt.AlignmentFlag.AlignLeft)
            elif flag == "right":
                self.editor.setAlignment(Qt.AlignmentFlag.AlignRight)
            elif flag == "justify":
                self.editor.setAlignment(Qt.AlignmentFlag.AlignJustify)
                    

        
        def highlight_color():
           defaultColor = qtg.QColor("#3498DB")
           choosed_bg_color = qtw.QColorDialog.getColor(defaultColor,self.parent,"Choose Background Color")
           choosed_fg_color = qtw.QColorDialog.getColor(defaultColor,self.parent,"Choose Foreground Color")
           self.editor.setTextBackgroundColor(choosed_bg_color)
           self.editor.setTextColor(choosed_fg_color)

        def google_it():
            try:
                cursor = self.editor.textCursor()
                text = cursor.selectedText()
                self.open_in_browser(text)
            except Exception as e:
                print(e + "google_it")

        def remove_extra_spaces():
            text = self.editor.toPlainText()
            xtraSpacesRemovedText = ""
            # using RegEx To Remove Extra Spaces
            pattern_to_get_character = re.compile(r"(.+)")
            matches = pattern_to_get_character.finditer(text)
            for match in matches:
                xtraSpacesRemovedText += match.group(1)

            self.editor.clear()
            self.editor.setText(xtraSpacesRemovedText)
            return xtraSpacesRemovedText

        def copy_text_length():
            removedSpacesText:str = remove_extra_spaces()
            words = len(removedSpacesText.split(" "))
            characters = len(removedSpacesText)
            self.clipboard.setText(f"{words} Words & {characters} Characters!")


        # ----------------- Rich Edit Menu ----------------- 
        richEditMenuWithActions = {
            "actionCenter":lambda:align("center"),
            "actionLeft":lambda:align("left"),
            "actionRight_Align":lambda:align("right"),
            "actionJustify_Text":lambda:align("justify"),
            "actionMake_Bold":lambda:self.editor.setFontWeight(qtg.QFont.Weight.Bold),
            "actionUn_Bold":lambda:self.editor.setFontWeight(qtg.QFont.Weight.Normal),
            "actionDemi_Bold":lambda:self.editor.setFontWeight(qtg.QFont.Weight.DemiBold),
            "actionXtra_Bold":lambda:self.editor.setFontWeight(qtg.QFont.Weight.ExtraBold),
            "actionBlack":lambda:self.editor.setFontWeight(qtg.QFont.Weight.Black),
            "actionXtra_Light":lambda:self.editor.setFontWeight(qtg.QFont.Weight.ExtraLight),
            "actionThin":lambda:self.editor.setFontWeight(qtg.QFont.Weight.Thin),
            "actionLight":lambda:self.editor.setFontWeight(qtg.QFont.Weight.Light),
            "actionMake_Italic":lambda:self.editor.setFontItalic(True),
            "actionRemove_Italic":lambda:self.editor.setFontItalic(False),
            "actionMake_Underlined":lambda:self.editor.setFontUnderline(True),
            "actionRemove_Underlined":lambda:self.editor.setFontUnderline(False),
            "actionNormal":lambda:self.editor.setFont(qtg.QFont(self.editor.font().family(),self.editor.font().pointSize(),qtg.QFont.Weight.Normal,False)),
            "actionHighlight":highlight_color,
            "actionChange_Text_Color":lambda:self.editor.setTextColor(qtw.QColorDialog.getColor(qtg.QColor("#3498DB"),self.parent,"Choose Color")),
            "actionSearch_With_Google":google_it,
            "actionRemove_Extra_Spaces":remove_extra_spaces,
            "actionCopy_Text_Length":copy_text_length,
        }
  
        # control Rich Edit Menu
        self.control_submenu(richEditMenuWithActions)

    def control_view_menu(self):
        def zoom(flag):
            if flag == "in":
                self.editor.zoomIn(2)
            else:
                self.editor.zoomOut(2)
            
        def find():
            try:
                def moveCaret():
                    inputed_text = input.text()

                    if len(inputed_text) > 1:
                        cursor = self.editor.textCursor()
                        # format
                        format = qtg.QTextCharFormat()
                        format_color = qtg.QColor("#fff36f")
                        format.setBackground(format_color)

                        # setup the regex
                        regex = QRegExp(inputed_text,Qt.CaseSensitivity.CaseSensitive)
                        pos = 0
                        index = regex.indexIn(self.editor.toPlainText(),pos)
            
                        while(index != -1):
                            # select the matched text
                            cursor.setPosition(index)
                            cursor.movePosition(qtg.QTextCursor.MoveOperation.EndOfWord,1)
                            cursor.mergeCharFormat(format)
                            # move the caret
                            pos = index + regex.matchedLength()
                            index = regex.indexIn(self.editor.toPlainText(),pos)


                input = self.multi_btns_dialog("Find Word","Enter The Word...","Find...","Cancel!",moveCaret)
            except Exception as e:
                print(e+ "moveCaret")

        
        def clear_findings():
            text = self.editor.toPlainText()
            self.editor.clear()
            self.editor.setPlainText(text)

        def toggle_word_wrap(e):
            if e:
               self.editor.setWordWrapMode(qtg.QTextOption.WrapMode.WordWrap)                
            else:
               self.editor.setWordWrapMode(qtg.QTextOption.WrapMode.NoWrap) 


        # ----------------- View Menu ----------------- 
        viewMenuWithActions = {
            "actionZoom_In":lambda:zoom("in"),
            "actionZoom_Out":lambda:zoom("out"),
            "actionFind":find,
            "actionClear_Findings":clear_findings,
            "actionWord_Wrap_2":toggle_word_wrap,
        }
        # controlling the view menu
        self.control_submenu(viewMenuWithActions)

    def control_about_menu(self):
        # ----------------- About Menu ----------------- 
        _REPL_IT_ID = "https://www.replit.com/@jawad989"
        _FACEBOOK_ID = "https://wwww.facebook.com/profile.php?id=100079902806743"
        _GMAIL_ = "janonymous9899@gmail.com"    

        aboutText = texts.Texts.get_about_text()
        developersText = texts.Texts.get_developers_text()
        aboutMyselfText = texts.Texts.about_myself()


        aboutMenuWithActions = {
            "actionAbout_Application":lambda:self.info_dialog("About Application","About Application",aboutText),
            "actionDevelopers":lambda:self.info_dialog("About Developers","Developers!",developersText),
            "actionLink_To_Repl_it":lambda:self.open_in_browser(_REPL_IT_ID),
            "actionLink_To_Facebook":lambda:self.open_in_browser(_FACEBOOK_ID),
            "actionLink_To_Gmail":lambda:self.clipboard.setText(_GMAIL_),
            "actionOther_About_Info":lambda:self.info_dialog("About Myself","About Me :)",aboutMyselfText)
        }
        # controlling the view menu
        self.control_submenu(aboutMenuWithActions)
    


    # method to control a sub-menu
    def control_submenu(self,menuWithAcions:dict):
        for object_name,objcet_action  in menuWithAcions.items():
            t = self.parent.findChild(qtw.QAction,object_name)
            t.triggered.connect(objcet_action)


    def get_raw_text(self,text):
        raw_text_obj = qtg.QTextDocument(text,self.editor)
        raw_text = raw_text_obj.toRawText()
        return raw_text

    def create_muliple_input_window(self,title:str,place_holder1:str="Enter...",place_holder2:str="Enter...",button_txt:str="Done!") -> list:
        dialog = qtw.QDialog(self.parent,Qt.WindowType.Dialog)
        dialog.setWindowTitle(title)
        dialog.setMinimumSize(500,150)
        dialog.setMaximumSize(500,150)
        dialog.setLayout(qtw.QVBoxLayout())
        dialog_font =qtg.QFont("Helvetica",15)

        dialog_input1 = qtw.QLineEdit(dialog)
        dialog_input1.setPlaceholderText(place_holder1)
        dialog_input1.setFont(dialog_font)

        dialog_input2 = qtw.QLineEdit(dialog)
        dialog_input2.setPlaceholderText(place_holder2)
        dialog_input2.setFont(dialog_font)


        dialog_btn = qtw.QPushButton(button_txt,dialog)
        dialog_btn.setFont(dialog_font)
        dialog_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        # adding widgets to dialog

        dialog.layout().addWidget(dialog_input1)
        dialog.layout().addWidget(dialog_input2)
        dialog.layout().addWidget(dialog_btn)
        dialog.show()
        return [dialog_input1,dialog_input2,dialog_btn,dialog]
    
    def multi_btns_dialog(self,title:str="Title",place_holder:str="Type...",btn_text1:str="Ok!",btn_text2:str="Cancel!",func=None):
        multi_btns_dialog = qtw.QDialog(self.parent,Qt.WindowType.Dialog)
        multi_btns_dialog.setWindowTitle(title)
        multi_btns_dialog.setMinimumSize(500,150)
        multi_btns_dialog.setMaximumSize(500,150)
        multi_btns_dialog.setLayout(qtw.QVBoxLayout())
        dialog_font =qtg.QFont("Helvetica",15)

        dialog_input = qtw.QLineEdit(multi_btns_dialog)
        dialog_input.setPlaceholderText(place_holder)
        dialog_input.setFont(dialog_font)

        multi_btns_dialog.layout().addWidget(dialog_input)
        btn_texts = [btn_text1,btn_text2]
        btns = []

        for text in btn_texts:
            btn = qtw.QPushButton(text,multi_btns_dialog)
            btn.setFont(dialog_font)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            multi_btns_dialog.layout().addWidget(btn)
            if text == btn_text1:
                btn.clicked.connect(func)
            btns.append(btn)


        multi_btns_dialog.show()
        btns[1].clicked.connect(lambda:multi_btns_dialog.destroy())

        return dialog_input

    def open_in_browser(self,query:str=""):
        searchQuery = f"https://www.google.com/https://www.google.com/search?q={query}"
        webbrowser.open_new_tab(searchQuery)

    def info_dialog(self,title:str,heading:str,editor_text:str="") -> None:
        dialog = info_dialog.InfoDialog(self.parent,title)
        dialog.setHeadingText(heading)
        dialog.setEditorText(editor_text)
        dialog.show()
    
