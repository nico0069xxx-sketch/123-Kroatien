with open('main/context_processors.py', 'r') as f:
    content = f.read()

# Füge Chatbot-Übersetzungen vor "return context" ein
old_return = "    return context"
new_code = '''    # Chatbot-Übersetzungen immer laden (für alle Seiten)
    chatbot_translations = Translation.objects.filter(page='chatbot')
    for t in chatbot_translations:
        if user_language == 'en': context[t.name] = t.english_content
        elif user_language == 'hr': context[t.name] = t.croatian_content
        elif user_language == 'fr': context[t.name] = t.french_content
        elif user_language == 'gr': context[t.name] = t.greek_content
        elif user_language == 'pl': context[t.name] = t.polish_content
        elif user_language == 'cz': context[t.name] = t.czech_content
        elif user_language == 'ru': context[t.name] = t.russian_content
        elif user_language == 'sw': context[t.name] = t.swedish_content
        elif user_language == 'no': context[t.name] = t.norway_content
        elif user_language == 'sk': context[t.name] = t.slovak_content
        elif user_language == 'nl': context[t.name] = t.dutch_content
        else: context[t.name] = t.german_content

    return context'''

content = content.replace(old_return, new_code)

with open('main/context_processors.py', 'w') as f:
    f.write(content)

print('Chatbot-Übersetzungen hinzugefügt!')
