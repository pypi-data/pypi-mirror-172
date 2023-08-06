from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import json
import seqhash


SAMPLES, = glob_wildcards("{sample}.fna")
if SAMPLES == []:
	SAMPLES, = glob_wildcards("{config[outdir]}/01_orf_homology/prodigal_out/{sample}.faa")

print("SAMPLES",SAMPLES)

def hmmsearch(queryFile, hmm):

	with pyhmmer.easel.SequenceFile(queryFile) as seq_file:
		sequences = [ seq.digitize(hmm.alphabet) for seq in seq_file ]
	pipeline = pyhmmer.plan7.Pipeline(hmm.alphabet)
	hits = pipeline.search_hmm(hmm, sequences)
	return hits

def build_hmm(alnFile):
	abc = pyhmmer.easel.Alphabet.amino()
 	builder = pyhmmer.plan7.Builder(alphabet=abc)

	with pyhmmer.easel.MSAFile(alnFile) as msa_file:
		msa_file.set_digital(abc)
		msa = next(msa_file)
  # MSA must have a name, otherwise building will fail
	if msa.name is None:
		msa.name = b"alignment"
	builder = pyhmmer.plan7.Builder(abc)
	background = pyhmmer.plan7.Background(abc)
	hmm, _, _ = builder.build_msa(msa, background)

	return hmm

def hasAllStandardAA(seq, alphabet="ACDEFGHIKLMNPQRSTVWY",ignore="*"):
	return (set(seq) - set(alphabet+ignore)) == set()


rule nonredundant_prodigal:
	input:
		expand(config["outdir"]+"/01_orf_homology/prodigal_out/{sample}.faa", sample=SAMPLES)
	output:
		fasta=config["outdir"] + "/01_orf_homology/prodigal_out.all.nr.faa",
		csv=config["outdir"] + "/01_orf_homology/prodigal_out.all.nr_expanded.csv"
	run:
		hashDict = {}
		idDict = {}
		print("INPUT:",input)
		for file in input:
			sample = file.split("01_orf_homology/prodigal_out/")[1].strip(".faa")
			with open(file) as handle:
				for seq_record in SeqIO.parse(handle, "fasta"):
					sequence = str(seq_record.seq)
					pephash = seqhash.seqhash(sequence.strip("*"),dna_type='PROTEIN')
					hashDict[pephash] = sequence
					descriptionParts = seq_record.description.split("#")
					start = descriptionParts[1].strip()
					stop = descriptionParts[2].strip()
					strand = descriptionParts[3].strip()
					contig = '_'.join(seq_record.id.split("_")[:-1])
					allStandardAA = hasAllStandardAA(sequence)
					seqID = f"{sample}|{contig}|{start}:{stop}:{strand}"
					idDict[seqID] = [pephash, sample, contig, start, stop, strand, allStandardAA, sequence]
		with open(output.fasta,"w") as fasta_file:
			for pephash in hashDict:
				outRecord = SeqRecord(
					Seq(hashDict[pephash]),
					id=pephash,
					description=""
				)
				SeqIO.write(outRecord, fasta_file, "fasta")

		idDF = pd.DataFrame.from_dict(idDict, orient="index", columns=["pephash","sample","contig","start","stop","strand","allStandardAA","seq"]).reset_index()
		idDF.rename(columns={'index': 'cinful_id'}, inplace = True)
#		idDF.columns = ["cinful_id","pephash","sample","contig","start","stop","strand","allStandardAA","seq"]
		idDF.to_csv(output.csv, index = None)


rule filter_microcin:
	input:
		config["outdir"] + "/01_orf_homology/prodigal_out.all.nr.faa"
	output:
		config["outdir"] + "/01_orf_homology/microcins/filtered_nr.fa"
	shell:
		"seqkit seq -m 30 -M 150 {input} | seqkit rmdup -s > {output}"



rule filter_immunity_protein:
	input:
		config["outdir"] + "/01_orf_homology/prodigal_out.all.nr.faa"
	output:
		config["outdir"] + "/01_orf_homology/immunity_proteins/filtered_nr.fa"
	shell:
		"seqkit seq -m 30 -M 250  {input} | seqkit rmdup -s > {output}"

rule filter_CvaB:
	input:
		config["outdir"] + "/01_orf_homology/prodigal_out.all.nr.faa"
	output:
		config["outdir"] + "/01_orf_homology/CvaB/filtered_nr.fa"
	shell:
		"seqkit seq -m 600 -M 800 {input} | seqkit rmdup -s > {output}"

rule filter_MFP:
	input:
		config["outdir"] + "/01_orf_homology/prodigal_out.all.nr.faa"
	output:
		config["outdir"] + "/01_orf_homology/MFP/filtered_nr.fa"
	shell:
		"seqkit seq -m 375 -M 450 {input} | seqkit rmdup -s > {output}"

# TODO: add a merge nonredundant step for each component
