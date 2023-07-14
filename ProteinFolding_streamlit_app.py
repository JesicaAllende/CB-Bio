#➿ProteinFolding is a predictor of single-sequence protein structures based on the ESM-2 language model.
import streamlit as st
from stmol import showmol
import py3Dmol
import requests
import biotite.structure.io as bsio

st.sidebar.title('➿ProteinFolding')
st.sidebar.write('[*ProteinFolding*](https://proteinfolding.com/about) is a predictor of single-sequence protein structures based on the ESM-2 language model. For more information, please check [Evolutionary-scale prediction of atomic level protein structure with a language model](https://www.biorxiv.org/content/10.1101/2022.07.20.500902v3) and [AI tools are designing entirely new proteins that could transform medicine](https://www.nature.com/articles/d41586-023-02227-y) published in *Nature*.')

def render_mol(pdb):
    pdbview = py3Dmol.view()
    pdbview.addModel(pdb,'pdb')
    pdbview.setStyle({'cartoon':{'color':'spectrum'}})
    pdbview.setBackgroundColor('white')#('0xeeeeee')
    pdbview.zoomTo()
    pdbview.zoom(2, 800)
    pdbview.spin(True)
    showmol(pdbview, height = 500,width=800)

# Protein sequence input
DEFAULT_SEQ = "MVTGGMASKWDQKGMDIAYEEAALGYKEGGVPIGGCLINNKDGSVLGRGHNMRFQKGSATLHGEISTLENCGRLEGKVYKDTTLYTTLSPCDMCTGAIIMYGIPRCVVGENVNFKSKGEKYLQTRGHEVV VVDDERCKKI MKQFIDERPQDWFEDIGE"
txt = st.sidebar.text_area('Input sequence', DEFAULT_SEQ, height=275)

# ProteinFolding
def update(sequence=txt):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.post('https://api.esmatlas.com/foldSequence/v1/pdb/', headers=headers, data=sequence)
    name = sequence[:3] + sequence[-3:]
    pdb_string = response.content.decode('utf-8')

    with open('predicted.pdb', 'w') as f:
        f.write(pdb_string)

    struct = bsio.load_structure('predicted.pdb', extra_fields=["b_factor"])
    b_value = round(struct.b_factor.mean(), 4)

    # Display protein structure
    st.subheader('Visualization of predicted protein structure')
    render_mol(pdb_string)

    # plDDT value is stored in the B-factor field
    st.subheader('plDDT')
    st.write('plDDT is a per-residue estimate of the confidence in prediction on a scale from 0-100.')
    st.info(f'plDDT: {b_value}')

    st.download_button(
        label="Download PDB",
        data=pdb_string,
        file_name='predicted.pdb',
        mime='text/plain',
    )

predict = st.sidebar.button('Predict', on_click=update)

if not predict:
    st.warning('👈 Enter protein sequence data here!')
