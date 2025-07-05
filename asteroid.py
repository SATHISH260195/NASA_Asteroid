import pandas as pd 
import streamlit as st 

st.title("NASA NEAR_EARTH ASTEROID")
import streamlit as st
from PIL import Image

# Load your image
# Make sure the path is correct and uses forward slashes or a raw string
image = Image.open(r"C:\Users\WELCOME\Downloads\images.jpeg")

st.image(image, caption="My Full-Width Image", use_container_width=True)

r = st.sidebar.radio('ASTEROID',['Criteria filter','queries'])



# Display results based on user selection
if analysis_option == "Select an Analysis":
    st.info("👈 Please select an analysis option from the sidebar to view the results.")

elif analysis_option == "1. Asteroid Approach Count":
    st.header("🔢 Count How Many Times Each Asteroid Has Approached Earth")
    query = """
    SELECT
        a.name,
        COUNT(ca.id) AS approach_count
    FROM
        asteroids a
    JOIN
        close_approach ca ON a.id = ca.id
    GROUP BY
        a.name
    ORDER BY
        approach_count DESC;
    """
    df = run_query(query)
    if not df.empty:
        st.dataframe(df)

elif analysis_option == "2. Average Velocity of Each Asteroid":
    st.header("⏩ Average Velocity of Each Asteroid Over Multiple Approaches")
    query = """
    SELECT
        a.name,
        AVG(ca.relative_velocity_km_per_second) AS average_velocity_km_per_second
    FROM
        asteroids a
    JOIN
        close_approach ca ON a.id = ca.id
    GROUP BY
        a.name
    ORDER BY
        average_velocity_km_per_second DESC;
    """
    df = run_query(query)
    if not df.empty:
        st.dataframe(df)

elif analysis_option == "3. Top 10 Fastest Asteroids":
    st.header("⚡ Top 10 Fastest Asteroids (by max recorded approach velocity)")
    query = """
    SELECT
        a.name,
        MAX(ca.relative_velocity_km_per_second) AS max_velocity_km_per_second
    FROM
        asteroids a
    JOIN
        close_approach ca ON a.id = ca.id
    GROUP BY
        a.name
    ORDER BY
        max_velocity_km_per_second DESC
    LIMIT 10;
    """
    df = run_query(query)
    if not df.empty:
        st.dataframe(df)

elif analysis_option == "4. Potentially Hazardous Asteroids (>3 Approaches)":
    st.header("⚠️ Potentially Hazardous Asteroids That Have Approached Earth More Than 3 Times")
    query = """
    SELECT
        a.name,
        COUNT(ca.id) AS approach_count
    FROM
        asteroids a
    JOIN
        close_approach ca ON a.id = ca.id
    WHERE
        a.is_potentially_hazardous_asteroid = TRUE
    GROUP BY
        a.name
    HAVING
        approach_count > 3
    ORDER BY
        approach_count DESC;
    """
    df = run_query(query)
    if not df.empty:
        st.dataframe(df)
    else:
        st.info("No potentially hazardous asteroids found with more than 3 approaches in the current dataset.")

elif analysis_option == "5. Month with Most Asteroid Approaches":
    st.header("🗓️ Month with the Most Asteroid Approaches")
    query = """
    SELECT
        DATE_FORMAT(close_approach_date, '%Y-%m') AS month,
        COUNT(id) AS approach_count
    FROM
        close_approach
    GROUP BY
        month
    ORDER BY
        approach_count DESC
    LIMIT 1;
    """
    df = run_query(query)
    if not df.empty:
        st.dataframe(df)

elif analysis_option == "6. Asteroid with Fastest Ever Approach Speed":
    st.header("🚀 Asteroid with the Fastest Ever Approach Speed")
    query = """
    SELECT
        a.name,
        ca.relative_velocity_km_per_second
    FROM
        asteroids a
    JOIN
        close_approach ca ON a.id = ca.id
    ORDER BY
        ca.relative_velocity_km_per_second DESC
    LIMIT 1;
    """
    df = run_query(query)
    if not df.empty:
        st.dataframe(df)

elif analysis_option == "7. Asteroids by Estimated Diameter (Descending)":
    st.header("📏 Asteroids Sorted by Maximum Estimated Diameter (Descending)")
    query = """
    SELECT
        name,
        estimated_diameter_max_km
    FROM
        asteroids
    ORDER BY
        estimated_diameter_max_km DESC;
    """
    df = run_query(query)
    if not df.empty:
        st.dataframe(df)

