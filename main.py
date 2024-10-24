import sys
import sympy as sp
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PySide6.QtGui import QPixmap, QIcon
from UI.main_window import Ui_MainWindow
from services.calculations import middle_rectangles, trapezoidal, monte_carlo

matplotlib.use('TkAgg')

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Числові методи обчислення інтегралів")
        self.setWindowIcon(QIcon("ico.png"))
        self.ui.calc_btn.clicked.connect(self.calculate)
        self.ui.chart_btn.clicked.connect(self.show_chart)
        self.ui.function_input.setText("1/(sqrt(x**2+1))")
        self.ui.X1SpinBox.setValue(0.2)
        self.ui.X2SpinBox.setValue(1.2)
        self.prev_method = None 
    
    def convert_func(self, func):
        x = sp.symbols('x')
        expr = sp.sympify(func)
        return expr, x
    
    def show_chart(self):
        function_str = self.ui.function_input.text()
        x1 = self.ui.X1SpinBox.value()
        x2 = self.ui.X2SpinBox.value()
        
        expr, x = self.convert_func(function_str)
        
        f = sp.lambdify(x, expr, 'numpy')
        
        
        x_vals = np.linspace(x1, x2, 100)
        y_vals = f(x_vals)
        plt.figure(figsize=(4, 3), dpi=100)
        plt.plot(x_vals, y_vals, label=function_str)
        plt.axhline(0, color='black', linewidth=1.5) 
        plt.title(f'Графік функції {function_str}')
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.legend()
        plt.grid(True)
        plt.savefig('plot.png')
        self.ui.img_place.setPixmap(QPixmap("plot.png"))
    
    def clear_table(self):
        self.ui.results_table.clear()
        self.ui.results_table.setHorizontalHeaderLabels(['К-ть ітерацій', 'Корінь', 'Значення'])
        self.ui.results_table.setRowCount(0)
    
    def calculate(self):

        x1 = self.ui.X1SpinBox.value()
        x2 = self.ui.X2SpinBox.value()
        accuracy = self.ui.AccuracySpinBox.value()
        
        if (x1 != x2) and (accuracy != 0) and (x1 < x2):
            expr, x = self.convert_func(self.ui.function_input.text())
            rec = round(middle_rectangles(x1, x2, accuracy, expr, x), 5)
            trap = round(trapezoidal(x1, x2, accuracy, expr, x), 5)
            monte = round(monte_carlo(x1, x2, accuracy, expr, x), 5)
            analit = round(sp.integrate(expr, (x, x1, x2)), 5)
            row = self.ui.results_table.rowCount()
            self.ui.results_table.insertRow(row)
            self.ui.results_table.setItem(row, 0, QTableWidgetItem(str(accuracy)))
            self.ui.results_table.setItem(row, 1, QTableWidgetItem(str(analit)))
            self.ui.results_table.setItem(row, 2, QTableWidgetItem(str(rec)))
            self.ui.results_table.setItem(row, 3, QTableWidgetItem(str(trap)))
            self.ui.results_table.setItem(row, 4, QTableWidgetItem(str(monte)))
            self.show_chart()
            
            # if res:
            #     row = self.ui.results_table.rowCount()
            #     self.ui.results_table.insertRow(row)
            #     self.ui.results_table.setItem(row, 0, QTableWidgetItem(str(res[0])))
            #     self.ui.results_table.setItem(row, 1, QTableWidgetItem(str(res[1])))
            #     self.ui.results_table.setItem(row, 2, QTableWidgetItem(str(res[2])))
            #     self.show_chart(draw_point=res[1])
            #     self.ui.img_place.setPixmap(QPixmap("plot.png"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())