import pandas as pd
import numpy as np

import pandas as pd
import numpy as np

df = pd.read_csv('taylor_swift_spotify.csv')


# STEP 1: Your reverse album list (now reversed for correct sort)
album_order_list = [
    'THE TORTURED POETS DEPARTMENT: THE ANTHOLOGY',
    'THE TORTURED POETS DEPARTMENT',
    "1989 (Taylor's Version) [Deluxe]",
    "1989 (Taylor's Version)",
    "Speak Now (Taylor's Version)",
    'Midnights (The Til Dawn Edition)',
    'Midnights (3am Edition)',
    'Midnights',
    "Red (Taylor's Version)",
    "Fearless (Taylor's Version)",
    'evermore (deluxe version)',
    'evermore',
    'folklore: the long pond studio sessions (from the Disney+ special) [deluxe edition]',
    'folklore (deluxe version)',
    'folklore',
    'Lover',
    'reputation',
    'reputation Stadium Tour Surprise Song Playlist',
    '1989 (Deluxe)',
    '1989',
    'Red (Deluxe Edition)',
    'Red',
    'Speak Now World Tour Live',
    'Speak Now',
    'Speak Now (Deluxe Package)',
    'Fearless (Platinum Edition)',
    'Fearless (International Version)',
    'Live From Clear Channel Stripped 2008',
    'Taylor Swift (Deluxe Edition)'
][::-1]  # reverse it to get Debut first

# STEP 2: Create album → priority mapping
album_priority = {album: i for i, album in enumerate(album_order_list)}

# STEP 3: Load CSV
df = pd.read_csv("taylor_swift_spotify.csv")

# STEP 4: Clean and prepare sorting columns
df['album_clean'] = df['album'].astype(str).str.strip()
df['album_order'] = df['album_clean'].map(album_priority)
df['track_order'] = range(len(df))  # preserves original track order

# STEP 5: Sort by album order and then by original row order
df_sorted = df.sort_values(by=['album_order', 'track_order']).reset_index(drop=True)

# STEP 6: Assign descending Sno (highest to 1)
df_sorted['Sno'] = range(len(df_sorted), 0, -1)

# STEP 7: Drop temp columns and save final result
df_sorted.drop(columns=['album_clean', 'album_order', 'track_order'], inplace=True)
df_sorted.to_csv("final.csv", index=False)
df = pd.read_csv("final.csv")
df_unique_versions = df.drop_duplicates(subset='name', keep='first')

df_unique_versions.to_csv("please.csv", index=False)

df = pd.read_csv("DATAY.csv")  # Make sure this file is in the same folder as your .py file
print(df.head())         # First 5 rows
print(df.columns)        # Column names
print(df.shape)          # (Rows, Columns)
Debut_Songs =df[df['album']=='Taylor Swift (Deluxe Edition)']
SONGS_1989 =df[df['album']=='1989']
Debut_acc=Debut_Songs[['name','acousticness']].sort_values(by='acousticness', ascending=False)
print(Debut_acc[['name','acousticness']])
Acc_1989 = SONGS_1989[['name','acousticness']].sort_values(by='acousticness', ascending=False)
print(Acc_1989[['name','acousticness']])
Debut_Songs = Debut_Songs.dropna(subset=['acousticness'])
SONGS_1989 = SONGS_1989.dropna(subset=['acousticness'])
Debut_acc['acousticness'] = pd.to_numeric(Debut_acc['acousticness'], errors='coerce')
Acc_1989['acousticness'] = pd.to_numeric(Acc_1989['acousticness'], errors='coerce')

Debut_acc['album'] = 'Debut'
Acc_1989['album'] = '1989'

combined_df = pd.concat([Debut_acc, Acc_1989])
combined_df.to_csv("1989_vs_Debut_Acousticness.csv", index=False)

df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')  # safest version

# Step 3: Extract year
df['year'] = df['release_date'].dt.year

# Step 4: Group by year and calculate averages
yearly_avg = df.groupby('year')[['popularity', 'energy', 'valence', 'acousticness', 'danceability']].mean().reset_index()

# Step 5: Save to CSV
yearly_avg.to_csv("yearly_trends.csv", index=False)

print("✅ Saved: yearly_trends.csv")
print(yearly_avg.head())


