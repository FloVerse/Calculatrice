import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QGridLayout


class Calculatrice(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.current_input = ''
        self.history = []
        self.display = None
        self.layout = None
        self.initUI()

    def initUI(self):
        super().__init__()
        self.setWindowTitle('Calculatrice')
        self.setGeometry(100, 100, 300, 400)

        self.layout = QGridLayout(self)

        self.display = QLineEdit(self)
        self.layout.addWidget(self.display, 0, 0, 1, 4)

        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+', 'C','←'
        ]

        # Traitement de la position des boutons
        row = 1
        col = 0
        # Taille des boutons
        button_width = 60
        button_height = 60

        # Création des boutons
        for button_text in buttons:
            button = QPushButton(button_text, self) # Création du bouton
            if button_text == 'C': # Si le bouton est C
                button.clicked.connect(self.resetAll) # Connecte à la fonction resetAll pour reinitialiser la calculatrice
            elif button_text == '←':
                button.clicked.connect(self.backspace) # Connecte à la fonction backspace pour supprimer le dernier caractère
            else:
                button.clicked.connect(self.button_click) # Connecte à la fonction button_click pour ajouter le texte du bouton à l'input

            button.setFixedSize(button_width, button_height) # Taille du bouton
            self.layout.addWidget(button, row, col) # Ajoute le bouton au layout

            #Traitement pour la matrice des boutons
            col += 1
            if col > 3:
                col = 0
                row += 1

        self.setLayout(self.layout)  # Ajout du layout de la fenêtre


    def resetAll(self):
        self.current_input = ''
        self.display.setText('')

    def backspace(self):
        self.current_input = self.current_input[:-1]
        self.display.setText(self.current_input)
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
