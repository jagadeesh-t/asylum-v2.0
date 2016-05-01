from openerp.osv import fields, osv
import time
from datetime import datetime
from datetime import timedelta
from openerp.tools.translate import _
import base64


class hotel_purchase(osv.osv):
    _name = "hotel.purchase"
    _description = "Purchase Order"

    def write(self, cr, uid, ids, dict_val, context):
        super(hotel_purchase, self).write(cr, uid, ids, dict_val, context=context)
        for do in self.browse(cr, uid, ids, context=context):
            tot = sum([l.pts for l in do.inv_lines])
            points_bal = do.guest_id.points
            balance_final = points_bal - tot
            if balance_final < 0:
                raise osv.except_osv(_('Warning!'), _("Guest doesn't have enough points to process the order.!"))
        return True



    def order_lines_change(self, cr, uid, ids, lines, partner_id=False, context=None):
        context = context or {}
        prod_obj = self.pool.get('hotel.product')
        guest_obj = self.pool.get('hotel.guest.partner')
        line_obj = self.pool.get('hotel.purchase.lines')
        tot = 0.0
        bal = 0.0
        order_line_ids = self.resolve_o2m_commands_to_record_dicts(cr, uid, "inv_lines", lines, ["pts_unit","qty","product_id"], context=context)


        for item in  order_line_ids:
            if int == type(item['product_id']):
                tot=tot+ prod_obj.browse(cr, uid,item['product_id']).value*item['qty']
            else:
                tot=tot+ prod_obj.browse(cr, uid,item['product_id'][0]).value*item['qty']

        if partner_id:
            pbal = guest_obj.read(cr, uid, partner_id, ['points'])['points']
        else:
            pbal = 0.0

        bal = pbal - tot

        print tot
        print bal
        return {'value': {'tss_cs_total': tot, 'tss_cs_balance': bal}}

    def onchange_balance(self, cr, uid, ids, balance, context=None):
        """ Otherwise a warning is thrown.
        """
        res = {'value': {}}
        if balance < 0:
            exp_message = "Guest doesn't have enough points to process the order.!"
            warning = {'title': 'warning', 'message': exp_message}
            res['warning'] = warning
        return res


    #
    def _get_total(self, cr, uid, ids, field_name, arg, context=None):
        """
        @return: Dictionary of values.
        """
        ords = self.browse(cr, uid, ids, context=context)
        res = {}
        for ord in ords:
            val = 0.0
            if ord.inv_lines:
                for lines in ord.inv_lines:
                    val += lines.pts
            res[ord.id] = val
        return res

    def _get_balance(self, cr, uid, ids, field_name, arg, context=None):
        """
        @return: Dictionary of values.
        """
        ords = self.browse(cr, uid, ids, context=context)
        res = {}
        for ord in ords:
            val = 0.0
            if ord.guest_id:
                bal = ord.guest_id.points
            else:
                bal = 0.0
            if ord.inv_lines:
                for lines in ord.inv_lines:
                    val += lines.pts
            res[ord.id] = bal - val
        return res

    def button_update(self, cr, uid, ids, context=None):
        return True

    def button_cancel(self, cr, uid, ids, context=None):

        for do in self.browse(cr, uid, ids, context=context):
            time_now = time.strftime('%Y-%m-%d %H:%M:%S')
            return self.write(cr, uid, ids, {'state': 'cancel', 'date': time_now, }, context=context)

    def button_done_bill(self, cr, uid, ids, context=None):
        for do in self.browse(cr, uid, ids, context=context):
            time_now = time.strftime('%Y-%m-%d %H:%M:%S')
            try:
                stock = self.pool.get('hotel.stock.location').search(
                    cr, uid, [('name', 'ilike', 'stock')])
                sale = self.pool.get('hotel.stock.location').search(
                    cr, uid, [('name', 'ilike', 'sale')])
            except:
                raise osv.except_osv(_('Location Error!'), _(
                    'Please create location name "Stock" and "Sale"! Contact Administrator'))
            if do.tss_cs_balance < 0.0:
                raise osv.except_osv(
                    _('Warning!'), _("Guest doesn't have enough points to process the order.!"))
            for lines in do.inv_lines:
                self.pool.get('hotel.stock.transfer').create(cr, uid, {'name': do.name,
                                                                       'product_id': lines.product_id.id,
                                                                       'qty': lines.qty,
                                                                       'loc_id': stock[0],
                                                                       'loc_des_id': sale[0],
                                                                       'date': time_now,
                                                                       'user_id': uid,
                                                                       'state': 'done'}, context=context)
            self.pool.get('hotel.guest.points').create(cr, uid, {'guest_id': do.guest_id.id,
                                                                       'name': do.name,
                                                                       'purchase_id': do.id,
                                                                       'qty': -do.tss_cs_total,
                                                                       'date': time_now,
                                                                       }, context=context)
            self.write(
                cr, uid, ids, {'state': 'done', 'date': time_now, }, context=context)
            return {
                'type': 'ir.actions.report.xml',
                        'report_name': 'hotel.purchase',
                        'datas': {
                            'model': 'hotel.purchase',
                            'id': ids and ids[0] or False,
                            'ids': ids and ids or [],
                            'report_type': 'pdf'
                        },
                'nodestroy': True
            }

    def button_go_bill(self, cr, uid, ids, context=None):

        for do in self.browse(cr, uid, ids, context=context):
            product_lines = do.inv_lines
            if len(do.inv_lines) == 0:
                raise osv.except_osv(
                    _('Warning!'), _("Select atleast one product to process the order.!"))
            tot = sum([l.pts for l in do.inv_lines])
            points_bal = do.guest_id.points
            balance_final = points_bal - tot
            if balance_final < 0:
                raise osv.except_osv(_('Warning!'), _("Guest doesn't have enough points to process the order.!"))

            time_now = time.strftime('%Y-%m-%d %H:%M:%S')
            write_value = {'date': time_now, 'total_final': tot, 'tss_cs_total': tot, 'balance_final': balance_final, 'tss_cs_balance': balance_final}
            write_value['state'] = 'bill'
            return self.write(cr, uid, ids, write_value, context=context)

    def button_back_bill(self, cr, uid, ids, context=None):
        for do in self.browse(cr, uid, ids, context=context):
            return self.write(cr, uid, ids, {'state': 'draft'}, context=context)

    def _get_balance_pts(self, cr, uid, ids, field_name, arg, context=None):
        """
        @return: Dictionary of values.
        """
        lst_current_records = self.browse(cr, uid, ids, context=context)
        res = {}
        for current_record in lst_current_records:
            tot = sum([l.pts for l in current_record.inv_lines])
            points_bal = current_record.guest_id.points
            balance_final = points_bal - tot
            res[current_record.id] = balance_final
        return res

    def _constraints_balance_points_zero(self, cr, uid, ids, context=None):
        result =True
        for current_rec in self.browse(cr, uid, ids):
            if current_rec.tss_cs_balance < 0 and current_rec.state == "draft":
                result = False
        return result

    _columns = {
        'guest_id': fields.many2one('hotel.guest.partner', 'Guest Billing', select=True),
        'name': fields.char('Name', size=128, required=True, select=True),
        'tss_cs_total': fields.function(_get_total, string='Total', type='float'),
        #'balance': fields.function(_get_balance, string='Balance', type='float'),
        'total_final': fields.float('Total'),
        'balance_final': fields.float('Balance'),
        # 'balance': fields.function(_get_balance_pts, string='Balance', type='float', readonly=True),
        'tss_cs_balance': fields.float('Balance'),
        # 'balance': fields.float('Balance'),
        'date': fields.datetime('Date', help="Date.", required=True, select=True, readonly=True),
        'state': fields.selection([
            ('draft', 'Draft'),
            ('bill', 'Billed'),
            ('done', 'Done'),
            ('cancel', 'Cancel'),
        ], 'Status', readonly=True, select=True),
        'user_id': fields.many2one('res.users', 'User', readonly=True),
        'inv_lines': fields.one2many('hotel.purchase.lines', 'inv_id', 'Purchase Order Lines', readonly=True, states={'draft': [('readonly', False)]}),
    }

    _defaults = {
        'date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
        'state': 'draft',
        'user_id': lambda obj, cr, uid, context: uid,
        'name': lambda obj, cr, uid, context: '/',
        'guest_id': lambda obj, cr, uid, context: context.get('guest_id', False),
        'tss_cs_balance': lambda obj, cr, uid, context: context.get('tss_cs_balance', False),
    }
    _constraints = [
        (_constraints_balance_points_zero, "Guest doesn't have enough points to process the order.!", ['Balance']),
    ]


    def create(self, cr, uid, vals, context=None):

        if context.get('guest_id', False):
            vals['guest_id'] = context.get('guest_id', False)
        product_lines = vals['inv_lines']
        if len(vals['inv_lines']) == 0:
            raise osv.except_osv(
                _('Warning!'), _("Select atleast one product to process the order.!"))
        lst_pts = []
        for l in vals['inv_lines']:
            product_rec = self.pool.get('hotel.product').browse(cr, uid, l[2]['product_id'])
            lst_pts.append(product_rec['value'] * l[2]['qty'])

        tot = sum(lst_pts)
        # tot = sum([l['pts'] for l in vals['inv_lines']])
        guest_rec = self.pool.get('hotel.guest.partner').browse(cr, uid, vals['guest_id'])

        points_bal = guest_rec['points']
        balance_final = points_bal - tot
        if balance_final < 0:
            raise osv.except_osv(_('Warning!'), _("Guest doesn't have enough points to process the order.!"))

        if vals.get('name', '/') == '/':
            vals['name'] = self.pool.get('ir.sequence').get(
                cr, uid, 'hotel.purchase') or '/'

        return super(hotel_purchase, self).create(cr, uid, vals, context=context)


