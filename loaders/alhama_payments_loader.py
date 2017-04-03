# -*- coding: UTF-8 -*-
import datetime

from budget_app.loaders import PaymentsLoader
from budget_app.models import Budget

class AlhamaPaymentsLoader(PaymentsLoader):

    # Parse an input line into fields
    def parse_item(self, budget, line):

        policy_id = line[7].strip()[:2] # First two digits of the programme make the policy id
        # But what we want as area is the policy description
        policy = Budget.objects.get_all_descriptions(budget.entity)['functional'][policy_id]

        payee = self._titlecase(line[12].strip())
        payee = ("Otros" if payee == "" else payee)

        return {
            'area': policy,
            'programme': None,
            'fc_code': None,  # We don't try (yet) to have foreign keys to existing records
            'ec_code': None,
            'date': line[0].strip(),
            'contract_type': None,
            'payee': payee,
            'anonymized': False,
            'description': line[14].strip(),
            'amount': self._read_english_number(line[2])
        }
