### Payment Voucher Module for Odoo

This module extends the accounting functionality of Odoo to incorporate a Payment Voucher feature. Designed an Odoo module to streamline payment processing with automated journal entries, featuring dynamically generated debit/credit lines linked to relevant journals. Integrated ir.sequence for different voucher and  cheque numbers.
The module provides a seamless way to manage payment vouchers and their associated journal entries, including handling cheque numbers and linking them with accounting journals.

Here's an overview of the module's features:

## Features

#     Payment Voucher Management:
        Creation of payment vouchers with auto-generated sequence numbers.
        Support for bank and cash journals with customizable prefixes (BPV for bank and CPV for cash).
        Automatic generation of cheque numbers for bank payment vouchers.

#    Journal Entry Integration:
        Automatic creation of journal entries upon voucher confirmation.
        Linkage between payment vouchers and their corresponding journal entries.

 #   State Management:
        Payment vouchers have states (Draft, Posted) for better tracking and control.
        Restrict editing once a voucher is posted.

#    Dynamic Views and Fields:
        Dynamic visibility of fields like cheque numbers based on journal type.
        Tree and form views for efficient voucher management.
        Notebook-style layout for organizing lines and details.

#    Voucher Lines:
        Detailed line items for each voucher, including accounts, narrations, and amounts.

#    User Interface Enhancements:
        Buttons for quick actions like viewing linked journal entries.
        Statusbar to indicate the state of the voucher.

#    Menu and Action Integration:
        A dedicated menu item for Payment Voucher under the "Accounting > Miscellaneous" menu.
        Predefined action for accessing payment vouchers in tree and form views.


## Installation

    git clone <repository_url> /path/to/odoo/addons/payment_voucher
    
Navigate to Apps in your Odoo instance, search for "Payment Voucher," and install the module.


# Usage

    Go to Accounting > Miscellaneous > Payment Voucher.
    Create a new payment voucher by selecting a journal, partner, and adding line items.
    Confirm the voucher to automatically generate a journal entry.
    View the linked journal entry directly from the voucher form.
