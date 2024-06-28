import sys
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.uic as UILoader
import menus
import toolbar


class Richify(qtw.QMainWindow):
    def __init__(self,clipboard) -> None:
        super().__init__()

        # setting the icon
        self.setWindowIcon(qtg.QIcon("icon.ico"))

        # Loadiung UI File
        UILoader.loadUi("UI Files/editor.ui", self)
        # setting window title
        self.setWindowTitle("Richify - A Rich Text Editor")
        # editor
        self.editor:qtw.QTextEdit = self.findChild(qtw.QTextEdit,"editor")
        # set the editor to auto format
        self.editor.setAutoFormatting(qtw.QTextEdit.AutoFormattingFlag.AutoAll)
        # clipboard
        self.clipboard = clipboard
        # loading menus and there actions
        self.main_menu = menus.MenuDealer(self,clipboard)
        # loading toolbar actions
        tool_bar_layout = self.findChild(qtw.QWidget,"toolbar_layout")
        other_controls_of_toolbar = self.findChild(qtw.QWidget,"otherControls")
        self.toolbar = toolbar.Toolbar(self,tool_bar_layout,other_controls_of_toolbar,self.editor)








if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    clipboard = app.clipboard()
    win = Richify(clipboard)
    win.show()

    try:
        sys.exit(app.exec_()) 
    except SystemError:
        pass
