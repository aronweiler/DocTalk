CHAIN_OF_THOUGHT_EXAMPLE_DATA_1 = """
Data: 
Apache Tomcat 4.1.0 through 4.1.39, 5.5.0 through 5.5.27, and 6.0.0 through 6.0.18 permits web applications to replace an XML parser used for other web applications, which allows local users to read or modify the (1) web.xml, (2) context.xml, or (3) tld files of arbitrary web applications via a crafted application that is loaded earlier than the target application.
This Tomcat vulnerability allows a web-apps to reference an XML parser instead of using the default Apache XML parser. The attacker must remove all existing web-apps including those in server/webapps, then install a web-app with an XML parser is stored in WEB-INF/lib. This will cause Tomcat to use the new XML parser to process all web.xml, context.xml and tld files of other webapps. If that non-standard XML parser is replaced with a malicious one, the content of the victim web app XML can be disclosed, the resulting JSP could be corrupted (if it compiled at all) or possibly even weaponized for further attacks.
There are 2 different ways this attack may manifest. First a local privileged user could simply replace the non-Apache XML parser with a malicious variant. The second is that an attacker may use social engineering and user interaction to inject the malicious XML parser into the system. We will score for the former.
"""

CHAIN_OF_THOUGHT_EXAMPLE_EVALUATION_1 = """
Evaluation:
- Local user access is required to 'remove all existing web-apps including those in server/webapps, then install a web-app with an XML parser is stored in WEB-INF/lib', so the Attack Vector (AV) is L (Local)
- The data provided does not contain any attack prerequisites, so Attack Complexity (AC) is L (Low)
- The data mentions requiring a user to perform the attack, 'a local privileged user could simply replace the non-Apache XML parser with a malicious variant', so Privileges Required (PR) is H (High)
- The vulnerability does not require any user interaction, so User Interaction (UI) is N (None)
- The data provided does not include information about a scope change, so Scope (S) is U (Unchanged)
- There is some loss of confidentiality (the content of the victim web app XML can be disclosed), so Confidentiality (C) is L (Low)
- The integrity of the XML parser is lost (the resulting JSP could be corrupted), but not a total loss of integrity, so Integrity (I) is L (Low)
- The reasonable outcome behind modifying the XML parser is to make certain web applications unavailable, but the attacker does not have the ability to completely deny service to legitimate users, so Availability (A) is L (Low)

Therefor, the CVSS Vector String is: CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:U/C:L/I:L/A:L
"""

CHAIN_OF_THOUGHT_EXAMPLE_DATA_2 = """
Data:
Our medical device, which helps healthcare professionals manage patient medications, experienced a vulnerability that allowed unauthorized individuals to modify the drug library. 
The drug library contains vital information about medications, including dosages, interactions, and safety guidelines. 
The attacker can use the lowest-level user account on the device to exploit the vulnerability, administrative privileges are not required.
The attacker must be highly skilled, and have access to special packet-crafting equipment to exploit the vulnerability.
Due to the vulnerability, an attacker with access to the device over the Internet could make unauthorized changes to this essential database, such as changing doses, or completely mangling the data within it to make it unusable.
The drug library also contains proprietary information which an attacker can obtain using this vulnerability.
"""

CHAIN_OF_THOUGHT_EXAMPLE_EVALUATION_2 = """
Evaluation:
- The attacker can access the medical device over the Internet, so the Attack Vector (AV) is N (Network)
- The data provided does not say the attacker needs any special knowledge to exploit the vulnerability, so Attack Complexity (AC) is L (Low)
- The attacker 'can use the lowest-level user account on the device to exploit the vulnerability', so Privileges Required (PR) is L (Low)
- The vulnerability does not require any user interaction, so User Interaction (UI) is N (None)
- The attacker can only impact the drug library, so Scope (S) is U (Unchanged)
- The proprietary information in the drug library can be obtained using this exploit, so Confidentiality (C) is L (Low)
- The attacker can modify the drug library, so Integrity (I) is H (High)
- The attacker can make the drug library unusable, so Availability (A) is H (High)

Therefor, the CVSS Vector String is: CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:H

"""

CVSS_INSTRUCT_PROMPT = """You are a security AI tasked with evaluating the CVSS score of a vulnerability.
Instructions for determining each metric:
- Use the following information to evaluate the data to arrive at a CVSS Evaluation, including Base Metric Group CVSS 3.1 Vector String and evaluation explanations (cite detailed source data in your explanation) for each metric.
    - When scoring Base metrics, it should be assumed that the attacker has advanced knowledge of the weaknesses of the target system, including general configuration and default defense mechanisms (e.g., built-in firewalls, rate limits, traffic policing). For example, exploiting a vulnerability that results in repeatable, deterministic success should still be considered a Low value for Attack Complexity, independent of the attacker's knowledge or capabilities.
        Attack Vector (AV) represents how the vulnerability can be exploited, the default value is 'N'.
        If the vulnerability does not require any special conditions to be exploited, assign the value 'N' (Network).
        If the vulnerable component is bound to the network stack and the set of possible attackers extends beyond the other options listed below, up to and including the entire Internet, or if an attack can be launched over a wide area network or from outside the logically adjacent administrative network domain, assign the value 'N' (Network).
        If the vulnerable component requires the attacker to be in close physical proximity, but not physically interact with the system, or is bound to the network stack, but the attack is limited at the protocol level to a logically adjacent topology (e.g., Bluetooth, IEEE 802.11, RF, Zigbee, NFC, etc.) or logical (e.g., local IP subnet) network, or from within a secure or otherwise limited administrative domain (e.g., MPLS, secure VPN to an administrative network zone), assign the value 'A' (Adjacent Network).
        If the vulnerable component is not bound to the network stack and the attacker's path is via read/write/execute capabilities, assign the value 'L' (Local).
        If the vulnerability requires requires the attacker to physically touch or manipulate the vulnerable component, assign the value 'P' (Physical).

        Attack Complexity (AC) describes the conditions outside of the attacker's control that must exist in order to exploit the vulnerability, the default value is 'L'.        
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
        If the data does not mention, or does not include enough information to determine the scope, assign the default value 'U' (Unchanged).
        If the vulnerability's impact is limited to the vulnerable component (e.g., the target application or device), assign the value 'U' (Unchanged).
        If a successful exploit can impact components beyond the vulnerable component (e.g., other software applications or the underlying operating system), assign the value 'C' (Changed).

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

CRITIQUE_PROMPT = """
{instructions}

