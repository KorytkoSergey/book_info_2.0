from flask import Flask, request, Response
import xml.etree.ElementTree as ET
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route("/bank", methods=["POST"])
def bank_endpoint():
    xml_data = request.data.decode("utf-8")
    logging.info(f"Received XML:\n{xml_data}")

    try:
        root = ET.fromstring(xml_data)
        request_type = root.attrib.get("type")

        if request_type == "check":
            account = root.findtext("account")
            amount = root.findtext("amount")
            currency = root.findtext("currency")

            logging.info(f"Check payment: account={account}, amount={amount}, currency={currency}")

            response_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<response>
    <status>ok</status>
    <message>Account found. Ready to accept payment.</message>
</response>"""

        elif request_type == "confirm":
            transaction_id = root.findtext("transaction_id")
            amount = root.findtext("amount")

            logging.info(f"Confirm payment: transaction_id={transaction_id}, amount={amount}")

            response_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<response>
    <status>confirmed</status>
    <message>Payment confirmed</message>
</response>"""

        elif request_type == "notify":
            transaction_id = root.findtext("transaction_id")
            status = root.findtext("status")
            timestamp = root.findtext("timestamp")

            logging.info(f"Notify: transaction_id={transaction_id}, status={status}, timestamp={timestamp}")

            response_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<response>
    <status>received</status>
    <message>Notification accepted</message>
</response>"""

        else:
            response_xml = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <status>error</status>
    <message>Unknown request type</message>
</response>"""

    except ET.ParseError as e:
        logging.error(f"XML Parse Error: {e}")
        response_xml = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <status>error</status>
    <message>Invalid XML format</message>
</response>"""

    return Response(response_xml, content_type='application/xml')

if __name__ == "__main__":
    app.run(debug=True, port=5000)
