import re

def estimate_tokens(text: str) -> int:
    """
    More accurate token estimation based on GPT tokenization rules:
    - Splits on whitespace and punctuation
    - Accounts for common patterns in English text
    - Numbers and special characters count differently
    """
    if not text:
        return 0
        
    # Basic cleanup
    text = text.strip()
    
    # Count specific patterns
    patterns = {
        'whitespace': len(re.findall(r'\s+', text)),  # Spaces, newlines
        'numbers': len(re.findall(r'\d+', text)),     # Numbers
        'punctuation': len(re.findall(r'[.,!?;:"]', text)),  # Common punctuation
        'special': len(re.findall(r'[^a-zA-Z0-9\s.,!?;:"]', text)),  # Other special chars
    }
    
    # Split into words
    words = re.findall(r'\b\w+\b', text)
    
    # Calculate token estimate
    token_count = 0
    
    # Words (accounting for length)
    for word in words:
        if len(word) <= 2:
            token_count += 0.5  # Very short words often share tokens
        elif len(word) <= 4:
            token_count += 1    # Average words
        else:
            # Longer words might be split into multiple tokens
            token_count += (len(word) / 4)
    
    # Add pattern counts
    token_count += patterns['whitespace'] * 0.1  # Whitespace usually combines with words
    token_count += patterns['numbers'] * 0.5     # Numbers are often efficient
    token_count += patterns['punctuation'] * 0.3 # Punctuation often combines
    token_count += patterns['special'] * 1       # Special characters often get own token
    
    # Round up to nearest whole token
    return max(1, round(token_count)) 