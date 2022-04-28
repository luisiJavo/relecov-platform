from itertools import count
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
    na_json_data = json.loads(request.POST['table_data'])
    heading_in_form = HEADING_FOR_RECORD_SAMPLES
    heading_in_database = HEADING_FOR_RECORD_SAMPLE_IN_DATABASE

    sample_recorded = {}

<<<<<<< HEAD
    #defined_samples, samples_continue = [], []
    #pre_defined_samples, pre_defined_samples_id = [], []
    #invalid_samples, invalid_samples_id = [], []
    #incomplete_samples = []
    #sample_recorded['all_samples_defined'] = True

    #reg_user = request.user.username
    #print(type(na_json_data))
    #print(na_json_data)
    #list_test = na_json_data.split(",")
    #print(list_test)
    print(na_json_data)
    #for row in na_json_data:
        #print(len(row))
        #sample_data = {}
        #sample_name = str(row[heading_in_form.index('Sample Name')])
        #if sample_name == '':
        #    continue
        
    """    
        if not check_if_sample_already_defined(row[heading_in_form.index('Sample Name')], reg_user):
            sample_type = str(row[heading_in_form.index('Type of Sample')])

            if sample_type == '':
                incomplete_samples.append(row)
                continue

            for i in range(len(heading_in_form)):
                sample_data[MAPPING_SAMPLE_FORM_TO_DDBB[i][1]] = row[i]
            # optional_fields = []

            # for opt_field in OPTIONAL_SAMPLES_FIELDS:
            #    optional_fields.append(HEADING_FOR_RECORD_SAMPLES.index(opt_field))
            optional_fields = SampleType.objects.get(sampleType__exact=sample_type, apps_name__exact=app_name).get_optional_values()

            # check_empty_fields does not consider if the optional values are empty
            if check_empty_fields(row, optional_fields):
                incomplete_samples.append(row)
                sample_recorded['all_samples_defined'] = False
                continue
            # Check if patient code  already exists on database, If not if will be created giving a sequencial dummy value
            if sample_data['p_code_id'] != '':
                patient_obj = check_patient_code_exists(sample_data['p_code_id'])
                if patient_obj == False:
                    # Define the new patient only Patient code is defined
                    patient_obj = create_empty_patient(sample_data['p_code_id'])
            else:
                patient_obj = None
            sample_data['patient'] = patient_obj
            sample_data['user'] = reg_user
            sample_data['sample_id'] = str(reg_user + '_' + sample_name)
            if not Samples.objects.exclude(uniqueSampleID__isnull=True).exists():
                sample_data['new_unique_value'] = 'AAA-0001'
            else:
                last_unique_value = Samples.objects.exclude(uniqueSampleID__isnull=True).last().uniqueSampleID
                sample_data['new_unique_value'] = increase_unique_value(last_unique_value)
            # set to Defined state the sample if not required to add more additional data

            if sample_data['project_service'] == 'None':
                sample_data['sampleProject'] = None
                if sample_data['onlyRecorded']:
                    sample_data['sampleState'] = 'Completed'
                    sample_data['completedDate'] = datetime.datetime.now()
                else:
                    sample_data['sampleState'] = 'Defined'
            else:
                sample_data['sampleProject'] = SampleProjects.objects.get(sampleProjectName__exact = sample_data['project_service'] )
                if SampleProjectsFields.objects.filter(sampleProjects_id = sample_data['sampleProject']).exists():
                    sample_recorded['all_samples_defined'] = False
                    sample_data['sampleState'] = 'Pre-Defined'
                else:
                    sample_data['sampleState'] = 'Defined'
            sample_data['app_name'] = app_name
            new_sample = Samples.objects.create_sample(sample_data)





            if sample_data['sampleState'] == 'Defined' or sample_data['sampleState'] == 'Completed':
                defined_samples.append(new_sample.get_sample_definition_information())
                samples_continue.append(new_sample.get_sample_id())
            else:
                # select the samples that requires to add additional Information
                pre_defined_samples.append(new_sample.get_sample_name())
                pre_defined_samples_id.append(new_sample.get_sample_id())
        else: # get the invalid sample to displays information to user
            sample_recorded['all_samples_defined'] = False
            sample_id = Samples.objects.get(sampleName__exact = sample_name).get_sample_id()
            if not 'sample_id_for_action' in sample_recorded:
                # get the first no valid sample to ask user for new action on the sample
                sample_recorded['sample_data_for_action'] = Samples.objects.get(sampleName__exact = sample_name).get_sample_definition_information()
                sample_recorded['sample_id_for_action'] = sample_id
                invalid_samples.append(Samples.objects.get(sampleName__exact = sample_name).get_sample_definition_information())
            else:
                invalid_samples_id.append(sample_id)
                invalid_samples.append(Samples.objects.get(sampleName__exact = sample_name).get_sample_definition_information())
    ## Add already recorded sample in Pre-defined that were not processed because incomplete informatio in samples
    if 'pre_defined_id' in request.POST:
        old_pre_defined_list = request.POST['pre_defined_id'].split(',')
        for old_pre_defined in old_pre_defined_list :
            sample_obj = get_sample_obj_from_id(old_pre_defined)
            pre_defined_samples.append(sample_obj.get_sample_name())
            pre_defined_samples_id.append(old_pre_defined)
    if 'pending_pre_defined' in request.POST:
        old_pending_pre_defined_list = request.POST['pending_pre_defined'].split(',')
        for old_pending_pre_defined in old_pending_pre_defined_list :
            sample_obj = get_sample_obj_from_id(old_pending_pre_defined)
            pre_defined_samples.append(sample_obj.get_sample_name())
            pre_defined_samples_id.append(old_pending_pre_defined)
    ##   collect data into sample_recorded
    if len(defined_samples) > 0 :
        sample_recorded['defined_samples'] = defined_samples
    if len(invalid_samples) >0 :
        sample_recorded['invalid_samples'] = invalid_samples
        sample_recorded['invalid_samples_id'] = ','.join(invalid_samples_id)
        sample_recorded['invalid_heading'] = HEADING_FOR_DISPLAY_RECORDED_SAMPLES
    if len(incomplete_samples) >0 :
        sample_recorded['incomplete_samples'] = incomplete_samples
    if len(pre_defined_samples) >0 :
        sample_recorded['pre_defined_samples'] = pre_defined_samples
        sample_recorded['pre_defined_samples_id'] = pre_defined_samples_id

    if sample_recorded['all_samples_defined']:
        sample_recorded['samples_to_continue'] = ','.join(samples_continue)
    sample_recorded['recorded_sample_heading'] = HEADING_FOR_DISPLAY_RECORDED_SAMPLES
    sample_recorded['valid_samples_ids'] = samples_continue
    """
=======
    print(na_json_data[1][1])
    
>>>>>>> d99fee6f49d721ebf9d2424f2cb510646560beff
    return sample_recorded