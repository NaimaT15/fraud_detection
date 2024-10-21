
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ipaddress
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
def ip_to_int(ip_string):
    """Convert an IP address to its integer representation."""
    return int(ipaddress.ip_address(ip_string))

def clean_data(df):
    """
    Cleans the dataset by removing duplicates, correcting data types, 
    and ensuring IP addresses are correctly formatted as strings.
    
    Parameters:
        df (pandas.DataFrame): The input dataframe.
        
    Returns:
        pandas.DataFrame: The cleaned dataframe.
    """
    
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Convert 'signup_time' and 'purchase_time' to datetime
    df['signup_time'] = pd.to_datetime(df['signup_time'])
    df['purchase_time'] = pd.to_datetime(df['purchase_time'])
    
    # Convert 'age' to integer
    df['age'] = df['age'].astype(int)
    
    # Ensure 'purchase_value' is a float
    df['purchase_value'] = df['purchase_value'].astype(float)
    
    # Ensure IP address is stored as string
    df['ip_address'] = df['ip_address'].astype(str)
    
    # Ensure categorical columns are strings
    categorical_columns = ['user_id', 'device_id', 'source', 'browser', 'sex', 'class']
    df[categorical_columns] = df[categorical_columns].astype(str)
    
    return df
def univariate_analysis(df, numerical_columns, categorical_columns):
    """
    Perform univariate analysis on the dataset, including summary statistics, 
    histograms for numerical features, and count plots for categorical features.
    
    Parameters:
    - df (pandas.DataFrame): The input dataframe.
    - numerical_columns (list): List of numerical columns.
    - categorical_columns (list): List of categorical columns.
    
    Returns:
    - None
    """
    # Summary statistics
    print("Summary Statistics:\n", df.describe())
    
    # Histograms for numerical features
    df[numerical_columns].hist(figsize=(10, 5))
    plt.suptitle("Histograms of Numerical Features")
    plt.show()
    
    # Box plot for numerical features (helps detect outliers)
    plt.figure(figsize=(10, 5))
    sns.boxplot(data=df[numerical_columns])
    plt.title("Box Plots of Numerical Features")
    plt.show()

    # Count plot for categorical features
    for column in categorical_columns:
        plt.figure(figsize=(6, 4))

        # Check if there are too many categories, and limit the plot to the top 10 if necessary
        if df[column].nunique() > 10:
            top_10_categories = df[column].value_counts().nlargest(10).index
            sns.countplot(data=df[df[column].isin(top_10_categories)], x=column)
            plt.title(f"Count Plot for Top 10 {column}")
        else:
            sns.countplot(data=df, x=column)
            plt.title(f"Count Plot for {column}")
        
        plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
        plt.show()


def bivariate_analysis(df):
    """
    Perform bivariate analysis on the dataset, including scatter plot and correlation matrix.
    
    Parameters:
    - df (pandas.DataFrame): The input dataframe.
    
    Returns:
    - None
    """
    # Scatter plot for purchase_value vs age (ensure both columns exist in your dataset)
    if 'age' in df.columns and 'purchase_value' in df.columns:
        plt.figure(figsize=(8, 6))
        sns.scatterplot(data=df, x='age', y='purchase_value', hue='sex')
        plt.title("Purchase Value vs Age (Colored by Sex)")
        plt.show()

    # Select only numerical columns for correlation matrix
    numerical_df = df.select_dtypes(include=['float64', 'int64'])
    
    # Correlation matrix for numerical features
    corr_matrix = numerical_df.corr()

    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
    plt.title("Correlation Matrix")
    plt.show()

    # Cross-tabulation for categorical variables
    if 'source' in df.columns and 'class' in df.columns:
        cross_tab = pd.crosstab(df['source'], df['class'])
        print("Cross Tabulation of Source vs Class:\n", cross_tab)
        
        # Bar plot for cross-tabulation
        cross_tab.plot(kind='bar', figsize=(8, 5))
        plt.title("Cross Tabulation of Source vs Class")
        plt.ylabel("Count")
        plt.show()
