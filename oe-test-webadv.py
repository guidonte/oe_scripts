#!/usr/bin/python

from oe_argparser import oe_parse_args

from openerp.modules.registry import RegistryManager
from openerp.netsvc import init_logger

from document_webdav import test_davclient

import sys
import logging

_logger = logging.getLogger(__name__)


def main(argv):
    args = oe_parse_args(argv)

    dc = test_davclient.DAVClient()

    registry = RegistryManager.get(args.database, update_module=False)
    cr = registry.db.cursor()

    Attachment = registry.get('ir.attachment')
    dc.get_creds(Attachment, cr, 1)

    dc.gd_options(path='/' + cr.dbname, expect={'DAV': ['1',]})
    print dc.gd_propname(path='/' + cr.dbname+'/Documents/')

    cr.close()


if __name__ == '__main__':
    init_logger()

    main(sys.argv[1:])
