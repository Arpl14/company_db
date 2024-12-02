import pandas as pd

# Load the dataset
def load_data():
    # Load the Excel file
    df = pd.read_excel("final_st_data.xlsx")
    
    # Ensure correct column names
    df.columns = ['Country', 'Company', 'Type_of_AM process', 'Type_of_Material', 
                  'Category', 'First_sales', 'Years_of_Experience', 'Company_type', 
                  'Description']
    return df

# Function to filter the DataFrame based on search criteria
def search_data(df, search_criteria):
    """
    Filters the DataFrame based on a dictionary of search criteria.
    
    Parameters:
        df (DataFrame): The dataset to filter.
        search_criteria (dict): A dictionary where keys are column names and values are search terms.
        
    Returns:
        DataFrame: Filtered DataFrame.
    """
    filtered_df = df.copy()
    for column, term in search_criteria.items():
        if term:  # Only apply the filter if a search term is provided
            filtered_df = filtered_df[filtered_df[column].astype(str).str.contains(term, case=False, na=False)]
    return filtered_df

# Main logic for creating the searchable database
def main():
    # Load data
    df = load_data()
    
    # Display all available columns
    print("Available Columns for Search:")
    print(df.columns.tolist())
    
    # User input for search criteria
    print("\nEnter search terms for the following fields (press Enter to skip a field):")
    search_criteria = {}
    for column in df.columns:
        term = input(f"Search term for {column}: ").strip()
        search_criteria[column] = term if term else None
    
    # Filter the data
    filtered_df = search_data(df, search_criteria)
    
    # Display results
    print("\nFiltered Results:")
    if not filtered_df.empty:
        print(filtered_df)
    else:
        print("No results match your search criteria.")

if __name__ == "__main__":
    main()
