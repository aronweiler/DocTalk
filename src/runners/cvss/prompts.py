OLD_CVSS_INSTRUCT_PROMPT = """
Instructions:
- Use the following information to provide a Base Metric Group CVSS 3.1 Vector String for the data I will provide you.    
    - Attack Vector (AV): N (Network), A (Adjacent Network), L (Local), or P (Physical). Default to N.
    - Attack Complexity (AC): L (Low) or H (High). Default to L.
    - Privileges Required (PR): N (None), L (Low), or H (High). Default to N.
    - User Interaction (UI): N (None) or R (Required). Default to N.
    - Scope (S): U (Unchanged) or C (Changed). Default to U.
    - Confidentiality (C): N (None), L (Low), or H (High). Default to H.
    - Integrity (I): N (None), L (Low), or H (High). Default to H.
    - Availability (A): N (None), L (Low), or H (High). Default to H.
    - Assign the corresponding option value to each metric.
    - Calculate the CVSS score based on the assigned values. 
- Include the reasoning as to why you selected each value, and make sure to provide explicit examples in your response.
- If the data does not include enough information for a metric, do the following:
    - Select the default value for that metric and,
    - Make sure to include an indication that you used a default value for that particular metric in your response
- Don't forget to prefix the CVSS vector with 'CVSS:3.1/'

DATA:
{data}
"""

CVSS_INSTRUCT_PROMPT = """
Instructions:
- Use the following information to evaluate the data I will provide you to arrive at a CVSS Evaluation, including Base Metric Group CVSS 3.1 Vector String and evaluation explanations (cite detailed source data in your explanation) for each metric.
    - Instructions for determining each metric:    
        Attack Vector (AV):
        AV represents how the vulnerability can be exploited.
        Determine the appropriate value based on the provided information:
        If the vulnerability can only be exploited locally (within the same machine or user context), assign the value 'L' (Local).
        If the vulnerability can be exploited adjacent to the target system (e.g., through the same local network), assign the value 'A' (Adjacent Network).
        If the vulnerability can be exploited remotely (across different networks or the Internet), assign the value 'N' (Network).
        If the vulnerability requires physical access or special conditions that limit its availability, assign the value 'P' (Physical).

        Attack Complexity (AC):
        AC represents the level of complexity required to exploit the vulnerability.
        Determine the appropriate value based on the provided information:
        If the vulnerability can be exploited with low complexity, assign the value 'L' (Low).
        If the vulnerability requires specialized conditions or high-level skills to exploit, assign the value 'H' (High).

        Privileges Required (PR):
        PR represents the level of privileges an attacker needs to exploit the vulnerability.
        Determine the appropriate value based on the provided information:
        If no privileges are required to exploit the vulnerability, assign the value 'N' (None).
        If limited privileges are required, assign the value 'L' (Low).
        If high privileges or administrative access are required, assign the value 'H' (High).

        User Interaction (UI):
        UI represents the level of user interaction required to exploit the vulnerability.
        Determine the appropriate value based on the provided information:
        If no user interaction is required to exploit the vulnerability, assign the value 'N' (None).
        If some form of user interaction is needed, assign the value 'R' (Required).

        Scope (S):
        S represents the impact of a successful exploit on the system's component or other components.
        Determine the appropriate value based on the provided information:
        If the vulnerability's impact is limited to the vulnerable component (e.g., an application), assign the value 'U' (Unchanged).
        If a successful exploit can impact components beyond the vulnerable component (e.g., other applications or the underlying operating system), assign the value 'C' (Changed).

        Confidentiality (C), Integrity (I), and Availability (A):
        C, I, and A represent the impact on each of these security aspects when the vulnerability is exploited.
        Determine the appropriate value for each based on the provided information:
        If there is no impact on the specific security aspect, assign the value 'N' (None).
        If there is partial impact, assign the value 'L' (Low).
        If there is complete impact or a total loss, assign the value 'H' (High).
    - Assume that all preconditions for the vulnerability to exist are met.
    - Assign the corresponding option value to each metric.
    - Calculate the CVSS score based on the assigned values. 
- If the data I provide does not include enough information to determine a metric's value, do the following:
    - Select the default value for that metric and,
    - Make sure to include an indication that you used a default value for that particular metric in your response
- Don't forget to prefix the CVSS vector with 'CVSS:3.1/'

DATA:
{data}

CVSS Evaluation, including Base Metric Group CVSS 3.1 Vector String and evaluation explanations (citing the source data in your explanation) for each metric:
"""

