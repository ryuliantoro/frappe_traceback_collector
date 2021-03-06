# -*- coding: utf-8 -*-
# Copyright (c) 2015, Maxwell Morais and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe.model.document import Document

class Traceback(Document):
	def onload(self):
		if not self.parent_traceback:
			self.seen = True
			
			frappe.db.set_value("Traceback", self.name, "seen", True)

			for relapsed in frappe.db.get_list("Traceback", filters=[[
				"Traceback", "parent_traceback", "=", self.name]]):
				frappe.db.set_value("Traceback", relapsed["name"], "seen", True)

			frappe.db.commit()

	def validate(self):
		parent = frappe.get_list('Traceback', filters=[
			['Traceback', 'evalue', '=', self.evalue],
			['Traceback', 'parent_traceback', '=', None]], fields=["name", "relapses", "seen"])

		if parent:
			parent = parent[0]
			self.update({"parent_traceback": parent['name']})
			frappe.db.set_value('Traceback', parent['name'], 'relapses', parent["relapses"] + 1)
			if parent["seen"]:
				frappe.db.set_value("Traceback", parent["name"], "seen", False)
