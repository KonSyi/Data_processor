@staticmethod
def _format_int(value: int) -> str:
    return f"{value:,}".replace(",", " ")


@staticmethod
def _format_float(value: float) -> str:
    return f"{value:.6g}"


@staticmethod
def _safe_filename(text: str) -> str:
    cleaned = text.replace("/", "_").replace("\\", "_")
    cleaned = re.sub(r'[^0-9A-Za-zА-Яа-я._ -]+', "_", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned or "channel"