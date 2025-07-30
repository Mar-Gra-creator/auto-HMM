# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import subprocess
import glob
import re
import shutil
import os
from Bio import SeqIO

def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        'Error: Creatboing directory. ' + directory
    
def remove_thing(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

def empty_directory(path):
    for i in glob.glob(os.path.join(path, '*')):
        remove_thing(i)

empty_directory('./ShortsAndLong/')
empty_directory('./Clustered/')
empty_directory('./ClustalO/')
empty_directory('./HMM/')

create_folder('./ShortsAndLong/')
create_folder('./Clustered/')
create_folder('./ClustalO/')
create_folder('./HMM/')

#set parameters
autor_of_hmm = 'MKrysinska'
cutoff = 50
cd_hit_treshold = 0.80
cd_hit_word_length = 5

first_proteins = {}
names = []

#cutoff

for file in glob.glob('*.fasta'):

    
    
    short_sequences = []
    longer_sequences = []
    
    handle = open(file,"r")
    
    name_base_split = file.split('.')
    name_base = name_base_split[0]
    
    proteins = list(SeqIO.parse(handle, 'fasta'))
    start_homologue = proteins[0].description
    first_proteins.update({file:start_homologue})
    for protein in proteins:
        if len(protein.seq) >= cutoff:
            longer_sequences.append(protein)
        else:
            short_sequences.append(protein)
            
    handle.close()
    
    with open(('./ShortsAndLong/' + name_base + '_longer_than_' + str(cutoff) + '_Longer.fasta'), 'w') as outputLonger_handle:
        SeqIO.write(longer_sequences, outputLonger_handle, "fasta")
        
    with open(('./ShortsAndLong/' + name_base + '_shorter_than_' + str(cutoff) + '_Shorter.fasta'), 'w') as outputShorter_handle:
        SeqIO.write(short_sequences, outputShorter_handle, "fasta")


#cd-hit

for file in glob.glob('./ShortsAndLong/*Longer.fasta'):
    get_file_name = file.split('/')
    file_name = get_file_name[-1].split('.')
    cutoff_sub = re.sub('\.','_', str(cutoff))
    file_out = './Clustered/' + file_name[0] + '_cdhit_' + cutoff_sub + '_clustered.fasta'
    print(file_out)
    subprocess.run(('cd-hit -i %s -c %s -n %s -M 0 -T 0 -o %s' % (file , str(cd_hit_treshold), str(cd_hit_word_length), file_out)),shell=True)
    
#align clustered
    
for file in glob.glob('./Clustered/*.fasta'):
    get_file_name = file.split('/')
    file_name = get_file_name[-1].split('.')
    out = './ClustalO/' + file_name[0] + '_aln.fasta'
    subprocess.run(('clustalo -i %s -o %s --auto' % (file , out)),shell=True)

#make HMM    

for file in glob.glob('./ClustalO/*.fasta'):
    
    get_file_name = file.split('/')
    file_name = get_file_name[-1].split('.') 
    split_file_name = file.split('_longer_than_')
    splited_name_to_map_path = str(split_file_name[0] + '.fasta').split('/')
    splited_name_to_map = splited_name_to_map_path[-1]
    first_protein_path = first_proteins[splited_name_to_map]
    out = './HMM/' + file_name[0] + '.hmm'
    name_of_hmm = file_name[0] + ' # ' + autor_of_hmm + ', homologues of ' + \
    split_file_name[0] + ', cd-hit ' + str(cd_hit_treshold) + '(word length: ' + \
    str(cd_hit_word_length) + ')'
    names.append(name_of_hmm)
    subprocess.run("hmmbuild %s %s" % (out, file),shell=True)

with open('HMM_names.txt', 'w') as save_names:
    for i in names:
        save_names.write((i + '\n'))
