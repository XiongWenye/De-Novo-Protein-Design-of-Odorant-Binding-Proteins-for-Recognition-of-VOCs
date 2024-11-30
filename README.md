# De Novo Protein Design of Odorant Binding Proteins for VOCs Recognition

Set up && installation

1.clone rf_diffusion_all_atom from baker lab
'''
git clone https://github.com/baker-laboratory/rf_diffusion_all_atom.git
cd rf_diffusion_all_atom
'''
you should also follow the step of https://github.com/baker-laboratory/rf_diffusion_all_atom?tab=readme-ov-file

2.To generate the Protein for OCTANAL Recognition, download the pdb of 2QHU from https://www.rcsb.org/structure/2QHU    after that, add it to the input folder of RFAA

3.Run the following code in the terminal

'''
~/apptainer/x86_64/bin/apptainer run --nv rf_se3_diffusion.sif -u run_inference.py inference.deterministic=True diffuser.T=100 inference.output_prefix=output/ligand_only/sample inference.input_pdb=input/2qhu.pdb contigmap.contigs=[\'150-150\'] inference.ligand=OYA inference.num_designs=1 inference.design_startnum=0
'''
