#![allow(unused, non_snake_case)]


use hashbrown::HashMap;
use itertools::Combinations;
use pyo3::{prelude::*, types::PyType};
use rayon::prelude::*;
use serde::{Deserialize, Serialize};
use serde_json::from_str;
use std::fs::read_to_string;
use std::{path::PathBuf, thread, vec};
use std::sync::atomic::{AtomicUsize, AtomicBool, Ordering};
use std::panic;

static GLOBAL_PRINT_LOG: AtomicBool = AtomicBool::new(false);


fn panic_silently(message: &str) {
    panic::set_hook(Box::new(|_info| {
        // do nothing
    }));

    let result = panic::catch_unwind(|| {
        panic!("");
    });

    match result {
        Ok(res) => res,
        Err(_) => println!("ERROR CAUGHT: {}", message),
    }
}


macro_rules! hashmap {
        ($( $key: expr => $val: expr ),*) => {{
        let mut map = ::hashbrown::HashMap::new();
        $( map.insert($key, $val); )*
        map
    }}
}


#[derive(Serialize, Deserialize, Clone, Debug)]
struct GeneTable {
    table_id: String,
    A: Option<Vec<String>>,
    L: Option<Vec<String>>,
    W: Option<Vec<String>>,
    Q: Option<Vec<String>>,
    Y: Option<Vec<String>>,
    E: Option<Vec<String>>,
    C: Option<Vec<String>>,
    D: Option<Vec<String>>,
    F: Option<Vec<String>>,
    G: Option<Vec<String>>,
    H: Option<Vec<String>>,
    I: Option<Vec<String>>,
    M: Option<Vec<String>>,
    K: Option<Vec<String>>,
    P: Option<Vec<String>>,
    R: Option<Vec<String>>,
    S: Option<Vec<String>>,
    V: Option<Vec<String>>,
    N: Option<Vec<String>>,
    T: Option<Vec<String>>,
    STOP: Option<Vec<String>>,
    DASH: Option<Vec<String>>,
}

impl GeneTable {
    pub fn from(filepath: PathBuf, table_id: u8) -> Self {
        let str_read = read_to_string(filepath).expect("Error reading file");

        let gene_tables: Vec<GeneTable> = from_str(&str_read).unwrap();

        let mut gene_table = gene_tables
            .iter()
            .cloned()
            .filter(|x| x.table_id == table_id.to_string())
            .collect::<Vec<GeneTable>>()
            .get(0)
            .unwrap()
            .clone();

        gene_table.set_dash();

        gene_table
    }

    pub fn set_dash(&mut self) {
        self.DASH = Some(vec!["".to_string()]);
    }

    pub fn get_by_char(&self, c: &char) -> &Option<Vec<String>> {
        match c {
            'A' => &self.A,
            'L' => &self.L,
            'W' => &self.W,
            'Q' => &self.Q,
            'Y' => &self.Y,
            'E' => &self.E,
            'C' => &self.C,
            'D' => &self.D,
            'F' => &self.F,
            'G' => &self.G,
            'H' => &self.H,
            'I' => &self.I,
            'M' => &self.M,
            'K' => &self.K,
            'P' => &self.P,
            'R' => &self.R,
            'S' => &self.S,
            'V' => &self.V,
            'N' => &self.N,
            'T' => &self.T,
            '*' => &self.STOP,
            '-' => &self.DASH,
            _ => {
                panic_silently("No acceptable index for gene table, must be one of the 18 AA chars + 4 ambiguous chars.");
                &self.STOP 
            }
        }
    }

    pub fn get_by_amb_char(&self, amb_char: AmbiguousChars) -> Vec<Option<Vec<String>>> {
        match amb_char {
            AmbiguousChars::X | AmbiguousChars::Period => vec![Some(vec!["...".to_string()])],
            AmbiguousChars::B => vec![self.D.clone(), self.N.clone()],
            AmbiguousChars::Z => vec![self.E.clone(), self.Q.clone()],
            AmbiguousChars::J => vec![self.I.clone(), self.L.clone()],
            AmbiguousChars::Dud => vec![self.STOP.clone()],
        }
    }

