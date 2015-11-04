import requests

from lxml import etree as ET

ONS = "http://www.openarchives.org/OAI/2.0/"
MARCXML = "http://www.loc.gov/MARC21/slim"
RDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
BL = "http://www.bl.uk/schemas/digitalobject/entities#"
RTS = "http://cosimo.stanford.edu/sdr/metsrights/"
PREMIS = "info:lc/xmlns/premis-v2"

ns = {"o": ONS, "m": MARCXML, 'rdf': RDF,
      'bl': BL, 'rts': RTS, 'premis': PREMIS}

def oai(text):
  return "{" + ONS + "}" + text

def mxl(text):
  return "{" + MARCXML + "}" + text

def get_marc_xml(identifier):
  try:
    payload = {'verb': 'GetRecord', 'metadataPrefix': 'marcxml', 'identifier': identifier}
    r = requests.get("http://v8b-bldgen01.ad.bl.uk/oaipmh/service", params=payload)
    if r.status_code == 200:
      return r.content
    else:
      print(r.status_code)
  except requests.exceptions.ConnectionError as e:
    print("Failed to connect to service.")
    raise e

def get_mers_data(logicalark, dtype = "Structural"):
  try:
    payload = {'ark': logicalark, 'type': dtype}
    r = requests.get("http://mer.ad.bl.uk/mer_access/metadata", params=payload)
    if r.status_code == 200:
      return r.content
    else:
      print(r.status_code)
  except requests.exceptions.ConnectionError as e:
    print("Failed to connect to service.")
    raise e

def parse(xml):
  try:
    doc = ET.fromstring(xml)
  except ET.XMLSyntaxError as e:
    print("Bad XML")
    raise e
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

