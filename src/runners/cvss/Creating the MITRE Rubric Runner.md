Creating the MITRE Rubric Runner

Loaded the rubric into DocTalk
	"--split_chunks=1000",
    "--split_overlap=100"

**Prompt**: 
Using a summary of the document, and several examples from the document, generate a prompt to instruct an LLM to do the following things:
    1. Inform the LLM of what the MITRE Rubric is.
    2. Present several correct examples from the documents in the prompt.
    3. Present several wrong examples in the prompt, explaining why they are wrong.

**Response**: 
The MITRE Rubric is a structured series of questions that can be used to assess the security of medical devices. It is organized into several sections, each of which corresponds to a different part of the CVSS vector. When using the rubric, the analyst should use the Decision Flow diagrams to provide an overview of the logical flow of the questions, and the text-based series of questions should be regarded as more authoritative, providing additional guidance and examples beyond the diagrams. When a question could have multiple valid answers, then choose the answer for the worst-case scenario. When the answer is not known or uncertain, select “Unknown” (U) for the question, and use the recommended metric value that is associated with “Unknown.”

Examples of correct answers include selecting the answer for the worst-case scenario when a question could have multiple valid answers, and selecting “Unknown” (U) for the question when the answer is not known or uncertain. Examples of incorrect answers include selecting the answer for the best-case scenario when a question could have multiple valid answers, and selecting a metric value that is not associated with “Unknown” when the answer is not known or uncertain.

**Prompt**:
Give me instruct-style examples from the document, try to cover a broad range of examples.

**Response**: 
Examples from the document include: a vulnerability allowing modification of a drug library, a vulnerability allowing code execution by causing a long log entry, a device exposed to the Internet accidentally or unintentionally, and a scenario where a manufacturer's service technician may have exposed a device to the Internet.

**Prompt**:
Provide an example of using the MITRE rubric to generate a CVSS score on each of the following scenarios, using dummy data that you make up in context.
    - Vulnerability allowing modification of a drug library
    - Vulnerability allowing code execution by causing a long log entry
    - A device exposed to the Internet accidentally or unintentionally

**Response**:
For the first scenario, a CVSS score of 8.0 could be generated, with a vector of AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H. For the second scenario, a CVSS score of 7.0 could be generated, with a vector of AV:L/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H. For the third scenario, a CVSS score of 6.0 could be generated, with a vector of AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H.

**Prompt**:
Provide a detailed example of using the MITRE rubric to generate a CVSS score for the following scenario, using dummy data that you make up in context.  Be sure to print all of the dummy data in your answer.

Vulnerability allowing modification of a drug library

**Response**:
For this scenario, the Attack Vector would be set to Network (N) since the device is exposed to the Internet. The Attack Complexity would be set to Low (L) since the device was exposed accidentally or unintentionally. The Privileges Required would be set to None (N) since no special privileges are required to access the device. The User Interaction would be set to None (N) since no user interaction is required to access the device. The Scope would be set to Unchanged (U) since the vulnerability affects the same device that is exposed to the Internet. The Confidentiality Impact would be set to High (H) since the device is exposed to the Internet and the data stored on the device is at risk of being accessed by an unauthorized user. The Integrity Impact would be set to High (H) since the data stored on the device is at risk of being modified by an unauthorized user. The Availability Impact would be set to High (H) since the device is exposed to the Internet and the data stored on the device is at risk of being accessed or modified by an unauthorized user. The CVSS score for this scenario would be 8.8 (High).

**Prompt**: 
Write that scenario out in the style of an incident report filed by a low-level, unpaid college intern, never-done-this-job-before, 19 year old.

**Response**:    
- see the text file

**Prompt**: 
Provide a detailed example of using the MITRE rubric to generate a CVSS score for the following scenario:
In this scenario, the Attack Vector would be set to Network (N) since the device is exposed to the Internet. The Attack Complexity would be set to Low (L) since the device was exposed accidentally or unintentionally. The Privileges Required would be set to None (N) since no special privileges are required to access the device. The User Interaction would be set to None (N) since no user interaction is required to access the device. The Scope would be set to Unchanged (U) since the vulnerability affects the same device that is exposed to the Internet. The Confidentiality Impact would be set to High (H) since the device is exposed to the Internet and the data stored on the device is at risk of being accessed by an unauthorized user. The Integrity Impact would be set to High (H) since the data stored on the device is at risk of being modified by an unauthorized user. The Availability Impact would be set to High (H) since the device is exposed to the Internet and the data stored on the device is at risk of being accessed or modified by an unauthorized user. The CVSS score for this scenario would be 8.8 (High)

**CORRECT Response**: 
The CVSS score for this scenario would be 8.8 (High), which is calculated using the FIRST CVSS v3.0 specification. The CVSS vector for this scenario would be: AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H. The answers to the rubric's questions in the Base Metric Group would include: Attack Vector: Network (N), Attack Complexity: Low (L), Privileges Required: None (N), User Interaction: None (N), Scope: Unchanged (U), Confidentiality Impact:High (H), Integrity Impact:High (H), Availability Impact:High (H).


**Prompt**:
Give complete and detailed textual instructions on how to classify the Attack Vector of a vulnerability.  Make sure to include all possible classifications, such as "A", "P", "L", etc.

**Response**:
The Attack Vector (AV) metric is used to characterize the attack complexity of a vulnerability. It is a single-character alphanumeric code that is used to represent the type of attack required to exploit the vulnerability. The possible values are:

