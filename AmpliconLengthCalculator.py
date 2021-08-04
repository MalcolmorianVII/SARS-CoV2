import pandas as pd

primer_bed_file = 'C:\\Users\\Belson\\Documents\\SNR-SARS-Cov\\primer_bed.tsv.txt'

bed_df = pd.read_csv(primer_bed_file,delimiter='\t')    # BED file represented as pandas dataframe

# print(df)

Start = bed_df.iloc[0::2]['Start'].reset_index(drop=True)   # Gives the evenly indexed rows i.e the start of the entire amplicon
End = bed_df.iloc[1::2]['End'].reset_index(drop=True)       # Resetting so that can subtract with the Start column

# New df containing columns genome name,Amplicon Start & Stop position
# Amplicon_Length is for entire amplicon
out_df = pd.DataFrame({'Genome':bed_df.Genome,'Start':Start,
                       'End':End,'Amplicon_Length':End - Start})
print(out_df.dropna()) # dropna() comes in coz of bed_df.Genome(on line 14) creates NAN valued rows in "Genome" column
