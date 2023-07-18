IDENTIFY_VULNERABLE_COMPONENT_PROMPT = """
Identify the vulnerable component(s) and/or system(s) in the following data.  Return only the description of the vulnerable components and/or systems.

Data:
{data}
"""

CHAIN_OF_THOUGHT_EXAMPLE_DATA_1 = """
Data: 
Apache Tomcat 4.1.0 through 4.1.39, 5.5.0 through 5.5.27, and 6.0.0 through 6.0.18 permits web applications to replace an XML parser used for other web applications, which allows local users to read or modify the (1) web.xml, (2) context.xml, or (3) tld files of arbitrary web applications via a crafted application that is loaded earlier than the target application.
This Tomcat vulnerability allows a web-apps to reference an XML parser instead of using the default Apache XML parser. The attacker must remove all existing web-apps including those in server/webapps, then install a web-app with an XML parser is stored in WEB-INF/lib. This will cause Tomcat to use the new XML parser to process all web.xml, context.xml and tld files of other webapps. If that non-standard XML parser is replaced with a malicious one, the content of the victim web app XML can be disclosed, the resulting JSP could be corrupted (if it compiled at all) or possibly even weaponized for further attacks.
There are 2 different ways this attack may manifest. First a local privileged user could simply replace the non-Apache XML parser with a malicious variant. The second is that an attacker may use social engineering and user interaction to inject the malicious XML parser into the system. We will score for the former.
"""

CHAIN_OF_THOUGHT_EXAMPLE_EVALUATION_1 = """
Vulnerable Component: 
- Apache Tomcat 4.1.0 through 4.1.39, 5.5.0 through 5.5.27, and 6.0.0 through 6.0.18
Evaluation (thinking it through, step-by-step):
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
Vulnerable Component:
- Medication management medical device
Evaluation (thinking it through, step-by-step):
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

CHAIN_OF_THOUGHT_EXAMPLE_DATA_3 = """
Data:
Our social media platform, which allows users to share photos and videos, has discovered a vulnerability that allows unauthorized users to delete content posted by other users.
The vulnerability can be exploited remotely without any special privileges. An attacker only needs to know the ID of the content they want to delete.
Once an attacker identifies the ID of a specific post or video, they can send a crafted request to the server, causing the targeted content to be deleted permanently.
This vulnerability poses a significant risk to user data integrity and can lead to the loss of important or sensitive content.
"""

CHAIN_OF_THOUGHT_EXAMPLE_EVALUATION_3 = """
Vulnerable Component: Social media platform for sharing photos and videos
Evaluation (thinking it through, step-by-step):
The vulnerability can be exploited remotely, so the Attack Vector (AV) is N (Network)
The data does not mention any complexity required to exploit the vulnerability, so Attack Complexity (AC) is L (Low)
The vulnerability does not require any special privileges, so Privileges Required (PR) is N (None)
The attacker does not need any user interaction to exploit the vulnerability, so User Interaction (UI) is N (None)
The scope of the vulnerability is limited to the targeted content, so Scope (S) is U (Unchanged)
The vulnerability does not directly impact confidentiality, but it can result in the loss of important or sensitive content, so Confidentiality (C) is N (None)
The attacker can delete content, resulting in a loss of data integrity, so Integrity (I) is H (High)
The vulnerability does not impact availability directly, so Availability (A) is N (None)

Therefore, the CVSS Vector String is: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N

