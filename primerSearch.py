from Bio.Seq import Seq
from Bio import SeqIO
import pandas as pd

primers_file = 'C:\\Users\\Belson\\Documents\\SNR-SARS-Cov\\Midnight_SARS_CoV2_sequences_only.xlsx'

ref_file = 'C:\\Users\\Belson\\Documents\\SNR-SARS-Cov\\SARS-CoV-2.reference.fasta'

ref_seq = SeqIO.read(ref_file, "fasta").seq

primers_df = pd.read_excel(primers_file, engine='openpyxl')  # Representing the primers file as pandas dataframe

# Adding two columns ,Start & End to the primers_df
primers_df['Start'] = ""
primers_df['End'] = ""


# Iterating over the primers_df and finding the Start & End pos of the primers
for index, row in primers_df.iterrows():
    primer_seq = row['Sequence']
    pos = ref_seq.find(primer_seq)
    if pos == -1:  # That means a reverse primer
        rev_comp = Seq(primer_seq).reverse_complement()
        pos = ref_seq.find(rev_comp)
    primers_df['Start'][index] = pos
    primers_df['End'][index] = len(primer_seq) + pos
print(primers_df)
