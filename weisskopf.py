#!/usr/bin/env python3

import math
import sympy
import sys

from PyQt4 import uic, QtGui, QtCore

from util import fill_placeholder
from latex_label import LatexLabel


# Load the GUI class from the .ui file
(Ui_MainWindow, QMainWindow) = uic.loadUiType('layout.ui')

# Define a class for the main window.
class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        # Initialize the GUI itself
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self._setup_formulas()
        self._connect_buttons()

        self._update_all()

    def _setup_formulas(self):
        label = LatexLabel(self)
        label.latex_text = (r'$' +
                            r'B_W(E\lambda) = \left(\frac{1}{4\pi}\right)' +
                            r'\left[ \frac{3}{3+\lambda} \right]^2' +
                            r'(1.2A^{1/3})^{2\lambda}' +
                            r'e^2\ \mathrm{fm}^{2\lambda}' +
                            r'$')
        fill_placeholder(self.ui.disp_b_e_lambda, label)

        label = LatexLabel(self)
        label.latex_text = (r'$' +
                            r'B_W(M\lambda) = \left(\frac{10}{\pi}\right)' +
                            r'\left[ \frac{3}{3+\lambda} \right]^2' +
                            r'(1.2A^{1/3})^{2\lambda - 2}' +
                            r'\mu_N^2\ \mathrm{fm}^{2\lambda - 2}' +
                            r'$')
        fill_placeholder(self.ui.disp_b_m_lambda, label)

        lambd,A,e,fm,mu_N = sympy.symbols('lambda A e fm mu_N')
        one = sympy.S(1)
        pi = sympy.pi

        self.subs_elambda = LatexLabel(self)
        fill_placeholder(self.ui.disp_subs_elambda, self.subs_elambda)

        self.subs_all = LatexLabel(self)
        fill_placeholder(self.ui.disp_subs_all, self.subs_all)

        self.disp_e_fm = LatexLabel(self)
        fill_placeholder(self.ui.output_e_fm, self.disp_e_fm)

        self.disp_wu = LatexLabel(self)
        fill_placeholder(self.ui.output_wu, self.disp_wu)

        self.base_formula = {
            'E': (3/(3+lambd))**2 / (4*pi)  * (1.2 * A**(one/3))**(2*lambd) * e**2 * fm**(2*lambd),
            'M': (3/(3+lambd))**2 * (10/pi) * (1.2 * A**(one/3))**(2*lambd-2) * mu_N**2 * fm**(2*lambd-2),
        }

    def _connect_buttons(self):
        self.ui.input_lambda.valueChanged.connect(self._update_all)
        self.ui.input_type.currentIndexChanged.connect(self._update_all)
        self.ui.nucleus_A.valueChanged.connect(self._update_all)
        self.ui.input_e_fm.valueChanged.connect(self._update_all)
        self.ui.input_wu.valueChanged.connect(self._update_all)

    def _update_all(self,*args):
        self._update_formulas()
        self._update_calc()

    def _update_formulas(self):
        transition_type = self.ui.input_type.currentText()
        transition_lambda = self.ui.input_lambda.value()
        nucleus_A = self.ui.nucleus_A.value()

        formula = self.base_formula[transition_type]
        formula = formula.subs({sympy.symbols('lambda'):transition_lambda,
                                sympy.pi:math.pi}).simplify()

        self.subs_elambda.latex_text = '$' + sympy.latex(formula) + '$'

        formula = formula.subs({sympy.symbols('A'):nucleus_A}).evalf()

        self.subs_all.latex_text = '$' + sympy.latex(formula) + '$'

        self.conversion = formula.args[0]
        self.units = formula/self.conversion

    def _update_calc(self):
        input_wu = self.ui.input_wu.value()
        input_e_fm = self.ui.input_e_fm.value()

        output_e_fm = input_wu * self.conversion
        output_wu = input_e_fm / self.conversion

        self.disp_wu.latex_text = ('$' +
                                   '{}'.format(output_wu) +
                                   r'\ \mathrm{w.u.}' +
                                   '$')

        self.disp_e_fm.latex_text = ('$' +
                                     '{}'.format(output_e_fm) +
                                     sympy.latex(self.units) +
                                     '$')


if __name__=='__main__':
    # Initialize the qt event loop.
    app = QtGui.QApplication(sys.argv)
    # Initialize and display our main window.
    w = MainWindow()
    w.show()
    # Run the qt event loop, exiting the script when done.
    sys.exit(app.exec_())
