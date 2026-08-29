POS_PERMISSION_CHOICES = (
    ('', "--SELECT--"),
    ('pos_billing', 'POS (Billing)'),
    ('due_collection', 'Due Collection'),
    ('refund', 'Refund'),
    ('order_update', 'Order Update'),

    ('supplier', 'Supplier'),
    ('purchase_order', 'Purchase Order'),
    ('purchase_history', 'Purchase History'),
    ('grn', 'GRN (Goods Received Note)'),
    ('product_reconciliation', 'Product Reconciliation'),
    ('stock_transfer', 'Stock Transfer'),

    ('expense_head', 'Expense Head'),
    ('expense_entry', 'Expense Entry'),
    ('cash_bank_ledger', 'Cash / Bank Ledger'),
    ('supplier_due_payment', 'Supplier Due / Payment'),

    ('product_master', 'Product Master'),
    ('customer_master', 'Customer Master'),
    ('branch_counter_setup', 'Branch / Counter Setup'),

    ('report_profit_loss', 'Profit & Loss'),
    ('report_sale_summary', 'Sale Summary'),
    ('report_sale_details', 'Sale Details'),
    ('report_due_summary', 'Due Summary'),
    ('report_due_details', 'Due Details'),
    ('report_income_statement', 'Income Statement'),
    ('report_refund_collection', 'Refund & Collection'),
    ('report_expense', 'Expense Report'),
    ('report_stock_inventory', 'Stock / Inventory'),
)


PERMISSION_GROUPS = (
    ("Sales Operations", ["pos_billing", "due_collection", "refund", "order_update"]),
    ("Inventory & Procurement", ["supplier", "purchase_order", "purchase_history", "grn", "product_reconciliation", "stock_transfer"]),
    ("Finance", ["expense_head", "expense_entry", "cash_bank_ledger", "supplier_due_payment"]),
    ("Master / Setup Data", ["product_master", "customer_master", "branch_counter_setup"]),
    ("Reports", ["report_profit_loss", "report_sale_summary", "report_sale_details", "report_due_summary", "report_due_details", "report_income_statement", "report_refund_collection", "report_expense", "report_stock_inventory"]),
)