"""

CHAIN_OF_THOUGHT_EXAMPLE_DATA_4 = """
Data:
Our e-commerce website, which processes online transactions, has identified a vulnerability that allows attackers to inject malicious scripts into the checkout page.
The vulnerability occurs due to improper input sanitization, which allows attackers to insert JavaScript code into the payment form fields.
Once a user submits the payment form, the injected script gets executed in the user's browser, potentially capturing sensitive information such as credit card details or login credentials.
The vulnerability can be exploited remotely without any special privileges, and it requires user interaction through the payment process.
The impact of this vulnerability can lead to significant financial loss, compromised customer data, and damage to the reputation of our e-commerce platform.
"""

CHAIN_OF_THOUGHT_EXAMPLE_EVALUATION_4 = """
Vulnerable Component: E-commerce website's checkout page
Evaluation (thinking it through, step-by-step):
The vulnerability can be exploited remotely, so the Attack Vector (AV) is N (Network)
The vulnerability occurs due to improper input sanitization, indicating a low complexity to exploit, so Attack Complexity (AC) is L (Low)
The vulnerability does not require any special privileges, so Privileges Required (PR) is N (None)
The attacker relies on user interaction during the payment process to execute the injected script, so User Interaction (UI) is R (Required)
The vulnerability affects the checkout page and potentially captures sensitive information, indicating a change in scope, so Scope (S) is C (Changed)
The impact includes the compromise of customer data and financial loss, signifying high confidentiality (C) and integrity (I) impacts, respectively, so C (Confidentiality) is H (High) and I (Integrity) is H (High)
The vulnerability does not directly impact availability, so Availability (A) is N (None)

Therefore, the CVSS Vector String is: CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N
"""

CVSS_INSTRUCT_PROMPT = """You are a security AI tasked with evaluating the CVSS score of a vulnerability.
For the vulnerable component(s): {vulnerable_component}
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
    - Prepend your evaluation with a description of the vulnerable component.
    - Assign the corresponding option value to each metric.
- IMPORTANT: If the data does not contain enough information to determine a metric's value, select the default value and explain why you selected it in your response.
- Don't forget to prefix the CVSS vector with 'CVSS:3.1/'
"""

# TODO: Add examples to the prompts below
CRITIQUE_PROMPT = """
{instructions}

Given the context above, use the following instructions to critique the Proposed CVSS Evaluation:
- Examine the reasoning behind the original decisions for each metric.
- Where possible, improve the accuracy of the evaluation by adding more context or making changes where necessary.
- Make sure to explain why you made changes, if any were made.

Original Data:
{data}

Proposed CVSS Evaluation:
{evaluation}
"""

# TODO: Add examples to the prompts below
CRITIQUE_PROMPT_SINGLE_METRIC = """
{instructions}

{example_data}
{example_evaluation}  

Use the workflow above to critique the CVSS Evaluation provided below.
Examine the reasoning behind the original decisions for the '{metric}' metric and, where possible, improve the accuracy of the evaluation by adding more context.
If you think the initial evaluation for the '{metric}' metric is incorrect, suggest changes where necessary, making sure to explain your reasoning behind the suggestions.
Return only the updated '{metric}' evaluation, ensuring that it only uses one of the defined values for that metric, do not return an updated CVSS vector.

Here is the data that was used to make the initial evaluation:
{data}

Here is the initial CVSS evaluation I would like you to critique:
{evaluation}
"""

# TODO: Add examples to the prompts below
SINGLE_METRIC_EVALUATION_PROMPT = """
{instructions}

For the vulnerable component(s): {vulnerable_component}
- Use the instructions above to evaluate the data provided below for the '{metric}' metric, providing an explanation for your evaluation in your response.
- Assume that all preconditions for the vulnerability to exist are met, and that the attacker has all of the skills and equipment necessary to exploit the vulnerability.    
- IMPORTANT: If the data provided does not contain enough information to determine a metric's value, select the default value and explain why you selected it in your response.

{example_data}
{example_evaluation}    

Data:
{data}
"""

COMBINE_SINGLE_RESULTS_PROMPT = """
Combine the following single metric evaluations into a single complete evaluation for the vulnerable component(s), including all of the original observations.
Generate a final Base Metric Group CVSS 3.1 Vector String (combining all of the single evaluation metrics).
Don't forget to prefix the CVSS vector string with 'CVSS:3.1/'
Try to format the final combined evaluation in a way that is easy to read and understand.

The final combined evaluation should look like this:
'Evaluation for vulnerable component(s): {{vulnerable component}}
- The Attack Vector (AV) is {{AV option}}, because {{detailed AV explanation}}.
- The Attack Complexity (AC) is {{AC option}}, because {{detailed AC explanation}}.
- The Privileges Required (PR) is {{PR option}}, because {{detailed PR explanation}}.
- The User Interaction (UI) is {{UI option}}, because {{detailed UI explanation}}.
- The Scope (S) is {{S option}}, because {{detailed S explanation}}.
- The Confidentiality (C) is {{C option}}, because {{detailed C explanation}}.
- The Integrity (I) is {{I option}}, because {{detailed I explanation}}.
- The Availability (A) is {{A option}}, because {{detailed A explanation}}.

