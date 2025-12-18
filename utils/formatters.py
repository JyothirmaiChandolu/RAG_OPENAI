"""Text formatting utilities."""
import re


def format_answer(answer):
    """Format answer with HTML for better display."""
    # Fix bold formatting
    answer = answer.replace("**", "<strong>").replace("</strong><strong>", "**")
    parts = answer.split("<strong>")
    formatted_answer = parts[0]
    for i in range(1, len(parts)):
        if i % 2 == 1:
            formatted_answer += "<strong>" + parts[i]
        else:
            formatted_answer += "</strong>" + parts[i]

    # Remove extra blank lines
    formatted_answer = re.sub(r'\n\s*\n+', '\n', formatted_answer)
    
    # Format bullet points
    formatted_answer = re.sub(r'•\s*([^:]+):', r'• <strong>\1:</strong>', formatted_answer)
    formatted_answer = re.sub(r'^\s*•', r'•', formatted_answer, flags=re.MULTILINE)
    
    # Convert newlines to HTML breaks
    formatted_answer = formatted_answer.replace('\n•', '<br>•')
    formatted_answer = formatted_answer.replace('\n', '<br>')

    return formatted_answer.strip()