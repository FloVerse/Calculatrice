import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QGridLayout, QTextEdit, QLabel, \
    QMenu, QListView, QSizePolicy


class Calculatrice(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.historique_view = None
        self.label = None
        self.history_display = None
        self.button_history = None
        self.current_input = ''
        self.history = []
        self.font = QFont("Arial", 12)
        self.display = None
        self.layout = None
        self.model_history = QStandardItemModel()
        self.initial_width = self.width()
        self.initUI()

    def initUI(self):
        super().__init__()
        self.setWindowTitle('Calculatrice')
        self.setGeometry(100, 100, 500, 650)

        self.layout = QGridLayout(self)
        self.layout.setHorizontalSpacing(0)
        self.layout.setVerticalSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Label
        self.label = QLabel('Standard', self)
        self.label.setFont(QFont("Arial", 13))
        self.label.setContentsMargins(10, 0, 0, 0)
        self.label.setFixedHeight(50)
        self.layout.addWidget(self.label, 0, 0, 1, 1)

        # Affichage
        self.display = QLineEdit(self)
        self.display.setFixedHeight(150)
        display_font = QFont("Arial", 25)
        self.display.setStyleSheet("QLineEdit { padding-top: 50px; }")
        self.display.setAlignment(Qt.AlignRight)
        self.display.setText('0')
        self.display.setFont(display_font)
        self.layout.addWidget(self.display, 1, 0, 1, 4)

        self.historique_view = QListView(self)
        self.historique_view.setModel(self.model_history)
        self.historique_view.setFixedHeight(75)
        self.historique_view.setFixedWidth(200)
        self.historique_view.setEditTriggers(QListView.NoEditTriggers)
        self.historique_view.setFont(self.font)
        self.historique_view.setHidden(True)
        self.historique_view.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding))
        self.initial_width = self.width() - self.historique_view.width()



        self.layout.addWidget(self.historique_view, 1, 5, 1, 5)


        # Bouton historique
        self.button_history = QPushButton('🕒', self)
        self.button_history.setFixedSize(50, 50)
        self.button_history.setFont(self.font)
        #mettre le fond vide -> self.button_history.setStyleSheet("QPushButton { background-color: #f0f0f0; border: 0px; }")
        self.button_history.setLayoutDirection(Qt.RightToLeft) # Mettre le bouton à droite
        self.button_history.clicked.connect(self.show_history)
        self.layout.addWidget(self.button_history, 0, 3, 1, 1)

        buttons = [
            'C', '←', '7', '8', '9', '*',
            '4', '5', '6', '-',
            '1', '2', '3', '+',
            '0', '.', '/', '='
        ]

        # Traitement de la position des boutons
        row = 2
        col = 2
        # Taille des boutons
        button_width = 120
        button_height = 70

        # Création des boutons
        for button_text in buttons:
            button = QPushButton(button_text, self)  # Création du bouton
            button.setFont(self.font)
            if button_text == 'C':  # Si le bouton est C
                button.clicked.connect(
                    self.resetAll)  # Connecte à la fonction resetAll pour reinitialiser la calculatrice
            elif button_text == '←':
                button.clicked.connect(
                    self.backspace)  # Connecte à la fonction backspace pour supprimer le dernier caractère
            else:
                button.clicked.connect(
                    self.button_click)  # Connecte à la fonction button_click pour ajouter le texte du bouton à l'input

            button.setFixedSize(button_width, button_height)  # Taille du bouton
            self.layout.addWidget(button, row, col)  # Ajoute le bouton au layout

            # Traitement pour la matrice des boutons
            col += 1
            if col > 3:
                col = 0
                row += 1

        self.setLayout(self.layout)  # Ajout du layout de la fenêtre

    # Fonctions

    def show_history(self):
        self.historique_view.setVisible(not self.historique_view.isVisible())
        if self.historique_view.isVisible():
            self.resize(self.width() + self.historique_view.width(), self.height())
        else:
            self.resize(self.initial_width, self.height())
        #print the history
        self.print_history()
    def print_history(self):
        self.model_history.clear()
        for value in self.history:
            history_entry = f"{value[0]} = {value[1]}"
            self.model_history.appendRow(QStandardItem(history_entry))
    # Reinitialise la calculatrice
    def resetAll(self):
        self.current_input = ''
        self.display.setText('0')

    # Supprime le dernier caractère de l'input
    def backspace(self):
        self.current_input = self.current_input[:-1]
        self.display.setText(self.current_input)

    # Traitement de l'input
    def button_click(self):
        button = self.sender()
        button_val = button.text()

        if button_val == '=':
            try:
                input = self.current_input
                result = str(eval(input))
                self.display.setText(result)
                self.current_input = result
                # Ajoute l'expression et le résultat à l'historique
                self.history.append((input, result))
                if self.historique_view.isVisible():
                    self.print_history()
            except Exception as e:
                self.display.setText('Error')
                self.current_input = ''
        else:
            self.current_input += button_val  # Ajoute le texte du bouton à l'input
            self.display.setText(self.current_input)  # Affiche l'input dans le display


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculatrice()
    calc.show()
    sys.exit(app.exec_())
