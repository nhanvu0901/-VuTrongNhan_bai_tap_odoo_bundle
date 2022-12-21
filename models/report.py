from odoo import models, fields, api


class Report(models.Model):
    _name ="product.bundle.report"



    bundle_id = fields.Char()
    product_id = fields.Char()
    total_sale = fields.Char()
    total_save = fields.Char()


