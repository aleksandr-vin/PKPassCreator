pass_dict = {
    "formatVersion": 1,
    "serialNumber": "0002",
    "webServiceURL": "https://aleksandr.vin/passes/",
    "authenticationToken": "vxwxd7J8AlNNFPS8k0a0FfUFtq0ewzFdx",
    "barcode": {
        # The barcode format PKBarcodeFormatCode128 isn’t supported for watchOS.
        # https://developer.apple.com/documentation/walletpasses/pass/barcodes
        "format": "PKBarcodeFormatQR", # Possible Values: PKBarcodeFormatQR, PKBarcodeFormatPDF417, PKBarcodeFormatAztec, PKBarcodeFormatCode128
        "message": "12010956",
        "messageEncoding": "UTF-8",
        "altText":"12010956"
    },
    "organizationName": "De Klimmuur",
    "description": "Membership for Aleksandr Vinokurov",
    "labelColor": "rgb(0, 0, 0)",
    "foregroundColor": "rgb(255, 255, 255)",
    "backgroundColor": "rgb(245, 100, 30)",
    "generic": {
        "headerFields": [
            {
                "key": "header",
                "label": "Aleksandr Vinokurov",
                "value": "12010956"
            }
        ],
        "primaryFields": [
            {
                "key": "full-name",
                "label": "Name",
                "value": "Aleksandr Vinokurov"
            },
        ],
        "secondaryFields": [
            {
                "key": "number",
                "label": "Number",
                "value": "12010956"
            },
            {
                "key": "valid-from",
                "label": "Valid from",
                "value": "2019-04-01T18:20+02:00",
                "dateStyle" : "PKDateStyleMedium",
                # "timeStyle" : "PKDateStyleShort",
                "textAlignment": "PKTextAlignmentRight",
            },
        ],
        "auxiliaryFields": [
            {
                "key": "authority",
                "label": "Authority",
                "value": "De Klimmuur"
            },
            {
                "key": "country",
                "label": "Country",
                "value": "Netherlands"
            },
        ],
        "backFields": [
            {
                "key": "title",
                "label": "Membership for Aleksandr Vinokurov",
                "value": "12010956"
            },
            {
                "key": "authority",
                "label": "Authority",
                "value": "De Klimmuur"
            },
            {
                "key": "country",
                "label": "Country",
                "value": "Netherlands"
            },
            {
                "key" : "rules",
                "label" : "Rules URL",
                "value" : "https://www.deklimmuur.nl/voorwaarden-en-regels/#klimregels"
            },
            {
                "key" : "contact",
                "label" : "De Klimmuur Contact",
                "value" : "https://www.deklimmuur.nl/over-ons/contact/"
            },
            {
                "key" : "website",
                "label" : "Designed by",
                "value" : "https://aleksandr.vin"
            },
            {
                "key" : "phone",
                "label" : "Phone",
                "value" : "+31(6)13018394"
            },
        ],
    },
}
