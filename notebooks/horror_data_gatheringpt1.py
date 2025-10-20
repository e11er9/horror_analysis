DATA_DIR = "/Users/Ryan/Desktop/horror_data_gathering/"

import pandas as pd

basics = pd.read_csv(
    DATA_DIR + "title.basics.tsv.gz",
    sep="\t",
    na_values="\\N",
    dtype={"tconst": "string"},
    usecols=["tconst", "titleType", "primaryTitle", "originalTitle", "isAdult", "startYear", "runtimeMinutes", "genres"],
    #nrows=50000  # only read the first 50k rows for now
)
#print(basics.head())

basics = basics[(basics["titleType"]=="movie") & (basics["isAdult"]!=1)]
basics["genres"] = basics["genres"].fillna("")
horror = basics[basics["genres"].str.contains("Horror", case=False, na=False)].copy()

print("Horror movies after filter:", len(horror))

print(horror.columns.tolist())


print(horror.head(10)) 


# 1) Load FULL basics
basics = pd.read_csv(
    DATA_DIR + "title.basics.tsv.gz",
    sep="\t",
    na_values="\\N",
    dtype={"tconst":"string"},
    usecols=["tconst","titleType","primaryTitle","originalTitle","isAdult","startYear","runtimeMinutes","genres"]
)

print("All titles loaded:", len(basics))
print(basics['titleType'].value_counts().head())

# 2) Filter to movies, non-adult
basics = basics[(basics["titleType"]=="movie") & (basics["isAdult"]!=1)].copy()

# 3) Filter to Horror
basics["genres"] = basics["genres"].fillna("")
horror = basics[basics["genres"].str.contains("Horror", case=False, na=False)].copy()

print("Number of horror movies:", len(horror))


#verifying

import os, pandas as pd

DATA_DIR = "/Users/Ryan/Desktop/horror_data_gathering/"  # make sure it ends with /
path = DATA_DIR + "title.basics.tsv.gz"

print("Exists:", os.path.exists(path))
print("Size (MB):", round(os.path.getsize(path) / (1024*1024), 1))

basics = pd.read_csv(
    path,
    sep="\t",
    na_values="\\N",
    dtype={"tconst":"string"},
    usecols=["tconst","titleType","primaryTitle","originalTitle","isAdult","startYear","runtimeMinutes","genres"]
)

print("All rows in basics:", len(basics))
print("titleType counts (top 10):")
print(basics["titleType"].value_counts().head(10))
print("Sample genres:")
print(basics["genres"].dropna().head())


#Starting to build the real db

import pandas as pd

DATA_DIR = "/Users/Ryan/Desktop/horror_data_gathering/"
path = DATA_DIR + "title.basics.tsv.gz"

# Re-read with steadier memory behavior
basics = pd.read_csv(
    path,
    sep="\t",
    na_values="\\N",
    dtype={"tconst":"string"},
    usecols=["tconst","titleType","primaryTitle","originalTitle","isAdult","startYear","runtimeMinutes","genres"],
    low_memory=False
)

# Coerce numerics cleanly
basics["isAdult"] = pd.to_numeric(basics["isAdult"], errors="coerce").astype("Int64")
basics["startYear"] = pd.to_numeric(basics["startYear"], errors="coerce").astype("Int64")
basics["runtimeMinutes"] = pd.to_numeric(basics["runtimeMinutes"], errors="coerce").astype("Int64")

# Filter: movie, non-adult, Horror in genres
movies = basics[(basics["titleType"]=="movie") & (basics["isAdult"]!=1)].copy()
movies["genres"] = movies["genres"].fillna("")
horror = movies[movies["genres"].str.contains(r"\bHorror\b", case=False, na=False)].copy()

print("Movie, non-adult:", len(movies))
print("Horror (movie, non-adult):", len(horror))
horror.head(10)

#######merging ratings

ratings = pd.read_csv(
    DATA_DIR + "title.ratings.tsv.gz",
    sep="\t",
    na_values="\\N",
    dtype={"tconst":"string"},
    usecols=["tconst","averageRating","numVotes"]
)
ratings["averageRating"] = pd.to_numeric(ratings["averageRating"], errors="coerce")
ratings["numVotes"] = pd.to_numeric(ratings["numVotes"], errors="coerce").astype("Int64")

