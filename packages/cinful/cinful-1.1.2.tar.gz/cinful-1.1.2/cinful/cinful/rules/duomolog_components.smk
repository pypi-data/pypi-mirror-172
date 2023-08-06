import pandas as pd
import pyhmmer
from functools import reduce


SAMPLES, = glob_wildcards(config["outdir"] + "/01_orf_homology/{sample}_prodigal")
COMPONENTS, = glob_wildcards("{component}.verified.pep")


def load_blast(blastout, hasHeaders=False):
	if hasHeaders:
		blastpDF = pd.read_csv(blastout, sep = "\t")
	else:
		blastpDF = pd.read_csv(blastout, sep = "\t", names = ["qseqid","sseqid","pident","length","mismatch","gapopen","qstart","qend","sstart","send","evalue","bitscore"])
	return blastpDF

def load_hmm(hmmFile):
    with pyhmmer.plan7.HMMFile(hmmFile) as h:
        hmm = next(h)
    return hmm

def run_hmmsearch(queryFile, hmmFile):
	hmm = load_hmm(hmmFile)
	with pyhmmer.easel.SequenceFile(queryFile) as seq_file:
		sequences = [ seq.digitize(hmm.alphabet) for seq in seq_file ]
	pipeline = pyhmmer.plan7.Pipeline(hmm.alphabet)
	hits = pipeline.search_hmm(hmm, sequences) # Has lots of goodies!

	return hits , hmm.name.decode() # [hit.name.decode() for hit in hmmerOut]





rule merged_results:
	input:
		nr_csv = config["outdir"] + "/01_orf_homology/prodigal_out.all.nr_expanded.csv",

		microcins = config["outdir"] + "/01_orf_homology/microcins/blast_v_hmmer.csv",
		microcin_pepHash = config["outdir"] + "/00_dbs/microcins.verified.pephash.csv",

		immunity_proteins = config["outdir"] + "/01_orf_homology/immunity_proteins/blast_v_hmmer.csv",
		immunity_protein_pepHash = config["outdir"] + "/00_dbs/immunity_proteins.verified.pephash.csv",

		unfilteredCvaB = config["outdir"] + "/01_orf_homology/CvaB/blast_v_hmmer.csv",
		QC_Cvab=config["outdir"] + "/01_orf_homology/CvaB/QC.csv",

		CvaB_pepHash = config["outdir"] + "/00_dbs/CvaB.verified.pephash.csv",

		unfilteredMFP = config["outdir"] + "/01_orf_homology/MFP/blast_v_hmmer.csv",
		QC_MFP=config["outdir"] + "/01_orf_homology/MFP/QC.csv",

		MFP_pepHash = config["outdir"] + "/00_dbs/MFP.verified.pephash.csv"

	output:
		config["outdir"] + "/02_homology_results/all_merged.csv"
	run:
		nrDF = pd.read_csv(input.nr_csv)
		microcinDF = pd.read_csv(input.microcins)
		immunity_proteinDF = pd.read_csv(input.immunity_proteins)

		QC_CvabDF = pd.read_csv(input.QC_Cvab)
		unfilteredCvaBDF = pd.read_csv(input.unfilteredCvaB)

		QC_MFPDF = pd.read_csv(input.QC_MFP)
		unfilteredMFPDF = pd.read_csv(input.unfilteredMFP)

		microcin_pepHashDF = pd.read_csv(input.microcin_pepHash)
		immunity_protein_pepHashDF = pd.read_csv(input.immunity_protein_pepHash)
		CvaB_pepHashDF = pd.read_csv(input.CvaB_pepHash)
		MFP_pepHashDF = pd.read_csv(input.MFP_pepHash)

		bestCvaB = unfilteredCvaBDF[unfilteredCvaBDF["qseqid"].isin(QC_CvabDF["id"]) ]
		bestMFP = unfilteredMFPDF[unfilteredMFPDF["qseqid"].isin(QC_MFPDF["id"]) ]

		microcinDF["verified"] = microcinDF["qseqid"].isin(microcin_pepHashDF["pephash"])
		immunity_proteinDF["verified"] = immunity_proteinDF["qseqid"].isin(immunity_protein_pepHashDF["pephash"])
		bestCvaB["verified"] = bestCvaB["qseqid"].isin(CvaB_pepHashDF["pephash"])
		bestMFP["verified"] = bestMFP["qseqid"].isin(MFP_pepHashDF["pephash"])

		componentDFs = [microcinDF, immunity_proteinDF, bestCvaB, bestMFP]
		mergedDf = pd.concat(componentDFs)
		mergedDf_nr = mergedDf.merge(nrDF, left_on ="qseqid", right_on= "pephash")
		mergedDf_nr.to_csv(output[0], index = None)
