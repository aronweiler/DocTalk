CREATE_UNIT_TESTS_PROMPT = """Create unit tests for the following code.  The unit tests should be written in {language}.
Please make sure you comment the tests so that it is clear what each test is testing.

Your output should ONLY contain code in the language specified- do not include any other text.

Code:
{code}

Unit Tests written in {language}:
"""