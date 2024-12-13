import pandas as pd

csv_file_path = 'Compound_OBP_binding.csv'
data = pd.read_csv(csv_file_path)

target_molecules = {
    'C4H8O2 丁酸': 'butanoic acid',
    'C13H22O 二环己基酮': 'Dicyclohexyl ketone',
    'C11H22O 十一醛': 'Undecanal / Hendecanal / Undecylic aldehyde',
    'C2H4O2 乙酸': 'acetic acid',
    'C7H14O 2-庚酮': '2-heptanone',
    'C6H12O 己醛': 'hexanal',
    'C5H8O 环戊酮': 'cyclopentanone',
    '3-羟基-2-丁酮': '3-hydroxy-2-butanone',
    '2-戊酮': '2-pentanone'
}

def process_binding_value(value):
    if isinstance(value, str) and '>' in value:
        return float(value.replace('>', '')) + 0.1 
    try:
        return float(value)
    except ValueError:
        return None

def find_best_obp(data, target_molecules):
    best_obps = {}
    for chinese_name, english_name in target_molecules.items():
        compound_data = data[data['Compound name'].str.lower() == english_name.lower()]
        if not compound_data.empty:
            best_obp = None
            best_obp_score = float('-inf')
            for obp in data.columns[2:]:
                if obp not in ['CAS-number', 'Compound name']:
                    binding_value = compound_data[obp].values[0]
                    if pd.notna(binding_value):
                        processed_value = process_binding_value(binding_value)
                        if processed_value is not None:
                            other_binding_sum = data[obp].apply(process_binding_value).sum() - processed_value
                            score = processed_value / (processed_value + other_binding_sum)
                            if score > best_obp_score:
                                best_obp = obp
                                best_obp_score = score
            if best_obp:
                best_obps[chinese_name] = best_obp
    return best_obps

best_obps = find_best_obp(data, target_molecules)

output_file_path = 'Best_OBP_Combination.csv'
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.write('Molecule,OBP\n')
    file.write('\n')
    for molecule, obp in best_obps.items():
        file.write(f"{molecule},{obp}\n")

print(f"Best OBP combinations have been written to {output_file_path}")