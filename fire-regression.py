import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# loading dataset
df = pd.read_csv("CA_Weather_Fire_Dataset_1984-2025.csv")

X = df[['PRECIPITATION', 'MAX_TEMP','MIN_TEMP', 'AVG_WIND_SPEED']]
Y = df['FIRE_START_DAY']

df = df.dropna()  # Drops all rows containing NaNs

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)


# Scale numerical features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)


from sklearn.linear_model import LogisticRegression

# Initialize model
model = LogisticRegression()

# Train the model
model.fit(X_train, Y_train)

# Print the logistic regression equation
intercept = model.intercept_[0]  # Intercept (bias)
coefficients = model.coef_[0]   # Coefficients for each feature

# Feature names (assuming 'X' is your features DataFrame)
feature_names = X.columns

# Construct the equation
equation = f"Logistic Regression Equation: log(P/1-P) = {intercept:.4f}"
for i in range(len(coefficients)):
    equation += f" + ({coefficients[i]:.4f}) * {feature_names[i]}"

print(equation)


from sklearn.metrics import accuracy_score, classification_report

# Predict on test set
y_pred = model.predict(X_test)

# Check accuracy
accuracy = accuracy_score(Y_test, y_pred)
print(f"Model Accuracy: {accuracy:.2f}")

# Print detailed performance metrics
print(classification_report(Y_test, y_pred))


# if you input test data, do 
#data=[[PRECIPITATION', 'MAX_TEMP','MIN_TEMP', 'AVG_WIND_SPEED']]

#prediction = model.predict(data)
#if prediction[0] == True: fire risk!!!