hotel_purchase()


class hotel_purchase_lines(osv.osv):
    _name = "hotel.purchase.lines"
    _description = "Purchase Order Lines"

    def _get_total_pts(self, cr, uid, ids, field_name, arg, context=None):
        """
        @return: Dictionary of values.
        """
        lines = self.browse(cr, uid, ids, context=context)
        res = {}
        for line in lines:
            res[line.id] = line.product_id.value * line.qty
        return res

    def _get_pts_unit(self, cr, uid, ids, field_name, arg, context=None):
        """
        @return: Dictionary of values.
        """
        lines = self.browse(cr, uid, ids, context=context)
        res = {}
        for line in lines:
            res[line.id] = line.product_id.value
        return res

    def _constraint_product_empty(self, cr, uid, ids, context=None):
        result = True
        for current_record in self.browse(cr, uid, ids):
            if not current_record.product_id:
                result = False
        return result

    _columns = {
        'inv_id': fields.many2one('hotel.purchase', 'INV'),
        'product_id': fields.many2one('hotel.product', 'Product', select=True),
        'pts_unit': fields.float('Points', digits=(14, 3)),
        'pts': fields.function(_get_total_pts, string='Total Points', type='float', readonly=True),
        'qty': fields.float('Quantity', digits=(14, 3)),
    }
    _constraints = [
        (_constraint_product_empty, "Warning! Product won't be empty.", ['Product']),
    ]
    _defaults = {
        'qty': 0.00,
    }

    def create(self, cr, uid, vals, context=None):
        print "valshotel_purchase_lines",vals
        if not vals['product_id']:
            return True
        if not vals.get('pts_unit', None):
            vals['pts_unit'] = self.pool.get('hotel.product').read(
                cr, uid, vals['product_id'], ['value'])['value']
        return super(hotel_purchase_lines, self).create(cr, uid, vals, context=context)

    def product_id_change(self, cr, uid, ids, product, partner_id=False, flag=False, context=None):
        context = context or {}
        if not partner_id:
            raise osv.except_osv(_('No Customer Defined !'), _(
                'Please use Cashier Page,\n to initiate the order.'))
        return {'value': {'qty': 1.00, 'product_id': product}}

    def onchange_product_id(self, cr, uid, ids, product_id, qty, context=None):
        """ Otherwise a warning is thrown.
        """
        res = {'value': {}}
        if not product_id:
            return res
        else:
            for prod in self.pool.get('hotel.product').browse(cr, uid, [product_id]):
                if qty:
                    if prod.total_stock < qty:
                        warning_msg = _(
                            'Product %s has low stock. Are you sure you want to select this Product!!') % (prod.name)
                        res.update({'warning': {
                            'title': _('Warning'),
                            'message': warning_msg,
                        }
                        })
                        res['value']['qty'] = qty
                        res['value']['pts_unit'] = prod.value
                        res['value']['pts'] = qty * prod.value
                        return res
                    else:
                        res['value']['qty'] = qty
                        res['value']['pts_unit'] = prod.value
                        res['value']['pts'] = qty * prod.value
                        return res
                else:
                    return res


    def on_change_qty(self, cr, uid, ids, product_id, qty, pts_unit,tss_cs_balance, tss_cs_total, context=None):
        """ Otherwise a warning is thrown.
        """
        res = {'value': {}}
        if product_id and qty:
            product_obj = self.pool.get("hotel.product")
            current_record = product_obj.browse(cr, uid, product_id)
            warning_msg_points=''
            status=False
            if tss_cs_balance <= tss_cs_total+qty * pts_unit:
                status=True
                warning_msg_points="Guest doesn't have enough points to process the order.!\n"

            if current_record.total_stock < qty:
                status=True
                warning_msg_points+'Product %s has low stock.' % (current_record.name)

            if status:
                qty=0
                warning_msg = _(
                    warning_msg_points+'Product %s has low stock.') % (current_record.name)
                res.update({'warning': {
                    'title': _('Warning'),
                    'message': warning_msg,
                }
                })
            res['value']['qty'] = qty
            res['value']['pts'] = qty * pts_unit
            return res

        if qty:
            res['value']['pts'] = qty * pts_unit
        return res

hotel_purchase_lines()