CRITIQUE_PROMPT = """
Use these instructions:
{instructions}

Look at the Original Data and the Proposed CVSS Evaluation. 
Critique the CVSS Evaluation using the instructions above, and the Original Data.
Evaluate reasoning behind the original decisions for each metric and improve the evaluation if possible, making sure to explain why you made changes.

Original Data:
{data}

Proposed CVSS Evaluation:
{evaluation}

Revised Evaluation (including updated 'CVSS:3.1/' Vector String):
"""

DETAILED_BASE_METRICS_INSTRUCTIONS = """
Detailed instructions for determining each metric:

Attack Vector (AV):
AV represents how the vulnerability can be exploited.
Determine the appropriate value based on the provided information:
If the vulnerability can only be exploited locally (within the same machine or user context), assign the value 'L' (Local).
If the vulnerability can be exploited adjacent to the target system (e.g., through the same local network), assign the value 'A' (Adjacent Network).
If the vulnerability can be exploited remotely (across different networks or the Internet), assign the value 'N' (Network).
If the vulnerability requires physical access or special conditions that limit its availability, assign the value 'P' (Physical).

Attack Complexity (AC):
AC represents the level of complexity required to exploit the vulnerability.
Determine the appropriate value based on the provided information:
If the vulnerability can be exploited with low complexity, assign the value 'L' (Low).
If the vulnerability requires specialized conditions or high-level skills to exploit, assign the value 'H' (High).

Privileges Required (PR):
PR represents the level of privileges an attacker needs to exploit the vulnerability.
Determine the appropriate value based on the provided information:
If no privileges are required to exploit the vulnerability, assign the value 'N' (None).
If limited privileges are required, assign the value 'L' (Low).
If high privileges or administrative access are required, assign the value 'H' (High).

User Interaction (UI):
UI represents the level of user interaction required to exploit the vulnerability.
Determine the appropriate value based on the provided information:
If no user interaction is required to exploit the vulnerability, assign the value 'N' (None).
If some form of user interaction is needed, assign the value 'R' (Required).

Scope (S):
S represents the impact of a successful exploit on the system's component or other components.
Determine the appropriate value based on the provided information:
If the vulnerability's impact is limited to the vulnerable component (e.g., an application), assign the value 'U' (Unchanged).
If a successful exploit can impact components beyond the vulnerable component (e.g., other applications or the underlying operating system), assign the value 'C' (Changed).

Confidentiality (C), Integrity (I), and Availability (A):
C, I, and A represent the impact on each of these security aspects when the vulnerability is exploited.
Determine the appropriate value for each based on the provided information:
If there is no impact on the specific security aspect, assign the value 'N' (None).
If there is partial impact, assign the value 'L' (Low).
If there is complete impact or a total loss, assign the value 'H' (High).
"""


BASE_METRIC_PROMPT = """
Generate a Base Metric Group CVSS 3.1 score and Vector String for the following data. Ensure that you include the reasoning as to why you selected that value, and quote the report in your response.  If it was not completely clear which option to use for a metric, make sure to let me know in the response.

{data}
"""


METRICS_TABLE = """
| Metric               | Description                                                                                                                  | Options and Explanation                                                                                      |
|----------------------|------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------|
| Attack Vector (AV)   | Describes how an attacker can exploit the vulnerability.                                                                     | Network (N): The vulnerability can be exploited remotely over a network connection.                           
                        |                                                                                                                              | Adjacent Network (A): The vulnerability can be exploited from a network adjacent to the target system.           
                        |                                                                                                                              | Local (L): The vulnerability requires local access to the target system.                                        
                        |                                                                                                                              | Physical (P): The vulnerability requires physical access to the target system.                                 |
| Attack Complexity (AC) | Represents the level of complexity required to exploit the vulnerability.                                                    | Low (L): The vulnerability is relatively easy to exploit.                                                        
                        |                                                                                                                              | High (H): The vulnerability is more complex and requires advanced techniques or conditions to exploit.         |
| Privileges Required (PR) | Indicates the level of privileges an attacker needs to exploit the vulnerability.                                           | None (N): The vulnerability can be exploited without any special privileges.                                     
                        |                                                                                                                              | Low (L): The vulnerability requires some privileges but not necessarily those of an administrator or root user.
                        |                                                                                                                              | High (H): The vulnerability requires elevated privileges, such as administrator or root access.                 |
| User Interaction (UI) | Considers whether user interaction is required for successful exploitation.                                                  | None (N): The vulnerability can be exploited without any user interaction.                                      
                        |                                                                                                                              | Required (R): Successful exploitation of the vulnerability depends on user interaction, such as opening a file or clicking a link.         |
| Scope (S)            | Defines the impact of a successful attack.                                                                                    | Unchanged (U): The vulnerability only affects the vulnerable component itself.                                 
                        |                                                                                                                              | Changed (C): The vulnerability has the potential to impact other components or resources in addition to the vulnerable component.                                          |
"""



