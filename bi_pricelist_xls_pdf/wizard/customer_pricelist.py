# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from datetime import date, timedelta, datetime
from odoo.tools.misc import xlwt
from odoo.exceptions import UserError
from io import BytesIO
import io
import base64



class CustomerPricelistReport(models.TransientModel):
    _name = 'customer.pricelist.wiz'
    _description = 'Customer Pricelist'

    def print_customer_pricelist_xls_report(self):

        filename = 'Customer Pricelist Report' + '.xls'
        workbook = xlwt.Workbook()
        font = xlwt.Font()
        font.bold = True
        for_left = xlwt.easyxf(
            "font: bold 1, color black; borders: top double, bottom double, left double, right double; align: horiz left")
        for_left_not_bold = xlwt.easyxf("font: color black; align: horiz left",num_format_str='0.00')
       
        alignment = xlwt.Alignment()  # Create Alignment
        alignment.horz = xlwt.Alignment.HORZ_RIGHT
        

        active_ids=self.env.context.get('active_ids')
        partner = self.env['res.partner'].search([('id','in',active_ids)])
        for data in partner:
            worksheet = workbook.add_sheet(data.name)
            worksheet.row(1).height = 500
            worksheet.row(2).height = 500
            worksheet.col(0).width = 10000
            worksheet.col(1).width = 4000
            worksheet.col(2).width = 4000
            worksheet.col(3).width = 4000
            worksheet.col(4).width = 4000
     
            row = 1
            worksheet.write(row, 0, 'PARTNER NAME' or '', for_left)
            worksheet.write(row, 4, 'PRICELIST NAME' or '', for_left)
            worksheet.write(row+1, 0, data.name or '', for_left)
            worksheet.write(row+1, 4, data.property_product_pricelist.name or '', for_left)
                
            row=3
            worksheet.write(row, 0, "PRODUCT NAME", for_left)
            worksheet.write(row, 1, "PRICE", for_left)
            worksheet.write(row, 2, "DISCOUNT PERCENTAGE", for_left)
            worksheet.write(row, 3, "Discount AMOUNT", for_left)
            worksheet.write(row, 4, "Discount PRICE", for_left)

            row=4
            data_price = self.env['product.template'].search([])
            for rec in data_price:
                dis_amt = 0.00
                dis =0.00
                price =data.property_product_pricelist._compute_price_rule([(rec, 1.0, data)], date=fields.Date.today(), uom_id=rec.uom_id.id)[rec.id][0]
                if rec.list_price > price:
                    dis_amt = rec.list_price - price
                    dis = (100 * dis_amt)/rec.list_price

                worksheet.write(row, 0,rec.display_name or '',for_left_not_bold)
                worksheet.write(row, 1,rec.list_price or '0.00',for_left_not_bold)
                worksheet.write(row, 2,dis or '0.00',for_left_not_bold)
                worksheet.write(row, 3,dis_amt or '0.00',for_left_not_bold)
                worksheet.write(row, 4,price or '0.00',for_left_not_bold)
                row+=1
           
        fp = io.BytesIO()
        workbook.save(fp)
        customer_pricelist_id = self.env['customer.pricelist.extended'].create(
            {'excel_file': base64.encodestring(fp.getvalue()), 'file_name': filename})
        fp.close()

        return{
            'view_mode': 'form',
            'res_id': customer_pricelist_id.id,
            'res_model': 'customer.pricelist.extended',
            'type': 'ir.actions.act_window',
            'context': self._context,
            'target': 'new',
        }

    # PDF Report
    def print_customer_pricelist_pdf(self):
        active_ids=self.env.context.get('active_ids')
        partner = self.env['res.partner'].search([('id','in',active_ids)])
        partner_list=[]
        for data in partner:
            partner_list.append({'partner_name':data.name, 'pricelist_name': data.property_product_pricelist.name})
            data_price= self.env['product.template'].search([])
            data_list = []
            for rec in data_price:
                dis_amt = 0.00
                dis =0.00
                price =data.property_product_pricelist._compute_price_rule([(rec, 1.0, data)], date=fields.Date.today(), uom_id=rec.uom_id.id)[rec.id][0]
                if rec.list_price > price:
                    dis_amt = rec.list_price - price
                    dis = (100 * dis_amt)/rec.list_price    

                data_list.append({'product_name':rec.display_name,'price':rec.list_price,'dis_per':dis,'dis_amt':dis_amt,'dis_price':price})

        datas = {'ids': self.ids,
                'form': self.ids,
                'model':'customer.pricelist.wiz',
                'partner_list': partner_list,
                'data_list': data_list,
                }
        return self.env.ref('bi_pricelist_xls_pdf.action_report_customer_pricelist_pdf').with_context().report_action(self, data=datas)
 


class CustomerPricelistExtended(models.Model):
    _name = 'customer.pricelist.extended'
    _description = "Customer Pricelist Extended"

    excel_file = fields.Binary('Download Report :- ')
    file_name = fields.Char('Excel File', size=64)


