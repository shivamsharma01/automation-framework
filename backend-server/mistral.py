
import spacy
from fuzzywuzzy import fuzz
from sklearn.metrics.pairwise import cosine_similarity
from exact_keyword import check_keyword_in_response
from selenium_driver import DriverManager
from db import get_db
from tinydb import Query

nlp = spacy.load('en_core_web_md')

def assert_rows(input_data, filename):
    '''
    Input:
    input_data: all the input rows containing question, response and keyword
    filename: filename containing these questions. This filename is used to update its progress in db
    Output:
    asserted_data: responses to all the input rows containing question, response, actual response, keywords, fuzzy score,
    spacy text-embeddings score, expected data validation using contains and together api prompt
    '''
    driver_manager = DriverManager()
    num_rows = len(input_data)
    asserted_input_data = []
    DB = get_db()
    for i in range(num_rows):
        question, expected, keyword = input_data[i]
        asserted_input_data.append(assert_row(question, expected, keyword))
        DB.update({'percent': int(float(((i+1)*100)/num_rows))}, Query().id == filename)
            
    driver_manager.close()
    return asserted_input_data

def assert_row(question, expected, keyword, driver_manager=None):
    '''
    Input:
    question: input question to pass to the mistral chat
    expected: the expected response
    keyword: key token present in the response
    driver_manager: driver_manager to fire the question to for the actual response
    Output:
    asserted_row: response to the input row containing question, response, actual response, keywords, fuzzy score,
    spacy text-embeddings score, expected data validation using contains and together api prompt
    '''
    def get_response(driver_manager, question):
        return driver_manager.get_question_response(question)

    def fuzzy_matching_score(response, expected_answer):
        '''
        Input:
        response: the response returned by mistral
        expected_answer: the response present in the input file
        Output:
        score: the score between response and expected_answer based on the fuzzy logic
        '''
        return fuzz.ratio(response, expected_answer)

    def cosine_similarity_spacy_score(response, expected_answer):
        '''
        Input:
        response: the response returned by mistral
        expected_answer: the response present in the input file
        Output:
        score: the score between response and expected_answer based on the text-embeddings of en_core_web_md model
        '''
        doc1, doc2 = nlp(expected_answer), nlp(response)
        cosine_sim = cosine_similarity([doc1.vector], [doc2.vector])
        return cosine_sim[0][0].item()*100
    
    def bool_to_string(token, error_string):
        '''
        Input:
        token: boolean response or string
        Output:
        token: boolean to string conversion if possible or else a custom error msg
        '''
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
