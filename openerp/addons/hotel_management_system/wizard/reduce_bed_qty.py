__author__ = 'pradeep'
from openerp.osv import osv, fields
class reduce_bed_qty(osv.TransientModel):
    _name = "reduce.bed.qty"
    _description = "Reduce Bed Qty"

    def _check_red_bed_type(self, cr, uid, ids, context=None):
        # print context['active_ids']
        print self.browse(cr, uid, ids)
        # total_avi_bed=0
        # for avi_bed in self.browse(cr, uid, ids):
        #     list_bed_types=self.pool.get("hotel.room.bed").search(cr, uid, [('name', '=', avi_bed.bed_type.id)],context=None)
        #     for list_bed_type_value in self.pool.get("hotel.bed.type").read(cr, uid, list_bed_types, ['available_stock'], context=context):
        #         total_avi_bed=total_avi_bed+list_bed_type_value['available_stock']
        # if total_avi_bed >= avi_bed.qty:
        #     return True
        # else:
        return False

    def _get_bed_type(self, cr, uid, context=None):
        list_assign_rooms=[False]
        if context.get('active_id'):
            list_avi_room_ids=self.pool.get("hotel.room.bed").search(cr, uid, [('room_id', '=', context.get('active_id'))],context=None)
            for list_avi_room_name_ids in self.pool.get("hotel.room.bed").read(cr, uid, list_avi_room_ids, ['name'], context=context):
                list_assign_rooms.append(list_avi_room_name_ids['name'][0])
        return list_assign_rooms


    _columns = {
        'bed_type': fields.many2one('hotel.bed.type', 'Bed Type', required=True,),
        'qty': fields.integer('Quantity'),
    }
    # _constraints = [
    #     (_check_red_bed_type, 'Error! Requested Number of Bed Are Not Avilable.', ['bed_type'],)
    # ]
    _defaults = {
            'bed_type': _get_bed_type,
    }

    def reduce_beds(self, cr, uid, ids, context=None):
        for active_ids in context['active_ids']:
            values={}
            list_avi_bed_qty=0
            for remove_beds in self.browse(cr, uid, ids):
                list_avi_bed=self.pool.get("hotel.room.bed").search(cr, uid,[('room_id','=',active_ids),('name','=',remove_beds.bed_type.id)])
                if len(list_avi_bed) != 0:
                    for list_avi_bed_type in self.pool.get("hotel.room.bed").read(cr, uid, list_avi_bed,['bed_qty']):
                        list_avi_bed_qty=list_avi_bed_qty+list_avi_bed_type['bed_qty']
                        if list_avi_bed_qty == remove_beds.qty:
                            self.pool.get("hotel.bed.type").unlink(cr, uid, list_avi_bed, context=None)
                        elif list_avi_bed > remove_beds.qty:
                            values={}
                            values['bed_qty']=list_avi_bed_qty-remove_beds.qty
                            self.pool.get("hotel.bed.type").write(cr, uid, list_avi_bed, values, context=None)
                        else:
                            pass
                else:
                    pass



        # eeeeeeeeeeeee
        return {'type': 'ir.actions.act_window_close'}

reduce_bed_qty()

