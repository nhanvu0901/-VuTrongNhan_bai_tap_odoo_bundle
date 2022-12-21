

from odoo import models, fields, api ,_
from odoo.exceptions import ValidationError
from odoo.http import request


class Bundle(models.Model):
    _name = 'product.bundle'

    title = fields.Char(string="Title", required=False)
    description = fields.Char(string="Description")
    bundle_type = fields.Selection([('bundle', 'Multiple Product Bundle (Discount by Purchasing Multiple Products)'), (
    'tier', 'Quantity Break Bundle (Discount by Purchasing a Product in a Larger Quantity)')], default='bundle',
                                   required=True)
    discount_rule = fields.Selection(
        [('discount_total', 'Discount on total bundle'), ('discount_products', 'Discount on each products/variants')], default='discount_total',
        required=True)

    discount_type = fields.Selection([('per', '%'), ('amount', 'Amount')], default='per', required=True)
    discount_value = fields.Integer(string="Discount value")
    enable = fields.Boolean(string='Enable')
    active = fields.Boolean(string='Active')
    priority = fields.Boolean(string='Priority')
    start_time = fields.Datetime(string='Start time')
    end_time = fields.Datetime(string='End time')
    indefinite_bundle = fields.Boolean(string='indefinte')

    product_total = fields.One2many('bundle.product.line','bundle')
    product_each = fields.One2many('bundle.product.line', 'bundle')
    product_tier= fields.One2many('bundle.product.line', 'bundle')

    quantity_ids = fields.One2many('product.bundle.qty', 'bundle_id', string='Quantity')
    product_variant = fields.Char("Product variant")

    @api.constrains('discount_value')
    def check_discount_value(self):
      if self.discount_value <0:
          raise ValidationError(_("Discount value greater than 0"))

    # @api.constrains('title')
    # def check_title(self):
    #    title_exist = request.env['product.bundle'].sudo().search([('title', '=', self.title)], limit=1)
    #    if title_exist:
    #        raise ValidationError(_("Title already exist choose again"))