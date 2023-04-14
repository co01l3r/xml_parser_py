FROM python:3.9-slim-buster

WORKDIR /app

COPY scripts/zip_xml_parser.py .

CMD [ "python3", "zip_xml_parser.py", "astra_export_xml.zip" ]

