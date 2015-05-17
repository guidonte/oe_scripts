#! /usr/bin/python

from oe_argparser import oe_args_parser

from openerp.netsvc import init_logger
from openerp.modules.registry import RegistryManager

import sys


def extend_args_parser(parser):
    parser.add_argument('-f', '--from-account', dest='from_account',
                        required=True)
    parser.add_argument('-t', '--to-account', dest='to_account',
                        required=True)
    parser.add_argument('-s', '--suffix', dest='suffix',
                        required=True)

    return parser


def main(argv):
    '''Duplicate accounts under specified account view.'''
    parser = extend_args_parser(oe_args_parser())

    args = parser.parse_args(argv)

    pool = registry = RegistryManager.get(args.database, update_module=False)
    cr = registry.db.cursor()
    uid = 1

    account_obj = pool.get('account.account')

    account_id = account_obj.search(
        cr, uid, [('code', '=', args.from_account)])[0]
    account = account_obj.browse(cr, uid, account_id)

    new_base_id = account_obj.create (cr, uid, {
        'code': args.to_account,
        'name': '%s %s' % (account.name, args.suffix),
        'reconcile': account.reconcile,
        'user_type': account.user_type.id,
        'active': True,
        'level': account.level,
        'company_id': account.company_id.id,
        'parent_id': account.parent_id.id,
        'type': account.type,
    })

    for i, child in enumerate(account.child_id):
        new_child_id = account_obj.create (cr, uid, {
            'code': child.code.replace(args.from_account, args.to_account, 1),
            'name': '%s %s' % (child.name, args.suffix),
            'reconcile': child.reconcile,
            'user_type': child.user_type.id,
            'active': True,
            'level': child.level,
            'company_id': child.company_id.id,
            'parent_id': new_base_id,
            'type': child.type,
        })

    account_obj._parent_store_compute (cr)

    cr.commit()


if __name__ == '__main__':
    init_logger()

    main(sys.argv[1:])
