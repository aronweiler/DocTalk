import logging
import time
from template_ingest import ingest_template
from template_completion import complete_template
from utilities.calculate_timing import convert_milliseconds_to_english

# Time it
start_time = time.time()

template_file_name = "C:\\Repos\\DocumentBuilder\\sample_templates\\device_description_template.md"

analyzed_template_file_path = ingest_template(template_file_name)

final_path = complete_template(analyzed_template_file_path)

end_time = time.time()
elapsed_time = end_time - start_time
logging.debug("Total Operation Time: ", convert_milliseconds_to_english(elapsed_time * 1000))

logging.debug("Template complete: ", final_path)