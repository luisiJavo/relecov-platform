#from itertools import count
from relecov_core.core_config import *
import json

def get_input_samples(request):
    '''
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
    '''
    sample_recorded = {}
    headings = HEADING_FOR_RECORD_SAMPLES

    sample_recorded["heading"] = [x[0] for x in HEADING_FOR_RECORD_SAMPLES]
    
    return sample_recorded


def analyze_input_samples(request):
    heading_author = HEADING_FOR_AUTHOR_TABLE
    sample_recorded = {}
    heading = [x[0] for x in HEADING_FOR_RECORD_SAMPLES]
    data_sample = {}
    data_author = {}
    na_json_data = json.loads(request.POST["table_data"])
    for row in na_json_data:
        print(row)
        #if row[1] == "":
        #    continue
        
        for idx in range(len(heading)):
            """
            data_sample["collecting_lab_sample_id"] = row[1]
            data_sample["sequencing_sample_id"] = row[5]
            data_sample["biosample_accession_ENA"] = ""
            data_sample["virus_name"] = ""
            data_sample["gisaid_id"] = ""
            data_sample["sequencing_date"] = ""
            #Sample.objects.create_new_sample(data_sample)
            """
            if heading[idx] in HEADING_FOR_AUTHOR_TABLE:
                data_author[HEADING_FOR_AUTHOR_TABLE[heading[idx]]] = row[idx]
                #data_author["analysis_authors"] = row[15]
                #data_author["author_submitter"] = row[16]
                #data_author["authors"] = row[17]
            #Authors.objects.create_new_authors(data_author)
        print(data_author)

    return sample_recorded