def merge_fraud_with_geolocation(fraud_data, ip_to_country):
    """Merge fraud data with geolocation data based on IP address."""
    
    # Convert the floating-point IP addresses in fraud_data to integers
    fraud_data['ip_address_int'] = fraud_data['ip_address'].astype('int64')

    # Ensure ip_to_country's bounds are in integer format
    ip_to_country['lower_bound_ip_address'] = ip_to_country['lower_bound_ip_address'].astype('int64')
    ip_to_country['upper_bound_ip_address'] = ip_to_country['upper_bound_ip_address'].astype('int64')

    # Perform a merge to match the IP address with its corresponding country
    merged_data = pd.merge_asof(
        fraud_data.sort_values('ip_address_int'),
        ip_to_country.sort_values('lower_bound_ip_address'),
        left_on='ip_address_int',
        right_on='lower_bound_ip_address',
        direction='backward',
        allow_exact_matches=True
    )
    
    # Filter to keep only rows where the IP address falls within the IP range
    merged_data = merged_data[merged_data['ip_address_int'] <= merged_data['upper_bound_ip_address']]
    
    return merged_data


def convert_to_datetime(df, time_columns):
    """
    Convert specified columns to datetime format.
    
    Parameters:
    - df (pd.DataFrame): The input dataframe.
    - time_columns (list): List of column names to convert to datetime.
    
    Returns:
    - pd.DataFrame: The dataframe with datetime-converted columns.
    """
    for col in time_columns:
        df[col] = pd.to_datetime(df[col])
    return df

def transaction_frequency(df):
    """
    Calculate transaction frequency (count of transactions per user).
    
    Parameters:
    - df (pd.DataFrame): The input dataframe.
    
    Returns:
    - pd.DataFrame: The dataframe with a new column 'transaction_count'.
    """
    df['transaction_count'] = df.groupby('user_id')['user_id'].transform('count')
    return df

def transaction_velocity(df):
    """
    Calculate transaction velocity (time difference between consecutive transactions).
    
    Parameters:
    - df (pd.DataFrame): The input dataframe.
    
    Returns:
    - pd.DataFrame: The dataframe with a new column 'time_since_last_transaction'.
    """
    df['time_since_last_transaction'] = df.groupby('user_id')['purchase_time'].diff().dt.total_seconds()
    df['time_since_last_transaction'].fillna(0, inplace=True)  # Fill NaN for first transaction with 0
    return df

def extract_time_features(df):
    """
    Extract time-based features: hour of day and day of week from 'purchase_time'.
    
    Parameters:
    - df (pd.DataFrame): The input dataframe.
    
    Returns:
    - pd.DataFrame: The dataframe with new columns 'hour_of_day' and 'day_of_week'.
    """
    df['hour_of_day'] = df['purchase_time'].dt.hour
    df['day_of_week'] = df['purchase_time'].dt.dayofweek  # Monday=0, Sunday=6
    return df


def normalize_features(df, columns):
    """
    Normalize specified columns using Min-Max Scaling.
    
    Parameters:
    - df (pd.DataFrame): The input dataframe.
    - columns (list): List of column names to normalize.
    
    Returns:
    - pd.DataFrame: The dataframe with normalized columns.
    """
    scaler = MinMaxScaler()
    df[columns] = scaler.fit_transform(df[columns])
    return df

def standardize_features(df, columns):
    """
    Standardize specified columns using Z-score scaling (mean=0, std=1).
    
    Parameters:
    - df (pd.DataFrame): The input dataframe.
    - columns (list): List of column names to standardize.
    
    Returns:
    - pd.DataFrame: The dataframe with standardized columns.
    """
    scaler = StandardScaler()
    df[columns] = scaler.fit_transform(df[columns])
    return df


def label_encode_features(df, columns):
    """
    Label encode specified categorical columns.
    
    Parameters:
    - df (pd.DataFrame): The input dataframe.
    - columns (list): List of column names to label encode.
    
    Returns:
    - pd.DataFrame: The dataframe with label-encoded columns.
    """
    label_encoders = {}
    for col in columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le  # Store label encoders in case they're needed later
    return df, label_encoders

def one_hot_encode_features(df, columns):
    """
    One-hot encode specified categorical columns.
    
    Parameters:
    - df (pd.DataFrame): The input dataframe.
    - columns (list): List of column names to one-hot encode.
    
    Returns:
    - pd.DataFrame: The dataframe with one-hot encoded columns.
    """
    df = pd.get_dummies(df, columns=columns, drop_first=True)  # drop_first=True to avoid multicollinearity
    return df
