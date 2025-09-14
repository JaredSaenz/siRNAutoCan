import os
import csv



def get_quality(sequences: dict) -> dict:
    result = {}
    quality = 0
    seq_p_s = sequences['passenger'].replace('T', 'U')
    seq_g_a = sequences['guide'].replace('T', 'U')
    
    #6 GC content in 2-7 nt  = 19% -> 17% and 8-18 nt = 52% -> 55% of the antisense strand 
    gc_count_1 = 0
    for j in seq_g_a[1:7]:
        if j in ['G', 'C']: 
            gc_count_1 += 1/6
    gc_count_1 = round(gc_count_1 * 100)

    gc_count_2 = 0
    for j in seq_g_a[7:18]:
        if j in ['G', 'C']: 
            gc_count_2 += 1/11
    gc_count_2 = round(gc_count_2 * 100)

    meets_6 = 1 if gc_count_1 == 17 and gc_count_2 == 55 else 0
    if meets_6:
        quality += 1

    #7 Asymmetrical base pairing
    init_p = seq_p_s[0]
    init_g = seq_g_a[1]
    meets_7 = 1 if init_p in ['C', 'G'] and init_g in ['A', 'U'] else 0
    if meets_7:
        quality += 2

    #8 Energy valley
    energy_count = 0
    for j in seq_p_s[8:14]:
        if j in ['G', 'C']: 
            energy_count += 1/6
    energy_count = round(energy_count * 100)

    meets_8 = 1 if energy_count < 50 else 0
    if meets_8:
        quality += 2

    #11 TT-3'-end overhang (fixed logic: check last 2 nt for typical 21-nt sequences)
    if len(seq_p_s) >= 2:
        tt_overhang = seq_p_s[-2:]
        meets_11 = 1 if tt_overhang == 'UU' else 0  # Using 'UU' since replaced to U
        if meets_11:
            quality += 1
    else:
        meets_11 = 0

    #12 Weak base pairing in guide/antisense strand
    weak_init = seq_g_a[0]
    meets_12 = 1 if weak_init in ['A', 'U'] else 0
    if meets_12:
        quality += 1 

    #13 Strong base pairing in passenger/sense strand (fixed: use seq_p_s[0] and check for strong G/C)
    strong_init = seq_p_s[0]
    meets_13 = 1 if strong_init in ['G', 'C'] else 0
    if meets_13:
        quality += 1 

    #14 Presence of A nucleotide at the sixth position of the antisense strand
    nt_6_g_a = seq_g_a[5] if len(seq_g_a) > 5 else ''
    meets_14 = 1 if nt_6_g_a == 'A' else 0
    if meets_14:
        quality += 1

    #15 Presence of A nucleotide at the third and the nineteenth position of the sense strand
    nt_3_p_s = seq_p_s[2] if len(seq_p_s) > 2 else ''
    nt_19_p_s = seq_p_s[18] if len(seq_p_s) > 18 else ''
    meets_15 = 1 if nt_3_p_s == 'A' and nt_19_p_s == 'A' else 0
    if meets_15:
        quality += 1

    #16 Absence of G/C at the nineteenth position of the sense strand
    meets_16 = 1 if nt_19_p_s not in ['G', 'C'] else 0
    if meets_16:
        quality += 1

    #17 Absence of G nucleotide at the thirteenth position of the sense strand
    nt_13_p_s = seq_p_s[12] if len(seq_p_s) > 12 else ''
    meets_17 = 1 if nt_13_p_s != 'G' else 0
    if meets_17:
        quality += 1

    #18 Presence of U nucleotide at the tenth position of the sense strand.
    nt_10_p_s = seq_p_s[9] if len(seq_p_s) > 9 else ''
    meets_18 = 1 if nt_10_p_s == 'U' else 0
    if meets_18:
        quality += 1

    result['quality'] = quality
    result['#6'] = meets_6
    result['#7'] = meets_7
    result['#8'] = meets_8
    result['#11'] = meets_11
    result['#12'] = meets_12
    result['#13'] = meets_13
    result['#14'] = meets_14
    result['#15'] = meets_15
    result['#16'] = meets_16
    result['#17'] = meets_17
    result['#18'] = meets_18

    return result

