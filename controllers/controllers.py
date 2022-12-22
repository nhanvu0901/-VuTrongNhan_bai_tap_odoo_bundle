from odoo.tools.image import image_data_uri

import binascii
import os
from base64 import b64encode

import requests
import shopify
import werkzeug.utils
import xmltodict
from odoo.http import request

from odoo import http

import json
import random
import string

import werkzeug

from odoo import http
from odoo.http import request
from datetime import datetime


class ShopBundle(http.Controller):
    @http.route('/bundle', type='json', auth='none', cors='*', csrf=False, save_session=False)
    def bundle_frontend(self, **kwargs):
        product_id_template = request.jsonrequest.get("data")

        combo_sale = request.env['product.bundle'].sudo().search([])
        if product_id_template:
            bundle_line_list = request.env['bundle.product.line'].sudo().search(
                [('product.id', '=', product_id_template)])

            combo_list = []
            # get the combo
            for product in bundle_line_list:
                combo_list.append(product.bundle)

            list_combo = []
            for bundle in combo_list:

                if (bundle.discount_rule == "discount_total" and bundle.bundle_type == "bundle"):
                    list_product_total = []
                    temp1 = ""
                    for bundle_line in bundle.product_total:
                        image_url = image_data_uri(bundle_line.image_1920)
                        item = {
                            "product_name": bundle_line.product.name,
                            "default_code": bundle_line.default_code,
                            "quantity": bundle_line.quantity,
                            "product_price": bundle_line.price,
                            "image_url": image_url

                        }
                        list_product_total.append(item)

                    if (bundle.discount_type == 'per'):
                        temp1 = str(bundle.discount_value) + "%"
                    else:
                        temp1 = str(bundle.discount_value)

                    combo_info_total = {
                        "title": bundle.title,
                        "discount_amount": temp1,
                        "products": list_product_total,
                        "start_time": bundle.start_time.strftime(
                            "%m/%d/%Y") if bundle.indefinite_bundle == False else '',
                        "end_time": bundle.end_time.strftime("%m/%d/%Y") if bundle.indefinite_bundle == False else '',
                        "bundle_type": "total",
                    }
                    list_combo.append(combo_info_total)


                elif (bundle.bundle_type == "bundle" and bundle.discount_rule == "discount_products"):
                    list_product_each = []
                    for bundle_line in bundle.product_each:
                        item = {
                            "product_name": bundle_line.product.name,
                            "default_code": bundle_line.default_code,
                            "quantity": bundle_line.quantity,
                            "product_price": bundle_line.price,
                            "discount_value": bundle_line.discount_value,
                            "image_url": image_data_uri(bundle_line.image_1920)
                        }
                        list_product_each.append(item)
                    if (bundle.discount_type == 'per'):
                        discoumt_ammout = str(bundle.discount_value) + "%"
                    else:
                        discoumt_ammout = str(bundle.discount_value)

                    combo_info_each = {
                        "title": bundle.title,
                        "discount_amount": discoumt_ammout,
                        "products": list_product_each,

                        "start_time": bundle.start_time.strftime(
                            "%m/%d/%Y") if bundle.indefinite_bundle == False else '',
                        "end_time": bundle.end_time.strftime("%m/%d/%Y") if bundle.indefinite_bundle == False else '',
                        "bundle_type": "each"
                    }
                    list_combo.append(combo_info_each)
                else:
                    list_product_tier = []
                    list_quantity_sale = []
                    for quantity_sale in bundle.quantity_ids:
                        if (quantity_sale.Is_add_range == True):
                            quantity = {
                                "Is_add_range": quantity_sale.Is_add_range,
                                "Qty_start": quantity_sale.Qty_start,
                                "Qty_end": quantity_sale.Qty_end,
                                "Discount_value": quantity_sale.Discount_value
                            }
                            list_quantity_sale.append(quantity)
                        else:
                            quantity = {
                                "Is_add_range": quantity_sale.Is_add_range,
                                "Quantity": quantity_sale.Quantity,

                                "Discount_value": quantity_sale.Discount_value
                            }
                            list_quantity_sale.append(quantity)

                    for bundle_line in bundle.product_tier:
                        item = {
                            "product_name": bundle_line.product.name,
                            "default_code": bundle_line.default_code,
                            "quantity": bundle_line.quantity,
                            "product_price": bundle_line.price,
                            "discount_value": bundle.discount_value,
                            "image_url": image_data_uri(bundle_line.image_1920)
                        }
                        list_product_tier.append(item)
                    if (bundle.discount_type == 'per'):
                        discoumt_ammout = str(bundle.discount_value) + "%"
                    else:
                        discoumt_ammout = str(bundle.discount_value)
                    combo_info_tier = {
                        "title": bundle.title,
                        "discount_amount": discoumt_ammout,
                        "products": list_product_tier,
                        "quantity": list_quantity_sale,
                        "start_time": bundle.start_time.strftime(
                            "%m/%d/%Y") if bundle.indefinite_bundle == False else '',
                        "end_time": bundle.end_time.strftime("%m/%d/%Y") if bundle.indefinite_bundle == False else '',
                        "bundle_type": "tier"
                    }

                    list_combo.append(combo_info_tier)

            return json.dumps(list_combo)

    def compare_combo(self, request):
        discount_combo = request.env['product.bundle'].sudo().search([])

        if request.jsonrequest:

            item_list = json.loads(request.jsonrequest.get("data"))

            for combo in discount_combo:
                if (len(combo.product_total) == len(item_list) or len(combo.product_each) == len(item_list) or len(
                        combo.product_tier) == len(item_list)):
                    count = 0
                    if (combo.bundle_type != 'tier'):
                        for item in item_list:
                            product_exist = request.env['bundle.product.line'].sudo().search(
                                ['&', ('product.id', '=', int(item.get("product_id"))),
                                 ('quantity', '=', int(item.get('product_quantity'))), ('bundle.id', '=', combo.id)],
                                limit=1)
                            if product_exist:
                                count += 1
                                if count == len(item_list):
                                    flag = combo
                                    print(combo)
                                    return flag;
                    else:
                        change = False
                        for quanity in combo.quantity_ids:
                            for item in item_list:
                                if (quanity.Is_add_range == True):
                                    if (quanity.Qty_start <= int(item.get('product_quantity')) <= quanity.Qty_end):
                                        change = True
                                else:
                                    if (int(item.get('product_quantity')) > quanity.Quantity):
                                        change = True
                        for item in item_list:
                            product_exist = request.env['bundle.product.line'].sudo().search(
                                ['&', ('product.id', '=', int(item.get("product_id"))),
                                 ('bundle.id', '=', combo.id)],
                                limit=1)

                            if product_exist and change == True:
                                count += 1
                                if count == len(item_list):
                                    flag = combo
                                    print(combo)
                                    return flag;

    @http.route('/cart', type='json', auth='none', cors='*', csrf=False, save_session=False)
    def cart_frontend(self, **kwargs):
        if request.jsonrequest:

            bundle = self.compare_combo(request)
            if bundle:
                sum = ''
                # product_total
                if (bundle.discount_rule == "discount_total" and bundle.bundle_type == "bundle"):
                    price_list = []
                    for bundle_line in bundle.product_total:
                        price = {
                            "quantity": bundle_line.quantity,
                            "product_price": bundle_line.price
                        }

                        price_list.append(price)

                    total_money = 0
                    for item in price_list:
                        total_money += int(item.get("product_price")) * int(item.get("quantity"))
                        if (bundle.discount_type == 'per'):
                            money = (total_money - total_money * (int(bundle.discount_value) / 100))
                            sum = str(money)

                        else:
                            money = total_money - int(bundle.discount_value)
                            sum = str(money)

                elif (bundle.bundle_type == "bundle" and bundle.discount_rule == "discount_products"):
                    price_list = []
                    for bundle_line in bundle.product_each:
                        price = {
                            "quantity": bundle_line.quantity,
                            "product_price": bundle_line.price,
                            "product_discount": bundle_line.discount_value
                        }

                        price_list.append(price)
                    money=0
                    for item in price_list:
                        total_money = int(item.get("product_price")) * int(item.get("quantity"))
                        if (bundle.discount_type == 'per'):
                            money += total_money - total_money * (int(item.get("product_discount")) / 100)

                        else:
                            money += total_money - int(item.get("product_discount"))
                    sum = str(money)
                else:
                    item_list = json.loads(request.jsonrequest.get("data"))
                    price = 0
                    quantity_list = []
                    for product in bundle.product_tier:
                        price = product.price
                    sum_list = []
                    for quantity in bundle.quantity_ids:
                        if quantity.Is_add_range == True:
                            for item in item_list:
                                money = int(price) * int(item.get("product_quantity")) - int(price) * int(
                                    item.get("product_quantity")) * (int(quantity.Discount_value) / 100)
                                sum = "Buy " + str(quantity.Qty_start) + " to " + str(
                                    quantity.Qty_end) + " only pay " + str(money) + "$ "
                                sum_list.append(sum)
                        else:
                            for item in item_list:
                                money = int(price) * int(item.get("product_quantity")) - int(price) * int(
                                    item.get("product_quantity")) * (int(quantity.Discount_value) / 100)
                                sum = "Buy more than " + str(quantity.Quantity) + " only pay " + str(
                                    money) + "$ "
                                sum_list.append(sum)
                    return json.dumps(sum_list)

                return sum
