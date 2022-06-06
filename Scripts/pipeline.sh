#!/bin/sh

###################################################################
#Script Name	: pipeline.sh                                                                                          
#Description	: this script runs the pipeline to predict allele inheritance in Strains                                                                               
#Args           	: 3 arguments are required                                                                                      
#Author       	: Soukaina Timouma                                             
#Email         	: soukaina.timouma@manchester.ac.uk                                           
###################################################################

one=false
two=false
three=false
four=false

if [ "$1" = "" ]; then
    echo "Error: missing arguments"
    echo "./pipeline.sh Strain parentA ..."
    exit 1
    break
fi

if [ "$2" = "" ]; then
    echo "Error: missing arguments"
    echo "./pipeline.sh Strain parentA ..."
    exit 1
    break
fi


if [ "$3" = "" ]; then
    echo "This Strain will be annotated with 1 parent"
    one=true
fi

if [ "$4" = "" ]; then
    echo "This Strain has 2 parents"
    two=true
fi


if [ "$4" != "" ] && [ "$5" = "" ]; then
    echo "This Strain has 3 parents"
    three=true
fi


if [ "$4" != "" ] && [ "$5" != "" ] && [ "$6" = "" ]; then
    echo "This Strain has 4 parents"
    four=true
fi



########################### 1 Parental organism

if [ "$one" = true ]; then

	echo "Strain file: $1"
	echo "Parent A file: $2"


	echo "\n--------Creation of BLAST databases--------------"

	makeblastdb -in ../Data/$1_prot.fasta -out ../Results/0_BlastDB/$1 -dbtype prot
	makeblastdb -in ../Data/$2_prot.fasta -out ../Results/0_BlastDB/$2 -dbtype prot


	echo "\n-----blastp------"

	mkdir -p ../Results/1_Raw_Blastp_output
	mkdir -p ../Results/2_Best_hits
	mkdir -p ../Results/3_Orthologs_Paralogs
	mkdir -p ../Results/4_Parental_alleles_prediction


	#Run blastp and parse:
		# Strain_X_ParentA(orthologs):
		echo "\n-$1 query VS $2 database-"
		blastp -query ../Data/$1_prot.fasta -db ../Results/0_BlastDB/$2 -out ../Results/1_Raw_Blastp_output/output_blastp_$1_vs_$2.txt -num_threads 4 -num_alignments 1
		echo "---------------Parsing BLAST output file---------------"
		perl blast_parser.pl ../Results/1_Raw_Blastp_output/output_blastp_$1_vs_$2.txt $1 $2 ../Results/2_Best_hits #->Strain-ParentA.csv

		# ParentA_X_Strain(orthologs):
		echo "\n-$2 query VS $1 database-"
		blastp -query ../Data/$2_prot.fasta -db ../Results/0_BlastDB/$1 -out ../Results/1_Raw_Blastp_output/output_blastp_$2_vs_$1.txt -num_threads 4 -num_alignments 1 
		echo "---------------Parsing BLAST output file---------------"
		perl blast_parser.pl ../Results/1_Raw_Blastp_output/output_blastp_$2_vs_$1.txt $2 $1 ../Results/2_Best_hits #->ParentA-Strain.csv

		# Strain_X_Strain(paralogs):
		echo "\n-$1 query VS $1 database-"
		blastp -query ../Data/$1_prot.fasta -db ../Results/0_BlastDB/$1 -out ../Results/1_Raw_Blastp_output/output_blastp_$1_vs_$1.txt -num_threads 4 -outfmt "6 qseqid sseqid qlen slen length nident mismatch positive gapopen gaps pident ppos qstart qend sstart send evalue bitscore score"


		# ParentA_X_ParentA(paralogs):
		echo "\n-$2 query VS $2 database-"
		blastp -query ../Data/$2_prot.fasta -db ../Results/0_BlastDB/$2 -out ../Results/1_Raw_Blastp_output/output_blastp_$2_vs_$2.txt -num_threads 4 -outfmt "6 qseqid sseqid qlen slen length nident mismatch positive gapopen gaps pident ppos qstart qend sstart send evalue bitscore score"

	echo "\n ---------------Search 1:1 orthologies Strain - Parent A ---------------"
	python3 orthologs.py --name $1_$2 --ortho1 ../Results/2_Best_hits/$1-$2.csv --ortho2 ../Results/2_Best_hits/$2-$1.csv 


fi




