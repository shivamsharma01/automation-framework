
import spacy
from fuzzywuzzy import fuzz
from sklearn.metrics.pairwise import cosine_similarity
from exact_keyword import check_keyword_in_response
from selenium_driver import DriverManager

nlp = spacy.load('en_core_web_md')

def assert_rows(input_data):
    driver_manager = DriverManager()
    asserted_input_data = [assert_row(question, expected, keyword) for question, expected, keyword in input_data]
    driver_manager.close()
    return asserted_input_data

def assert_row(question, expected, keyword, driver_manager=None):
    def get_response(driver_manager, question):
        return driver_manager.get_question_response(question)

    def fuzzy_matching_score(response, expected_answer):
        return fuzz.ratio(response, expected_answer)

    def cosine_similarity_spacy_score(response, expected_answer):
        doc1, doc2 = nlp(expected_answer), nlp(response)
        cosine_sim = cosine_similarity([doc1.vector], [doc2.vector])
        return cosine_sim[0][0].item()*100
    
    def bool_to_string(token, error_string):
        if token == True:
            token = 'True'
        elif token == False:
            token = 'False'
        else:
            token = error_string
        return token

    is_external_driver = True
    if driver_manager == None:
        driver_manager = DriverManager()
        is_external_driver = False

    response = get_response(driver_manager, question)
    assertion_1_using_fuzzy = fuzzy_matching_score(response, expected)
    assertion_1_using_text_embedding = cosine_similarity_spacy_score(response, expected)
    
    is_keyword_present_llm = check_keyword_in_response(response, keyword)
    is_keyword_present_llm = bool_to_string(is_keyword_present_llm, 'Assertion 2 failed (LLM)')
    
    is_keyword_present_contains = keyword.lower() in response.lower() 
    is_keyword_present_contains = bool_to_string(is_keyword_present_contains, 'Assertion 2 failed (contains)')

    asserted_row = [question, expected, response, keyword, assertion_1_using_fuzzy, assertion_1_using_text_embedding, is_keyword_present_llm, is_keyword_present_contains]

    if is_external_driver == False:
        driver_manager.close()
    
    return asserted_row
