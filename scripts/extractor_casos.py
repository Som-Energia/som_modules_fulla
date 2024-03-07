#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from erppeek import Client
import argparse
import configdb
from datetime import datetime, timedelta
from yamlns import namespace as ns


def parse_arguments():
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        '--desti',
        dest='erp_desti',
        help="URL del servidor ERP de destí"
    )

    parser.add_argument(
        '--polissa',
        dest='polissa_id',
        help="Id de la pòlissa"
    )

    args = parser.parse_args(namespace=ns())

    return args


def ssl_unverified_context():
    import ssl

    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context


def search_tariff_id(c, name):
    tarifa_o = c.model('product.pricelist')
    tarifa_id = tarifa_o.search([('name', '=', name)])[0]
    return tarifa_id


def serialitzar_item(cpre, cprod, item_id):
    data = {}

    item_o = cprod.model('product.pricelist.item')
    tarifa_pre_o = cpre.model('product.pricelist')
    tarifa_prod_o = cprod.model('product.pricelist')

    item_bw = item_o.browse(item_id)

    params = [
        'base', 'base_price', 'base_pricelist_id', 'categ_id',
        'min_quantity', 'name', 'price_discount', 'price_max_margin',
        'price_min_margin', 'price_round', 'price_subcharge',
        'price_version_id', 'product_category_id', 'product_id',
        'product_tmpl_id', 'sequence', 'tram', 'tram_quantity'
    ]

    data = item_o.read(item_id, params)

    data['product_tmpl_id'] = data['product_tmpl_id'][0] if data['product_tmpl_id'] else False
    data['categ_id'] = data['categ_id'][0] if data['categ_id'] else False
    data['base_pricelist_id'] = data['base_pricelist_id'][0] if data['base_pricelist_id'] else False

    if data.get('base_pricelist_id'):
        name_tarifa_prod = tarifa_prod_o.read(
            data['base_pricelist_id'], ['name'])['name']
        data['base_pricelist_id'] = tarifa_pre_o.search(
            [('name', '=', name_tarifa_prod)])[0]

    data['price_version_id'] = data['price_version_id'][0] if data['price_version_id'] else False
    data['product_category_id'] = data['product_category_id'][0] if data['product_category_id'] else False
    data['product_id'] = data['product_id'][0] if data['product_id'] else False
    data.pop('id')

    return [0, 0, data]


def serialitzar_dades_polissa(cpre, cprod, polissa_id):
    data = {}

    pol_o = cprod.model('giscedata.polissa')

    pol_bw = pol_o.browse(int(polissa_id))

    data['name'] = pol_bw.name + '_bis'
    data['active'] = pol_bw.active
    data['state'] = pol_bw.state
    # data['process_id'] = pol_bw.date_end
    # data['comercialitzadora'] = pol_bw.date_start

    return data


def create_polissa(c, data):
    version_o = c.model('giscedata.polissa')
    version_o.create(data)


def migracio(args):
    ssl_unverified_context()
    import pudb
    pu.db

    if args.erp_desti == 'testing':
        erppeek_desti = configdb.erppeek_test
    elif args.erp_desti == 'staging':
        erppeek_desti = configdb.erppeek_stage
    elif args.erp_desti == 'pre':
        erppeek_desti = configdb.erppeek_pre
    else:
        print "No s'ha trobat servidor de destí"
        return

    cpre = Client(**erppeek_desti)
    cprod = Client(**configdb.erppeek_prod)

    polissa_id = args.polissa_id

    data = serialitzar_dades_polissa(
        cpre, cprod, polissa_id)

    if data:
        create_polissa(cpre, data)
        print "Polissa creada correctament"


if __name__ == "__main__":
    args = parse_arguments()
    migracio(args)
