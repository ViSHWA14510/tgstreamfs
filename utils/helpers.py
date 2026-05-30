import base64
import re


def encode_file_id(file_id: str) -> str:
    """
    Encode a MongoDB ObjectId string to a URL-safe base64 token.
    Prefixed with 'file_' in the start link.
    """
    encoded = base64.urlsafe_b64encode(file_id.encode()).decode()
    return encoded


def decode_file_id(token: str) -> str:
    """
    Decode a URL-safe base64 token back to a MongoDB ObjectId string.
    Strips 'file_' prefix if present.
    """
    token = token.removeprefix("file_")
    # Add padding if needed
    padding = 4 - len(token) % 4
    if padding != 4:
        token += "=" * padding
    decoded = base64.urlsafe_b64decode(token).decode()
    return decoded


def get_file_size_str(size_bytes: int) -> str:
    """Convert bytes to a human-readable size string."""
    if not size_bytes:
        return "Unknown"
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} PB"


def sanitize_filename(name: str) -> str:
    """Remove unsafe characters from filenames."""
    return re.sub(r'[\\/*?:"<>|]', "_", name)