    pub fn map_singe_aa_seq_to_triplets(
        &self,
        amino_acid: &String,
    ) -> Vec<Vec<String>> {
        let mut ret_vec = vec![];


        amino_acid.chars().for_each(|c| {
            match AmbiguousChars::matches_ambiguous(&c) {
                true => {
                    let amb_char = AmbiguousChars::from(c);
                    let mut v_final = vec![];

                    let vec_opt_vec_triplets = self.get_by_amb_char(amb_char);

                    vec_opt_vec_triplets.iter().cloned().for_each(|x| match x {
                        Some(v) => v_final.extend(v),
                        None => (),
                    });

                    ret_vec.push(v_final);
                }
                false => match &self[c] {
                    Some(v) => {
                        ret_vec.push(v.clone());
                    }
                    None => (),
                },
            }
        });

        ret_vec
    }
}

impl std::ops::Index<char> for GeneTable {
    type Output = Option<Vec<String>>;

    fn index(&self, index: char) -> &Self::Output {
        self.get_by_char(&index)
    }
}

enum AmbiguousChars {
    X,
    Period,
    B,
    Z,
    J,
    Dud,
}

impl AmbiguousChars {
    pub fn from(c: char) -> Self {
        match c {
            'X' => Self::X,
            '.' => Self::Period,
            'B' => Self::B,
            'Z' => Self::Z,
            'J' => Self::J,
            _ => {
                panic_silently("The character must be [X*.BZJ]");
                Self::Dud
            },
        }
    }

    pub fn matches_ambiguous(c: &char) -> bool {
        vec!['X', '.', 'B', 'Z', 'J'].contains(c)
    }
}

struct AminoAcidTranslator((String, String), (String, String), bool);

impl AminoAcidTranslator {
    pub fn do_checks(&mut self) {
        let AminoAcidTranslator((aa_header, aa), (nt_header, nt), do_skip) = self;

        if aa_header != nt_header {
            panic_silently(&format!("AA header -> {} is not the same as NT header -> {}", aa_header, nt_header));
        }

        let len_aa = aa.len();
        let len_nt = nt.len();
        let aa_filt_mul = aa.chars().filter(|c| *c != '-').count() * 3;

        if len_nt != aa_filt_mul {
            let longer_shorter = match aa_filt_mul > len_nt {
                true => (
                    format!("(AA -> {})", aa_header),
                    format!("(NT -> {})", nt_header)
                ),
                false => (
                    format!("(NT -> {})", nt_header),
                    format!("(AA -> {})", aa_header),
                )
            };

            let diff = {
                let num_marker = match aa_filt_mul > len_nt {
                        true => ((aa_filt_mul - len_nt) / 3, "PEP char(s)"),
                        false => ((len_nt - aa_filt_mul) / 3, "NT triplet(s)"),
                    };
                format!("with a difference of {} {}", num_marker.0, num_marker.1)
            };

            panic_silently(&format!("{} is larger than {} {}", longer_shorter.0, longer_shorter.1, diff));
            *do_skip = true;

        }                     
    }

    
    pub fn streamline_amino_acid(&mut self) {
        let AminoAcidTranslator((header, amino_acid), _, _) = self;

        let mut amino_acid_trimmed = amino_acid.trim().to_uppercase();

        let mut amino_acid_filtered = String::new();

        amino_acid_trimmed
            .char_indices()
            .for_each(|(i, c)| {
                match !vec![
                    'A', 
                    'L',
                    'W',
                    'Q',
                    'Y',
                    'E',
                    'C',
                    'D',
                    'F',
                    'G',
                    'H',
                    'I',
                    'M',
                    'K',
                    'P',
                    'R',
                    'S',
                    'V',
                    'N',
                    'T',
                    '*',
                    '-',
                ].contains(&c) {
                    true => {
                        let _ = match GLOBAL_PRINT_LOG.load(Ordering::Relaxed) {
                            true => println!("INFO: Amino Acid {} has an unknown character at string index {}. Replaced with `X`.", header, i),
                            false => (),
                        };

                        amino_acid_filtered.push('X');
                    },
                    false => amino_acid_filtered.push(c),
                } 
        });

        *amino_acid = amino_acid_filtered;

    }

