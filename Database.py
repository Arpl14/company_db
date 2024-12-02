import streamlit as st
import pandas as pd
from fuzzywuzzy import process
import Levenshtein  # Ensures fuzzywuzzy uses python-Levenshtein for better performance

# Load the dataset
df = pd.read_excel("Combined Data.xlsx")

def fuzzy_filter(df, column, search_term, limit=10, threshold=50):
    """
    Perform fuzzy search on a specific column of the DataFrame.
    Args:
        df (pd.DataFrame): DataFrame to filter.
        column (str): Column to apply the fuzzy search on.
        search_term (str): Term to search for.
        limit (int): Max number of results to return.
        threshold (int): Minimum similarity score to include matches.
    Returns:
        pd.DataFrame: Filtered DataFrame.
    """
    if not search_term:
        return df
    if column not in df.columns:
        st.warning(f"Column '{column}' not found in the dataset.")
        return df
    matches = process.extract(search_term, df[column].dropna().astype(str), limit=limit)
    matched_indices = [df.index[df[column] == match[0]][0] for match in matches if match[1] >= threshold]
    return df.loc[matched_indices]

def main():
    st.set_page_config(layout="wide")  # Set layout to wide
    st.title("Searchable Additive Manufacturing Database")
    
    # Sidebar Filters
    st.sidebar.header("Filters by Column")
    
    # Data Preview Option
    if st.sidebar.checkbox("Show Dataset Preview"):
        st.write("Preview of the Dataset:")
        st.dataframe(df.head(), use_container_width=True)
    
    # Fuzzy Search Filters for Text Columns
    country_filter = st.sidebar.text_input("Search by Country")
    company_filter = st.sidebar.text_input("Search by Company")
    am_process_filter = st.sidebar.text_input("Search by AM Process Type")
    material_filter = st.sidebar.text_input("Search by Material Type")
    category_filter = st.sidebar.text_input("Search by Category")
    company_type_filter = st.sidebar.text_input("Search by Company Type")
    description_filter = st.sidebar.text_input("Search by Description")
    
    # Threshold Control for Fuzzy Search
    threshold = st.sidebar.slider("Fuzzy Match Threshold", 0, 100, 50, 5)
    
    # Apply Filters
    filtered_df = df.copy()
    
    if country_filter:
        filtered_df = fuzzy_filter(filtered_df, "Country", country_filter, threshold=threshold)
    if company_filter:
        filtered_df = fuzzy_filter(filtered_df, "Company", company_filter, threshold=threshold)
    if am_process_filter:
        filtered_df = fuzzy_filter(filtered_df, "Type fo AM process", am_process_filter, threshold=threshold)
    if material_filter:
        filtered_df = fuzzy_filter(filtered_df, "Type of Material", material_filter, threshold=threshold)
    if category_filter:
        filtered_df = fuzzy_filter(filtered_df, "Category", category_filter, threshold=threshold)
    if company_type_filter:
        filtered_df = fuzzy_filter(filtered_df, "Type of company", company_type_filter, threshold=threshold)
    if description_filter:
        filtered_df = fuzzy_filter(filtered_df, "Description", description_filter, threshold=threshold)
    
    # Display Results
    st.subheader("Filtered Results")
    if filtered_df.empty:
        st.warning("No results match your search criteria.")
    else:
        st.dataframe(filtered_df, use_container_width=True)

if __name__ == "__main__":
    main()
