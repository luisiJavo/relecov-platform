from relecov_core.models import *

class Manager_db():
    
    def __init__(self,table_name, data_dict) -> None:
        table_name = self.table_name
        data_dict =self.data_dict
        
    #setters, insert into tables
    def insert_into_variant_table(variant_dict):
        for variant in variant_dict:
            variants = Variant(
                pos=variant["pos"],
                ref=variant["ref"],
                alt = variant["alt"],
                dp = variant["dp"],
                ref_dp = variant["ref_dp"],
                alt_dp = variant["alt_dp"],
                af = variant["af"],
                )
            variants.save()
            
    def insert_into_caller_table(caller_list):
        for caller in caller_list:
            callers = Caller(caller=caller["caller"])
            callers.save()
            
    def insert_into_effect_table(effect_list):
        for effect in effect_list:
            effects = Effect(
                effect = effect["effect"],
                hgvs_c = effect["hgvs_c"],
                hgvs_p = effect["hgvs_p"],
                hgvs_p_1_letter = effect["hgvs_p_1_letter"],
            )
            effects.save()
            
    def insert_into_effect_table(filter_list):
        for filter in filter_list:
            filters = Filter(
                filter = filter["filter"]
            )
            filters.save()
            
    def insert_into_chromosome_table(chromosome_list):
        for chrom in chromosome_list:
            chroms = Chromosome(
                chromosome = chrom["chromosome"]
            )
            chroms.save()
            
    def insert_into_sample_table(sample_list):
        for samp in sample_list:
            samples = Sample(
                sample = samp["sample"]
            )
            samples.save()
            
    def insert_into_lineage_table(lineage_list):
        for lineag in lineage_list:
            lineages = Lineage(
                lineage = lineag["lineage"],
                week = lineag["week"],
            )
            lineages.save()


    def insert_into_gene_table(gene_list):
        for gen in gene_list:
            genes = Gene(
                gene = gen["gene"]
            )
            genes.save()
        
