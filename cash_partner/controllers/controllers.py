# -*- coding: utf-8 -*-
# from odoo import http


# class CashPartner(http.Controller):
#     @http.route('/cash_partner/cash_partner', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cash_partner/cash_partner/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('cash_partner.listing', {
#             'root': '/cash_partner/cash_partner',
#             'objects': http.request.env['cash_partner.cash_partner'].search([]),
#         })

#     @http.route('/cash_partner/cash_partner/objects/<model("cash_partner.cash_partner"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cash_partner.object', {
#             'object': obj
#         })
