# Retail Automated Inventory Reorder Point Optimizer

## 📌 Project Overview

The Retail Automated Inventory Reorder Point Optimizer is a machine learning-based application designed to help retail stores make better inventory replenishment decisions.

The system predicts expected daily product/store sales using historical sales data and store-related factors such as promotions, holidays, competition, and time-based features.

The predicted demand is then used with lead time and safety stock to calculate the inventory Reorder Point.

---

## 📝 Problem Statement

Stores often struggle with either stocking too few items, which can lead to lost sales, or stocking too many items, which can increase storage costs and tie up money.

This project uses machine learning regression to predict future sales and combines the prediction with inventory management logic to determine whether inventory should be reordered.

---

## 🎯 Objectives

- Predict expected daily sales using machine learning.
- Analyze the effect of promotions, holidays, competition, and time-related factors.
- Calculate the inventory Reorder Point.
- Determine whether current inventory requires replenishment.
- Calculate a recommended order quantity.
- Provide the prediction through a simple Flask web application.

---

## 🧠 Machine Learning Approach

The project uses **Random Forest Regression**.

Random Forest Regression is suitable because the target variable, Sales, is continuous. The algorithm combines multiple decision trees and can capture nonlinear relationships between sales and different store and calendar features.

### Model

```text
RandomForestRegressor