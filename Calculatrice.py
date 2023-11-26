import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QGridLayout, QTextEdit, QLabel


class Calculatrice(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.label = None
        self.history_display = None
        self.button_history = None
        self.current_input = ''
        self.history = []
        self.font = QFont("Arial", 12)
        self.display = None
        self.layout = None
        self.initUI()

    def initUI(self):
        super().__init__()
        self.setWindowTitle('Calculatrice')
        self.setGeometry(100, 100, 500, 650)

        self.layout = QGridLayout(self)

        # Label
        self.label = QLabel('Standard', self)
        self.label.setFont(self.font)
        self.layout.addWidget(self.label, 0, 0, 1, 1)
        # Affichage
        self.display = QLineEdit(self)
        self.display.setFixedHeight(50)
        self.display.setFont(self.font)
        self.layout.addWidget(self.display, 1, 0, 1, 4)

        self.history_display = QTextEdit(self)
        self.history_display.setFixedHeight(50)
        self.history_display.setFont(self.font)
        self.history_display.setReadOnly(True)
        self.layout.addWidget(self.history_display, 1, 4, 1, 1)

        # Bouton historique
        self.button_history = QPushButton('Historique', self)
        self.button_history.clicked.connect(self.show_history)
        self.layout.addWidget(self.button_history, 0, 4)

        buttons = [
            'C', '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+', '←'
        ]

        # Traitement de la position des boutons
        row = 2
        col = 0
        # Taille des boutons
        button_width = 60
        button_height = 60

        # Création des boutons
        for button_text in buttons:
            button = QPushButton(button_text, self)  # Création du bouton
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
        self.history_display.clear()
        for value in self.history:
            history_entry = f"{value[0]} = {value[1]}"
            self.history_display.append(history_entry)

    # Reinitialise la calculatrice
    def resetAll(self):
        self.current_input = ''
        self.display.setText('')

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
