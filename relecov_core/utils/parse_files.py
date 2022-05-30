from relecov_core.models import (
    Variant,
    VariantInSample,
    Chromosome,
    Position,
    Filter,
    Gene,
    Effect,
    Sample,
)


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
    data_dict_ids = {}
    data_dict = {}

    with open(file_path) as fh:
        lines = fh.readlines()

    for line in lines[1:]:
        data_list = line.strip().split(",")

        if Chromosome.objects.filter(chromosome__iexact=data_list[1]).exists():
            chromosome_obj = Chromosome.objects.filter(
                chromosome__iexact=data_list[1]
            ).last()
        else:
            chromosome_obj = Chromosome.objects.create_new_chromosome(data_list[1])
        data_dict_ids["chromosomeID_id"] = chromosome_obj

        if Position.objects.filter(pos__iexact=data_list[2]).exists():
            position_obj = Position.objects.filter(pos__iexact=data_list[2]).last()
        else:
            data_dict["pos"] = data_list[2]
            data_dict["nucleotide"] = data_list[4]
            position_obj = Position.objects.create_new_position(data_dict)
        data_dict_ids["positionID_id"] = position_obj

        if Filter.objects.filter(filter__iexact=data_list[5]).exists():
            filter_obj = Filter.objects.filter(filter__iexact=data_list[5]).last()
        else:
            filter_obj = Filter.objects.create_new_filter(data_list[5])
        data_dict_ids["filterID_id"] = filter_obj

        if VariantInSample.objects.filter(af__iexact=data_list[9]).exists():
            variant_in_sample_obj = VariantInSample.objects.filter(
                af__iexact=data_list[9]
            ).last()
        else:
            data_dict["dp"] = data_list[6]
            data_dict["ref_dp"] = data_list[7]
            data_dict["alt_dp"] = data_list[8]
            data_dict["af"] = data_list[9]

            variant_in_sample_obj = (
                VariantInSample.objects.create_new_variant_in_sample(data_dict)
            )
        data_dict_ids["variant_in_sampleID_id"] = variant_in_sample_obj

        if Gene.objects.filter(gene__iexact=data_list[1]).exists():
            gene_obj = Gene.objects.filter(gene__iexact=data_list[10]).last()
        else:
            gene_obj = Gene.objects.create_new_gene(data_list[10])
        data_dict_ids["geneID_id"] = gene_obj

        if Effect.objects.filter(effect__iexact=data_list[11]).exists():
            effect_obj = Effect.objects.filter(effect__iexact=data_list[11]).last()
        else:
            data_dict["effect"] = (data_list[11],)
            data_dict["hgvs_c"] = (data_list[12],)
            data_dict["hgvs_p"] = (data_list[13],)
            data_dict["hgvs_p_1_letter"] = (data_list[14],)
            effect_obj = Effect.objects.create_new_effect(data_dict)
        data_dict_ids["effectID_id"] = effect_obj

        if Sample.objects.filter(
            collecting_lab_sample_id__iexact=data_list[0]
        ).exists():
            data_dict_ids["sampleID_id"] = Sample.objects.filter(
                collecting_lab_sample_id__iexact=data_list[0]
            ).last()

        if Variant.objects.filter(ref__iexact=data_list[3]).exists():
            Variant.objects.filter(ref__iexact=data_list[3]).last()
        else:
            Variant.objects.create_new_variant(data_list[3], data_dict_ids)
