# creating preprocessing function
def Preprocessor(df):
    # dropping the playerstats below season 1982 as it contains some missing stats
    df = df[df["Season"] > 1981]
    # filling nan values with 0 because the missing values are percentages like 3P% they are nan because player as not scored 3P and similar for other
    df = df.fillna(0)
    # dropping useless columns
    df = df.drop(columns=["Unnamed: 0.1", "Unnamed: 0"])

    return df