# Classify songs by valence
df['mood'] = df['valence'].apply(lambda x: 'Happy' if x > 0.7 else ('Sad' if x < 0.3 else 'Neutral'))

# Keep only happy and sad songs for comparison
mood_df = df[df['mood'].isin(['Happy', 'Sad'])]

# Save only needed columns
mood_df[['name', 'album', 'valence', 'popularity', 'mood']].to_csv("valence_popularity.csv", index=False)

# Albums you want to include
target_albums = [
    "1989 (Taylor's Version) [Deluxe]",
    "1989 (Taylor's Version)",
    "Speak Now (Taylor's Version)",
    "Red (Taylor's Version)",
    "Fearless (Taylor's Version)",

    "1989 (Deluxe)",
    "1989",
    "Red (Deluxe Edition)",
    "Red",
    "Speak Now (Deluxe Package)",
    "Fearless (Platinum Edition)"
]

# Filter only the target albums
filtered_df = df[df['album'].isin(target_albums)].copy()

# Create version column: 'TV' if it contains Taylor's Version, else 'OG'
def assign_version(album):
    if "taylor's version" in album.lower():
        return "TV"
    else:
        return "OG"

filtered_df['version'] = filtered_df['album'].apply(assign_version)

# Keep only the required columns
final_df = filtered_df[['name', 'album', 'version', 'release_date', 'popularity']]

# Save to CSV
final_df.to_csv("tv_vs_og_popularity.csv", index=False)
print("✅ Cleaned data saved to 'tv_vs_og_popularity.csv'")
# Keep relevant columns
tempo_valence_df = df[['name', 'tempo', 'valence', 'album']].dropna()

# Add category columns (optional for visualization)
tempo_valence_df['tempo_level'] = tempo_valence_df['tempo'].apply(lambda x: 'Fast' if x > 120 else 'Medium' if x > 90 else 'Slow')
tempo_valence_df['mood'] = tempo_valence_df['valence'].apply(lambda x: 'Happy' if x > 0.6 else 'Sad' if x < 0.4 else 'Neutral')

# Save to CSV for Power BI
tempo_valence_df.to_csv("tempo_vs_mood.csv", index=False)
print("✅ Saved: 'tempo_vs_mood.csv'")
# Filter only track 13s
track_13_df = df[df['track_number'] == 13]

# Keep key columns
track_13_df = track_13_df[['name', 'album', 'duration_ms', 'valence', 'popularity']].copy()
track_13_df['duration_min'] = track_13_df['duration_ms'] / 60000

# Save
track_13_df.to_csv("track_13_analysis.csv", index=False)
print("✨ Track 13 analysis file saved!")
tempo_valence_df = df[['name', 'tempo', 'valence', 'album']].dropna()

# Add tempo and mood categories
tempo_valence_df['tempo_level'] = tempo_valence_df['tempo'].apply(
    lambda x: 'Fast' if x > 120 else ('Slow' if x < 90 else 'Medium')
)
tempo_valence_df['mood'] = tempo_valence_df['valence'].apply(
    lambda x: 'Happy' if x > 0.6 else ('Sad' if x < 0.4 else 'Neutral')
)

# Filter only Fast/Slow and Happy/Sad (exclude Medium and Neutral)
filtered_df = tempo_valence_df[
    tempo_valence_df['tempo_level'].isin(['Fast', 'Slow']) &
    tempo_valence_df['mood'].isin(['Happy', 'Sad'])
]
filtered_df.to_csv("tempo_mood_filtered.csv", index=False)
print("✅ Saved: 'tempo_mood_filtered.csv'")
df['energy_level'] = df['energy'].apply( lambda x: 'High' if x > 0.7 else ('Low' if x < 0.3 else 'Medium'))
df['energy_level'] = df['energy'].apply( lambda x: 'High' if x > 0.7 else ('Low' if x < 0.3 else 'Medium'))
energy_df = df[df['energy_level'].isin(['High', 'Low', 'Medium'])]
energy_df['duration_minutes'] = energy_df['duration_ms'] / 60000
final_df = energy_df[['name', 'album', 'energy', 'duration_minutes', 'energy_level']]
final_df.to_csv("high_low_energy_duwzation.csv", index=False)








