'''
Tests for chatbot class only
- tests aspects of the chatbot class that do not require a populated knowledge base
- note:  db is required to instantiate chatbot class
'''
import logging
from db.chatbot.chatbot_class import Chatbot

def test_instantiate_chatbot_class(test_db):
    chatbot = Chatbot('12345', test_db)
    logging.info(f'type(pipe), {type(chatbot).__name__} {isinstance(chatbot, Chatbot)}')
    assert type(chatbot).__name__ == 'Chatbot'

def test_get_default_prompt():
    template = Chatbot.get_default_prompt()
    logging.info(f'get_default_prompt template : {template}')
    assert "{context_str}" in template
    assert "{query_str}" in template
    assert "Context information is below" in template
    assert "Given the context information and not prior knowledge, answer the query." in template
