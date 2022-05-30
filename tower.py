import constants
from PyQt5 import QtGui, QtCore
from math import *


class Tower(object):
	def __init__(self):
		self.x_pos = -100
		self.y_pos = -100
		self.size = 1
		self.occupied = []
		self.range = 120
		self.cost = 0
		self.color = QtGui.QColor(0, 0, 0)

	def get_center(self):
		return QtCore.QPoint(self.x_pos + (self.size * 20 / 2), self.y_pos + self.size * 20 / 2)

	def get_occupied(self):
		return self.occupied

	def get_range(self):
		return self.range

	def in_range(self, target):
		towerX = self.get_center().x()
		towerY = self.get_center().y()
		enemyX = target.get_center().x()
		enemyY = target.get_center().y()
		return int(sqrt(pow(towerX - enemyX, 2) + pow(towerY - enemyY, 2))) <= self.range

	def find_target(self, targets):
		arr = []
		for target in targets:
			if self.in_range(target):
				arr.append(target)
		try:
			s = len(arr) - 1
			return [arr[s]]
		except:
			return []


class R2X2(Tower):
	def __init__(self):
		super(R2X2, self).__init__()
		self.size = 1
		self.range = 30
		self.cost = 150
		self.damage = 5
		self.rof = 4
		self.color = QtGui.QColor(0, 116, 63)


class BB8(Tower):
	def __init__(self):
		super(BB8, self).__init__()
		self.size = 1
		self.range = 50
		self.cost = 600
		self.damage = 20
		self.rof = 2
		self.color = QtGui.QColor(241, 161, 4)


class R2D2(Tower):
	def __init__(self):
		super(R2D2, self).__init__()
		self.size = 2
		self.range = 70
		self.cost = 1000
		self.damage = 50
		self.rof = 1
		self.color = QtGui.QColor(30, 101, 167)
