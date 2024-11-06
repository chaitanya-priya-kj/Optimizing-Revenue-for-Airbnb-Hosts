import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from collections import Counter
import ast
import calendar


def analyze_airbnb_data(airbnb_data, user_zipcode):

  zipcode_data = airbnb_data[airbnb_data['zipcode'] == user_zipcode]
  zipcode_data.loc[:, 'amenities'] = zipcode_data['amenities'].apply(ast.literal_eval)
  # zipcode_data.loc[:, 'month_booked'] = zipcode_data['month_booked'].apply(ast.literal_eval)


  # Getting the average price and number of listings in the zipcode
  average_price = zipcode_data['price'].mean()
  num_listings = len(zipcode_data)
  
  print("Average price: $",round(average_price,2))
  print("Number of listings:",num_listings)

  # Getting the top 10 amenities
  all_amenities = []
  for amenities_list in zipcode_data['amenities']:
      all_amenities.extend(amenities_list)

  amenities_count = Counter(all_amenities)

  top_ten_amenities = amenities_count.most_common(10)
  print("Top Ten Amenities:")
  for amenity, _ in top_ten_amenities:
      print(amenity)

  # Percentage of listings having the top 5 amenities
  top_five_amenities_names = [amenity for amenity, _ in top_ten_amenities[:5]]
  
  percentage_listings_with_amenities = []
  total_listings = len(zipcode_data)
  for amenity, count in top_ten_amenities[:5]:
      percentage = (count / total_listings) * 100
      percentage_listings_with_amenities.append(percentage)

  plt.figure(figsize=(8, 6))
  bars_1 = plt.barh(top_five_amenities_names, percentage_listings_with_amenities, color='skyblue')

  for bar, percentage in zip(bars_1, percentage_listings_with_amenities):
      plt.text(bar.get_width(), bar.get_y() + bar.get_height()/2, f'{percentage:.2f}%', va='center')

  plt.xlabel('Percentage of Listings (%)')
  plt.title('Top 5 Amenities in Airbnb Listings')
  plt.gca().invert_yaxis() 
  plt.xticks([]) 
  plt.tight_layout()
  plt.show()

  # Getting the top months booked 
  all_months = []
  for months_list in zipcode_data['month_booked']:
      all_months.extend(months_list)

  months_count = Counter(all_months)
  top_three_months = months_count.most_common(3)
  month_names = [calendar.month_name[month_number] for month_number, _ in top_three_months]

  print("Top Three Months Booked:")
  for month in month_names:
      print(month)

  
  # Getting property type by percentages

  property_type_groupby = zipcode_data.groupby(['property_type'])['listing_id'].count().reset_index()
  property_type_groupby['percentage'] = (property_type_groupby['listing_id']/property_type_groupby['listing_id'].sum())*100
  top_five_property_types = property_type_groupby['property_type'].head()
  top_five_percentages = property_type_groupby['percentage'].head()

  plt.figure(figsize=(8, 8))
  plt.pie(top_five_percentages, labels=top_five_property_types, autopct='%1.1f%%', colors=['red', 'blue', 'green', 'orange', 'purple'])
  plt.title('Top 5 Property Types')

  plt.show()

  analysis_result = {
        'average_price': round(average_price, 2),
        'num_listings': num_listings,
        'top_ten_amenities': top_ten_amenities,
        'top_three_months': top_three_months,
        'top_five_property_types': list(zip(top_five_property_types, top_five_percentages))
    }

  return analysis_result

# if __name__ == "__main__":
#     data_path = "data/listings+reviews+crime+attractions.csv"
#     preprocessed_data = preprocess_data(data_path)
#     user_zipcode = input("Enter the zip code: ")
#     analyze_airbnb_data(preprocessed_data,user_zipcode)