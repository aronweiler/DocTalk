GENERATED_PROMPTS = [
    """Below is an instruction that describes a task. Write a response that appropriately completes the request.

### Instruction: Review the following {language} code and identify any potential areas for code optimizations. Consider algorithm improvements, better data structures, or any other performance-enhancing suggestions.

{code}

### Response in Markdown:
# Here is the review of the {language} code in Markdown. I've highlighted potential areas for optimization and provided alternative approaches:
""",
"""Below is an instruction that describes a task. Write a response that appropriately completes the request.

### Instruction: Conduct a security-focused review of the following {language} code. Look for potential security vulnerabilities, such as SQL injection, cross-site scripting (XSS), or improper handling of sensitive data. Suggest remedies to strengthen the code's security.

{code}

### Response in Markdown:
# Here is the security review of the {language} code in Markdown. I've outlined potential vulnerabilities and proposed security measures:
""",
"""Below is an instruction that describes a task. Write a response that appropriately completes the request.

### Instruction: Review the following {language} code for any instances of uninitialized variables or undefined behavior. Identify problematic areas and suggest corrections to ensure reliable code execution.

{code}

### Response in Markdown:
# Here is the review of the {language} code in Markdown. I've pointed out uninitialized variables and potential undefined behavior, along with proposed solutions:
""",
"""Below is an instruction that describes a task. Write a response that appropriately completes the request.

### Instruction: Conduct a memory-focused review of the following {language} code. Look for any memory leaks or buffer overflow possibilities that might lead to runtime issues. Recommend strategies to manage memory efficiently.

{code}

### Response in Markdown:
# Here is the memory review of the {language} code in Markdown. I've highlighted memory leak concerns and potential buffer overflow risks, along with suggested mitigations:
""",
"""Below is an instruction that describes a task. Write a response that appropriately completes the request.

### Instruction: Perform a comprehensive review of the following {language} code to ensure clarity and correct behavior. Check for any confusing sections or logic errors that could lead to incorrect outcomes. Provide suggestions for improving code readability and correctness.

{code}

### Response in Markdown:
# Here is the review of the {language} code in Markdown. I've addressed concerns related to clarity and correctness, with recommended code enhancements:
""",
"""Below is an instruction that describes a task. Write a response that appropriately completes the request.

### Instruction: Review the following {language} code for any issues, such as buffer overflow, memory leaks, uninitialized variables, undefined behavior, or potential code optimizations. Provide feedback and suggestions for improvement.

{code}

### Response in Markdown:
# Here is the review of the {language} code in Markdown (double checking the line numbers).  I have placed my concerns at the top of my response:
"""
]