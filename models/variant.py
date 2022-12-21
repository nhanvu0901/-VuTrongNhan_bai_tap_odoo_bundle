from odoo import models, fields, api


class Variant(models.Model):

    _inherit = 'product.product'


    name = fields.Char(string="Name", required=False)


