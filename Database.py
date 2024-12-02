import streamlit as st
import pandas as pd

# Load the dataset
@st.cache_data  # Correct caching decorator
def load_data():
    return pd.read_excel("Combined Data.xlsx")

def filter_dataframe(df, column, search_term):
    """
    Filters the DataFrame for rows where the specified column contains the search term.
    Automatically handles numeric and string columns.
    """
    if not search_term:
        return df

    # Check if the column is numeric
    if pd.api.types.is_numeric_dtype(df[column]):
        # Convert the search term to a number (if necessary)
        return df[df[column].astype(str).str.contains(str(search_term), na=False)]
    else:
        # For string columns, use the str.contains() method
        return df[df[column].str.contains(search_term, case=False, na=False)]

def main():
    st.set_page_config(layout="wide")  # Set the layout to wide
    st.title("Searchable Database")
    
    # Load data
    df = load_data()

    # Dynamically check if the "Year" column exists and process it only if it does
    if "Year" in df.columns:
        df["Year"] = df["Year"].astype(str)  # Convert Year to string, if necessary

    # Create sidebar for search inputs
    st.sidebar.header("Search Filters")
    
    # Create a search box for each column dynamically
    search_terms = {}
    for column in df.columns:
        search_terms[column] = st.sidebar.text_input(f"Search by {column}", "")
    
    # Apply filters
    filtered_df = df.copy()

    for column, search_term in search_terms.items():
        if search_term:  # Only apply filter if there's a search term
            filtered_df = filter_dataframe(filtered_df, column, search_term)
    
    # Display filtered results
    st.subheader("Filtered Results")
    st.dataframe(filtered_df, use_container_width=True)

if __name__ == "__main__":
    main()
