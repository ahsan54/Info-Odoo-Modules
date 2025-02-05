# Payment Voucher Module for Odoo

This module extends the accounting functionality of Odoo to incorporate a Payment Voucher feature. Designed an Odoo module to streamline payment processing with automated journal entries, featuring dynamically generated debit/credit lines linked to relevant journals. Integrated ir.sequence for different voucher and  cheque numbers.
The module provides a seamless way to manage payment vouchers and their associated journal entries, including handling cheque numbers and linking them with accounting journals.

Here's an overview of the module's features:

## Features

####     Payment Voucher Management:
        Creation of payment vouchers with auto-generated sequence numbers.
        Support for bank and cash journals with customizable prefixes (BPV for bank and CPV for cash).
        Automatic generation of cheque numbers for bank payment vouchers.

####    Journal Entry Integration:
        Automatic creation of journal entries upon voucher confirmation.
        Linkage between payment vouchers and their corresponding journal entries.

 ####   State Management:
        Payment vouchers have states (Draft, Posted) for better tracking and control.
        Restrict editing once a voucher is posted.

####    Dynamic Views and Fields:
        Dynamic visibility of fields like cheque numbers based on journal type.
        Tree and form views for efficient voucher management.
        Notebook-style layout for organizing lines and details.

####    Voucher Lines:
        Detailed line items for each voucher, including accounts, narrations, and amounts.

####    User Interface Enhancements:
        Buttons for quick actions like viewing linked journal entries.
        Statusbar to indicate the state of the voucher.

####    Menu and Action Integration:
        A dedicated menu item for Payment Voucher under the "Accounting > Miscellaneous" menu.
        Predefined action for accessing payment vouchers in tree and form views.

### Usage

    Go to Accounting > Miscellaneous > Payment Voucher.
    Create a new payment voucher by selecting a journal, partner, and adding line items.
    Confirm the voucher to automatically generate a journal entry.
    View the linked journal entry directly from the voucher form.



# Employee-Loan-Management
This Odoo module streamlines the management of employee loans, from application and approval to installment tracking and accounting integration. It automates the creation and updating of journal entries, including profit journal entries (JV) linked to loan installments. The module ensures that when subsequent installments are paid, the related profit JV is updated rather than creating new ones. It provides features for configuring loan types, reflecting these configurations in the loan application form, and preventing employees from applying for a new loan if they already have an active loan. Additionally, it integrates loan information into the employee form, with smart buttons for accessing the related journal entries and profit JVs. The loan details, including applied amount, interest rate, and outstanding balance, are displayed on the employee’s profile, providing full visibility and control for HR and Finance teams.


## Features
### Loan Application & Approval: 
                          Streamlines loan application and approval workflows for HR and Finance.

### Loan Types Configuration: 
                          Allows configuration of loan types, including interest rates and installment policies.

### Automated Installment Calculations: 
                          Automatically computes loan installments based on defined loan type settings.

### Accounting Integration: 
                          Creates and updates related journal entries and profit journal entries (JV) based on loan installment payments.

### Loan Visibility on Employee Form: 
                          Displays loan details, including principal amount, interest rate, and remaining balance on the employee’s profile.

### Smart Button Navigation: 
                          Smart buttons on employee forms for quick access to related journal entries and profit JVs.

### Loan Application Restrictions: 
                          Prevents employees from applying for new loans if they have an active loan.

### Profit JV Management: 
                          Updates existing profit JVs for subsequent installments, instead of creating new ones, ensuring accurate financial tracking.




![validation_error_on_applying_loan_when_one_loan_is_active](https://github.com/user-attachments/assets/c496ff7e-d709-48dd-9c96-a3c46eb16893)
![Screenshot from 2025-01-08 10-50-53](https://github.com/user-attachments/assets/dd4d8e08-d527-43d6-b0d4-60dc87655598)
![Screenshot from 2025-01-08 10-50-31](https://github.com/user-attachments/assets/a91e545d-a3c5-4e2d-afb9-2f96516c4ba9)
![proper_link_btw_loan_jv](https://github.com/user-attachments/assets/c40695aa-b9f9-4ffe-854e-5b87afe4a558)
![profit_jv_update_on_clicking_paid_plus_or_minus](https://github.com/user-attachments/assets/aafbc440-15e8-49d8-b6c2-bc8480acdaa4)
![profit_jv_auto_created_on_clicking_paid](https://github.com/user-attachments/assets/7c420627-565d-4ecc-8b70-e7541bd51fc0)
![Loan_Front_Empty](https://github.com/user-attachments/assets/8061df21-ff8a-4500-a0c8-8280cf5d4db5)
![jv_auto_created](https://github.com/user-attachments/assets/59ea4510-bd1a-410c-a9ca-2bca616da687)
![employee_form_loan_page_and_smart_button](https://github.com/user-attachments/assets/f1dffe6d-6ab0-48f9-8116-b149829ea2f7)





# Fleet-Fuel-Tank

This module implements a Fuel Tank Management System in Odoo. It is designed to provide a complete solution for managing fuel tanks, tracking fuel consumption, recording fuel filling operations, and maintaining tank-related details. By integrating advanced validation logic, computed fields, and a user-friendly wizard, this module ensures robust and efficient fuel management while maintaining data integrity.

## Features:

 Track fuel tank details like the tank's name, location, last cleaning date, capacity, and current fuel levels.
 
 Manage fuel entries to record each fuel addition, including the amount of fuel added and its price.
 
 Monitor fuel consumption by calculating how much of the tank's capacity is filled and tracking the cost of the last fuel addition.
 
 Enable easy fuel additions through a wizard, allowing users to add fuel while ensuring that the tank is not overfilled.
 
 This system ensures efficient management and tracking of fuel tanks, helping to maintain accurate records of fuel usage, cost, and filling operations.





# Hospital-Management-Odoo

This module implements a Hospital Management System in Odoo, designed to manage patients, doctors, and appointments efficiently. It provides features to track patient details, their medical history, and appointment schedules while maintaining a seamless workflow.

## Key Features:
### Patient Management:

### Patient Details: 
                    Capture essential patient information, including name, gender, date of birth, and medical condition.
### Disease Tracking: 
                      Link patients to doctors and their areas of expertise to identify and manage diseases.
### Age Calculation: 
                    Automatically compute the patient's age based on their date of birth.
#### Visit Records: 
                  Maintain details about the patient's last visit and associated medical notes.

### Validation Logic: 
                      Prevent errors by ensuring the date of birth is not set in the future.

### Automated Reference Numbering:
                                  Each patient is assigned a unique, auto-generated reference number for identification and record-keeping.

### Doctor Management:
                      Maintain a database of doctors, including their names and areas of expertise, ensuring the right doctor is assigned to the right patient.
Appointment Scheduling:

### Appointment Records: 
                        Create and manage patient appointments with details like date and patient age.







                          
    
