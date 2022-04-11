import os


def parse_variant_csv_file(csv_file):
    """Parse the variant csv file and return a dictionary with the information"""
    if not os.path.isfile(csv_file):
        return False
    with open(csv_file, "r") as fh:
        lines = fh.readlines()
    variant_data = []
    variant_fields = ["pos", "ref", "alt", "dp", "ref_dp", "alt_dp", "af"]
    variant_pos = [2, 3, 4, 6, 7, 8, 9]

    effect_fields = ["effect", "hgvs_c", "hgvs_p", "hgvs_p_1_letter"]
    effect_pos = [11, 12, 13, 14]

    for line in lines[1:]:
        data_array = line.split(",")
        data_dict = {"variant_dict": {}, "effect_dict": {}}
        for iv in range(len(variant_fields)):
            data_dict["variant_dict"][variant_fields[iv]] = data_array[variant_pos[iv]]
            data_dict["effect_dict"] = {}
        for ix in range(len(effect_fields)):
            data_dict["effect_dict"][effect_fields[ix]] = data_array[effect_pos[ix]]
            data_dict["filter"] = data_array[5]
            data_dict["chromosome"] = data_array[1]
            data_dict["sample"] = data_array[0]
            data_dict["caller"] = data_array[15]
            data_dict["lineage_dict"] = {
                "lineage": data_array[16],
                "week": data_array[17],
            }
            data_dict["gene"] = data_array[10]
            variant_data.append(data_dict)

    return variant_data
