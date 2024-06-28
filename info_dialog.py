import PyQt5.QtWidgets as qtw
import PyQt5.uic as UILoader



class InfoDialog(qtw.QDialog):
    def __init__(self, parent,title:str="Dialog"):
        super().__init__(parent)

        # load info dialog ui
        UILoader.loadUi("UI Files/infoDialog.ui",self)

        # set dialog title
        self.setWindowTitle(title)
    
        # find the Qwidgets
        self._plain_editor = self.findChild(qtw.QPlainTextEdit,"textArea")
        self._heading = self.findChild(qtw.QLabel,"infoHeading")


    def setEditorText(self,text:str) -> None:
        self._plain_editor.setPlainText(text)

    def setHeadingText(self,text:str) -> None:
        self._heading.setText(text)
    
   