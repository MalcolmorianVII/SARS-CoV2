from Bio.Seq import Seq
from Bio import SeqIO
import pandas as pd

primers = 'C:\\Users\\Belson\\Documents\\SNR-SARS-Cov\\Midnight_SARS_CoV2_sequences_only.xlsx'

ref = 'C:\\Users\\Belson\\Documents\\SNR-SARS-Cov\\SARS-CoV2-2.reference.fasta'

ref_seq = SeqIO.read(ref,"fasta").seq

# print(ref_seq.find('ACCAACCAACTTTCGATCTCTTGT'))

df = pd.read_excel(primers,engine='openpyxl')
df['PrimerPos'] = ""
for index,row in df.iterrows():
    # print(ref_seq.find(row['Sequence']))
    pos = ref_seq.find(row['Sequence'])
    if pos == -1:
        reversed = Seq(row['Sequence']).reverse_complement()
        pos = ref_seq.find(reversed)
    df['PrimerPos'][index] = pos
print(df)

