import sys
from PyQt5 import QtWidgets 

class Widget(QtWidgets.QDialog):
	def __init__(self, parent=None):
		super(Widget, self).__init__()

		grid = QtWidgets.QGridLayout()
		# grid.setSpacing(1)
		
		self.edit_first = QtWidgets.QLineEdit()
		grid.addWidget(QtWidgets.QLabel('Question 1'), 1, 0)
		grid.addWidget(self.edit_first, 1, 1)

		#   add layout for second widget
		self.edit_second = QtWidgets.QLineEdit()
		grid.addWidget(QtWidgets.QLabel('Question 2'), 2, 0)
		grid.addWidget(self.edit_second, 2, 1)

		apply_button = QtWidgets.QPushButton('Apply', self)
		apply_button.clicked.connect(self.accept)

		grid.addWidget(apply_button, 4, 3)
		self.setLayout(grid)
		self.setGeometry(300, 300, 350, 300)

	def return_strings(self):
		#   Return list of values. It need map with str (self.lineedit.text() will return QString)
		return list(map(str, [self.edit_first.text(), self.edit_second.text()]))

	@staticmethod
	def get_data(parent=None):
		dialog = Widget(parent)
		a = dialog.exec_()
		if a:
			return dialog.return_strings()
		else:
			return 'SHUTUP'

def main():
	app = QtWidgets.QApplication([])
	window = Widget()
	print (window.get_data())  # window is value from edit field


if __name__ == '__main__':
	main()