elif analysis_option == "8. Asteroids with Closest Approach Getting Nearer":
    st.header("📉 Asteroid Whose Closest Approach is Getting Nearer Over Time")
    st.info("This query attempts to identify asteroids with multiple approaches where the miss distance is decreasing over time. **Note:** Due to the often limited time range of API data (e.g., Jan 1-7, 2024 in your notebook), finding clear, statistically significant trends of decreasing miss distance might be challenging with small datasets. A longer historical dataset would yield more meaningful results.")
    query = """
    SELECT
        a.name,
        ca.close_approach_date,
        ca.miss_distance_km
    FROM
        asteroids a
    JOIN
        close_approach ca ON a.id = ca.id
    WHERE
        a.id IN (
            SELECT id
            FROM close_approach
            GROUP BY id
            HAVING COUNT(id) > 1 -- Ensure the asteroid has multiple approaches
        )
    ORDER BY
        a.name, ca.close_approach_date ASC, ca.miss_distance_km ASC;
    """
    df = run_query(query)
    if not df.empty:
        st.dataframe(df)
    else:
        st.info("No asteroids with multiple approaches found to analyze for decreasing miss distance in the current data, or no clear trend observed.")

elif analysis_option == "9. Closest Approach Details (Name, Date, Miss Distance)":
    st.header("📅 Name of Each Asteroid Along with Date and Miss Distance of Its Closest Approach")
    query = """
    SELECT
        a.name,
        ca.close_approach_date,
        ca.miss_distance_km
    FROM
        asteroids a
    JOIN
        close_approach ca ON a.id = ca.id
    ORDER BY
        ca.close_approach_date ASC, ca.miss_distance_km ASC;
    """
    df = run_query(query)
    if not df.empty:
        st.dataframe(df)

elif analysis_option == "10. Asteroids with Velocity > 50,000 km/h":
    st.header("💨 Names of Asteroids That Approached Earth with Velocity > 50,000 km/h")
    query = """
    SELECT DISTINCT
        a.name
    FROM
        asteroids a
    JOIN
        close_approach ca ON a.id = ca.id
    WHERE
        ca.relative_velocity_km_per_second * 3600 > 50000; -- Convert km/s to km/h
    """
    df = run_query(query)
    if not df.empty:
        st.dataframe(df)
    else:
        st.info("No asteroids found with approach velocity greater than 50,000 km/h in the current dataset.")

elif analysis_option == "11. Approaches Count Per Month":
    st.header("📊 Count How Many Approaches Happened Per Month")
    query = """
    SELECT
        DATE_FORMAT(close_approach_date, '%Y-%m') AS month,
        COUNT(id) AS approach_count
    FROM
        close_approach
    GROUP BY
        month
    ORDER BY
        month;
    """
    df = run_query(query)
    if not df.empty:
        st.dataframe(df)

elif analysis_option == "12. Asteroid with Highest Brightness (Lowest Magnitude)":
    st.header("✨ Asteroid with the Highest Brightness (Lowest Magnitude Value)")
    query = """
    SELECT
        name,
        absolute_magnitude_h
    FROM
        asteroids
    ORDER BY
        absolute_magnitude_h ASC
    LIMIT 1;
    """
    df = run_query(query)
    if not df.empty:
        st.dataframe(df)

elif analysis_option == "13. Hazardous vs Non-Hazardous Asteroids Count":
    st.header("🛑 Number of Hazardous vs Non-Hazardous Asteroids")
    query = """
    SELECT
        CASE
            WHEN is_potentially_hazardous_asteroid = TRUE THEN 'Hazardous'
            ELSE 'Non-Hazardous'
        END AS asteroid_type,
        COUNT(id) AS asteroid_count
    FROM
        asteroids
    GROUP BY
        asteroid_type;
    """
    df = run_query(query)
    if not df.empty:
        st.dataframe(df)

elif analysis_option == "14. Asteroids Closer than the Moon (< 1 Lunar Distance)":
    st.header("🌙 Asteroids That Passed Closer Than the Moon (< 1 Lunar Distance)")
    st.info("Lunar distance (LD) is approximately 384,400 km. The 'miss_distance_lunar' column directly indicates distance in multiples of lunar distances.")
    query = """
    SELECT
        a.name,
        ca.close_approach_date,
        ca.miss_distance_lunar AS miss_distance_lunar_distances,
        ca.miss_distance_km
    FROM
        asteroids a
    JOIN
        close_approach ca ON a.id = ca.id
    WHERE
        ca.miss_distance_lunar < 1
    ORDER BY
        ca.miss_distance_lunar ASC;
    """
    df = run_query(query)
    if not df.empty:
        st.dataframe(df)
    else:
        st.info("No asteroids found that passed closer than the Moon in the current dataset.")

elif analysis_option == "15. Asteroids Within 0.05 AU (Astronomical Units)":
    st.header("🌌 Asteroids That Came Within 0.05 AU (Astronomical Units)")
    st.info("1 Astronomical Unit (AU) is the average distance from Earth to the Sun (approx. 149.6 million km).")
    query = """
    SELECT
        a.name,
        ca.close_approach_date,
        ca.astronomical_distance_km AS miss_distance_km,
        ca.astronomical_distance_km / 149597870.7 AS miss_distance_au
    FROM
        asteroids a
    JOIN
        close_approach ca ON a.id = ca.id
    WHERE
        ca.astronomical_distance_km / 149597870.7 < 0.05
    ORDER BY
        ca.astronomical_distance_km ASC;
    """
    df = run_query(query)
    if not df.empty:
        st.dataframe(df)
    else:
        st.info("No asteroids found that came within 0.05 AU in the current dataset.")

