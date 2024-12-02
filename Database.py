import streamlit as st
import pandas as pd

# Function to load and preprocess the dataset
@st.cache_data
def load_data():
    # Load the Excel file
    df = pd.read_excel("final_st_data.xlsx")
    
    # Ensure correct column names
    df.columns = ['Country', 'Company', 'Type_of_AM process', 'Type_of_Material', 
                  'Category', 'First_sales', 'Years_of_Experience', 'Company_type', 
                  'Description']
    
    return df

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
    st.title("Searchable Additive Manufacturing Database")
    
    # Load dataset
    df = load_data()

    # Sidebar Filters
    st.sidebar.header("Search Filters")
    
    # Exclude filters for 'First_sales' and 'Years_of_Experience'
    columns_to_filter = [col for col in df.columns if col not in ['First_sales', 'Years_of_Experience']]
    
    # Create a search box for each column dynamically
    search_terms = {}
    for column in columns_to_filter:
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
