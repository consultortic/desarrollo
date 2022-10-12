# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Export Customers Pricelist in XLS/PDF',
    'version': '14.0.0.0',
    'category': 'Extra Tools',
    'summary': 'Export customer pricelist in excel export pricelist in excel export customer pricelist in pdf export pricelist in pdf export sales pricelist in excel pricelist export in xls export pricelist in xls export customer pricelist in xls pricelist xls report',
    'description' :"""
        This odoo app helps user to export multiple customer's pricelist (Group By Partner) in to multiple file type like PDF or Excel.
    """,
    'author': 'BrowseInfo',
    'website': 'https://www.browseinfo.in',
    "price": 19,
    "currency": 'EUR',
    'depends': ['sale_management','base','contacts'],
    'data': [
        'security/ir.model.access.csv',
        'report/report_view.xml',
        'wizard/customer_pricelist_view.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'live_test_url':'https://youtu.be/VEt11dlGDWs',
    "images":['static/description/Banner.png'],
}
