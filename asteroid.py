import streamlit as st
import mysql.connector
import pandas as pd
import requests

# --- Database Configuration ---
# IMPORTANT: For a real-world application, store these credentials securely
# (e.g., using Streamlit Secrets or environment variables)
DB_CONFIG = {
    "host": "gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
    "user": "1D3T6mastHsd7CC.root",
    "password": "W8WMaCTTjC9jmy08", # Your database password from the notebook
    "port": 4000,
    "database": "near_earth_objects"
}

# --- Database Connection and Query Functions ---

# Use st.cache_resource to cache the database connection across reruns
@st.cache_resource
def get_db_connection():
    """Establishes and returns a database connection."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        st.success("Successfully connected to the database! 🚀")
        return conn
    except mysql.connector.Error as err:
        st.error(f"Error connecting to database: {err}. Please ensure your credentials and network are correct.")
        return None

def run_query(query: str) -> pd.DataFrame:
    """
    Executes a SQL query and returns the result as a Pandas DataFrame.
    Automatically handles connection closing.
    """
    conn = get_db_connection()
    if conn:
        try:
            df = pd.read_sql(query, conn)
            return df
        except pd.io.sql.DatabaseError as e:
            st.error(f"Error executing query: {e}. Please check your SQL syntax.")
            return pd.DataFrame()
        finally:
            if conn.is_connected():
                conn.close()
    return pd.DataFrame()

# --- Streamlit App Layout and Logic ---

st.set_page_config(
    layout="wide",
    page_title="NASA Near-Earth Objects Dashboard ☄️"
)

st.title("☄️ NASA Near-Earth Objects Analysis Dashboard")
st.markdown("This dashboard provides insightful analysis of asteroid close approaches to Earth, based on NASA NeoWs data stored in your TiDB Cloud database.")
st.markdown("---")


url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date=2024-01-01&end_date=2024-01-07&api_key=uQkEB3zlMF0iGyd9P78eZ0gRkMk0oYMCUpkTKVog"

response = requests.get(url)

response

asteroids_data = []
target = 10000
url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date=2024-01-01&end_date=2024-01-07&api_key=uQkEB3zlMF0iGyd9P78eZ0gRkMk0oYMCUpkTKVog"

while len(asteroids_data) < target:
  response = requests.get(url)
  data = response.json()
  details = data["near_earth_objects"]
  for date, asteroids in details.items():
    for earth in asteroids:
      asteroids_data.append(dict(id=int(earth["id"]),
                                 neo_reference_id=int(earth["neo_reference_id"]),
                                 name=earth['name'],
                                 absolute_magnitude_h=earth["absolute_magnitude_h"],
                                 estimated_diameter_min_km=earth["estimated_diameter"]["feet"]["estimated_diameter_min"],
                                 estimated_diameter_max_km=earth["estimated_diameter"]["feet"]["estimated_diameter_max"],
                                 is_potentially_hazardous_asteroid=earth["is_potentially_hazardous_asteroid"],
                                 close_approach_date=earth['close_approach_data'][0]['close_approach_date'],
                                 relative_velocity_km_per_second=float(earth['close_approach_data'][0]['relative_velocity']['kilometers_per_second']),
                                 astronomical_distance_km=float(earth['close_approach_data'][0]['miss_distance']['astronomical']),
                                 miss_distance_km=float(earth['close_approach_data'][0]['miss_distance']['kilometers']),
                                 miss_distance_lunar=float(earth['close_approach_data'][0]['miss_distance']['lunar']),
                                 orbiting_body=earth['close_approach_data'][0]['orbiting_body']
                                 ))
      if len(asteroids_data) >= target:
          break
    if len(asteroids_data) >= target:
        break
  url = data["links"]["next"]


asteroids_data = pd.DataFrame(asteroids_data)
asteroids_data


# Sidebar for navigation
st.sidebar.header("Explore Asteroid Insights")
analysis_option = st.sidebar.selectbox(
    "Choose an analysis type:",
    [
        "Select an Analysis",
        "1. Asteroid Approach Count",
        "2. Average Velocity of Each Asteroid",
        "3. Top 10 Fastest Asteroids",
        "4. Potentially Hazardous Asteroids (>3 Approaches)",
        "5. Month with Most Asteroid Approaches",
        "6. Asteroid with Fastest Ever Approach Speed",
        "7. Asteroids by Estimated Diameter (Descending)",
        "8. Asteroids with Closest Approach Getting Nearer",
        "9. Closest Approach Details (Name, Date, Miss Distance)",
        "10. Asteroids with Velocity > 50,000 km/h",
        "11. Approaches Count Per Month",
        "12. Asteroid with Highest Brightness (Lowest Magnitude)",
        "13. Hazardous vs Non-Hazardous Asteroids Count",
        "14. Asteroids Closer than the Moon (< 1 Lunar Distance)",
        "15. Asteroids Within 0.05 AU (Astronomical Units)",
        "--- Additional Insights ---",
        "16. Top 5 Largest Hazardous Asteroids",
        "17. Average Miss Distance (Hazardous vs. Non-Hazardous)",
        "18. Asteroids Approaching on a Specific Date",
        "19. Distribution of Asteroid Sizes",
        "20. Brightest Potentially Hazardous Asteroids",
        "--- Custom Query ---",
        "21. Run Your Own Custom SQL Query"
    ]
)


st.markdown("---")
st.markdown("✨ Data provided by NASA's NeoWs (Near Earth Object Web Service).")
st.markdown("Developed with ❤️ using Streamlit and TiDB Cloud.")

