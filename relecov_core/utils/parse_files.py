from relecov_core.models import Chromosome


def parse_csv_into_list_of_dicts(file_path):
    """
    fields => SAMPLE(0), CHROM(1), POS(2), REF(3), ALT(4),
    FILTER(5), DP(6),  REF_DP(7), ALT_DP(8), AF(9), GENE(10),
    EFFECT(11), HGVS_C(12), HGVS_P(13), HGVS_P1LETTER(14),
    CALLER(15), LINEAGE(16)
    """
    data_array = []  # one field per position

    variant_data = []
    variant_fields = ["pos", "ref", "alt", "dp", "ref_dp", "alt_dp", "af"]
    variant_pos = [2, 3, 4, 6, 7, 8, 9]

    effect_fields = ["effect", "hgvs_c", "hgvs_p", "hgvs_p_1_letter"]
    effect_pos = [11, 12, 13, 14]

    with open(file_path) as fh:
        lines = fh.readlines()

    for line in lines[1:]:
        data_array = line.split(",")
        data_dict = {"variant_dict": {}, "effect_dict": {}}
        for iv in range(len(variant_fields)):
            data_dict["variant_dict"][variant_fields[iv]] = data_array[variant_pos[iv]]
        # effect_dict = {}
        for ix in range(len(effect_fields)):
            data_dict["effect_dict"][effect_fields[ix]] = data_array[effect_pos[ix]]
        data_dict["filter"] = data_array[5]
        data_dict["chromosome"] = data_array[1]
        data_dict["sample"] = data_array[0]
        data_dict["caller"] = data_array[15]
        data_dict["lineage_dict"] = {"lineage": data_array[16], "week": data_array[17]}
        data_dict["gene"] = data_array[10]
        variant_data.append(data_dict)

    return variant_data


def parse_csv(file_path):
    """
    fields => SAMPLE(0), CHROM(1), POS(2), REF(3), ALT(4),
    FILTER(5), DP(6),  REF_DP(7), ALT_DP(8), AF(9), GENE(10),
    EFFECT(11), HGVS_C(12), HGVS_P(13), HGVS_P1LETTER(14),
    CALLER(15), LINEAGE(16)
    """
    data_dict = {}
    list_of_dictionaries = []

    with open(file_path) as fh:
        lines = fh.readlines()

    csv_headings_list = lines[0].strip().split(",")
    # csv_headings_list = csv_headings.split(",")

    # delete final \n

    for line in lines[1:]:
        data_list = line.strip().split(",")
        if Chromosome.objects.filter(chromosome__iexact=data_list[1]).exists():
            chromosome_obj = Chromosome.objects.filter(
                chromosome__iexact=data_list[1]
            ).last()
        else:
            chromosome_obj = Chromosome.objects.create_new_chromosome(data_list[1])

        # for idx in range(len(data_list)):
        #    data_dict[csv_headings_list[idx]] = data_list[idx]

        # list_of_dictionaries.append(data_dict)

    return list_of_dictionaries
