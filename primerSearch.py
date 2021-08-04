from Bio.Seq import Seq
from Bio import SeqIO
import pandas as pd

primers_file = 'C:\\Users\\Belson\\Documents\\SNR-SARS-Cov\\Midnight_SARS_CoV2_sequences_only.xlsx'

ref_file = 'C:\\Users\\Belson\\Documents\\SNR-SARS-Cov\\SARS-CoV-2.reference.fasta'

ref_seq = SeqIO.read(ref_file,"fasta").seq


primer_df = pd.read_excel(primers_file,engine='openpyxl') # Representing the primers file as pandas dataframe

#Adding two columns ,Start & End to the primer_df
primer_df['Start'] = ""
primer_df['End']   = ""

# Iterating over the primer_df and finding the Start & End pos of the primers
for index,row in primer_df.iterrows():
    primer = row['Sequence']
    pos = ref_seq.find(primer)
    if pos == -1:   # Reverse primer
        reversed = Seq(primer).reverse_complement()
        pos = ref_seq.find(reversed)
    primer_df['Start'][index] = pos
    primer_df['End'][index] = len(primer) + pos
print(primer_df)

