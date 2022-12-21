from odoo import models, fields, api


class Setiing(models.Model):
    _name = 'product.bundle.setting'


    Bundle_position = fields.Selection([('below', 'Below add to cart form'), ('above', 'Above add to cart form')], default='below', required=True)
    Bundle_number = fields.Integer()
    Bundle_title_color = fields.Char()
    Button_label = fields.Char()


