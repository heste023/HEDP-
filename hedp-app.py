import streamlit as st
import pandas as pd
import numpy as np

# Load the data
@st.cache
def load_data():
    data = pd.read_csv('hedp-datafile.csv')
    return data

# Function to format data based on column name
def format_data(df):
    for column in df.columns:
        if "percent" in column.lower():
            df[column] = df[column].apply(lambda x: "{:.2f}%".format(float(x)) if pd.notnull(x) and x != ' ' else '')
        elif ("revenue" in column.lower() or "expenses" in column.lower()) and "percent" not in column.lower():
            df[column] = df[column].apply(lambda x: "${:,.2f}".format(float(x)) if pd.notnull(x) and x != ' ' else '')
    return df



def get_institution_index(institutions, institution_name):
    institutions_list = list(institutions)
    indices = [i for i, x in enumerate(institutions_list) if x == institution_name]
    if len(indices) > 0:
        return indices[0]
    else:
        st.error(f"Institution {institution_name} not found in the dataset.")
        return 0  # default to the first institution if the desired institution is not found

# The main function where we will build the actual app
def main():
    st.title('Higher Ed Decision Pointer')

    # Add sidebar
    st.sidebar.title('Categories')
    category = st.sidebar.selectbox('Select a category:', 
                                    ['', 'Funding', 
                                    'Academic Reputation',
                                    'Research and Innovation',
                                    'Student Recruitment',
                                    'Faculty Recruitment',
                                    'Sports and Athletics',
                                    'Endowment Size',
                                    'Student Outcomes',
                                    'Facilities and Infrastructure',
                                    'Program Diversity',
                                    'Sustainability Initiatives'])
    
    if category == 'Funding':
        # Load the dataset
        data = load_data()

        # Get the list of institutions from the dataset
        institutions = data['Institution name'].unique()
        
        first_institution_index = get_institution_index(institutions, 'The University of Alabama')
        second_institution_index = get_institution_index(institutions, 'University of Alabama at Birmingham')
        third_institution_index = get_institution_index(institutions, 'University of Alabama in Huntsville')
        
        institution_1 = st.selectbox('Select first Institution:', institutions, index=first_institution_index)
        institution_2 = st.selectbox('Select second Institution:', institutions, index=second_institution_index)
        institution_3 = st.selectbox('Select third Institution:', institutions, index=third_institution_index)

        if st.button('Compare'):
            # Filter the data for the selected institutions and apply formatting
            data_1 = format_data(data[data['Institution name'] == institution_1])
            data_2 = format_data(data[data['Institution name'] == institution_2])
            data_3 = format_data(data[data['Institution name'] == institution_3])

            # Transpose data after formatting
            data_1 = data_1.T
            data_2 = data_2.T
            data_3 = data_3.T

            # Prepare the comparison dataframe
            comparison_df = pd.concat([data_1, data_2, data_3], axis=1)
            comparison_df.columns = [institution_1, institution_2, institution_3]

            # Display the comparison dataframe
            st.dataframe(comparison_df)

# Run the app
if __name__ == '__main__':
    main()
