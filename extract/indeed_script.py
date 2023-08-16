# %%


import pandas as pd
import spacy

from config import API_BASE_URL

df = pd.read_json(f'{API_BASE_URL}/indeed')

# Cleaning data
'''Remove unnecessary columns'''
cleaned_data = df['data']
# %% md
'''Map key value to column'''
cleaned_data = pd.json_normalize(cleaned_data)

## Transformation
'''There is an address on the location, but we need only the country'''


# %%
def detect_location(text):
    """
    :str text containing a country
    :rtype: str
    """
    nlp = spacy.load("en_core_web_sm")
    # Process the text with spaCy
    doc = nlp(text)
    result_list = [ent.text for ent in doc.ents if ent.label_ == "GPE"]
    if len(result_list) > 0:
        return " ".join(result_list)
    return text


cleaned_data['company.processed_location'] = cleaned_data['company.location'].apply(detect_location)

"""Convert relative date to a of format d-m-y"""
from datetime import timedelta, datetime


def parse(date_literal_value: str):
    if not date_literal_value.isalnum():
        result = date_literal_value.split("+")[0]
    else:
        result = date_literal_value
    return result


def convert_relative_date(relative_date: str):
    current_date = datetime.now()
    split_date = relative_date.split()
    if len(split_date) >= 3:
        split_date = split_date[1:]

    if "today" in relative_date.lower():
        estimated_posting_date = current_date
        return estimated_posting_date.strftime("%d-%m-%y")
    if "days" in relative_date:
        # If "days" is present, assume it represents days
        parsed_date = parse(split_date[0])
        days_ago = int(parsed_date)
        estimated_posting_date = current_date - timedelta(days=days_ago)
    elif "months" in relative_date:
        # If "months" is present, assume it represents months
        parsed_date = parse(split_date[0])
        months_ago = int(parsed_date)
        estimated_posting_date = current_date - timedelta(days=months_ago * 30)  # Assuming 30 days in a month
    else:
        return None  # Unable to determine the format

    return estimated_posting_date.strftime("%d-%m-%y")


cleaned_data["posted"] = cleaned_data["posted"].apply(convert_relative_date)

'''Transform salary'''
import re


def format_salary(salary_text: str):
    pattern_with_k = r'\$([\d,]+)K\s*-\s*\$([\d,]+)K'
    pattern_without_k = r'\$([\d,]+)\s*-\s*\$([\d,]+)'

    match = re.search(pattern_with_k, salary_text)
    if match:
        # Because K mean 1000 we need to multiply it by 1000
        lower_salary = int(match.group(1).replace(".", "")) * 1000
        upper_salary = int(match.group(2).replace(".", "")) * 1000
    elif re.search(pattern_without_k, salary_text):
        match = re.search(pattern_without_k, salary_text)
        lower_salary = match.group(1).replace(",", "")
        upper_salary = match.group(2).replace(",", "")
    else:
        return None
    return [lower_salary, upper_salary]


cleaned_data['salary'] = cleaned_data['salary'].apply(format_salary)

# %% md
# Transformation
'''Matching programming language based on the description and the job offer title'''
framework_df = pd.read_csv("../data/framework_list.csv")
language_df = pd.read_csv("../data/programming-languages.csv")
combined = framework_df["Framework Name"].tolist() + language_df["name"].tolist()


def find_matching_languages(text: list[str] | str):
    matching_languages = []
    if type(text) == list:
        for entry in text:
            matching_languages = detect_lib_lang(entry, matching_languages)
    else:
        matching_languages = detect_lib_lang(text, matching_languages)
    return list(set(matching_languages))


def detect_lib_lang(entry, matching_languages):
    for language in combined:
        if len(language) == 1:
            result = [text for text in entry.lower().split(" ") if text.lower() == language.lower()]
            matching_languages = matching_languages + result
            pass
        if language.lower() in entry.lower():
            matching_languages.append(language)
    return matching_languages


cleaned_data["skills"] = cleaned_data['title'].apply(find_matching_languages) + cleaned_data['descriptions'].apply(
    find_matching_languages)
cleaned_data['skills'] = cleaned_data["skills"].apply(lambda x: list(set(x)))
'''Cleaning Drop row where at salary is None'''
cleaned_data.replace("", None, inplace=True)
cleaned_data.dropna(subset=['title'], how='all', inplace=True)
import matplotlib.pyplot as plt


# cleaned_data['salary'].apply(lambda x: (x[0]+x[1])/2)
def process(x):
    if not x:
        return 0
    return (int(x[0]) + int(x[1])) / 2


cleaned_data['salary'] = cleaned_data["salary"].apply(process)
grouped = cleaned_data.sort_values(by="posted").groupby('posted')["salary"].mean()

## Plot
grouped.plot()
plt.plot(grouped['posted'].to_list(), grouped["salary"].to_list())
to_plot = cleaned_data.groupby('company.location')["company.location"].count()
plt.plot(to_plot.get().tolist())
" ".join(cleaned_data['skills'].tolist())