Final CVSS 3.1 Vector String: CVSS:3.1/AV:{{AV option}}/AC:{{AC option}}/PR:{{PR option}}/UI:{{UI option}}/S:{{S option}}/C:{{C option}}/I:{{I option}}/A:{{A option}}'

Single Metric Evaluations:
{evaluations}
"""

SINGLE_METRIC_SAMPLE_DATA = """EXAMPLE DATA:
Our social media platform, which allows users to share photos and videos, has discovered a vulnerability that allows unauthorized users to delete content posted by other users.
The vulnerability can be exploited remotely without any special privileges. An attacker only needs to know the ID of the content they want to delete.
Once an attacker identifies the ID of a specific post or video, they can send a crafted HTTP request to the server, causing the targeted content to be deleted permanently.
Using a crafted request, the attacker can also associate the content with a different account, potentially exposing sensitive data to unauthorized users.
This vulnerability poses a significant risk to user data integrity and can lead to the loss of important or sensitive content."""

SINGLE_METRIC_INSTRUCTIONS = [
    [
        "Attack Vector (AV)", 
        """Attack Vector (AV) represents the path or means through which a vulnerability can be exploited. It characterizes the specific entry point or method used by an attacker to target the system. The default value of Attack Vector is Network (N).
Determine the Attack Vector (AV). Only use one of the following values: 'N', 'A', 'L', or 'P'.
- Can the attacker use the vulnerability to exploit the system remotely in any manner? (e.g. using things such as Radio Frequency, Wi-Fi, Bluetooth, TCP, HTTP, UDP, Zigbee, Z-Wave, etc.)
    - Yes: Does the network use OSI layer 3 or 4 protocols? (e.g. IP, ICMP, TCP, UDP, OSPF, BGP, SNMP, FTP, SSH, Telnet, etc.)
        - Yes: Then the Attack Vector is Network (N)
        - No: Is the communication over a wireless channel?  (e.g. Bluetooth, Wi-Fi, Zigbee, Z-Wave, NFC, LTE, LoRa, 5G, RF, etc.)
            - Yes: Is the range of the wireless channel approximately 10 feet or less?  (e.g. short-range wireless such as NFC, Zigbee, RFID, wireless charging, etc.)
                - Yes: Then the Attack Vector is Local (L)
                - No: Then the Attack Vector is Adjacent (A)
                - Unknown: Then the Attack Vector is Adjacent (A)
            - No: Then the Attack Vector is Adjacent (A)
            - Unknown: Then the Attack Vector is Adjacent (A)
        - Unknown: Then the Attack Vector is Network (N)
    - No: Must the attacker have direct physical contact with the device (e.g. in order to open it, insert something into a port, physically extract memory, etc.), excluding input devices such as mouse and keyboard?
        - Yes: Then the Attack Vector is Physical (P)
        - No: Then the Attack Vector is Local (L)
        - Unknown: Then the Attack Vector is Local (L)
    - Unknown: Then the Attack Vector is Network (N)""",
    """Example Evaluation:
Vulnerable Component:
- Social Media Platform
Evaluation:
1. Can the attacker use the vulnerability to exploit the system remotely in any manner?
   - Yes, the vulnerability can be exploited remotely via an HTTP request over a network.
    1a. Does the network use OSI layer 3 or 4 protocols, e.g., IP, TCP/IP, UDP?
        - Yes, the attacker can use the HTTP protocol to exploit the vulnerability, which uses TCP/IP.

The Attack Vector (AV) is Network (N).
    """
    ],
    [
        "Attack Complexity (AC)", 
        """Attack Complexity (AC) describes the conditions outside of the attacker's control that must exist in order to exploit the vulnerability, the default value of Attack Complexity is Low (L).
Determine the Attack Complexity (AC). Only use one of the following values: 'L' or 'H'.
- Can the attacker exploit the vulnerability at will, without requiring special circumstances, configurations, or other vulnerabilities/attacks before attacking this vulnerability?
    - Yes: Then the Attack Complexity is Low (L)
    - No: Then the Attack Complexity is High (H)
    - Unknown: Then the Attack Complexity is Low (L)""",
    """Example Evaluation:
