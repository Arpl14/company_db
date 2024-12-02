import streamlit as st
import pandas as pd
from fuzzywuzzy import process
import Levenshtein  # Ensures fuzzywuzzy uses python-Levenshtein for better performance

# Function to load and preprocess the dataset
@st.cache_data
def load_data():
    # Load the Excel file
    df = pd.read_excel("final_st_data.xlsx")
    
    # Rename duplicate columns by appending a suffix
    df.columns = pd.io.parsers.ParserBase({'names': df.columns})._maybe_dedup_names(df.columns)
    
    # Log the updated column names for debugging
    st.write("Column Names After Deduplication:", df.columns.tolist())
    return df

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
    
    # Load and preprocess the dataset
    df = load_data()

    # Sidebar Filters
    st.sidebar.header("Filters by Column")
    
    # Fuzzy Search Filters for Text Columns
    country_filter = st.sidebar.text_input("Search by Country")
    company_filter = st.sidebar.text_input("Search by Company")
    am_process_filter = st.sidebar.text_input("Search by AM Process Type")
    material_filter = st.sidebar.text_input("Search by Material Type")
    category_filter = st.sidebar.text_input("Search by Category (Primary)")
    company_type_filter = st.sidebar.text_input("Search by Category (Type of Company)")
    description_filter = st.sidebar.text_input("Search by Description")
    
    # Apply Filters
    filtered_df = df.copy()
    
    # Apply fuzzy filters for text-based columns
    if country_filter:
        filtered_df = fuzzy_filter(filtered_df, "Country", country_filter)
    if company_filter:
        filtered_df = fuzzy_filter(filtered_df, "Company", company_filter)
    if am_process_filter:
        filtered_df = fuzzy_filter(filtered_df, "Type of AM process", am_process_filter)
    if material_filter:
        filtered_df = fuzzy_filter(filtered_df, "Type of Material", material_filter)
    if category_filter:
        filtered_df = fuzzy_filter(filtered_df, "Category", category_filter)  # First "Category"
    if company_type_filter:
        filtered_df = fuzzy_filter(filtered_df, "Category.1", company_type_filter)  # Second "Category"
    if description_filter:
        filtered_df = fuzzy_filter(filtered_df, "Description", description_filter)
    
    # Display Results
    st.subheader("Filtered Results")
    st.dataframe(filtered_df, use_container_width=True)

if __name__ == "__main__":
    main()
