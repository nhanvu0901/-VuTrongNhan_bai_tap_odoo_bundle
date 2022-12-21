from odoo import models, fields, api ,_
from odoo.exceptions import ValidationError


class BundleProductLine(models.Model):
    _name ="bundle.product.line"

    product = fields.Many2one('product.template',string="Product")
    quantity = fields.Integer(string="Quantity")
    product_variant = fields.Many2one('product.product',domain="[('product_tmpl_id', '=', product)]")

    discount_value = fields.Char("Discount value")
    bundle = fields.Many2one('product.bundle')
    price = fields.Float("Product price",related="product.list_price")
    default_code = fields.Char('Product code',related='product.default_code')
    image_1920 = fields.Image("Image", related="product.image_1920")