# --- Additional Insights ---
elif analysis_option == "16. Top 5 Largest Hazardous Asteroids":
    st.header("🌟 Top 5 Largest Hazardous Asteroids (by Max Estimated Diameter)")
    query = """
    SELECT
        name,
        estimated_diameter_max_km,
        is_potentially_hazardous_asteroid
    FROM
        asteroids
    WHERE
        is_potentially_hazardous_asteroid = TRUE
    ORDER BY
        estimated_diameter_max_km DESC
    LIMIT 5;
    """
    df = run_query(query)
    if not df.empty:
        st.dataframe(df)
    else:
        st.info("No hazardous asteroids found in the dataset.")

elif analysis_option == "17. Average Miss Distance (Hazardous vs. Non-Hazardous)":
    st.header("🧮 Average Miss Distance (in KM) for Hazardous vs. Non-Hazardous Asteroids")
    query = """
    SELECT
        CASE
            WHEN a.is_potentially_hazardous_asteroid = TRUE THEN 'Hazardous'
            ELSE 'Non-Hazardous'
        END AS asteroid_type,
        AVG(ca.miss_distance_km) AS average_miss_distance_km
    FROM
        asteroids a
    JOIN
        close_approach ca ON a.id = ca.id
    GROUP BY
        asteroid_type;
    """
    df = run_query(query)
    if not df.empty:
        st.dataframe(df)

elif analysis_option == "18. Asteroids Approaching on a Specific Date":
    st.header("🗓️ Asteroids Approaching on a Specific Date")
    selected_date = st.date_input("Select a Date:", pd.to_datetime('2024-01-05'))
    query = f"""
    SELECT
        a.name,
        ca.close_approach_date,
        ca.miss_distance_km,
        ca.relative_velocity_km_per_second
    FROM
        asteroids a
    JOIN
        close_approach ca ON a.id = ca.id
    WHERE
        ca.close_approach_date = '{selected_date.strftime('%Y-%m-%d')}';
    """
    df = run_query(query)
    if not df.empty:
        st.dataframe(df)
    else:
        st.info(f"No asteroid approaches found on {selected_date.strftime('%Y-%m-%d')}.")

elif analysis_option == "19. Distribution of Asteroid Sizes":
    st.header("📦 Distribution of Asteroid Sizes (by Max Estimated Diameter)")
    query = """
    SELECT
        CASE
            WHEN estimated_diameter_max_km < 0.01 THEN 'Very Small (<10m)'
            WHEN estimated_diameter_max_km >= 0.01 AND estimated_diameter_max_km < 0.1 THEN 'Small (10m-100m)'
            WHEN estimated_diameter_max_km >= 0.1 AND estimated_diameter_max_km < 1 THEN 'Medium (100m-1km)'
            WHEN estimated_diameter_max_km >= 1 AND estimated_diameter_max_km < 10 THEN 'Large (1km-10km)'
            ELSE 'Very Large (>=10km)'
        END AS diameter_range,
        COUNT(id) AS asteroid_count
    FROM
        asteroids
    GROUP BY
        diameter_range
    ORDER BY
        diameter_range;
    """
    df = run_query(query)
    if not df.empty:
        st.dataframe(df)

elif analysis_option == "20. Brightest Potentially Hazardous Asteroids":
    st.header("💡 Brightest Potentially Hazardous Asteroids (Lowest Absolute Magnitude)")
    query = """
    SELECT
        name,
        absolute_magnitude_h,
        estimated_diameter_min_km,
        estimated_diameter_max_km
    FROM
        asteroids
    WHERE
        is_potentially_hazardous_asteroid = TRUE
    ORDER BY
        absolute_magnitude_h ASC
    LIMIT 5;
    """
    df = run_query(query)
    if not df.empty:
        st.dataframe(df)
    else:
        st.info("No potentially hazardous asteroids found in the dataset with magnitude data.")

# --- Custom Query Section ---
elif analysis_option == "21. Run Your Own Custom SQL Query":
    st.header("👩‍💻 Run Your Own Custom SQL Query")
    st.warning("⚠️ **Caution:** Use valid SQL for your TiDB/MySQL database. Incorrect queries may cause errors or slow performance.")
    custom_query = st.text_area("Enter your SQL query here:", height=200, value="SELECT name, is_potentially_hazardous_asteroid, estimated_diameter_max_km FROM asteroids LIMIT 10;")

    if st.button("🚀 Execute Custom Query"):
        if custom_query.strip():
            df = run_query(custom_query)
            if not df.empty:
                st.success("Query executed successfully!")
                st.dataframe(df)
            else:
                st.warning("No results returned or an error occurred. Please check your query.")
        else:
            st.error("Please enter a SQL query to execute.")

st.markdown("---")
st.markdown("✨ Data provided by NASA's NeoWs (Near Earth Object Web Service).")
st.markdown("Developed with ❤️ using Streamlit and TiDB Cloud.")


