# from itertools import count
from relecov_core.core_config import *
import json
from relecov_core.models import *


def get_input_samples(request):
    """
    Description:
        The function will get the samples data that user filled in the form.
        defined_samples are the samples that either has no sample project or for
            the sample projects that no requires additional data
        pre_definde_samples are the ones that requires additional Information
        For already defined samples, no action are done on them and  they are included in not_valid_samples.
        it will return a dictionary which contains the processed samples.
    Input:
        request

    Constants:
        HEADING_FOR_DISPLAY_RECORDED_SAMPLES
        HEADING_FOR_RECORD_SAMPLE_IN_DATABASE

    Return:
        sample_recorded # Dictionnary with all samples cases .
    """
    sample_recorded = {}
    sample_recorded["heading"] = [x[0] for x in HEADING_FOR_RECORD_SAMPLES]

    return sample_recorded


def analyze_input_samples(request):
    sample_recorded = {}
    headings = [x[0] for x in HEADING_FOR_RECORD_SAMPLES]
    data_sample = {}
    data_author = {}
    data_lineage = {}
    data_analysis = {}
    data_qc_stats = {}
    data_caller = {}
    data_filter = {}
    data_effect = {}
    data_gene = {}
    data_chromosome = {}
    data_variant = {}
    data_chromosome = {}
    data_incomplete_fields = {}
    list_of_incomplete_fields_per_row = []
    list_of_incomplete_rows = []
    # data_public_database = {}
    # data_public_database_fields = {}

    na_json_data = json.loads(request.POST["table_data"])
    # row read
    for row in na_json_data:
        print(row)
        if row[1] == "":
            #list_of_incomplete_rows.append(row)
            continue

        # column read
        for idx in range(len(headings)):
            """
            if row[idx] == "":
                #list_of_incomplete_rows.append(row)
                list_of_incomplete_fields_per_row.append(row[idx])
                data_incomplete_fields[row] = list_of_incomplete_rows
            """

            if headings[idx] in HEADING_FOR_AUTHOR_TABLE:
                data_author[HEADING_FOR_AUTHOR_TABLE[headings[idx]]] = row[idx]

            if headings[idx] in HEADING_FOR_SAMPLE_TABLE:
                data_sample[HEADING_FOR_SAMPLE_TABLE[headings[idx]]] = row[idx]

            if headings[idx] in HEADING_FOR_LINEAGE_TABLE:
                data_lineage[HEADING_FOR_LINEAGE_TABLE[headings[idx]]] = row[idx]

            if headings[idx] in HEADING_FOR_ANALYSIS_TABLE:
                data_analysis[HEADING_FOR_ANALYSIS_TABLE[headings[idx]]] = row[idx]

            if headings[idx] in HEADING_FOR_QCSTATS_TABLE:
                data_qc_stats[HEADING_FOR_QCSTATS_TABLE[headings[idx]]] = row[idx]

        print(data_author)
        print(data_sample)
        print(data_lineage)
        print(data_analysis)
        print(data_qc_stats)
        print(data_incomplete_fields)
        
        data_author_error = False
        
        for data in data_author:
            print(data)
            if data != "":
                data_author_error == True
            else:
                data_author_error == False
                break
            
        if data_author_error:
            sample_recorded["check"] = "Success"
        else:
            sample_recorded["check"] = "Error"
        
        print(sample_recorded)
        # Insert into tables
        """
        Authors.objects.create_new_authors(data_author)
        Sample.objects.create_new_sample(data_sample)
        Lineage.objects.create_new_Lineage(data_lineage)
        Analysis.objects.create_new_analysis(data_analysis)
        QcStats.objects.create_new_qc_stats(data_qc_stats)
        """

    return sample_recorded