Vulnerable Component:
- Social Media Platform
Evaluation:
1. Can the attacker exploit the vulnerability at will, without requiring special circumstances, configurations, or other vulnerabilities/attacks before attacking this vulnerability?
    - Yes, the attacker can exploit the vulnerability at will, without requiring special circumstances, configurations, or other vulnerabilities/attacks before attacking this vulnerability.

 The Attack Complexity (AC) is Low (L).    

    """
    ],
    [
        "Privileges Required (PR)",
        """Privileges Required (PR) describes the privileges an attacker must possess, such as user account access, kernel access, access to a VM, PIN code, etc., before successfully exploiting the vulnerability, the default value of Privileges Required is None (N).
Determine the Privileges Required (PR). Only use one of the following values: 'N', 'L', or 'H'.        
- Does the device/component use an authorization model that supports login for multiple different users or roles with different privilege levels?
	- Yes: Before attempting to exploit the vulnerability, must the attacker be authorized to the affected component(s)?
        - Yes: Must the attacker have administrator, maintainer, or other system-level privileges to attempt to exploit the vulnerability?
            - Yes: Then the Privileges Required is High (H)
            - No: Then the Privileges Required is Low (L)
            - Unknown: Then the Privileges Required is None (N)
        - No: Then the Privileges Required is None (N)
        - Unknown: Then the Privileges Required is None (N)
	- No: Then the Privileges Required is None (N)
	- Unknown: Then the Privileges Required is None (N)""",
    """Example Evaluation:
    Vulnerable Component:
    - Social Media Platform
    Evaluation:
1. Does the social media platform use an authorization model that supports login for multiple different users or roles with different privilege levels?
    - Yes: The social media platform supports login for multiple users with different privilege levels.

2. Before attempting to exploit the vulnerability, must the attacker be authorized to the affected component(s)?
    - No: The attacker does not need to be authorized to the affected component(s).

3. Must the attacker have administrator, maintainer, or other system-level privileges to attempt to exploit the vulnerability?
    - No: The attacker does not need administrator or system-level privileges.

The Privileges Required (PR) is None (N)."""
    ],
    [
        "User Interaction (UI)",
        """User Interaction (UI) represents the level of user (not attacker) interaction required to exploit the vulnerability, the default value of User Interaction is None (N).
Determine the User Interaction (UI). Only use one of the following values: 'N' or 'R'.
- To successfully exploit the vulnerability, must the attacker depend on some user or victim to perform an action or otherwise interact with the system?
	- Yes: Then User Interaction is Required (R)
	- No: Then User Interaction is None (N)
	- Unknown: Then User Interaction is None (N)""",
    """Example Evaluation:
Vulnerable Component:
- Social Media Platform
Evaluation:
1. To successfully exploit the vulnerability, must the attacker depend on some user or victim to perform an action or otherwise interact with the system?
    - No, the attacker does not depend on any user or victim interaction, because the attacker can exploit the vulnerability independently by directly sending the crafted request to the server.

The User Interaction (UI) is None (N)."""
    ],
    [
        "Scope (S)",
        """Scope (S) represents the extent of impact a successful exploit has on the system's component or other components. It determines whether the vulnerability's effect is limited to the specific component being targeted or if it has the potential to affect other interconnected components within the vulnerable system itself or other systems (excluding users), the default value of Scope is Changed (C).
Determine the Scope (S). Only use one of the following values: 'U' or 'C'.
- Is a successful exploit contained within the targeted component only and does it not have a cascading effect on other system components, or does the impact remain localized without propagating to other parts of the system?
	- Yes: Then the Scope is Unchanged (U)
	- No: Then the Scope is Changed (C)
	- Unknown: Then the Scope is Changed (C)""",
    """Example Evaluation:
    Vulnerable Component:
    - Social Media Platform
    Evaluation:
