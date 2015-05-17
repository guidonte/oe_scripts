#! /usr/bin/python

from oe_argparser import oe_parse_args

from openerp.netsvc import init_logger
from openerp.modules.registry import RegistryManager

import sys


def main(argv):
    '''Fix partners for a broken database.'''
    args = oe_parse_args(argv)

    pool = registry = RegistryManager.get(args.database, update_module=False)
    cr = registry.db.cursor()
    uid = 1

    move_obj = pool.get('account.move')
    line_obj = pool.get('account.move.line')

    move_line_ids = line_obj.search(
        cr, uid, [('partner_id', 'like', 'NON CANC')])
    move_lines = line_obj.browse(cr, uid, move_line_ids)

    move_ids = move_obj.search(cr, uid, [('partner_id', 'like', 'NON CANC')])
    move_ids += [l.move_id.id for l in move_lines]
    move_ids = list(set(move_ids))
    print "%s moves" % len(move_ids)

    for i, move in enumerate(move_obj.browse(cr, uid, move_ids)):
        if not (i % 100):
            print i

        partner_id = None
        multiple_partners = False
        for line in move.line_id:
            if partner_id and partner_id != line.partner_id and \
               line.partner_id.id != 105:
                multiple_partners = True
                break

            if line.partner_id and line.partner_id.id != 105:
                partner_id = line.partner_id

        if multiple_partners:
            print "FOUND MOVE WITH MULTIPLE PARTNERS: ID %d. %s" % (move.id,
                                                                    move.ref)
            line_ids = line_obj.search(cr, uid, [('move_id', '=', move.id),
                                                 ('partner_id', '=', 105)])
            line_obj.write(cr, uid, line_ids, {'partner_id': None})

            continue

        line_ids = line_obj.search(cr, uid, [('move_id', '=', move.id)])

        if partner_id:
            move.write({'partner_id': partner_id.id})

            if move.journal_id.type in ['sale', 'purchase', 'sale_refund',
                                        'purchase_refund', 'bank', 'cash']:
                line_obj.write(cr, uid, line_ids, {
                    'partner_id': partner_id.id})
            else:
                line_ids = line_obj.search(
                    cr, uid, [('move_id', '=', move.id),
                              ('partner_id', '=', 105)])
                line_obj.write(cr, uid, line_ids, {'partner_id': None})
        else:
            move.write({'partner_id': None})
            line_obj.write(cr, uid, line_ids, {'partner_id': None})

    cr.commit()


if __name__ == '__main__':
    init_logger()

    main(sys.argv[1:])
