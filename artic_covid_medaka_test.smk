#guppyplex needs in_dir,batch_name,max_min
#nums = [01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
#ruleorder: guppyplex > artic_medaka_minion > run_qc > run_samtools_depth
configfile:'/home/ubuntu/data/belson/SARS-Cov2/2021.08.11/scripts/artic_covid_medaka_test_config.yaml'
barcodes = config['batches_barcodes']['20210810_1431_MN34547_FAO36609_68382386']
root_dir='/home/ubuntu/data/belson/test_data/2021.08.11/20210810_1431_MN34547_FAO36609_68382386'
results='/home/ubuntu/data/belson/test_data/2021.08.11/guppyplexed'
scheme = config['scheme']
min = config['max_length'][scheme]['min']
max = config['max_length'][config['scheme']]['max']
#batch_name = config['batches_barcodes'].key()
batch_name = '20210810_1431_MN34547_FAO36609_68382386'
medaka_model = 'r941_min_high_g360'
rule all:
	input:
		expand('{results}/{barcode}/{barcode}_guppyplex.fastq',results=results,barcode=barcodes),
		expand('{results}/{barcode}/{batch_name}_{barcode}.consensus.fasta',results=results,batch_name=batch_name,barcode=barcodes),
		expand('{results}/{barcode}/qc/{batch_name}_{barcode}.trimmed.rg.sorted.bam.depth',results=results,batch_name=batch_name,barcode=barcodes),
		expand('{results}/{barcode}/qc/{batch_name}_{barcode}.qc.csv',results=results,batch_name=batch_name,barcode=barcodes)

rule guppyplex:
	input:
		expand('{root}/{{barcode}}',root=root_dir,barcode=barcodes)
	output:
		'{results}/{barcode}/{barcode}_guppyplex.fastq'
	conda:
		'/home/ubuntu/data/belson/SARS-Cov2/2021.08.11/scripts/artic.yml'
	shell:
		'bash artic_covid_medaka.sh guppyplex {min} {max} {input} {batch_name} {output}'

rule artic_medaka_minion:
	input:
		#p_schemes = '/home/ubuntu/data/belson/test_data/2021.08.11/20210810_1431_MN34547_FAO36609_68382386',
		gu = rules.guppyplex.output
	output:
		'{results}/{barcode}/{batch_name}_{barcode}.consensus.fasta'
	conda:
		'/home/ubuntu/data/belson/SARS-Cov2/2021.08.11/scripts/artic.yml'
	shell:
		'bash artic_covid_medaka.sh minion {root_dir} {scheme} {medaka_model} {input.gu} {wildcards.results}/{wildcards.barcode}/{wildcards.batch_name}_{wildcards.barcode}'

rule run_qc:
	input:
		ref = expand('{root}/{scheme}/SARS-CoV-2.reference.fasta',root=root_dir,scheme=scheme),
		con = '{results}/{barcode}/{batch_name}_{barcode}.consensus.fasta',
		bam = '{results}/{barcode}/{batch_name}_{barcode}.primertrimmed.rg.sorted.bam',
		amm = rules.artic_medaka_minion.output
	output:
		'{results}/{barcode}/qc/{batch_name}_{barcode}.qc.csv'
	shell:
		'python /home/ubuntu/data/belson/SARS-Cov2/2021.08.11/connor_lab/ncov2019-artic-nf/bin/qc.py --nanopore --outfile {output} --sample {wildcards.batch_name}_{wildcards.barcode} --ref {input.ref} --bam {input.bam} --fasta {input.con}'


rule run_samtools_depth:
	input:
		'{results}/{barcode}'
	output:
		'{results}/{barcode}/qc/{batch_name}_{barcode}.trimmed.rg.sorted.bam.depth'
	shell:
		'samtools depth -aa -o {output} {input}/{wildcards.batch_name}_{wildcards.barcode}.primertrimmed.rg.sorted.bam'