# -*- coding: UTF-8 -*-
from budget_app.models import *
from budget_app.loaders import SimpleBudgetLoader
from decimal import *

import re


class AlhamaBudgetLoader(SimpleBudgetLoader):
    def parse_item(self, filename, line):
        # Programme codes have changed in 2015, due to new laws. Since the application expects a code-programme
        # mapping to be constant over time, we are forced to amend budget data prior to 2015.
        # See https://github.com/dcabo/presupuestos-aragon/wiki/La-clasificaci%C3%B3n-funcional-en-las-Entidades-Locales
        programme_mapping = {
            # old programme: new programme
            '1340': '1350',  # Protección Civil
            '1350': '1600',  # Extinción de incendios
            '1550': '1532',  # Vías públicas
            '1690': '1621',  # Otros servicios de bienestar comunitario
            '2300': '2310',  # Admon. general servicios sociales
            '2310': '2311',  # Acción Social
            '2320': '2312',  # Promoción social
            '2330': '2313',  # Asistencia a personas dependientes
            '2340': '2412',  # Mujer
            '2410': '2411',  # Fomento del empleo
            '3130': '3110',  # Acciones públicas relativas a la salud
        }

        is_expense = filename.find('gastos.csv') != -1
        is_actual = filename.find('/ejecucion_') != -1

        if is_expense:
            # We got 3- or 4- digit functional codes as input, so add a trailing zero
            fc_code = line[4].ljust(4, '0')
            ec_code = line[5][:-2]  # First three digits (everything but last two)
            ic_code = '000'  # All expense goes to the root node
            item_number = line[5][-2:]  # Last two digits
            description = line[7]
            amount_budgeted = line[8]
            amount_actual = line[12]

            # For years before 2015 we check whether we need to amend the programme code
            year = re.search(r'municipio/(\d+)/', filename).group(1)
            if int(year) < 2015:
                fc_code = programme_mapping.get(fc_code, fc_code)

        else:
            fc_code = None
            ec_code = line[5][:-2]  # First three digits
            ic_code = '000'  # All income goes to the root node
            item_number = line[5][-2:]  # Fourth and fifth digit; careful, there's trailing dirt
            description = line[7]
            amount_budgeted = line[8]
            amount_actual = line[19]

        return {
            'is_expense': is_expense,
            'is_actual': is_actual,
            'fc_code': fc_code,
            'ec_code': ec_code,
            'ic_code': ic_code,
            'item_number': item_number,
            'description': description,
            'amount': self._parse_amount(amount_actual if is_actual else amount_budgeted),
        }
