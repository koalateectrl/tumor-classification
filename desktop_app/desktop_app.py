import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QDialogButtonBox
from PyQt5.QtWidgets import QToolBar
from PyQt5.QtWidgets import QStatusBar
from functools import partial
from pickle import load
import numpy as np
import pandas as pd

class Second(QMainWindow):
    def __init__(self, parent=None):
        super(Second, self).__init__(parent)

class Window(QMainWindow):
    """Main Window."""
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle('QMainWindow')
        self._createButtons()
        self._createMenu()
        self._createToolBar()
        self._createStatusBar()
        self._connectSignals()

    def _evaluate_model(self):
        if self._msg.text():
            self._msg.setText('')
        else:
            self._msg.setText(f'Evaluating Model!')

        df_reduced_1 = self.input[self.first_reduced_features_list]
        df_reduced_1 = self.first_scaler.transform(df_reduced_1)
        first_proba = self.first_model.predict_proba(df_reduced_1)

        if first_proba[0][0] < 0.5:
            self._msg.setText(f'You have PILO! Seq 1 Score: {first_proba[0][1]}')
            return

        df_reduced_2 = self.input[self.second_reduced_features_list]
        df_reduced_2 = self.second_scaler.transform(df_reduced_2)
        second_proba = self.second_model.predict_proba(df_reduced_2)

        if second_proba[0][0] > 0.5:
            self._msg.setText(f'You have EP! Seq 1 Score: {round(first_proba[0][0], 4)}'
                f'; Seq 2 Score: {round(second_proba[0][0], 4)}')
        else:
            self._msg.setText(f'You have MB! Seq 1 Score: {round(first_proba[0][0], 4)}'
                f'; Seq 2 Score: {round(second_proba[0][1], 4)}')
        return

    def _clickLoadPath(self):
        if self._msg.text():
            self._msg.setText('')
        else:
            self._msg.setText(f'Loading Data!')

        path = str(self.path.text())
        self.first_reduced_features_list = load(open('./first_reduced_features_list.pkl', 'rb'))
        self.first_scaler = load(open('./first_scaler.pkl', 'rb'))
        self.first_model = load(open('./lr_seq_1_model.pkl', 'rb'))

        self.second_reduced_features_list = load(open('./second_reduced_features_list.pkl', 'rb'))
        self.second_scaler = load(open('./second_scaler.pkl', 'rb'))
        self.second_model = load(open('./nn_seq_2_model.pkl', 'rb'))
        print(path)
        self.input = pd.read_excel(path)
        self._path_window.close()

    def _connectPathSignal(self):
        self._buttons['Click Done'].clicked.connect(self._clickLoadPath)

    def _loadPath(self):
        self._path_window = Second(self)
        wid = QWidget()
        self._path_window.setCentralWidget(wid)
        layout = QFormLayout()
        self.path = QLineEdit()
        layout.addRow('Data Path: ', self.path)
        self._buttons['Click Done'] = QPushButton('Done')
        layout.addWidget(self._buttons['Click Done'])
        wid.setLayout(layout)
        self._path_window.show()
        self._connectPathSignal()

    def _connectSignals(self):
        self._buttons['Load Data'].clicked.connect(self._loadPath)
        self._buttons['Evaluate Model'].clicked.connect(self._evaluate_model)
        
    def _createButtons(self):
        wid = QWidget()
        self.setCentralWidget(wid)
        layout = QVBoxLayout()
        buttons_labels = ['Load Data', 'Evaluate Model']
        self._buttons = {}
        for btn_text in buttons_labels:
            self._buttons[btn_text] = QPushButton(btn_text)
            layout.addWidget(self._buttons[btn_text])
        self._msg = QLabel('')
        layout.addWidget(self._msg)
        wid.setLayout(layout)

    def _createMenu(self):
        self.menu = self.menuBar().addMenu("&Menu")
        self.menu.addAction('&Exit', self.close)

    def _createToolBar(self):
        tools = QToolBar()
        self.addToolBar(tools)
        tools.addAction('Exit', self.close)

    def _createStatusBar(self):
        status = QStatusBar()
        status.showMessage("I'm the Status Bar")
        self.setStatusBar(status)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = Window()
    view.show()
    sys.exit(app.exec_())

