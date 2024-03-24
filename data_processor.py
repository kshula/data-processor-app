import streamlit as st
import pandas as pd

class DataProcessor:
    def __init__(self, file_path):
        self.file_path = file_path

    def extract(self):
        try:
            # Load CSV file into a pandas DataFrame
            df = pd.read_csv(self.file_path)
            return df
        except FileNotFoundError:
            st.error("File not found.")
            return None
        except Exception as e:
            st.error("An error occurred during extraction: {}".format(e))
            return None

    def transform(self, df):
        try:
            # Drop rows with null values
            df_transformed = df.dropna()
            return df_transformed
        except Exception as e:
            st.error("An error occurred during transformation: {}".format(e))
            return None

    def filter_data(self, df, column, threshold):
        try:
            # Filter data based on user-specified conditions
            filtered_df = df[df[column] >= threshold]
            return filtered_df
        except Exception as e:
            st.error("An error occurred during data filtering: {}".format(e))
            return None

def home():
    st.title("Data Processor App")
    st.write("This is a Streamlit app for data processing.")
    st.write("Upload a CSV file to get started.")

def data_view(df):
    st.title("Data View")
    if df is not None:
        # Display head and tail of the DataFrame
        st.write("Head of DataFrame:")
        st.write(df.head())
        st.write("Tail of DataFrame:")
        st.write(df.tail())

        # Compute and display data summary statistics
        st.write("Summary Statistics:")
        st.write(df.describe())
    else:
        st.warning("No data available to display.")

def data_filtering(df):
    st.title("Data Filtering")
    if df is not None:
        st.write("Original DataFrame:")
        st.write(df)

        # Allow user to specify filtering criteria
        column = st.selectbox("Select column for filtering:", df.columns)
        threshold = st.number_input("Enter threshold value:", min_value=float(df[column].min()), max_value=float(df[column].max()), step=0.01)

        # Filter data based on user-specified conditions
        filtered_data = DataProcessor.filter_data(df, column, threshold)

        if filtered_data is not None:
            st.write("Filtered DataFrame:")
            st.write(filtered_data)
        else:
            st.warning("No data available after filtering.")
    else:
        st.warning("No data available to filter.")

def main():
    st.set_page_config(page_title="Data Processor App", layout="wide")

    # File path of the CSV file
    file_path = st.sidebar.file_uploader("Upload CSV file", type=["csv"])

    # Create an instance of DataProcessor
    data_processor = DataProcessor(file_path)

    # Sidebar navigation
    page = st.sidebar.radio("Navigation", ["Home", "Data View", "Data Filtering"])

    if page == "Home":
        home()
    elif page == "Data View":
        if file_path is not None:
            # Extract data from the CSV file
            df = data_processor.extract()
            # Transform the DataFrame
            df_transformed = data_processor.transform(df)
            # Display data view page
            data_view(df_transformed)
        else:
            st.warning("Please upload a CSV file.")
    elif page == "Data Filtering":
        if file_path is not None:
            # Extract data from the CSV file
            df = data_processor.extract()
            # Display data filtering page
            data_filtering(df)
        else:
            st.warning("Please upload a CSV file.")

if __name__ == "__main__":
    main()
