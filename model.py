import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import RandomOverSampler
from sklearn.model_selection import StratifiedKFold, cross_val_score, GridSearchCV
import joblib
import os

# Load the data
df = pd.read_csv('data/updated_dataset_new.csv')

# Handle missing values by filling with the mode of each column
df.fillna(df.mode().iloc[0], inplace=True)

# Initialize label encoders for categorical columns
label_encoders = {}
categorical_columns = ['Name', 'Season', 'Weather','Intensity', 'Gender', 'Occasion']
for col in categorical_columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Define features and target variable
features = ['Occasion', 'Season', 'Weather', 'Intensity', 'Gender']
target = 'Name'

# Extract features and target from the dataframe
x = df[features]
y = df[target]

# Initial minimum samples threshold
min_samples = 2

# Filter out classes with fewer samples than the threshold
while True:
    filtered_df = df[df[target].map(df[target].value_counts()) >= min_samples]
    if not filtered_df.empty:
        break
    min_samples -= 1

# Update features and target after filtering
x = filtered_df[features]
y = filtered_df[target]

# Print the distribution of the target variable to inspect class imbalance
class_counts = y.value_counts()
print("Class Distribution Before Oversampling:")
print(class_counts)

# Apply RandomOverSampler to balance the dataset
ros = RandomOverSampler(random_state=42)
X_resampled, y_resampled = ros.fit_resample(x, y)

# Check the distribution of the target variable after oversampling
class_counts_resampled = pd.Series(y_resampled).value_counts()
print("Class Distribution After Oversampling:")
print(class_counts_resampled)

# Initialize the Random Forest Classifier
model = RandomForestClassifier(random_state=42)

# Define parameter grid for hyperparameter tuning
param_grid = {
    'n_estimators': [100, 300, 500],
    'max_depth': [20, 30, 40, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'bootstrap': [True, False]
}


# Initialize StratifiedKFold with 3 splits
cv = StratifiedKFold(n_splits=2)

# Initialize GridSearchCV for hyperparameter tuning
grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=cv, n_jobs=-1, verbose=2)
grid_search.fit(X_resampled, y_resampled)

# Get the best model from GridSearchCV
best_model = grid_search.best_estimator_

# Evaluate the model using cross-validation
cv_results = cross_val_score(best_model, X_resampled, y_resampled, cv=cv, scoring='accuracy')

print("Cross-Validation Accuracy Scores:", cv_results)
print("Mean Cross-Validation Accuracy:", cv_results.mean())

# Fit the model on the entire resampled dataset
best_model.fit(X_resampled, y_resampled)

model_folder = 'model'
if not os.path.exists(model_folder):
    os.makedirs(model_folder)

model_file = os.path.join(model_folder, 'perfume_recommender_model.pkl')
joblib.dump(best_model, model_file)

# Create a folder for label encoders if it doesn't exist
label_encoders_folder = 'label_encoders'
if not os.path.exists(label_encoders_folder):
    os.makedirs(label_encoders_folder)

# Save each label encoder into the label encoders folder
for col, encoder in label_encoders.items():
    encoder_file = os.path.join(label_encoders_folder, f'{col}_encoder.pkl')
    joblib.dump(encoder, encoder_file)
