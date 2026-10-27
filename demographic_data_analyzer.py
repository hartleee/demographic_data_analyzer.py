import pandas as pd
import numpy as np


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('adult.data.csv')

    # print(df.shape)

    # DATA CLEANING - Missing Values
        # print(df.isna().sum())
        # print(df.info())

    # DATA CLEANING - Not Valid Values
    # Look at values
    # for col in df.columns:
    #     print(f"--- Value Counts for {col} ---")
    #     print(df[col].value_counts())
    #     print("\n")
    # Replace question marks
    df_cleaned = df.replace({'occupation': '?', 'native-country': '?'}, np.nan, inplace=True)

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df_cleaned['race'].value_counts()

    # What is the average age of men?
    average_age_men = df_cleaned.loc[df_cleaned['sex'] == 'Male', 'age'].mean().round(1)

    # What is the percentage of people who have a Bachelor's degree?
    percentage_bachelors = round(((len(df_cleaned.loc[df['education'] == 'Bachelors']) / len(df_cleaned['education'])) * 100),1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education = df_cleaned.loc[(df_cleaned['education'] == 'Bachelors') | (df_cleaned['education'] == 'Masters') | (df_cleaned['education'] == 'Doctorate')]
    lower_education = df_cleaned.loc[~((df_cleaned['education'] == 'Bachelors') | (df_cleaned['education'] == 'Masters') | (df_cleaned['education'] == 'Doctorate'))]

    # percentage with salary >50K
    higher_education_rich = round(((len(higher_education.loc[higher_education['salary'] == '>50K']) / len(higher_education)) * 100),1)
    lower_education_rich = round(((len(lower_education.loc[lower_education['salary'] == '>50K']) / len(lower_education)) * 100),1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df_cleaned['hours-per-week'].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    num_min_workers = len(df_cleaned[(df_cleaned['hours-per-week'] == df_cleaned['hours-per-week'].min())])
    rich_percentage = (len(df_cleaned[(df_cleaned['hours-per-week'] == df_cleaned['hours-per-week'].min()) & (df_cleaned['salary'] == '>50K')]) / len(df_cleaned[df_cleaned['hours-per-week'] == df_cleaned['hours-per-week'].min()])) * 100

    # What country has the highest percentage of people that earn >50K?
    
    # add is_high_salary column (0 or 1)
    df_cleaned['is_high_salary'] = (df_cleaned['salary'] == '>50K').astype(int)

    # get df > gorup by country > mean of is_high_salary (% of >50K) > index max 
    highest_earning_country = df_cleaned.groupby('native-country')['is_high_salary'].mean().idxmax()

    # get df > group by country > take is_high_salary mean (% of >50K) > return max value
    highest_earning_country_percentage = round(((df_cleaned.groupby('native-country')['is_high_salary'].mean().max()) * 100),1)

    # Identify the most popular occupation for those who earn >50K in India.
    # df > for >50K in India > group by occupation > count occupation > index max
    top_IN_occupation = df_cleaned[(df_cleaned['salary'] == '>50K') & (df_cleaned['native-country'] == 'India')].groupby('occupation')['occupation'].count().idxmax()

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }