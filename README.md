# moadian

```python
import json
from moadian import Moadian

with open("private.key", "r") as f:
    private_key = f.read()

moadian = Moadian("YourFiscalID", key)

```
```python
moadian.get_server_information()
...
#{'signature': None, 'signatureKeyId': None, 'timestamp': 1693947922222, 'result':{'uid': 'c4f374f6-2fe7-4df2-9b39-150310a5dec1', 'packetType': 'SERVER_INFORMATION', 'data': {'serverTime': 1693947922222, 'publicKeys': [{'key': 'MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAxdzREOEfk3vBQogDPGTMqdDQ7t0oDhuKMZkA+Wm1lhzjjhAGfSUOuDvOKRoUEQwP8oUcXRmYzcvCUgcfoRT5iz7HbovqH+bIeJwT4rmLmFcbfPke+E3DLUxOtIZifEXrKXWgSVPkRnhMgym6UiAtnzwA1rmKstJoWpk9Nv34CYgTk8DKQN5jQJqb9L/Ng0zOEEtI3zA424tsd9zv/kP4/SaSnbbnj0evqsZ29X6aBypvnTnwH9t3gbWM4I9eAVQhPYClawHTqvdaz/O/feqfm06QBFnCgL+CBdjLs30xQSLsPICjnlV1jMzoTZnAabWP6FRzzj6C2sxw9a/WwlXrKn3gldZ7Ctv6Jso72cEeCeUI1tzHMDJPU3Qy12RQzaXujpMhCz1DVa47RvqiumpTNyK9HfFIdhgoupFkxT14XLDl65S55MF6HuQvo/RHSbBJ93FQ+2/x/Q2MNGB3BXOjNwM2pj3ojbDv3pj9CHzvaYQUYM1yOcFmIJqJ72uvVf9Jx9iTObaNNF6pl52ADmh85GTAH1hz+4pR/E9IAXUIl/YiUneYu0G4tiDY4ZXykYNknNfhSgxmn/gPHT+7kL31nyxgjiEEhK0B0vagWvdRCNJSNGWpLtlq4FlCWTAnPI5ctiFgq925e+sySjNaORCoHraBXNEwyiHT2hu5ZipIW2cCAwEAAQ==', 'id': '6a2bcd88-a871-4245-a393-2843eafe6e02', 'algorithm': 'RSA', 'purpose': 1}]}, 'encryptionKeyId': None, 'symmetricKey': None, 'iv': None}}
```
```python
moadian.get_economic_code_information("14007650912")
...
#{'signature': None, 'signatureKeyId': None, 'timestamp': 1693948551814, 'result': {'uid': '2c176d39-f90d-4e34-8629-3812716a5803', 'packetType': 'ECONOMIC_CODE_INFORMATION', 'data': {'nameTrade': 'گروه تجارت الکترونیک دیجی کالا', 'taxpayerStatus': 'ENABLED', 'taxpayerType': 'LEGAL', 'postalcodeTaxpayer': '1917763913', 'addressTaxpayer': 'استان تهران - شهر تهران محله جردن بلوار نلسون ماندلا بلوار صبا غربی پلاک 38 طبقه دوم'}, 'encryptionKeyId': None, 'symmetricKey': None, 'iv': None}}
```

```python
# replace invoice with your invoice json and make sure you generate 'taxid' correctly.
invoice = '{"header": {}, "body": [{}], "payments": [{}]}'
invoice = json.loads(invoice)
moadian.send_invoice(invoice)

#{'signature': None, 'signatureKeyId': None, 'timestamp': 1693947237, 'result': [{'uid': '88a4e907-10f4-429f-ae89-3327579df***', 'referenceNumber': '395655e5-7830-4b68-bdf8-31ed1f098***', 'errorCode': None, 'errorDetail': None}]}
```

```python
moadian.inquiry_by_reference_number("395655e5-7830-4b68-bdf8-31ed1f098***")
# this is just an example of inquiry response, your errors will be different.
...
#'signature': None, 'signatureKeyId': None, 'timestamp': 1693947277561, 'result': {'uid': None, 'packetType': 'INQUIRY_RESULT', 'data': [{'referenceNumber': '395655e5-7830-4b68-bdf8-31ed1f098***', 'uid': '88a4e907-10f4-429f-ae89-3327579df***', 'status': 'FAILED', 'data': {'confirmationReferenceId': None, 'error': [{'code': '010504', 'message': 'در مقدار وارد شده در فیلد «سریال صورتحساب» الگو(^[a-fA-F0-9]{10}$) رعایت نشده است.', 'errorType': 'ERROR'}, {'code': '011204', 'message': 'در مقدار وارد شده در فیلد «شماره اقتصادی خریدار» الگو(^\\d{14}$) رعایت نشده است.', 'errorType': 'ERROR'}], 'warning': [], 'success': False}, 'packetType': 'receive_invoice_confirm', 'fiscalId': 'YourFiscalId'}], 'encryptionKeyId': None, 'symmetricKey': None, 'iv': None}}
```