    pub fn reverse_translate_and_compare(
        &self,
        gene_table: &GeneTable,
    ) -> String {
        let AminoAcidTranslator((header, amino_acid), (_, compare_dna), do_skip) = self;
        
        let range_map = gene_table.map_singe_aa_seq_to_triplets(amino_acid);
        let mut final_str = String::new();

        let mut i = 0;

        range_map
            .into_iter()
            .zip(amino_acid.char_indices())
            .for_each(|(possible_triplets, (j, compare_substr_aa))| {
               
                match compare_substr_aa == '-' {
                    true => {
                        final_str.push_str("---");
                    },
                    false => {
                        match compare_substr_aa.is_digit(10) {
                            true => {
                                let num = compare_substr_aa.to_digit(10).unwrap();
                                let repeated_substr = String::from(".").repeat(num as usize);

                                final_str.push_str(&repeated_substr);
                            },
                            false => {
                                let compare_substr_nuc = compare_dna[i..=i + 2].to_string();

                                i += 3;

                                let mut final_possible_triplets = possible_triplets.clone();

                                if compare_substr_aa == 'M' &&
                                        final_str.len() == 0 
                                {
                                    final_possible_triplets.extend(
                                        gene_table
                                            .get_by_amb_char(
                                                AmbiguousChars::B
                                            )
                                                    .iter()
                                                    .cloned()
                                                    .flatten()
                                                    .into_iter()
                                                    .flatten()
                                        );
                                    final_possible_triplets.extend(
                                        gene_table
                                            .get_by_amb_char(
                                                AmbiguousChars::Z
                                            )
                                                .iter()
                                                .cloned()
                                                .flatten()
                                                .into_iter()
                                                .flatten()
                                        );
                                }
                                
                                final_possible_triplets
                                    .iter()
                                    .cloned()
                                    .for_each(|s| {        
                                        match s == compare_substr_nuc {
                                            true => {
                                                final_str.push_str(&s);
                                            },
                                            false => {
                                                let position = format!("[{}, {})", i - 3, i);

                                                match GLOBAL_PRINT_LOG.load(Ordering::Relaxed) {
                                                    true => {
                                                        println!(
                                                            "LOG: {header} -> Possible nucleotide triplet {s} for Amino Acid {compare_substr_aa} at position {j} did not match with source nucleotide triplet {compare_substr_nuc} at position {position}."
                                                        )
                                                    },
                                                    false => (),
                                                }

                                                
                                            },
                                        };
                                    });
                            },
                        }


                    }
                }             
             });

        
        
        if final_str.chars().filter(|c| *c != '-' && *c != '.').count() != compare_dna.len() {
            panic_silently(&format!(r#" 
            ======
            MISMATCH ERROR:
            The following Amino Acid failed to match with its source Nucleotide pair.

                Header: `{}`,                    
                Amino Acid: `{}`,
                Source Nucleotide: `{}`,

            =======
            "#, 
                header, 
                amino_acid, 
                compare_dna,
            ));
        }
        

        final_str
    }
}

#[pyfunction]
fn pn2codon(
    filepath: PathBuf,
    table_id: u8,
    amino_seqs: Vec<(String, String)>,
    nuc_seqs: Vec<(String, String)>,
    do_log: bool,
) -> Vec<(String, String)> {
    GLOBAL_PRINT_LOG.store(do_log, Ordering::Relaxed);

    let aa_seq_len = amino_seqs.len();
    let nt_seq_len = nuc_seqs.len();

    if aa_seq_len != nt_seq_len {
        let longer_shorter = match aa_seq_len > nt_seq_len {
            true => ("AA", "NT"),
            false => ("NT", "AA")
        };

        let diff = match aa_seq_len > nt_seq_len {
            true => (aa_seq_len as isize - aa_seq_len as isize).abs(),
            false => (nt_seq_len as isize - aa_seq_len as isize).abs(),
        };

        panic_silently(&format!("Length of the {} sequence is longer than the length of {} sequence by a number of {}.", longer_shorter.0, longer_shorter.1, diff));
    
    }
    
    let gene_table = GeneTable::from(filepath, table_id);

    amino_seqs
        .par_iter()
        .zip(nuc_seqs.par_iter())
        .map(|((aa_header, aa), (nt_header, nt))| {

            let mut amino_acid = AminoAcidTranslator(
                (aa_header.clone(), aa.clone()),
                (nt_header.clone(), nt.clone()),
                false
            );
            amino_acid.do_checks();
            amino_acid.streamline_amino_acid();

            let codon = amino_acid.reverse_translate_and_compare(&gene_table);

            (nt_header.clone(), codon)
        })
        .collect()           
}

