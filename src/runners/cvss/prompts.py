CHAIN_OF_THOUGHT_EXAMPLE_DATA_1 = """DATA:
Apache Tomcat 4.1.0 through 4.1.39, 5.5.0 through 5.5.27, and 6.0.0 through 6.0.18 permits web applications to replace an XML parser used for other web applications, which allows local users to read or modify the (1) web.xml, (2) context.xml, or (3) tld files of arbitrary web applications via a crafted application that is loaded earlier than the target application.
This Tomcat vulnerability allows a web-apps to reference an XML parser instead of using the default Apache XML parser. The attacker must remove all existing web-apps including those in server/webapps, then install a web-app with an XML parser is stored in WEB-INF/lib. This will cause Tomcat to use the new XML parser to process all web.xml, context.xml and tld files of other webapps. If that non-standard XML parser is replaced with a malicious one, the content of the victim web app XML can be disclosed, the resulting JSP could be corrupted (if it compiled at all) or possibly even weaponized for further attacks.
There are 2 different ways this attack may manifest. First a local privileged user could simply replace the non-Apache XML parser with a malicious variant. The second is that an attacker may use social engineering and user interaction to inject the malicious XML parser into the system. We will score for the former.
"""

CHAIN_OF_THOUGHT_EXAMPLE_EVALUATION_1 = """CVSS Evaluation:
Local user access is required to 'remove all existing web-apps including those in server/webapps, then install a web-app with an XML parser is stored in WEB-INF/lib', so the Attack Vector (AV) is L (Local)
The data provided does not contain any attack prerequisites, so Attack Complexity (AC) is L (Low)
The data mentions requiring a user to perform the attack, 'a local privileged user could simply replace the non-Apache XML parser with a malicious variant', so Privileges Required (PR) is H (High)
The vulnerability does not require any user interaction, so User Interaction (UI) is N (None)
The data provided does not include information about a scope change, so Scope (S) is U (Unchanged)
There is some loss of confidedntiallity (the content of the victim web app XML can be disclosed), so Confidentiality (C) is L (Low)
The integrity of the XML parser is lost (the resulting JSP could be corrupted), but not a total loss of integrity, so Integrity (I) is L (Low)
The reasonable outcome behind modifying the XML parser is to make certain web applications unavailable, but the attacker does not have the ability to completely deny service to legitimate users, so Availability (A) is L (Low)

The CVSS Vector String is: CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:U/C:L/I:L/A:L
"""

CHAIN_OF_THOUGHT_EXAMPLE_DATA_2 = """DATA:
Our medical device, which helps healthcare professionals manage patient medications, experienced a vulnerability that allowed unauthorized individuals to modify the drug library. 
The drug library contains vital information about medications, including dosages, interactions, and safety guidelines. 
The attacker can use the lowest-level user account on the device to exploit the vulnerability, administrative privliges are not required.
The attacker must be highly skilled, and have access to special packet-crafting equipment to exploit the vulnerability.
Due to the vulnerability, an attacker with access to the device over the Internet could make unauthorized changes to this essential database, such as changing doses, or completely mangling the data within it to make it unusable.
The drug library also contains proprietary information which an attacker can obtain using this vulnerability.
"""
CHAIN_OF_THOUGHT_EXAMPLE_EVALUATION_2 = """CVSS Evaluation:
The attacker can access the medical device over the Internet, so the Attack Vector (AV) is N (Network)
The data provided does not say the attacker needs any special knowledge to exploit the vulnerability, so Attack Complexity (AC) is L (Low)
The attacker 'can use the lowest-level user account on the device to exploit the vulnerability', so Privileges Required (PR) is L (Low)
The vulnerability does not require any user interaction, so User Interaction (UI) is N (None)
The attacker can only impact the drug library, so Scope (S) is U (Unchanged)
The proprietary information in the drug library can be obtained using this exploit, so Confidentiality (C) is L (Low)
The attacker can modify the drug library, so Integrity (I) is H (High)
The attacker can make the drug library unusable, so Availability (A) is H (High)

The CVSS Vector String is: CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:H
"""

