def generate_references(chunks: list[dict], style: str = "APA") -> list[str]:
    seen = set()
    references = []

    for chunk in chunks:
        key = (chunk["source_doc_id"], chunk["journal"], chunk["publish_year"])
        if key in seen:
            continue
        seen.add(key)

        journal = chunk["journal"]
        year = chunk["publish_year"]
        title = chunk["source_doc_id"].replace("_", " ").replace(".pdf", "").title()

        if style == "APA":
            ref = f"{journal} ({year}). *{title}*. Internal document."
        elif style == "MLA":
            ref = f"{journal}. \"{title}.\" {year}. Internal document."
        elif style == "Chicago":
            ref = f"{journal}. *{title}*. {year}. Internal document."
        else:
            ref = f"{journal} ({year}). *{title}*."

        references.append(ref)

    return references