horror = horror.merge(ratings, on="tconst", how="left")
print(horror[["primaryTitle","startYear","averageRating","numVotes"]].head())


# merge primary language/region

akas = pd.read_csv(
    DATA_DIR + "title.akas.tsv.gz",
    sep="\t",
    na_values="\\N",
    dtype={"titleId":"string"},
    usecols=["titleId","isOriginalTitle","region","language"]
)

akas_primary = akas[akas["isOriginalTitle"]==1].drop_duplicates("titleId")
horror = horror.merge(akas_primary, left_on="tconst", right_on="titleId", how="left") \
               .drop(columns=["titleId"])
print(horror[["primaryTitle","language","region"]].head())

#new method for merge primary language/region

import pandas as pd

DATA_DIR = "/Users/Ryan/Desktop/horror_data_gathering/"

# --- re-load AKAs with only what we need ---
akas = pd.read_csv(
    DATA_DIR + "title.akas.tsv.gz",
    sep="\t",
    na_values="\\N",
    dtype={"titleId": "string"},
    usecols=["titleId", "isOriginalTitle", "region", "language"]
)

# Prefer original-title language if present
orig_lang = (
    akas[akas["isOriginalTitle"] == 1]
      .dropna(subset=["language"])
      .drop_duplicates("titleId")[["titleId", "language"]]
      .rename(columns={"language": "language_pref"})
)

# Otherwise, take the most frequent language across all AKAs for that title
def mode_or_first(s):
    m = s.mode(dropna=True)
    if len(m) > 0:
        return m.iloc[0]
    # if all NaN or empty, return NaN
    return pd.NA

lang_fallback = (
    akas.dropna(subset=["language"])
        .groupby("titleId")["language"]
        .agg(mode_or_first)
        .reset_index()
        .rename(columns={"language": "language_fallback"})
)

# Combine to a single best_language
lang_best = (orig_lang
             .merge(lang_fallback, on="titleId", how="outer"))
lang_best["language_best"] = lang_best["language_pref"].combine_first(lang_best["language_fallback"])
lang_best = lang_best[["titleId", "language_best"]]

# Region preference:
#   Use US if present for that title
has_us = (
    akas[akas["region"] == "US"]
        .drop_duplicates("titleId")[["titleId"]]
        .assign(region_us="US")
)

#     Else use the most frequent non-null region
region_fallback = (
    akas.dropna(subset=["region"])
        .groupby("titleId")["region"]
        .agg(mode_or_first)
        .reset_index()
        .rename(columns={"region": "region_fallback"})
)

region_best = has_us.merge(region_fallback, on="titleId", how="outer")
region_best["region_best"] = region_best["region_us"].combine_first(region_best["region_fallback"])
region_best = region_best[["titleId", "region_best"]]

# Merge both language + region into your horror dataframe
horror = horror.merge(lang_best, left_on="tconst", right_on="titleId", how="left") \
               .merge(region_best, on="titleId", how="left") \
               .drop(columns=["titleId"])

# 5) Quick check
print(
    horror[["primaryTitle", "language_best", "region_best"]]
      .head(10)
)

print("Non-null language rows:", horror["language_best"].notna().sum(), "of", len(horror))
print("Non-null region rows:", horror["region_best"].notna().sum(), "of", len(horror))


# add directors and writers

import pandas as pd

crew = pd.read_csv(
    DATA_DIR + "title.crew.tsv.gz",
    sep="\t",
    na_values="\\N",
    dtype={"tconst": "string"},
    usecols=["tconst", "directors", "writers"]
)

horror = horror.merge(crew, on="tconst", how="left")

# Quick verification
print("✅ Step 4 done — merged crew data")
print("Columns now:", horror.columns.tolist()[:12])
print("Rows:", len(horror))
print(horror[["primaryTitle", "directors", "writers"]].head(5))

# Build a lookup: nconst -> primaryName 
names = pd.read_csv(
    DATA_DIR + "name.basics.tsv.gz",
    sep="\t",
    na_values="\\N",
    dtype={"nconst":"string"},
    usecols=["nconst","primaryName"]
)
id_to_name = dict(zip(names["nconst"], names["primaryName"]))