CVSS_INSTRUCT_PROMPT = """
Instructions for determining each metric:
- Use the following information to evaluate the data to arrive at a CVSS Evaluation, including Base Metric Group CVSS 3.1 Vector String and evaluation explanations (cite detailed source data in your explanation) for each metric.
    - Instructions for determining each metric:    
        Attack Vector (AV) represents how the vulnerability can be exploited, the default value is 'N'.
        If the vulnerability does not require any special conditions to be exploited, assign the value 'N' (Network).
        If the vulnerable component is bound to the network stack and the set of possible attackers extends beyond the other options listed below, up to and including the entire Internet, or if an attack can be launched over a wide area network or from outside the logically adjacent administrative network domain, assign the value 'N' (Network).
        If the vulnerable component requires the attacker to be in close physical proximity, but not physically interact with the system, or is bound to the network stack, but the attack is limited at the protocol level to a logically adjacent topology (e.g., Bluetooth, IEEE 802.11, RF, Zigbee, NFC, etc.) or logical (e.g., local IP subnet) network, or from within a secure or otherwise limited administrative domain (e.g., MPLS, secure VPN to an administrative network zone), assign the value 'A' (Adjacent Network).
        If the vulnerable component is not bound to the network stack and the attacker's path is via read/write/execute capabilities, assign the value 'L' (Local).
        If the vulnerability requires requires the attacker to physically touch or manipulate the vulnerable component, assign the value 'P' (Physical).

        Attack Complexity (AC) represents the level of complexity required to exploit the vulnerability, the default value is 'L'.
        If the vulnerability does not contain specialized access conditions or extenuating circumstances, assign the value 'L' (Low).
        If the vulnerability depends on conditions beyond the attacker's control, i.e. a successful attack cannot be accomplished at will, but requires the attacker to invest in some measurable amount of effort in preparation or execution against the vulnerable component before a successful attack can be expected, assign the value 'H' (High).

        Privileges Required (PR) describes the privileges an attacker must possess, such as user account access, kernel access, access to a VM, PIN code, etc., before successfully exploiting the vulnerability, the default value is 'N'.
        If the attacker is anonymous, unauthorized, or does not require any legitimate access to the vulnerable system to carry out an attack, assign the value 'N' (None).
        If the attacker requires privileges that provide basic user capabilities (such as a user account), or an attack can be performed with low privileges (e.g. access to only non-sensitive resources), assign the value 'L' (Low).
        If the attacker requires privileges that provide significant control over the vulnerable component (such as an administrative account, or OS kernel access), assign the value 'H' (High).

        User Interaction (UI) represents the level of user (not attacker) interaction required to exploit the vulnerability, the default value is 'N'.
        If no user interaction is required to exploit the vulnerability, assign the value 'N' (None).
        If some form of user interaction is needed, to exploit the vulnerability, assign the value 'R' (Required).

        Scope (S) represents the impact of a successful exploit on the system's component or other components, the default value is 'U'.
        If the vulnerability's impact is limited to the vulnerable component (e.g., an application), or can only affect resources managed by the same security authority, assign the value 'U' (Unchanged).
        If a successful exploit can impact components beyond the vulnerable component (e.g., other applications or the underlying operating system), assign the value 'C' (Changed).

        Confidentiality (C), Integrity (I), and Availability (A):
        C, I, and A represent the impact on each of these security aspects when the vulnerability is exploited, the default value is 'H'.
        If the data does not mention, or does not include enough information to determine the impact to Confidentiality, Integrity, or Availability, assign the default value 'H' (High)
        If there is no impact on the specific security aspect, assign the value 'N' (None).
        If there is partial impact, for example:
            - There is some loss of confidentiality. Access to some restricted information is obtained, but the attacker does not have control over what information is obtained, or the amount or kind of loss is limited. The information disclosure does not cause a direct, serious loss to the impacted component.
            - Modification of data is possible, but the attacker does not have control over the consequence of a modification, or the amount of modification is limited. The data modification does not have a direct, serious impact on the impacted component.
            - Performance is reduced or there are interruptions in resource availability. Even if repeated exploitation of the vulnerability is possible, the attacker does not have the ability to completely deny service to legitimate users. The resources in the impacted component are either partially available all of the time, or fully available only some of the time, but overall there is no direct, serious consequence to the impacted component.
        assign the value 'L' (Low).
        If there is complete impact or a total loss, for example:
            - There is a total loss of confidentiality, resulting in all resources within the impacted component being divulged to the attacker. Alternatively, access to only some restricted information is obtained, but the disclosed information presents a direct, serious impact.
            - There is a total loss of integrity, resulting in the attacker being able to modify any/all files within the impacted component. Alternatively, only some files can be modified, but malicious modification would present a direct, serious consequence to the impacted component.
            - There is a total loss of availability, resulting in the attacker being able to fully deny access to resources in the impacted component, or the attacker has the ability to deny some availability, but the loss of availability presents a direct, serious consequence to the impacted component
        assign the value 'H' (High).
    - Assume that all preconditions for the vulnerability to exist are met, and that the attacker has all of the skills and equipment necessary to exploit the vulnerability.
    - DO NOT INCLUDE SPECIAL SKILLS OR EQUIPMENT REQUIRED TO EXPLOIT THE VULNERABILITY IN YOUR EVALUATION!
    - Assign the corresponding option value to each metric.
- IMPORTANT: If the data does not contain enough information to determine a metric's value, select the default value and explain why you selected it in your response.
- Don't forget to prefix the CVSS vector with 'CVSS:3.1/'
"""

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



