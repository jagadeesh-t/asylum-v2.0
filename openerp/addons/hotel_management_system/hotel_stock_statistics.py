from openerp.osv import fields, osv
import time
from datetime import datetime
from datetime import timedelta
from openerp.tools.translate import _
import base64


class hotel_stock_statistics(osv.osv):
    _name = "hotel.stock.statistics"
    _description = "Stock Statistics"

    def button_gen_stats(self, cr, uid, ids, context=None):
        for do in self.browse(cr, uid, ids, context=context):
            if not (do.date_start and do.date_end):
                raise osv.except_osv(
                    _('Warning !'), _('Please specify Start and End Date to generate statistics.'))

            trans_obj = self.pool.get('hotel.stock.transfer')
            prod_obj = self.pool.get('hotel.product')
            line_obj = self.pool.get('hotel.stock.statistics.lines')
            sols = line_obj.search(cr, uid, [('stats_id', '=', do.id)])
            line_obj.unlink(cr, uid, sols, context)
            prod_ids = prod_obj.search(cr, uid, [])
            t_point = 0.0
            for prod in prod_ids:
                points, serv, serv_in, serv_start = 0.0, 0.0, 0.0, 0.0
                sm_ids = trans_obj.search(
                    cr, uid, [('product_id.id', '=', prod), ('state', '=', 'done')])
                for sm in trans_obj.browse(cr, uid, sm_ids):
                    if sm.date[:10] < do.date_start:
                        if sm.loc_des_id.name == 'Stock':
                            serv_start += sm.qty
                        else:
                            serv_start -= sm.qty
                    if do.date_start <= sm.date[:10] <= do.date_end:
                        if sm.loc_des_id.name == 'Stock':
                            serv_in += sm.qty
                        else:
                            serv += sm.qty

                    points += sm.qty * sm.product_id.value

                t_point += points
                line_obj.create(cr, uid, {'stats_id': do.id,
                                          'product_id': prod,
                                          'points': points,
                                          'serving': serv,
                                          'serving_start': serv_start,
                                          'serving_end': serv_start + serv_in - serv,
                                          'serving_in': serv_in,
                                          })
            name = 'Stats from %s to %s' % (do.date_start, do.date_end)
            return self.write(cr, uid, ids, {'total': t_point, 'name': name}, context=context)

    def print_csv_report(self, cr, uid, ids, context=None):
        """
        @param self: The object pointer.
        @param cr: A database cursor
        @param uid: ID of the user currently logged in
        @param ids: List of IDs selected
        @param context: A standard dictionary
        @return:
        """
        contents = ""
        pick_ids = []
        cr.execute(
            """DELETE FROM ir_attachment WHERE res_model ='hotel.stock.stats'""")
        for wiz in self.browse(cr, uid, ids, context=context):
            fname = "Statistics from %s to %s.csv" % (
                wiz.date_start[5:], wiz.date_end[5:])
            contents += "Statistics from %s to %s \n Product,Points,Serving,Serving Start,Serving End,Serving In\n" % (
                wiz.date_start, wiz.date_end)
            for line in wiz.stat_lines:
                contents += line.product_id.name + "," + str(line.points) + "," + str(line.serving) + "," + str(
                    line.serving_start) + "," + str(line.serving_end) + "," + str(line.serving_in) + "\n"
            contents += "Total Points,%s" % (wiz.total)
            for i in ids:
                integer_id = int(i)

            data_attach = {'name': fname,
                           'datas': base64.encodestring(contents.encode('utf-8')),
                           'datas_fname': fname,
                           'res_model': self._name,
                           'description': 'description',
                           'res_id': i}
            attach_id = self.pool.get(
                'ir.attachment').create(cr, uid, data_attach)
            mod_obj = self.pool.get('ir.model.data')
            pick_ids.append(attach_id)
            action_model, action_id = tuple(
                mod_obj.get_object_reference(cr, uid, 'base', 'action_attachment'))
            action = self.pool.get(action_model).read(
                cr, uid, action_id, context=context)
            ctx = eval(action['context'])
            if pick_ids and len(pick_ids) == 1:
                form_view_ids = [
                    view_id for view_id, view in action['views'] if view == 'form']
                view_id = form_view_ids and form_view_ids[0] or False
                action.update({
                    'views': [],
                    'view_mode': 'form',
                    'view_id': view_id,
                    'res_id': pick_ids[0]
                })
            action.update({
                'context': ctx,
            })
            return action

    _columns = {
        'name': fields.char('Name', size=128, select=True),
        'date_start': fields.date('Start Date', help="Date.", required=True, select=True),
        'date_end': fields.date('End Date', help="Date.", required=True, select=True),
        'total': fields.float('Total Points'),
        'stat_lines': fields.one2many('hotel.stock.statistics.lines', 'stats_id', 'Statistics Lines', readonly=True),
    }

    _defaults = {
        'date_start': lambda *a: (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
        'date_end': lambda *a: (datetime.now()).strftime('%Y-%m-%d'),
    }

hotel_stock_statistics()


class hotel_stock_statistics_lines(osv.osv):
    _name = "hotel.stock.statistics.lines"
    _description = "Stock Statistics lines"

    _columns = {
        'stats_id': fields.many2one('hotel.stock.statistics', 'stats'),
        'product_id': fields.many2one('hotel.product', 'Product'),
        'points': fields.float('Points'),
        'serving': fields.float('Serving', digits=(14, 3)),
        'serving_start': fields.float('Serving at Start Date', digits=(14, 3)),
        'serving_end': fields.float('Serving at End Date', digits=(14, 3)),
        'serving_in': fields.float('Serving IN', digits=(14, 3)),
    }
hotel_stock_statistics_lines()
