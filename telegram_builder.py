import requests
import re
import html

# =========================
# TELEGRAM SEND
# =========================
def send_to_telegram(text, token, chat_id):
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
        "disable_web_page_preview": True 
    }

    response = requests.post(url, json=payload)
    return response.json()

def parse_custom_links(text):
    parts = text.split("|")

    for part in parts:
        part = part.strip()

        if " - " in part:
            fragment, url = part.split(" - ", 1)
            fragment = fragment.strip()
            url = url.strip()

            link_html = f"<a href='{url}'>{html.escape(fragment)}</a>"

            # reemplaza solo la primera coincidencia
            text = re.sub(re.escape(fragment), link_html, text, count=1)

    return text
# =========================
# BASE BLOCK
# =========================
class Block:
    def render(self):
        raise NotImplementedError


# =========================
# TEXT BLOCKS
# =========================
class Title(Block):
    def __init__(self, text):
        self.text = html.escape(text)

    def render(self):
        return f"<b>{self.text}</b>\n"


class Subtitle(Block):
    def __init__(self, text):
        self.text = html.escape(text)

    def render(self):
        return f"<i>{self.text}</i>\n"


class TextBlock(Block):
    def __init__(self, text):
        self.text = html.escape(text)

    def render(self):
        return f"{self.text}\n"


# =========================
# LISTS
# =========================
class BulletList(Block):
    def __init__(self, items):
        self.items = items

    def render(self):
        return "\n".join([
            f"- {html.escape(str(item))}" for item in self.items
        ]) + "\n"


class ArrowList(Block):
    def __init__(self, items):
        self.items = items

    def render(self):
        return "\n\n".join([
            f"→ {html.escape(str(item))}" for item in self.items
        ]) + "\n"


# =========================
# AUTHORS
# =========================
class AuthorList(Block):
    def __init__(self, authors):
        self.authors = authors

    def render(self):
        output = []

        for a in self.authors:
            name = html.escape(a.get("name", ""))
            url = a.get("url", "")
            desc = html.escape(a.get("desc", ""))

            if url:
                linea = f"• <a href='{url}'>{name}</a>"
            else:
                linea = f"• {name}"

            if desc:
                linea += f" - {desc}"

            output.append(linea)

        return "\n".join(output) + "\n"


# =========================
# QUOTES
# =========================
class QuoteBlock(Block):
    def __init__(self, text):
        self.text = html.escape(text)

    def render(self):
        return f"<i>“{self.text}”</i>\n"


class QuoteList(Block):
    def __init__(self, quotes):
        self.quotes = quotes

    def render(self):
        output = []

        for q in self.quotes:
            if isinstance(q, dict):
                texto = html.escape(q.get("text", ""))
                url = q.get("url", "")

                if url:
                    output.append(f"- <a href='{url}'>{texto}</a>")
                else:
                    output.append(f"- {texto}")
            else:
                output.append(f"• {html.escape(str(q))}")

        return "\n".join(output) + "\n"


# =========================
# MESSAGE BUILDER
# =========================
class TelegramMessage:
    def __init__(self):
        self.blocks = []

    def add(self, block):
        self.blocks.append(block)

    def render(self):
        return "\n".join(block.render() for block in self.blocks)


# =========================
# TEMPLATE ENGINE
# =========================
def build_from_template(template_name, data, templates):
    msg = TelegramMessage()
    template = templates[template_name]

    for i, (block_type, content) in enumerate(template):

        # =========================
        # Resolver contenido
        # =========================
        if isinstance(content, str) and content.startswith("{") and content.endswith("}"):
            key = content[1:-1]
            content = data.get(key, [])

        elif isinstance(content, str):
            content = content.format(**data)

        # =========================
        # 🔥 Saltar bloques vacíos
        # =========================
        if block_type in ["arrow_list", "bullet_list", "quote_list", "author_list"] and not content:
            continue

        # =========================
        # 🔥 Saltar subtítulo si lo siguiente está vacío
        # =========================
        if block_type == "subtitle":
            if i + 1 < len(template):
                next_block_type, next_content = template[i + 1]

                if isinstance(next_content, str) and next_content.startswith("{"):
                    key = next_content[1:-1]
                    if not data.get(key):
                        continue

        # =========================
        # Render blocks (AHORA sí)
        # =========================
        if block_type == "title":
            msg.add(Title(content))

        elif block_type == "text":
            msg.add(TextBlock(content))

        elif block_type == "subtitle":
            msg.add(Subtitle(content))

        elif block_type == "bullet_list":
            msg.add(BulletList(content))

        elif block_type == "arrow_list":
            msg.add(ArrowList(content))

        elif block_type == "author_list":
            msg.add(AuthorList(content))

        elif block_type == "quote_list":
            msg.add(QuoteList(content))

        elif block_type == "quote":
            msg.add(QuoteBlock(content))

    return msg.render()

# =========================
# SPLIT TELEGRAM
# =========================
def split_message(text, limit=4000):
    parts = []
    while len(text) > limit:
        split_index = text.rfind("\n", 0, limit)
        if split_index == -1:
            split_index = limit
        parts.append(text[:split_index])
        text = text[split_index:]
    parts.append(text)
    return parts