/// A Python module implemented in Rust.
#[pymodule]
fn pro2codon(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(pn2codon, m)?)?;
    Ok(())
}


#[test]
fn test_revtrans_success() {
    let nuc = vec![("aa".to_string(), String::from("ATGTGCCATCAGCATCCGAATCATTTGCTGAAGCAGTCTCTCCAAACGTACGTGTTCCGCCGAAATGAGCTACTGGACGCCGGCAAAAGTGCACTGCGGCATCGCATTCGCCTTCAGGAGCGAAATTGGATGACGACAGGGGCCAAACCACAGCAGCAGCAAGTCGTGCGAACCGGGGAAAGGAGCTCAAGGGTTCTGAGGTTACTGCTGGCAGGAACCGCCGTGAGTGTCACCGTAGGGTATCAATGCCGCCGGTGGTTCGTGCATTGTGAAGCGGCTGTTGTAAACAACCGGCTGGTGGGACAGAAGGTTCCGGGAGCAGGAGATGGGATCAAATTTGACTGGAGGAAATTTTGGAGCTATTTGAGACCGCACCTGGTGAAACTGATTGGGGCGATTATGGCGGCGCTGGCCGTGGCCTATTTTAATATTCAGATTCCCAACATGCTGGGAGTAGTGGTGAATACGCTGTCGAAATATGCCAGGACGAGTTTGAGCGACATTGATTCTTCAACGTTCATGAACGAAATGAAACTGCCATCGCTGCGACTGTTCGGTATGTACATTGCCCAAGCCGGATTCACATTCGTCTACATTTTGCTGCTGAGTCAGATAGGCGAACAGATGGCCGCGAAGATCCGACAGGATCTGTTCAAGCAGATCATCATCCAGGATCTGGAGTTCTTCGACGAAAACCGAACCGGAGAGTTGGTCAACCGGTTGACGGCCGACGTGCAAGACTTCAAATCTAGCTTCAAGCAATGCATCTCGCAAGGATTACGGTCATTTGCCCAGCTGATCGGAGGTGGCATATCGTTGTTCCTTATCTCGCCACAGCTGGCCAGTATCGCTTTGGTATCGGTCCCTGCCGCGGTGGCAATGTTCTCCTTTCTTGGAAAGTCTTTGAGAGCGCTGAGCAAGAAGAGTCAAGCCCAATCGGAACGAGCGACTTCAGTGAGTGAGGAAGCGCTGTCCAACATCAGAACTGTCCGCTCCAGTGCATGCGAGTTTGCCGAAGTTGAACTGTTGCGGCAGGAAACGGAAAAGGCAGCTGAGCTGTCCCAGCAGCTGGGTGTGAAATCGCACTCTATCATGCCACTGACTAATTTATACGTGAACGGCATGGTGCTAAACGACGCTGGTTCTCGTTCAATAAGTGCCGGAGATTTGATGGCATTCTTGGTTGCATCTCAAGGTGTTCAACGCTCTCTTGCCCAAGGCTCTATTCTGCTTGGATCCGTAATCCGTGGAATGACAGCCGGCACCCGTGTATTCGAATACCTCTCGGTTCAGCCTAAAGTAGATCTCAAATACGGACAAATCATTCCCGAGTCGGAAATTCGTGGCGAAATCCGATTCGAAAACGTGTCTTTCACGTATCCTTCCCGACCCAATCATCCTGTTCTCAAAAACTTTTCGCTTGTCCTGAAACCTGGACAAACTGTGGCCCTGGTGGGAGCCAGTGGCTCAGGGAAATCGACCATTGCTTCGCTTCTGGAGCGATTTTACGAGCCAACCGGTGGCCGCATCACCATAGATGGTTATGAACTCTCACAATTGTCGCCTTATTGGCTCCGAGGCCACCTGATAGGATTCATCGAACAGCAACCGATACTGTTCGGAACGTCCATCTACGAGAACATACGCTACGGCCGTCCAGAGGCGTCACAAGCGGAAGTCCTGGAAGCGGCCAAGCTGTCTCAGTCGCATCAGTTTGTGAGCAAATTGCCTGAGGGCTACGAGACGCCAGTTGGCGAAAGGGGCATCCAACTGAGTGGTGGCCAACGGCAAAGGATAGCAATAGCTAGAGCTTTGCTCAAACAGCCCTCGGTGTTGATCTTGGACGAGGCTACCAGTGCATTAGATGCTTCCAGTGAGGCCATCGTGCAGAAAGCCCTTGATGCAGCGGTAGTCGACAGAACTACGCTGGTTATTGCCCACCGGCTATCAACCATCAGGAACGCGGATGTGATTGTGGTGCTGGAAAAAGGCCGAATAGTAGAGATTGGCAATCATGATGCGCTGCTGCGCAAGAAGGGCTACTACTTTGAACTGGTCAAACAGCAAGAACGGGAACAACGCGAGGAACAACAGCAAAGGGCCTACGGA"))];
    let aa = vec![("aa".to_string(), String::from("MC-------HQHPNHLLKQSLQTYVFRRNELLDAGKSALR-HRIRLQERNWMTTGAKPQQQQVVRTGERSSRVLR-------LLLAGTA----VSVTVGYQCRRWF-------VHCEAAVVNNRLVG--QKVPG-AGDGIKFDWRKFWSYLRPHLVKLIGAIMAALAVAYFNIQIPNMLGVVVNTLSKYARTSLSDIDSSTFMNEMKLPSLRLFGMYIAQAGFTFVYILLLSQIGEQMAAKIRQDLFKQIIIQDLEFFDENRTGELVNRLTADVQDFKSSFKQCISQGLRSFAQLIGGGISLFLISPQLASIALVSVPAAVAMFSFLGKSLRALSKKSQAQ----------SERATSVSEEALSNIRTVRSSACEFAEVELLRQETEKAAELSQQLGVKSHSIMPLTNLYVNGMVLND-------AGSRSISAGDLMAFLVASQGVQRSLAQGSILLGSVIRGMTAGTRVFEYLSVQPKVDLKYGQIIPESEIRGEIRFENVSFTYPSRPNHPVLKNFSLVLKPGQTVALVGASGSGKSTIASLLERFYEPTGGRITIDGYELSQLSPYWLRGHLIGFIEQQPILFGTSIYENIRYGRPEASQAEVLEAAKLSQSHQFVSKLPEGYETPVGERGIQLSGGQRQRIAIARALLKQPSVLILDEATSALDASSEAIVQKALDAAVVDRTTLVIAHRLSTIRNADVIVVLEKGRIVEIGNHDALLRKKGYYFELVKQQEREQREEQQQRAYG------------"))];
    let table_id = 1u8;
    let filepath = PathBuf::from("genetic_table.json");

    let codon = pn2codon(filepath, table_id, aa, nuc, false);

    let should_be = String::from("ATGTGC---------------------CATCAGCATCCGAATCATTTGCTGAAGCAGTCTCTCCAAACGTACGTGTTCCGCCGAAATGAGCTACTGGACGCCGGCAAAAGTGCACTGCGG---CATCGCATTCGCCTTCAGGAGCGAAATTGGATGACGACAGGGGCCAAACCACAGCAGCAGCAAGTCGTGCGAACCGGGGAAAGGAGCTCAAGGGTTCTGAGG---------------------TTACTGCTGGCAGGAACCGCC------------GTGAGTGTCACCGTAGGGTATCAATGCCGCCGGTGGTTC---------------------GTGCATTGTGAAGCGGCTGTTGTAAACAACCGGCTGGTGGGA------CAGAAGGTTCCGGGA---GCAGGAGATGGGATCAAATTTGACTGGAGGAAATTTTGGAGCTATTTGAGACCGCACCTGGTGAAACTGATTGGGGCGATTATGGCGGCGCTGGCCGTGGCCTATTTTAATATTCAGATTCCCAACATGCTGGGAGTAGTGGTGAATACGCTGTCGAAATATGCCAGGACGAGTTTGAGCGACATTGATTCTTCAACGTTCATGAACGAAATGAAACTGCCATCGCTGCGACTGTTCGGTATGTACATTGCCCAAGCCGGATTCACATTCGTCTACATTTTGCTGCTGAGTCAGATAGGCGAACAGATGGCCGCGAAGATCCGACAGGATCTGTTCAAGCAGATCATCATCCAGGATCTGGAGTTCTTCGACGAAAACCGAACCGGAGAGTTGGTCAACCGGTTGACGGCCGACGTGCAAGACTTCAAATCTAGCTTCAAGCAATGCATCTCGCAAGGATTACGGTCATTTGCCCAGCTGATCGGAGGTGGCATATCGTTGTTCCTTATCTCGCCACAGCTGGCCAGTATCGCTTTGGTATCGGTCCCTGCCGCGGTGGCAATGTTCTCCTTTCTTGGAAAGTCTTTGAGAGCGCTGAGCAAGAAGAGTCAAGCCCAA------------------------------TCGGAACGAGCGACTTCAGTGAGTGAGGAAGCGCTGTCCAACATCAGAACTGTCCGCTCCAGTGCATGCGAGTTTGCCGAAGTTGAACTGTTGCGGCAGGAAACGGAAAAGGCAGCTGAGCTGTCCCAGCAGCTGGGTGTGAAATCGCACTCTATCATGCCACTGACTAATTTATACGTGAACGGCATGGTGCTAAACGAC---------------------GCTGGTTCTCGTTCAATAAGTGCCGGAGATTTGATGGCATTCTTGGTTGCATCTCAAGGTGTTCAACGCTCTCTTGCCCAAGGCTCTATTCTGCTTGGATCCGTAATCCGTGGAATGACAGCCGGCACCCGTGTATTCGAATACCTCTCGGTTCAGCCTAAAGTAGATCTCAAATACGGACAAATCATTCCCGAGTCGGAAATTCGTGGCGAAATCCGATTCGAAAACGTGTCTTTCACGTATCCTTCCCGACCCAATCATCCTGTTCTCAAAAACTTTTCGCTTGTCCTGAAACCTGGACAAACTGTGGCCCTGGTGGGAGCCAGTGGCTCAGGGAAATCGACCATTGCTTCGCTTCTGGAGCGATTTTACGAGCCAACCGGTGGCCGCATCACCATAGATGGTTATGAACTCTCACAATTGTCGCCTTATTGGCTCCGAGGCCACCTGATAGGATTCATCGAACAGCAACCGATACTGTTCGGAACGTCCATCTACGAGAACATACGCTACGGCCGTCCAGAGGCGTCACAAGCGGAAGTCCTGGAAGCGGCCAAGCTGTCTCAGTCGCATCAGTTTGTGAGCAAATTGCCTGAGGGCTACGAGACGCCAGTTGGCGAAAGGGGCATCCAACTGAGTGGTGGCCAACGGCAAAGGATAGCAATAGCTAGAGCTTTGCTCAAACAGCCCTCGGTGTTGATCTTGGACGAGGCTACCAGTGCATTAGATGCTTCCAGTGAGGCCATCGTGCAGAAAGCCCTTGATGCAGCGGTAGTCGACAGAACTACGCTGGTTATTGCCCACCGGCTATCAACCATCAGGAACGCGGATGTGATTGTGGTGCTGGAAAAAGGCCGAATAGTAGAGATTGGCAATCATGATGCGCTGCTGCGCAAGAAGGGCTACTACTTTGAACTGGTCAAACAGCAAGAACGGGAACAACGCGAGGAACAACAGCAAAGGGCCTACGGA------------------------------------");

    assert_eq!(codon[0].1, should_be);

}