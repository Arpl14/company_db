import streamlit as st
import pandas as pd
from fuzzywuzzy import process
import Levenshtein  # Ensures fuzzywuzzy uses python-Levenshtein for better performance

# Load the dataset (replace with your new dataset file)
df = pd.read_excel("Combined Data.xlsx")

def fuzzy_filter(df, column, search_term, limit=10):
    """
    Perform fuzzy search on a specific column of the DataFrame.
    """
    if not search_term:
        return df
    matches = process.extract(search_term, df[column], limit=limit)
    matched_indices = [df.index[df[column] == match[0]][0] for match in matches if match[1] > 50]  # Threshold of 50
    return df.loc[matched_indices]

def main():
    st.set_page_config(layout="wide")  # Set the layout to wide
    st.title("Searchable Additive Manufacturing Database")
    
    # Sidebar Filters
    st.sidebar.header("Filters by Column")
    
    # Fuzzy Search Filters for Text Columns
    country_filter = st.sidebar.text_input("Search by Country")
    company_filter = st.sidebar.text_input("Search by Company")
    am_process_filter = st.sidebar.text_input("Search by AM Process Type")
    material_filter = st.sidebar.text_input("Search by Material Type")
    category_filter = st.sidebar.text_input("Search by Category")
    company_type_filter = st.sidebar.text_input("Search by Company Type")
    description_filter = st.sidebar.text_input("Search by Description")
    
    # # Exact Match Filters for Numeric Columns
    # first_sales_filter = st.sidebar.slider(
    #     "Filter by First Sales Year", 
    #     int(df["first_sales"].min()), 
    #     int(df["first_sales"].max()), 
    #     (int(df["first_sales"].min()), int(df["first_sales"].max()))
    # )
    # years_experience_filter = st.sidebar.slider(
    #     "Filter by Years of Experience", 
    #     int(df["years_of_experience"].min()), 
    #     int(df["years_of_experience"].max()), 
    #     (int(df["years_of_experience"].min()), int(df["years_of_experience"].max()))
    # )
    
    # Apply Filters
    filtered_df = df.copy()
    
    # Apply fuzzy filters for text-based columns
    if country_filter:
        filtered_df = fuzzy_filter(filtered_df, "Country", country_filter)
    if company_filter:
        filtered_df = fuzzy_filter(filtered_df, "Company", company_filter)
    if am_process_filter:
        filtered_df = fuzzy_filter(filtered_df, "Type fo AM process", am_process_filter)
    if material_filter:
        filtered_df = fuzzy_filter(filtered_df, "Type of Material", material_filter)
    if category_filter:
        filtered_df = fuzzy_filter(filtered_df, "Category", category_filter)
    if company_type_filter:
        filtered_df = fuzzy_filter(filtered_df, "Type of company", company_type_filter)
    if description_filter:
        filtered_df = fuzzy_filter(filtered_df, "Description", description_filter)
    
    # # Apply numeric filters
    # filtered_df = filtered_df[
    #     (filtered_df["first_sales"] >= first_sales_filter[0]) & 
    #     (filtered_df["first_sales"] <= first_sales_filter[1])
    # ]
    # filtered_df = filtered_df[
    #     (filtered_df["years_of_experience"] >= years_experience_filter[0]) & 
    #     (filtered_df["years_of_experience"] <= years_experience_filter[1])
    # ]
    
    # Display Results
    st.subheader("Filtered Results")
    st.dataframe(filtered_df, use_container_width=True)

if __name__ == "__main__":
    main()
