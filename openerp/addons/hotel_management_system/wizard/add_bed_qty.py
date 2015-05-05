from openerp.osv import osv, fields
class add_bed_qty(osv.TransientModel):
    _name = "add.bed.qty"
    _description = "Add The Bed Qty"

    def _check_avi_bed_type(self, cr, uid, ids, context=None):
        total_avi_bed=0
        for avi_bed in self.browse(cr, uid, ids):
            list_bed_types=self.pool.get("hotel.bed.type").search(cr, uid, [('id', '=', avi_bed.bed_type.id)],context=None)
            for list_bed_type_value in self.pool.get("hotel.bed.type").read(cr, uid, list_bed_types, ['available_stock'], context=context):
                total_avi_bed=total_avi_bed+list_bed_type_value['available_stock']
        if total_avi_bed >= avi_bed.qty:
            return True
        else:
            return False


    _columns = {
        'bed_type': fields.many2one('hotel.bed.type', 'Bed Type', required=True),
        'qty': fields.integer('Quantity'),
    }
    _constraints = [
        (_check_avi_bed_type, 'Error! Requested Number of Bed Are Not Avilable.', ['bed_type'])
    ]

    def add_bed_qty(self, cr, uid, ids, context=None):
        for active_ids in context['active_ids']:
            values={}
            for bed_qty in self.browse(cr,uid,ids):
                list_ids=self.pool.get("hotel.room.bed").search(cr, uid, [('room_id', '=', active_ids),('id', '=', bed_qty.bed_type.id)],context=None)
                if len(list_ids)!=0:
                    total_bed_calculation=0
                    for list_bed_qty in self.pool.get("hotel.room.bed").read(cr, uid, list_ids, ['bed_qty'], context=context):
                        total_bed_calculation=total_bed_calculation+list_bed_qty['bed_qty']
                    total_bed_calculation=total_bed_calculation+bed_qty.qty
                    values['bed_qty']=total_bed_calculation
                    self.pool.get("hotel.room.bed").write(cr, uid, [active_ids], values, context=None)
                else:
                    for bed_qty in self.browse(cr,uid,ids):
                        values['room_id']=active_ids
                        values['name']=bed_qty.bed_type.id
                        values['bed_qty']=bed_qty.qty
                        self.pool.get("hotel.room.bed").create(cr, uid, values, context=None)

        return {'type': 'ir.actions.act_window_close'}

add_bed_qty()