N: Network - The vulnerability can be exploited remotely, either from the Internet or from an Intranet. This includes access from third-party networks (e.g. manufacturer systems with access to hospital-internal network).

A: Adjacent Network - The vulnerability can be exploited over a local area network (LAN), such as Ethernet or Wi-Fi.

L: Local - The vulnerability can be exploited by an attacker with physical access to the vulnerable system.

P: Physical - The vulnerability can be exploited by an attacker with physical access to the vulnerable system and requires the attacker to have specialized knowledge or tools.

To classify the Attack Vector of a vulnerability, the analyst must first consider if the vulnerability can be exploited remotely, either from the Internet or from an Intranet. If so, the Attack Vector is classified as “N” (Network). If not, the analyst must consider if the vulnerability can be exploited over a local area network (LAN), such as Ethernet

**SHORTENED Response**:
Attack Vector (AV) categorizes the complexity of a vulnerability's exploitation. It's a single alphanumeric code representing the attack type:

N: Remote exploit from Internet or Intranet.
A: Exploit on adjacent network (LAN).
L: Exploit with physical access to system.
P: Exploit with physical access and specialized knowledge/tools.

To determine the Attack Vector, analyze if the vulnerability can be remotely exploited (N). If not, check if it can be exploited on an adjacent network (A) like Ethernet or Wi-Fi.


**Prompt 1**:
Give complete and detailed textual instructions on how to classify the following elements of a vulnerability using the MITRE Rubric.  Make sure to list the element and all possible classifcation values.  Include how the metric is calculated.  Condense your answers down to the smallest number of characters you can, while still being explicit in the instructions they contain.
Attack Vector (AV): 
Q1, 
Q2, 
Q3, 
Q4, 
Q5, 
Q5.1

Attack Complexity (AC): Q1 (XACL)
Privileges Required (PR): Q1 (XPRL), Q2 (XPRZ), Q3 (XPRS)
User Interaction (UI): Q1 (XUI)
Scope (S): Q1 (XS), Q2 (XSLC)

**Prompt 2**:
Give complete and detailed textual instructions on how to classify the following elements of a vulnerability.  Make sure to include all possible classifications, such as "X", "P", "Z", etc.  Compress your answers into as little text as possible to explain how to classify each item in the elements.
Privileges Required
User Interaction
Scope

**Prompt 2**:
Give complete and detailed textual instructions on how to classify the following elements of a vulnerability.  Make sure to include all possible classifications, such as "X", "P", "Z", etc.  Compress your answers into as little text as possible to explain how to classify each item in the elements.
Environmental Metric Group elements:
Confidentiality Requirement
Integrity Requirement
Availability Requirement
Modified Confidentiality
Modified Integrity
Modified Availability
Other Metrics: CVSS v3.0 Gaps

**Prompt 3**:
Give complete and detailed textual instructions on how to classify the following elements of a vulnerability.  Make sure to include all possible classifications, such as "X", "P", "Z", etc.  Compress your answers into as little text as possible to explain how to classify each item in the elements.
Remediation Level elements:
Report Confidence
Exploit Code Maturity
Remediation Level
Requirements for Security Functional Level


Look up the Attack Vector (AV) Metric Values and their meanings.  Return only a list of the values and their meanings.

Look up the Attack Vector (AV) Metric Values (N,A,L,P) and their meanings.  Then score the following report.  Ensure that you include the reasoning as to why you selected that value, and quote the report in your response.

Look up the Attack Complexity (AC) Metric Values (L,H) and their meanings.  Then score the following report.  

Generate a CVSS score and Vector String for the following report. Ensure that you include the reasoning as to why you selected that value, and quote the report in your response.
Incident Report
Date: 7/9/2023
Reported By: Karen
Position: Intern
Subject: Vulnerability allowing modification of a drug library
Description
On 7/9/2023, during routine system monitoring, I came across a critical vulnerability in the drug library of our medical device system. This incident report aims to provide a plain English description of the scenario in which the vulnerability occurred.
Scenario
Our medical device, which helps healthcare professionals manage patient medications, experienced a vulnerability that allowed unauthorized individuals to modify the drug library. The drug library contains vital information about medications, including dosages, interactions, and safety guidelines. Due to the vulnerability, an attacker with access to the device over the Internet could make unauthorized changes to this essential database.
In this scenario, imagine a situation where our medical device accidentally became accessible over the Internet without proper security measures in place. This exposure created an opportunity for malicious actors to exploit the vulnerability without needing any special permissions or interaction from users. The vulnerable device remained unchanged, maintaining its original purpose and functionality.
The impact of this vulnerability on the device was significant. The confidentiality of patient data stored within the drug library was at high risk, as unauthorized individuals could access and potentially misuse this sensitive information. Moreover, the integrity of the drug library data was compromised, as the vulnerability allowed unauthorized modification, leading to potential errors or incorrect medication information.
Furthermore, the availability of the device and the accuracy of the drug library were severely impacted. The device, being exposed to the Internet, faced a high risk of unauthorized access or modification by individuals with malicious intent. This situation posed a serious threat to patient safety and the proper management of medications within the healthcare system.
Considering the severity of the vulnerability and its potential impact, it is crucial to address this issue promptly to protect patient data, ensure the integrity of the drug library, and mitigate the risks associated with unauthorized access and modifications.