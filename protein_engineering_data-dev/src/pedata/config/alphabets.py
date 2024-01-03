"""specification for different alphabets"""

# encoding for missing values
missing_value_enc = "*"
# and for padding
padding_value_enc = " "

# only valid (i.e. synthesizable) amino acids
valid_aa_alphabet = [
    "A",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "K",
    "L",
    "M",
    "N",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "V",
    "W",
    "Y",
]

# dictionary: which amino acid contains how many carbon atoms
# took out Selenocysteine "U"
valid_aa_Carbon_content = {
    "A": 3,
    "C": 3,
    "D": 4,
    "E": 5,
    "F": 9,
    "G": 2,
    "H": 6,
    "I": 6,
    "K": 6,
    "L": 6,
    "M": 5,
    "N": 4,
    "P": 5,
    "Q": 5,
    "R": 6,
    "S": 3,
    "T": 4,
    "V": 5,
    "W": 11,
    "Y": 9,
}

# amino acids and a missing value symbol
aa_alphabet = valid_aa_alphabet + [missing_value_enc]
padded_aa_alphabet = [padding_value_enc] + aa_alphabet

# only valid (i.e. synthesizable) DNA bases
valid_dna_alphabet = ["A", "C", "G", "T"]

# DNA bases and a missing value symbol
dna_alphabet = valid_dna_alphabet + [missing_value_enc]
padded_dna_alphabet = [padding_value_enc] + dna_alphabet

# do we actually handle RNA specially? Or just got with the DNA encoding?
rna_alphabet = ["A", "C", "G", "U", missing_value_enc]

atomic_symbols_names = [
    ["H", "Hydrogen"],
    ["He", "Helium"],
    ["Li", "Lithium"],
    ["Be", "Beryllium"],
    ["B", "Boron"],
    ["C", "Carbon"],
    ["N", "Nitrogen"],
    ["O", "Oxygen"],
    ["F", "Fluorine"],
    ["Ne", "Neon"],
    ["Na", "Sodium"],
    ["Mg", "Magnesium"],
    ["Al", "Aluminum"],
    ["Si", "Silicon"],
    ["P", "Phosphorus"],
    ["S", "Sulfur"],
    ["Cl", "Chlorine"],
    ["Ar", "Argon"],
    ["K", "Potassium"],
    ["Ca", "Calcium"],
    ["Sc", "Scandium"],
    ["Ti", "Titanium"],
    ["V", "Vanadium"],
    ["Cr", "Chromium"],
    ["Mn", "Manganese"],
    ["Fe", "Iron"],
    ["Co", "Cobalt"],
    ["Ni", "Nickel"],
    ["Cu", "Copper"],
    ["Zn", "Zinc"],
    ["Ga", "Gallium"],
    ["Ge", "Germanium"],
    ["As", "Arsenic"],
    ["Se", "Selenium"],
    ["Br", "Bromine"],
    ["Kr", "Krypton"],
    ["Rb", "Rubidium"],
    ["Sr", "Strontium"],
    ["Y", "Yttrium"],
    ["Zr", "Zirconium"],
    ["Nb", "Niobium"],
    ["Mo", "Molybdenum"],
    ["Tc", "Technetium"],
    ["Ru", "Ruthenium"],
    ["Rh", "Rhodium"],
    ["Pd", "Palladium"],
    ["Ag", "Silver"],
    ["Cd", "Cadmium"],
    ["In", "Indium"],
    ["Sn", "Tin"],
    ["Sb", "Antimony"],
    ["Te", "Tellurium"],
    ["I", "Iodine"],
    ["Xe", "Xenon"],
    ["Cs", "Cesium"],
    ["Ba", "Barium"],
    ["La", "Lanthanum"],
    ["Ce", "Cerium"],
    ["Pr", "Praseodymium"],
    ["Nd", "Neodymium"],
    ["Pm", "Promethium"],
    ["Sm", "Samarium"],
    ["Eu", "Europium"],
    ["Gd", "Gadolinium"],
    ["Tb", "Terbium"],
    ["Dy", "Dysprosium"],
    ["Ho", "Holmium"],
    ["Er", "Erbium"],
    ["Tm", "Thulium"],
    ["Yb", "Ytterbium"],
    ["Lu", "Lutetium"],
    ["Hf", "Hafnium"],
    ["Ta", "Tantalum"],
    ["W", "Tungsten"],
    ["Re", "Rhenium"],
    ["Os", "Osmium"],
    ["Ir", "Iridium"],
    ["Pt", "Platinum"],
    ["Au", "Gold"],
    ["Hg", "Mercury"],
    ["Tl", "Thallium"],
    ["Pb", "Lead"],
    ["Bi", "Bismuth"],
    ["Po", "Polonium"],
    ["At", "Astatine"],
    ["Rn", "Radon"],
    ["Fr", "Francium"],
    ["Ra", "Radium"],
    ["Ac", "Actinium"],
    ["Th", "Thorium"],
    ["Pa", "Protactinium"],
    ["U", "Uranium"],
    ["Np", "Neptunium"],
    ["Pu", "Plutonium"],
    ["Am", "Americium"],
    ["Cm", "Curium"],
    ["Bk", "Berkelium"],
    ["Cf", "Californium"],
    ["Es", "Einsteinium"],
    ["Fm", "Fermium"],
    ["Md", "Mendelevium"],
    ["No", "Nobelium"],
    ["Lr", "Lawrencium"],
    ["Rf", "Rutherfordium"],
    ["Db", "Dubnium"],
    ["Sg", "Seaborgium"],
    ["Bh", "Bohrium"],
    ["Hs", "Hassium"],
    ["Mt", "Meitnerium"],
    ["Ds", "Darmstadtium"],
    ["Rg", "Roentgenium"],
    ["Cn", "Copernicium"],
    ["Nh", "Nihonium"],
    ["Fl", "Flerovium"],
    ["Mc", "Moscovium"],
    ["Lv", "Livermorium"],
    ["Ts", "Tennessine"],
    ["Og", "Oganesson"],
]

atm_alphabet = [symbol for symbol, _ in atomic_symbols_names] + [missing_value_enc]
padded_atm_alphabet = [padding_value_enc] + atm_alphabet

atm_alphabet_to_protons = {
    symbol: i + 1 for i, symbol in enumerate(padded_atm_alphabet[1:-1])
}
