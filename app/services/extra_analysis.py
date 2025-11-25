def analyze_top_phrases(df, ngram_min=2, ngram_max=4, top=20):
    from collections import Counter
    import re

    # --- STOP PHRASES AMPLIADOS ---
    stop_prefixes = {
        "que me", "q me",
        "que no", "q no",
        "no me", "no te", "no se",
        "y me", "y no",
        "a la", "a ver", "a mi", "a mí",
        "por eso", "por qué",
        "lo q", "creo q", "se me",
        "pero no", "ya me", "en el",
        "si no", "y si", "voy a",
        "a hacer", "va a", "vas a",
        "de la", "en la", "de mi", "de mí",
        "es que", "es q",
    }

    # Frases basura que pueden aparecer en cualquier parte
    stop_substrings = {
        " q ", " x ", " de ", " la ", " no ", " si ",
    }

    def clean_text(t):
        t = t.lower()
        t = re.sub(r"[^\w\sáéíóúüñ]", "", t)
        return t

    def is_stop_phrase(phrase):
        # Si empieza con un prefijo prohibido
        for bad in stop_prefixes:
            if phrase.startswith(bad):
                return True
        # Si contiene substrings muy comunes
        for bad in stop_substrings:
            if bad in f" {phrase} ":
                return True
        return False

    # --- GENERAR FRASES ---
    all_phrases = []

    for msg in df["text"]:
        msg = clean_text(msg)
        words = msg.split()

        if len(words) < 2:
            continue

        for n in range(ngram_min, ngram_max + 1):
            for i in range(len(words) - n + 1):
                phrase = " ".join(words[i:i+n])

                # Filtrar frases basura
                if is_stop_phrase(phrase):
                    continue

                all_phrases.append(phrase)

    counts = Counter(all_phrases)
    return dict(counts.most_common(top))


def analyze_conversation_starters(df):
    """Quién inicia más conversaciones (cambio de remitente)."""
    df = df.sort_values("timestamp")

    df["conversation_start"] = (
        df["sender"] != df["sender"].shift(1)
    ).astype(int)

    return df[df["conversation_start"] == 1]["sender"].value_counts().to_dict()


def analyze_saludos(df):
    """
    Cuenta saludos matutinos ("buenos días") y despedidas nocturnas
    ("hasta mañana"), tolerando variaciones de escritura.
    """

    import re
    from app.utils.normalize_text import normalize_text

    # Normalizamos todo el texto para asegurar coincidencias robustas
    df["normalized"] = df["text"].apply(normalize_text)

    # Patrones flexibles (sin tildes y tolerando variaciones)
    patrones = {
        "buenos_dias": re.compile(r"\bbuenos?\s+dias?\b"),
        "hasta_mañana": re.compile(r"\bhasta\s+mañana\b"),
    }

    resultados = {
        "buenos_dias_total": 0,
        "hasta_mañana_total": 0,
        "buenos_dias_por_persona": {},
        "hasta_mañana_por_persona": {}
    }

    for idx, row in df.iterrows():
        sender = row["sender"]
        text = row["normalized"]

        # --- BUENOS DÍAS ---
        if patrones["buenos_dias"].search(text):
            resultados["buenos_dias_total"] += 1
            resultados["buenos_dias_por_persona"][sender] = \
                resultados["buenos_dias_por_persona"].get(sender, 0) + 1

        # --- HASTA MAÑANA ---
        if patrones["hasta_mañana"].search(text):
            resultados["hasta_mañana_total"] += 1
            resultados["hasta_mañana_por_persona"][sender] = \
                resultados["hasta_mañana_por_persona"].get(sender, 0) + 1

    return resultados



def analyze_te_amo(df):
    """Quién escribe más 'te amo' y total general."""
    mask = df["text"].str.lower().str.contains("te amo")

    total = mask.sum()

    by_sender = df[mask]["sender"].value_counts().to_dict()

    return {
        "total_te_amo": total,
        "te_amo_by_sender": by_sender
    }


def analyze_conversation_duration(df, threshold_minutes=30):
    """
    Calcula la duración promedio de las conversaciones.
    Una conversación termina cuando hay más de `threshold_minutes` entre mensajes.
    """
    from datetime import timedelta

    df = df.sort_values("timestamp")

    # diferencia entre mensajes
    df["time_diff"] = df["timestamp"].diff()

    # inicio de conversación cuando hay más de X minutos sin mensajes
    threshold = timedelta(minutes=threshold_minutes)
    df["new_conversation"] = (df["time_diff"] > threshold) | (df["time_diff"].isna())

    # asignar ID incremental de conversación
    df["conversation_id"] = df["new_conversation"].cumsum()

    # calcular duración de cada conversación
    conv = df.groupby("conversation_id").agg(
        start=("timestamp", "min"),
        end=("timestamp", "max")
    )

    conv["duration"] = conv["end"] - conv["start"]

    if len(conv) == 0:
        return {
            "average_duration_minutes": 0,
            "conversations_count": 0
        }

    # promedio
    avg_duration = conv["duration"].mean()

    return {
        "average_duration_minutes": avg_duration.total_seconds() / 60,
        "conversations_count": len(conv)
    }
