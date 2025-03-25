import spacy
from db import get_db
from tinydb import Query
# from rapidfuzz import process, fuzz

nlp = spacy.load("en_core_web_md")

def find_grant_by_id(grant_id):
    DB = get_db()
    rows = DB.search(Query().id == grant_id)
    return rows[0] if rows else None

def find_best_matches_for_eligibility_list(input_list):
    DB = get_db()
    grants = DB.all()
    choices = set(eligibility for grant in grants for eligibility in grant["eligibility"])
    
    def find_best_matches_for_eligibility(input):
        input_doc = nlp(input.lower())
        similar_eligibilities = {choice.lower() for choice in choices if input_doc.similarity(nlp(choice.lower())) > 0.6}
        # choices_using_fuzzy = process.extract(input, choices, scorer=fuzz.partial_ratio, limit=5)
        # similar_eligibilities.update(choice[0].lower() for choice in choices_using_fuzzy)
        return similar_eligibilities
    
    input_list = [x.lower() for x in input_list]
    if "all" in input_list or "any" in input_list:
        return None
    
    result_set = set()
    for input_category in input_list:
        result_set.update(find_best_matches_for_eligibility(input_category))
    
    return result_set

def find_best_matches_for_category_list(input_list):
    DB = get_db()
    grants = DB.all()
    choices = set([grant["category"] for grant in grants])
    
    def find_best_matches_for_category(input):
        input_doc = nlp(input.lower())
        similar_categories = {choice.lower() for choice in choices if input_doc.similarity(nlp(choice.lower())) > 0.6}
        # choices_using_fuzzy = process.extract(input, choices, scorer=fuzz.partial_ratio, limit=5)
        # similar_categories.update(choice[0].lower() for choice in choices_using_fuzzy)
        return similar_categories
    
    input_list = [x.lower() for x in input_list]
    if "all" in input_list or "any" in input_list:
        return None
    
    result_set = set()
    for input_category in input_list:
        result_set.update(find_best_matches_for_category(input_category))
    
    return result_set

def find_best_matches_for_grants(categories, eligibilities):
    DB = get_db()
    grants = DB.all()
    db_categories = find_best_matches_for_category_list(categories)
    db_eligibilities = find_best_matches_for_eligibility_list(eligibilities)
    if db_categories is not None:
        grants = [grant for grant in grants if grant["category"].lower() in db_categories]
    if db_eligibilities is not None:
        grants = [grant for grant in grants if any(elig.lower() in db_eligibilities for elig in grant["eligibility"])]
    return grants
