from cvss import CVSS3
import json

class CVSSTool:

    def __init__(self):
        print("CVSSTool initialized")
        pass

    def run(self, cvss_vector) -> str:
        c = CVSS3(vector=cvss_vector)

        return json.dumps({
            "original_vector": cvss_vector,
            "clean_vector": c.clean_vector(),
            "scores": c.scores(),
            "severities": c.severities()
        })