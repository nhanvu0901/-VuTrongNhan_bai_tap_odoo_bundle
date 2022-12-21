from odoo import models, fields, api


class ProductType(models.Model):

    _inherit = 'product.product'
    bundle = fields.Many2one('product.bundle')
    product_qty = fields.Integer("Quantity")
    product_variant = fields.Char("Product variant",compute='get_product_varient')
    discount_value = fields.Char("Discount value")


    def get_product_varient(self):
      for product in self:
          temp1=""
          temp2=""
          for variant in product.product_template_variant_value_ids:
              if variant.display_name:
                  temp1 +=variant.display_name

      self.product_variant = temp1











