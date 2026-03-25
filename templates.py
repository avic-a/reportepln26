TEMPLATES = {
    "corte": [
        ("title", "{titulo}"),
        ("text", "{fecha}"),
        ("text", "Menciones: {menciones}"),

        ("subtitle", "Líneas de discusión"),
        ("arrow_list", "{lineas}"),

        # 👇 dinámico
        ("subtitle", "{citas_titulo}"),
        ("text", "{citas_desc}"),
        ("quote_list", "{citas}"),

        ("subtitle", "{autores_titulo}"),
        ("text", "{autores_desc}"),
        ("author_list", "{autores}")
    ]
}
