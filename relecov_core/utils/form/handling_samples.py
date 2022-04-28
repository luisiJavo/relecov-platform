#from itertools import count
from relecov_core.core_config import *
import json

def analyze_input_samples(request):
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
    Functions:
        
    Constants:
        HEADING_FOR_DISPLAY_RECORDED_SAMPLES # relecov_core/core_config.py
        HEADING_FOR_RECORD_SAMPLE_IN_DATABASE # relecov_core/core_config.py
    Variables:
        defined_samples  # contains the list of sample in defined state
        samples_continue  # samples id's from the samples in defined state
        pre_defined_samples  # contains the list of sample in pre-defined state
        pre_defined_samples_id  # samples id's from the samples in pre-defined state
        invalid_samples     # samples that already exists on database
        invalid_samples_id  # sample id's from the samples that already exists on database
        incomplete_samples  # samples that contain missing information
    Return:
        sample_recorded # Dictionnary with all samples cases .
    '''
    #na_json_data = json.loads(request.POST['table_data'])
    headings = HEADING_FOR_RECORD_SAMPLES

    sample_recorded = {}
    #print(headings[1][1])
    sample_recorded["heading"] = [x[0] for x in HEADING_FOR_RECORD_SAMPLES]
    #print(na_json_data[1][1])
    #print(na_json_data)
    
    
    return sample_recorded