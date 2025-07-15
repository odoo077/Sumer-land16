# -*- coding: utf-8 -*-
# from odoo import http


# class SaleReturn(http.Controller):
#     @http.route('/sale_return/sale_return/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sale_return/sale_return/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sale_return.listing', {
#             'root': '/sale_return/sale_return',
#             'objects': http.request.env['sale_return.sale_return'].search([]),
#         })

#     @http.route('/sale_return/sale_return/objects/<model("sale_return.sale_return"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sale_return.object', {
#             'object': obj
#         })
