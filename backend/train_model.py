import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import os

CSV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'messwise_full_august_2026_menu_dataset.csv'))
MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'model.joblib'))

def load_data():
    df = pd.read_csv(CSV_PATH)
    return df

def prepare_features(df):
    # Select features that are available at prediction time
    feature_cols = [
        'hostel_attendance_estimate',
        'exam_intensity',
        'temperature_c',
        'rainfall_mm',
        'historical_demand_rate',
        'synthetic_liking_score',
    ]
    X = df[feature_cols]
    y = df['expected_consumers']
    return X, y

def train():
    df = load_data()
    X, y = prepare_features(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=2)
    model.fit(X_train, y_train)
    # Evaluation
    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)
    print(f"Model trained. MAE={mae:.2f}, R2={r2:.3f}")
    # Save model
    joblib.dump({'model': model, 'version': 'v1.0'}, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train()
