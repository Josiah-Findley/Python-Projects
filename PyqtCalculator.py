#!/usr/bin/env python3

# Filename: pycalc.py

"""PyCalc is a simple calculator built using Python and PyQt5."""
from math import *
import sys

# Import QApplication and the required widgets from PyQt5.QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from functools import partial
ERROR_MSG = 'ERROR'
class PyCalcCtrl:
    """PyCalc Controller class."""
    def __init__(self, model, view):
        """Controller initializer."""
        self._evaluate = model
        self._view = view
        # Connect signals and slots
        self._connectSignals()

    def _calculateResult(self):
        """Evaluate expressions."""
        result = self._evaluate(expression=self._view.displayText())
        self._view.setDisplayText(result)

    def _buildExpression(self, sub_exp):
        """Build expression."""
        if self._view.displayText() == ERROR_MSG:
            self._view.clearDisplay()

        expression = self._view.displayText() + sub_exp
        self._view.setDisplayText(expression)

    def _connectSignals(self):
        """Connect signals and slots."""
        for btnText, btn in self._view.buttons.items():
            if btnText not in {'=', 'C'}:
                btn.clicked.connect(partial(self._buildExpression, btnText))

        self._view.buttons['='].clicked.connect(self._calculateResult)
        self._view.display.returnPressed.connect(self._calculateResult)
        self._view.buttons['C'].clicked.connect(self._view.clearDisplay)




__version__ = '0.1'

# Create a subclass of QMainWindow to setup the calculator's GUI
# Create a subclass of QMainWindow to setup the calculator's GUI
class PyCalcUi(QMainWindow):
    """PyCalc's View (GUI)."""
    def __init__(self):
        """View initializer."""
        super().__init__()
        # Set some main window's properties
        self.setWindowTitle('PyCalc')
        self.setFixedSize(270, 310)
        # Set the central widget and the general layout
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        # Create the display and the buttons
        self._createDisplay()
        self._createButtons()

    def _createDisplay(self):
        """Create the display."""
        # Create the display widget
        self.display = QLineEdit()
        # Set some display's properties
        self.display.setFixedHeight(35)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        # Add the display to the general layout
        self.generalLayout.addWidget(self.display)

    def _createButtons(self):
        """Create the buttons."""
        self.buttons = {}
        buttonsLayout = QGridLayout()

        # Button text | position on the QGridLayout
        buttons = {'7': (0, 0),
                   '8': (0, 1),
                   '9': (0, 2),
                   '/': (0, 3),
                   'C': (0, 4),
                   '4': (1, 0),
                   '5': (1, 1),
                   '6': (1, 2),
                   '*': (1, 3),
                   '(': (1, 4),
                   '1': (2, 0),
                   '2': (2, 1),
                   '3': (2, 2),
                   '-': (2, 3),
                   ')': (2, 4),
                   '0': (3, 0),
                   '00': (3, 1),
                   '.': (3, 2),
                   '+': (3, 3),
                   ', ': (3, 4),
                   'pi': (4, 0),
                   'cos(': (4, 1),
                   'sin(': (4, 2),
                   'tan(': (4, 3),
                   'sqrt(': (4, 4),
                   'e': (5, 0),
                   'exp(': (5, 1),
                   'log(': (5, 2),
                   'pow(': (5, 3),
                   '=': (5, 4),

                   }
        # Create the buttons and add them to the grid layout
        for btnText, pos in buttons.items():
            self.buttons[btnText] = QPushButton(btnText)
            self.buttons[btnText].setFixedSize(50, 40)
            buttonsLayout.addWidget(self.buttons[btnText], pos[0], pos[1])
            # Add buttonsLayout to the general layout
            self.generalLayout.addLayout(buttonsLayout)

    def setDisplayText(self, text):
        """Set display's text."""
        self.display.setText(text)
        self.display.setFocus()

    def displayText(self):
        """Get display's text."""
        return self.display.text()

    def clearDisplay(self):
        """Clear the display."""
        self.setDisplayText('')

# Create a Model to handle the calculator's operation
def evaluateExpression(expression):
    """Evaluate an expression."""
    try:
        result = str(eval(expression,{'pi':pi,'cos(':cos,
                 'degrees(':degrees, 'e':e, 'exp(':exp,
                 'log(':log,'log2(':log2,'pow(':pow,
                 'radians(':radians, 'sin(':sin, 'sqrt(':sqrt,
                 'tan(':tan}))
    except Exception:
        result = ERROR_MSG

    return result

# Client code
def main():
    """Main function."""
    # Create an instance of QApplication
    pycalc = QApplication(sys.argv)
    # Show the calculator's GUI
    view = PyCalcUi()
    view.show()
    model = evaluateExpression
    PyCalcCtrl(model=model, view=view)
    # Create instances of the model and the controller

    # Execute calculator's main loop
    sys.exit(pycalc.exec_())

if __name__ == '__main__':
    main()