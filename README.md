# De Novo Protein Design of Odorant Binding Proteins for VOCs Recognition

Set up && installation

## 1.clone rf_diffusion_all_atom from baker lab

``` 
git clone https://github.com/baker-laboratory/rf_diffusion_all_atom.git
cd rf_diffusion_all_atom
```

you should also follow the step of https://github.com/baker-laboratory/rf_diffusion_all_atom?tab=readme-ov-file

## 2. Natural OBP selection
To generate the Protein for VOC Recognition, we download the pdb of all possible PDB.
We have also written a a Python script to analyze the binding affinities of various compounds to different OBP (Odorant Binding Proteins) and identify the best OBP combinations for specified target molecules based on a new scoring method. After that, we successfully found the best OBP to detect Hexanal, Octanal, Nonanal respectively.

We also combine the two structures (OBP and its corresponding VOC) by simple concatenation. Then we got our OBP with ligands: BminOBP9_S24P_lig.pdb, SaveOBP9_lig.pdb, AgamCSP3_lig.pdb  

## 3.RFDiffusion_AA Backbone Design
We put all these natural OBP into training.
For time reasons, we’re only generating 15 output structures (inference.num_designs=15). Generally, you’ll
want to create hundreds of different structures and then filter them for those with the properties which you desire.
Also, we’re reducing the number of diffusion timesteps taken (diffuser.T=100).

Here is an example of running the backbone of Hexanal:


```
~/apptainer/x86_64/bin/apptainer run --nv rf_se3_diffusion.sif -u run_inference.py inference.deterministic=True diffuser.T=100 inference.output_prefix=output/hexanal/sample
inference.input_pdb=input/BminOBP9_S24P_lig.pdb contigmap.contigs=[\'120-140\'] inference.ligand=UNK
inference.num_designs=15 inference.design_startnum=0
```

## 4.Analysis of generated backbones.
While RFdiffusionAA attempts to come up with biologically relevant backbone conformations, the particular backbones it comes up with do not always accord with what you are interested in.

The filtering process is going to be dependent on the particular design goals of the specific project you’re doing.
Factors such as radius of gyration, size and type of secondary structural elements, contact order, and burial of
certain residues (e.g. the ligand) can all be assessed with tools such as RosettaScripts and PyRosetta, as well as
other structural examination programs. The important thing to keep in mind when building filters is that sidechains
and sequences have yet to be assigned. As such, all the filters at this stage of the pipeline should be ones which
are based on the backbone only.
Note that often times the best filtering approach is a manual one – simply open up the structures in a viewing
program like PyMol and use your biochemical knowledge about the system to determine which structures have the
possibility to work, and which are obviously silly.  
After picking the possible backbone, now we have a possible one for each VOC. We will further design the protein sequence using LigandMPNN.  

## 5.LigandMPNN design of protein seqeunces.
Like regular RFdiffusion, RFdiffusionAA only creates backbone structures, with the added residues represented in
the output structure as glycine. Before using these results, sequences need to be generated. Just like RFdiffusionAA
is a version of RFdiffusion trained to be ligand-aware, LigandMPNN is a ligand-aware version of ProteinMPNN.
We’ll be using LigandMPNN to assign amino acid identities to the generated residues.  

Giving Nonanal as an example:
```
conda activate ligandmpnn_env
python run.py \
--checkpoint_ligand_mpnn ./LigandMPNN/model_params/ligandmpnn_v_32_010_25.pt \
--checkpoint_path_sc ./LigandMPNN/model_params/ligandmpnn_sc_v_32_002_16.pt \
--pdb_path "./inputs/nonanal_rfaa.pdb" \
--out_folder "./outputs/nonanal" \
--model_type "ligand_mpnn" \
--number_of_batches 1 \
--batch_size 10 \
--pack_side_chains 1 \
--number_of_packs_per_design 1 \
--pack_with_ligand_context 1
```

## 6.Analysis of generated sequences
For the generated sequences, we want it to combine the target VOC better than natural OBP does. Also, we want it to be less affinity to other VOC. So we test each sample with AutoDock and select the best generated OBP among them.

Also, we performed a Pyrosetta Scoring Function with relaxation on both natural OBP and denovo OBPs. We were glad to find that the denovo OBPs performed better both in affinity by AutoDock and stability by Pyrosetta Scoring Function.

## 7.Refolding
One approach which has been shown to work quite well to improve the success rate of designs is the concept of
“forward folding”. That is, after using a particular structure to design a sequence, can you recapitulate the structure
from that sequence? The concept is that under experimental conditions, the only information you’re providing is
the input protein sequence. You’re therefore looking for designs which can robustly produce the desired structure
from that sequence.

Here we use ESM Fold to refold the generated sequence. 