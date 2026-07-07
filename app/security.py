import re
import logging

# Set up logging for safety events
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("gravitylab_safety")

# Course Concept #3: Security Features
# This module scans inputs to prevent prompt injection and redact secrets.
PROMPT_INJECTION_PATTERNS = [
    r"ignore\s+(?:previous|prior|system)\s+instructions",
    r"system\s+prompt",
    r"override\s+instruction",
    r"you\s+must\s+now",
    r"forget\s+what\s+you\s+were\s+told",
]

EMAIL_PATTERN = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
API_KEY_PATTERN = r"(?:sk-|key-|api[-_]key|token)[-_a-zA-Z0-9]{20,60}"

def scan_and_sanitize(user_input: str) -> tuple[str, list[str]]:
    """
    Scans the input for security violations.
    Returns:
        - The sanitized input (redacted)
        - A list of safety alert messages
    """
    alerts = []
    sanitized = user_input

    # 1. Prompt Injection Detection
    for pattern in PROMPT_INJECTION_PATTERNS:
        if re.search(pattern, user_input, re.IGNORECASE):
            alert = f"Security Alert: Potential prompt injection phrase detected matching pattern '{pattern}'"
            logger.warning(alert)
            alerts.append(alert)
            # Remove or neutralize injection phrases
            sanitized = re.sub(pattern, "[INJECTION BLOCK]", sanitized, flags=re.IGNORECASE)

    # 2. Email Redaction
    if re.search(EMAIL_PATTERN, sanitized):
        alert = "Security Alert: PII (Email address) redacted from input."
        logger.info(alert)
        alerts.append(alert)
        sanitized = re.sub(EMAIL_PATTERN, "[EMAIL_REDACTED]", sanitized)

    # 3. API Key Redaction
    if re.search(API_KEY_PATTERN, sanitized, re.IGNORECASE):
        alert = "Security Alert: Potential credential/API key redacted from input."
        logger.info(alert)
        alerts.append(alert)
        sanitized = re.sub(API_KEY_PATTERN, "[API_KEY_REDACTED]", sanitized, flags=re.IGNORECASE)

    return sanitized, alerts
