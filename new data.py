import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder

# =================================================================
# STEP 1: Load and Combine All Sheets with Consistent Column Names
# =================================================================

def load_and_combine_sheets(file_path):
    years = ['2021', '2020', '2019', '2018', '2016']
    dfs = []
    
    # Column name mapping for consistency across years
    column_mapping = {
        'Cases Pending Investigation from Previous Year': 'feature1',
        'Cases Reported during the year': 'feature2',
        'Cases Reopened for Investigation': 'feature3',
        'Total Cases for Investigation': 'feature4',
        'Crime Head': 'target'
    }

    for year in years:
        try:
            df = pd.read_excel(file_path, sheet_name=year)
            
            # Standardize column names
            df.columns = df.columns.str.replace(r'\n|\(.*?\)|-', ' ', regex=True).str.strip()
            df.rename(columns=lambda x: x.split('(')[0].strip() if '(' in x else x, inplace=True)
            df.rename(columns=column_mapping, inplace=True)
            
            # Add year column
            df['Year'] = int(year)
            dfs.append(df)
            
        except Exception as e:
            print(f"Error processing {year}: {str(e)}")
            continue

    return pd.concat(dfs, ignore_index=True)

# =================================================================
# STEP 2: Data Cleaning and Preprocessing
# =================================================================

def clean_and_preprocess(df):
    # Handle missing values
    for col in df.select_dtypes(include=[np.number]).columns:
        df[col] = df[col].fillna(df[col].median())
    
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].fillna('Unknown')
    
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Filter and keep only essential columns
    essential_cols = ['feature1', 'feature2', 'feature3', 'feature4', 'target', 'Year']
    df = df[essential_cols].copy()
    
    # Remove non-numeric characters from numeric columns
    for col in ['feature1', 'feature2', 'feature3', 'feature4']:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(r'\D', '', regex=True), errors='coerce')
    
    # Feature Scaling
    scaler = StandardScaler()
    numeric_cols = ['feature1', 'feature2', 'feature3', 'feature4']
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    
    # Encode target variable
    le = LabelEncoder()
    df['target'] = le.fit_transform(df['target'].astype(str))
    
    return df

# =================================================================
# EXECUTION
# =================================================================

if __name__ == "__main__":
    # Load data
    raw_df = load_and_combine_sheets(r'C:\Users\GARV BANSAL\Desktop\DATASET.xlsx')  # Update path
    
    # Clean and preprocess
    processed_df = clean_and_preprocess(raw_df)
    
    # Save final dataset
    processed_df.to_csv('cyber_crime_virgit_dataset.csv', index=False)
    print("Processing complete! Dataset saved as 'cyber_crime_virgit_dataset.csv'")
    
    # Show preview
    print("\nPreview of processed data:")
    print(processed_df.sample(5))


