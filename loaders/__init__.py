import six

if six.PY2:
    from alhama_budget_loader import AlhamaBudgetLoader
    from alhama_payments_loader import AlhamaPaymentsLoader
else:
    from .alhama_budget_loader import AlhamaBudgetLoader
    from .alhama_payments_loader import AlhamaPaymentsLoader
