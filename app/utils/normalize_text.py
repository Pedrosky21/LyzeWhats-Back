import re
import unicodedata

def normalize_text(t: str) -> str:
    # Minúsculas
    t = t.lower()
    # Reemplazar ñ temporalmente por un marcador
    t = t.replace("ñ", "{n}")
    # Quitar tildes
    t = ''.join(
        c for c in unicodedata.normalize('NFD', t)
        if unicodedata.category(c) != 'Mn'
    )
    # Restaurar ñ
    t = t.replace("{n}", "ñ")
    # Reducir letras repetidas (>2)
    t = re.sub(r'(.)\1{2,}', r'\1\1', t)
    # Quitar caracteres especiales, dejando letras, números, espacios y ñ
    t = re.sub(r'[^a-z0-9\sñ]', '', t)
    # Eliminar espacios extra
    t = re.sub(r'\s+', ' ', t).strip()
    return t
