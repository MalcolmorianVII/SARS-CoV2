from Bio.Seq import Seq
from Bio import SeqIO
import pandas as pd

primers_file = 'C:\\Users\\Belson\\Documents\\SNR-SARS-Cov\\Midnight_SARS_CoV2_sequences_only.xlsx'

ref_file = 'C:\\Users\\Belson\\Documents\\SNR-SARS-Cov\\SARS-CoV-2.reference.fasta'

ref_seq = SeqIO.read(ref_file,"fasta").seq


df = pd.read_excel(primers_file,engine='openpyxl')
df['Start'] = ""
df['End']   = ""
for index,row in df.iterrows():
    primer = row['Sequence']
    pos = ref_seq.find(primer)
    if pos == -1:   # Reverse primer
        reversed = Seq(primer).reverse_complement()
        pos = ref_seq.find(reversed)
    df['Start'][index] = pos
    df['End'][index] = len(primer) + pos
print(df)