def ids_to_names(id_field, max_people=2):
    """Turn 'nm1234,nm5678' -> 'Person A, Person B' (limit to first N)."""
    if pd.isna(id_field):
        return pd.NA
    ids = [x.strip() for x in str(id_field).split(",") if x.strip()]
    ids = ids[:max_people]
    names_ = [id_to_name.get(i) for i in ids if i in id_to_name]
    return ", ".join([n for n in names_ if pd.notna(n)]) if names_ else pd.NA

# Create readable columns
horror["DirectorsNames"] = horror["directors"].apply(ids_to_names)
horror["WritersNames"]   = horror["writers"].apply(ids_to_names)

# Quick verify
print("✅ Mapped crew IDs to names")
print(horror[["primaryTitle","DirectorsNames","WritersNames"]].head(5))

# add top billed cast

import pandas as pd

# Load principals (role listings) ---
print("Loading title.principals …")
principals = pd.read_csv(
    DATA_DIR + "title.principals.tsv.gz",
    sep="\t",
    na_values="\\N",
    dtype={"tconst":"string", "nconst":"string", "category":"string"},
    usecols=["tconst","nconst","category","ordering"]
)
print("✅ Principals loaded:", len(principals))
print(principals.head(3))

# --- 5B) Keep only actors/actresses and top billing (ordering <= 2) ---
print("\nFiltering to actors/actresses, top 1–2 billing …")
# Make sure ordering is numeric
principals["ordering"] = pd.to_numeric(principals["ordering"], errors="coerce")
cast_top = principals[
    principals["category"].isin(["actor","actress"])
    & (principals["ordering"] <= 2)
].copy()
print("✅ Top-billed actor/actress rows:", len(cast_top))
print(cast_top.head(3))

# Map person IDs -> names 
try:
    id_to_name
except NameError:
    print("\nLoading name.basics for ID->name mapping …")
    names = pd.read_csv(
        DATA_DIR + "name.basics.tsv.gz",
        sep="\t",
        na_values="\\N",
        dtype={"nconst":"string"},
        usecols=["nconst","primaryName"]
    )
    id_to_name = dict(zip(names["nconst"], names["primaryName"]))
    print("✅ Names loaded:", len(names))

print("\nMapping cast IDs to names …")
cast_top["PersonName"] = cast_top["nconst"].map(id_to_name)
print("Sample mapped names:")
print(cast_top[["tconst","nconst","PersonName","ordering"]].head(5))

# Collapse to one row per movie: "TopCast" as a comma-separated string 
print("\nCollapsing to one row per movie …")
top_cast_names = (
    cast_top
    .dropna(subset=["PersonName"])
    .sort_values(["tconst","ordering"])
    .groupby("tconst")["PersonName"]
    .apply(lambda s: ", ".join(s.dropna().unique()))
    .reset_index(name="TopCast")
)
print("✅ TopCast rows:", len(top_cast_names))
print(top_cast_names.head(5))

# Merge TopCast into your horror table 
print("\nMerging TopCast into horror …")
before_cols = set(horror.columns)
horror = horror.merge(top_cast_names, on="tconst", how="left")
after_cols = set(horror.columns)
print("✅ Merge complete")
print("New columns added:", list(after_cols - before_cols))
print("Rows (should be unchanged):", len(horror))

# Quick verification sample 
print("\nSample with cast:")
print(horror[["primaryTitle","DirectorsNames","WritersNames","TopCast"]].head(10))

# Optional: how many have non-null TopCast?
non_null_cast = horror["TopCast"].notna().sum()
print(f"\nMovies with TopCast: {non_null_cast} of {len(horror)}")


#saving then moving to collab because this is using too much memory

# Minimal set of columns to keep (add/remove as you like)
keep_cols = [
    "tconst","primaryTitle","originalTitle","startYear","runtimeMinutes","genres",
    "averageRating","numVotes","language_best","region_best",
    "DirectorsNames","WritersNames","TopCast"
]

horror_small = horror[keep_cols].copy()

#Compressed CSV 
horror_small.to_csv("horror_imdb_enriched.csv.gz", index=False, compression="gzip")