1. Is a successful exploit contained within the targeted component only and does it not have a cascading effect on other system components, or does the impact remain localized without propagating to other parts of the system?
    - Yes. The vulnerable component is the social media platform, which includes the functionality to manage and store user-generated content. The content is a part of the social media platform. The attacker can only affect the content within the social media platform. The attacker cannot affect a component outside of the vulnerable component. In this case, the impact is limited to the content within the social media platform. The attacker's actions do not extend beyond the content itself.
    
The Scope (S) is Unchanged (U)."""
    ],
    [
        "Confidentiality (C)",
        """Confidentiality refers to limiting information access and disclosure to only authorized users, as well as preventing access by, or disclosure to, unauthorized ones, the default value of Confidentiality is High (H).
Determine the Confidentiality Impact (C). Only use one of the following values: 'N', 'L', or 'H'.
- Can the attacker can gain access to read (or exfiltrate) any data?
    - Yes: Is the data sensitive (e.g. financial, health, or personal data)?
        - Yes: Then the Confidentiality Impact is High (H)
        - No: Then the Confidentiality Impact is Low (L)
    - No: Then the Confidentiality Impact is None (N)""",
    """Example Evaluation:
Vulnerable Component:
- Social Media Platform
Evaluation:
1. Can the attacker can gain access to read (or exfiltrate) any data?
    - Yes, the vulnerability allows the attacker to associate content with a different account.  The attacker could create their own separate account, and then associate someone elses content with their account, which would allow them to read the content.
    1a. Is the data sensitive (e.g. financial, health, or personal data)?
        - Yes, the data is sensitive. The description of the vulnerability itself calls the data sensitive.  Additionally, while the content is not financial or health data, it is personal data.

The Confidentiality Impact (C) is High (H)."""
    ],
    [
        "Integrity (I)",
        """Integrity refers to the trustworthiness and veracity of information, the default value of Integrity is High (H).
Determine the Integrity Impact (I). Only use one of the following values: 'N', 'L', or 'H'.
- Can the attacker can modify any data?
    - Yes: Is the data sensitive (e.g. financial, health, or personal data)?
        - Yes: Then the Integrity Impact is High (H)
        - No: Then the Integrity Impact is Low (L)
    - No: Then the Integrity Impact is None (N)""",
    """Example Evaluation:
Vulnerable Component:
- Social Media Platform
Evaluation:
1. Can the attacker can modify any data?
    - Yes, The vulnerability allows the attacker to delete content.  Additionally, the vulnerability allows the attacker to associate content with a different account.  The attacker could create their own separate account, and then associate someone elses content with their account, which could also allow them to modify the content.
    1a. Is the data sensitive (e.g. financial, health, or personal data)?
        - Yes, the data is sensitive. The description of the vulnerability itself calls the data sensitive.  Additionally, while the content is not financial or health data, it is personal data.

The Integrity Impact (I) is High (H)."""
    ],
    [
        "Availability (A)",
        """Availability refers to the loss of availability of the impacted component itself, such as a networked service (e.g., web, database, email). Since availability refers to the accessibility of information resources, attacks that consume network bandwidth, processor cycles, or disk space all impact the availability of an impacted component. The default value of Availability is High (H).
Determine the Availability Impact (A). Only use one of the following values: 'N', 'L', or 'H'.
- Can the attacker cause a denial of service (DoS) to the vulnerable component, or any sub-component within the vulnerable component?
    - Yes: Is the DoS a complete DoS (i.e. the entire component is unavailable)?
        - Yes: Then the Availability Impact is High (H)
        - No: Then the Availability Impact is Low (L)
    - No: Then the Availability Impact is None (N)""",
    """Example Evaluation:
Vulnerable Component:
- Social Media Platform
Evaluation:
1. Can the attacker cause a denial of service (DoS) to the vulnerable component, or any sub-component within the vulnerable component?
    - Yes, The vulnerability allows the attacker to delete content.  Additionally, the vulnerability allows the attacker to associate content with a different account.  The attacker could create their own separate account, and then associate someone elses content with their account, which could also allow them to delete the content.
    1a. Is the DoS a complete DoS (i.e. the entire component is unavailable)?
        - No, the DoS is not a complete DoS.  The attacker can only delete or modify the content, but the social media platform itself is still available.

The Availability Impact (A) is Low (L)."""
    ]
]