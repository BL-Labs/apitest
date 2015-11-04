import requests

from lxml import etree as ET

ONS = "http://www.openarchives.org/OAI/2.0/"
MARCXML = "http://www.loc.gov/MARC21/slim"

ns = {"o": ONS, "m": MARCXML}

def oai(text):
  return "{" + ONS + "}" + text

def mxl(text):
  return "{" + MARCXML + "}" + text

def get_marc_xml(identifier):
  try:
  if True:
    payload = {'verb': 'GetRecord', 'metadataPrefix': 'marcxml', 'identifier': '016959122 '}
    r = requests.get("http://v8b-bldgen01.ad.bl.uk/oaipmh/service", params=payload)
    if r.status_code == 200:
      return r.text
    else:
      print(r.status_code)
  except requests.exceptions.ConnectionError as e:
    print("Failed to connect to service."
    raise e

def parse_oaipmh(xml):
  try:
    doc = ET.fromstring(xml)
  except ET.XMLSyntaxError as e:
    print("Bad XML from OAIPMH server")
    raise e
  # root/GetRecord/record/metadata/record/datafield[@tag=876]
  # ARK is in subfield a
  return doc

def get_ark_from_doc(doc):
  arks = doc.xpath("//o:GetRecord/o:record/o:metadata/m:record/m:datafield[@tag=876]/m:subfield[@code='a']", namespaces = ns)

  if len(arks) != 1:
    raise Exception("Couldn't find an ARK")
  else:
    return arks[0].text

def getarkfor(identifier):
  try:
    xmltext = get_marc_xml(identifier)
  except Exception as e:
    print("Failed to get XML")
    raise e
  try:
    doc = parse_oaipmh(xmltext)
    ark = get_ark_from_doc(doc)
    return ark
  except Exception as e:
    print("Failed to parse the response")
    print(e)

