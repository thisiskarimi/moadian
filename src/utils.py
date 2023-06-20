from . import verhoeff
import datetime


def fiscal_id_to_number(fiscal_id):
    result = ''
    for char in fiscal_id:
        if str.isdigit(char):
            result += char
        else:
            result += str(ord(char))
    return result


def generate_tax_id(fiscal_id, date, internal_invoice_id):
    days_past_epoch = (date.date() - datetime.datetime(1970, 1, 1).date()).days
    days_past_epoch_padded = str(days_past_epoch).rjust(6, "0")
    hex_days_past_epoch_padded = str(f'{days_past_epoch:x}').rjust(5, "0")
    numeric_fiscal_id = fiscal_id_to_number(fiscal_id)
    internal_invoice_id_padded = internal_invoice_id.rjust(12, '0')
    hex_internal_invoice_id_padded = str(
        f'{int(internal_invoice_id):x}').rjust(10, '0')
    decimal_invoice_id = str(numeric_fiscal_id) + \
        str(days_past_epoch_padded) + str(internal_invoice_id_padded)
    checksum = verhoeff.checkSum(decimal_invoice_id)
    return (fiscal_id + str(hex_days_past_epoch_padded) + str(hex_internal_invoice_id_padded) + str(checksum)).upper()
