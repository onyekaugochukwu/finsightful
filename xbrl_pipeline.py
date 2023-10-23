import xml.etree.ElementTree as ET
from haystack.nodes import BaseConverter
from haystack.schema import Document
from typing import List, Optional, Dict, Any
from pathlib import Path

class XMLToTextConverter(BaseConverter):
    def convert(self,
                file_path: Path,
                meta: Optional[Dict[str, str]] = None,
                remove_numeric_tables: Optional[bool] = None,
                valid_languages: Optional[List[str]] = None) -> List[Document]:
        
        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Define the namespace
        ns = {'iascf-pfs': 'http://www.xbrl.org/taxonomy/int/fr/ias/ci/pfs/2002-11-15'}

        # Extract text from specific XML elements
        text = '\n'.join([elem.text for elem in root.iterfind('.//iascf-pfs:PropertyPlantEquipment', ns) if elem.text])

        # Create a Document object
        doc = Document(
            content=text,
            content_type="text",
            meta=meta if meta else {}
        )

        return [doc]



converter = XMLToTextConverter()
docs = converter.convert(file_path=Path("SampleCompany-2002-11-15.xml"), meta=None)

print(docs)