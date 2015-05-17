#!/usr/bin/python

from oe_argparser import oe_parse_args

import xmlrpclib


def migrate_attachment(sock, att_id):
    att = sock.execute(args.database, uid, args.password, 'ir.attachment',
                       'read', att_id, ['db_datas'])

    sock.execute(args.database, uid, args.password, 'ir.attachment',
                 'write', [att_id], {'db_datas': att['db_datas']})


def main(argv):
    args = oe_parse_args(argv)

    sock_common = xmlrpclib.ServerProxy(
        'http://%s:%s%s' % (args.host, args.port, '/xmlrpc/common'))

    uid = sock_common.login(args.database, args.username, args.password)

    sock = xmlrpclib.ServerProxy(
        'http://%s:%s%s' % (args.host, args.port, '/xmlrpc/object'))

    att_ids = sock.execute(args.database, uid, args.password, 'ir.attachment',
                           'search', [('store_fname', '=', False)])

    for i, id in enumerate(att_ids):
        sock.execute(args.database, uid, args.password, 'ir.attachment',
                     'read', id, ['db_datas', 'parent_id'])

        migrate_attachment(sock, id)

        print 'Migrated ID %d (attachment %d of %d)' % (id, i, len(att_ids))


if __name__ == '__main__':
    main(sys.argv[1:])
