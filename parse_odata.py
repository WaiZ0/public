import xml.dom.minidom as minidom
import json

class ODataServiceParser:
    def __init__(self, xml_file_path):
        self.xml_file_path = xml_file_path

    def read_metadata_from_file(self):
        with open(self.xml_file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def generate_requests(self, metadata_xml):
        """
        Parse the metadata XML and generate HTTP requests for OData services.
        """
        try:
            print("Parsing XML...")
            dom = minidom.parseString(metadata_xml)
        except Exception as e:
            raise Exception(f"Failed to parse XML: {str(e)}")

        namespaces = {
            "edmx": "http://docs.oasis-open.org/odata/ns/edmx",
            "edm": "http://docs.oasis-open.org/odata/ns/edm",
        }

        try:
            # Finding the base service URL (from edmx:DataServices element if available)
            print("Looking for base service URL...")
            service_url = "http://example.com/odata"  # Default URL as there's no base URL attribute in this XML
            print(f"Base URL: {service_url}")
        except Exception as e:
            raise Exception(f"Error finding base URL: {str(e)}")

        # Finding entity sets, actions, and functions in the metadata
        entity_sets = dom.getElementsByTagNameNS(namespaces['edm'], 'EntitySet')
        actions = dom.getElementsByTagNameNS(namespaces['edm'], 'Action')
        functions = dom.getElementsByTagNameNS(namespaces['edm'], 'Function')

        # Generate the HTTP requests
        http_requests = []

        # Add requests for entity sets (GET method)
        for entity_set in entity_sets:
            name = entity_set.getAttribute("Name")
            entity_type_name = entity_set.getAttribute("EntityType")
            print(f"Processing entity set: {name}, entity type: {entity_type_name}")

            url = f"{service_url}/{name}"
            http_requests.append({"method": "GET", "url": url, "parameters": {}})

        # Add requests for actions (POST method)
        for action in actions:
            name = action.getAttribute("Name")
            print(f"Processing action: {name}")
            url = f"{service_url}/{name}"
            parameters = {}
            for param in action.getElementsByTagNameNS(namespaces['edm'], 'Parameter'):
                param_name = param.getAttribute("Name")
                param_type = param.getAttribute("Type")
                parameters[param_name] = {"type": param_type, "value": None}  
            http_requests.append({"method": "POST", "url": url, "parameters": parameters})

        # Add requests for functions (GET method)
        for function in functions:
            name = function.getAttribute("Name")
            print(f"Processing function: {name}")
            url = f"{service_url}/{name}"
            parameters = {}
            for param in function.getElementsByTagNameNS(namespaces['edm'], 'Parameter'):
                param_name = param.getAttribute("Name")
                param_type = param.getAttribute("Type")
                parameters[param_name] = {"type": param_type, "value": None}
            http_requests.append({"method": "GET", "url": url, "parameters": parameters})

        return http_requests

    def format_data(self, data):
        """
        Format the generated HTTP requests for display in the result area.
        """
        requests = []
        for row in data:
            method = row["method"]
            url = row["url"]
            parameters = row["parameters"]

            if method == 'GET':
                request = f"{method} {url} HTTP/1.1\r\nHost: your-odata-service-url\r\n\r\n"
            elif method == 'POST':
                payload = {}
                for key, value in parameters.items():
                    if value["value"] is None:
                        payload[key] = ''
                    else:
                        payload[key] = value["value"]
                payload_json = json.dumps(payload)
                headers = f"Content-Type: application/json\r\nContent-Length: {len(payload_json)}\r\n"
                request = f"{method} {url} HTTP/1.1\r\nHost: your-odata-service-url\r\n{headers}\r\n{payload_json}\r\n"
            else:
                raise NotImplementedError(f"Unsupported method: {method}")

            requests.append(request)

        return requests

    def run(self):
        metadata_xml = self.read_metadata_from_file()
        try:
            requests = self.generate_requests(metadata_xml)
            formatted_requests = self.format_data(requests)
            print("Formatted requests:")
            for req in formatted_requests:
                print(req)
        except Exception as e:
            print(f"Error: {str(e)}")


# Example usage
if __name__ == "__main__":
    parser = ODataServiceParser("/home/waiz/Downloads/test.xml")
    parser.run()
