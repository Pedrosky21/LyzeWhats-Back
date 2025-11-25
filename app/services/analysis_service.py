def analyze_chat(messages):
    from app.services.dataframe_builder import messages_to_dataframe
    from app.services.extra_analysis import (
        analyze_conversation_starters,
        analyze_saludos,
        analyze_te_amo,
        analyze_conversation_duration,
        analyze_top_phrases
    )
    from app.utils.normalize_types import normalize
    from app.utils.normalize_text import normalize_text

    df = messages_to_dataframe(messages)
    # Si no hay mensajes, devolver error
    if df.empty:
        return {"error": "No messages"}

    # Reemplazar la columna original por la normalizada
    df["text"] = df["text"].apply(normalize_text)

    # --- ANÁLISIS BÁSICOS ---
    messages_by_sender = df["sender"].value_counts().to_dict()

    if df["emojis"].apply(len).sum() > 0:
        exploded = df.explode("emojis")
        top_emoji = exploded["emojis"].value_counts().head(5).to_dict()
    else:
        top_emoji = {}

    # --- ANÁLISIS EXTRA ---
    conversation_starts = analyze_conversation_starters(df)
    saludos = analyze_saludos(df)
    te_amo = analyze_te_amo(df)
    conversation_duration = analyze_conversation_duration(df)
    top_phrases = analyze_top_phrases(df)

    result = {
        "messages_by_sender": messages_by_sender,
        "top_emoji": top_emoji,
        "conversation_starts": conversation_starts,
        "saludos": saludos,
        "te_amo": te_amo,
        "conversation_duration": conversation_duration,
        "top_phrases": top_phrases  
    }

    return normalize(result)