Use the instructions above to critique the CVSS Evaluation below.
Critique the reasoning behind the original decisions for each metric and improve the accuracy of the evaluation, making sure to explain why you made changes.

Original Data:
{data}

Proposed CVSS Evaluation:
{evaluation}
"""

CRITIQUE_PROMPT_SINGLE_METRIC = """
{instructions}

Use the workflow above to critique the CVSS Evaluation provided below.
Examine the reasoning behind the original decisions for the '{metric}' metric and, where possible, improve the accuracy of the evaluation by adding more context.
If you think the initial evaluation for the '{metric}' metric is incorrect, suggest changes where necessary, making sure to explain your reasoning behind the suggestions.
Return only the updated '{metric}' evaluation, ensuring that it only uses one of the defined values for that metric.

Here is the original data that was used to make the initial evaluation:
{data}

Here is the initial CVSS evaluation I would like you to critique:
{evaluation}
"""

SINGLE_METRIC_INSTRUCTIONS = [
    [
        "Attack Vector (AV)", 
        """Determine the Attack Vector (AV). Only use one of the following values: 'N', 'A', 'L', or 'P'.
- Can the attacker use some type of network or communication protocol to exploit the vulnerability?
    - Yes: Does the network use OSI layer 3 or 4 protocols, e.g. IP, TCP/IP, UDP?
        - Yes: Then the Attack Vector is Network (N)
        - No: Is the communication over a wireless channel?
            - Yes: Is the range of the wireless channel approximately 10 feet or less?
                - Yes: Then the Attack Vector is Local (L)
                - No: Then the Attack Vector is Adjacent (A)
                - Unknown: Then the Attack Vector is Adjacent (A)
            - No: Then the Attack Vector is Adjacent (A)
            - Unknown: Then the Attack Vector is Adjacent (A)
        - Unknown: Then the Attack Vector is Network (N)
    - No: Must the attacker have physical contact with the device?
        - Yes: Then the Attack Vector is Physical (P)
        - No: Then the Attack Vector is Local (L)
        - Unknown: Then the Attack Vector is Local (L)
    - Unknown: Then the Attack Vector is Network (N)"""
    ],
    [
        "Attack Complexity (AC)", 
        """Determine the Attack Complexity (AC). Only use one of the following values: 'L' or 'H'.
- Can the attacker exploit the vulnerability at will, without requiring special circumstances, configurations, or other vulnerabilities/attacks before attacking this vulnerability?
    - Yes: Then the Attack Complexity is Low (L)
    - No: Then the Attack Complexity is High (H)
    - Unknown: Then the Attack Complexity is Low (L)"""
    ],
    [
        "Privileges Required (PR)",
        """Determine the Privileges Required (PR). Only use one of the following values: 'N', 'L', or 'H'.
- Does the device/component use an authorization model that supports login for multiple different users or roles with different privilege levels?
	- Yes: Before attempting to exploit the vulnerability, must the attacker be authorized to the affected component(s)?
        - Yes: Must the attacker have administrator, maintainer, or other system-level privileges to attempt to exploit the vulnerability?
            - Yes: Then the Privileges Required is High (H)
            - No: Then the Privileges Required is Low (L)
            - Unknown: Then the Privileges Required is None (N)
        - No: Then the Privileges Required is None (N)
        - Unknown: Then the Privileges Required is None (N)
	- No: Then the Privileges Required is None (N)
	- Unknown: Then the Privileges Required is None (N)"""
    ],
    [
        "User Interaction (UI)",
        """Determine the User Interaction (UI). Only use one of the following values: 'N' or 'R'.
- To successfully exploit the vulnerability, must the attacker depend on some user or victim to perform an action or otherwise interact with the system?
	- Yes: Then User Interaction is Required (R)
	- No: Then User Interaction is None (N)
	- Unknown: Then User Interaction is None (N)"""
    ],
    [
        "Scope (S)",
        """Determine the Scope (S). Only use one of the following values: 'U' or 'C'.
- Can the attacker affect a component who's authority ("authorization scope") is different than that of the vulnerable component?
	- Yes: Then the Scope is Changed (C)
	- No: Then the Scope is Unchanged (U)
	- Unknown: Then the Scope is Changed (C)"""
    ],
    # TODO: Add instructions for the CIA metrics    
]