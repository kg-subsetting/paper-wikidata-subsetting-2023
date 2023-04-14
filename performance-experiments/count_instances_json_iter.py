import sys
import json
import itertools
import multiprocessing
from datetime import datetime

def count_instances_worker(dump: str, start_line: int, end_line: int):
    genes = 0
    proteins = 0
    chemicals = 0
    diseases = 0
    operons = 0
    acids = 0
    gene_statements = 0
    protein_statements = 0
    chemical_statements = 0
    disease_statements = 0
    all_statements = 0
    all_items = 0
    statement_ctr = 0
    is_gene = False
    is_protein = False
    is_chemical = False
    is_disease = False
    is_operon = False
    is_acid = False
    with open(dump, 'r') as d:
        for _ in itertools.islice(d, start_line-1):
            pass
        
        for line_number, line in enumerate(itertools.islice(d, end_line - start_line + 1), start=start_line):            
            try:
                data = json.loads(line[:-2])
            except Exception as e:
                print('Error processing line {0}: {1}'.format(line_number,e))
                continue
            for key in data:
                if key == 'claims':
                    statement_ctr = 0
                    is_gene = False
                    is_protein = False
                    is_chemical = False
                    is_disease = False
                    is_operon = False
                    is_acid = False
                    for subkey in data[key]:                        
                        for item in data[key][subkey]:
                            statement_ctr += 1
                            if subkey == 'P31':
                                if 'mainsnak' not in item.keys(): continue
                                if 'datavalue' not in item['mainsnak'].keys(): continue
                                if 'value' not in item['mainsnak']['datavalue'].keys(): continue
                                if 'numeric-id' not in item['mainsnak']['datavalue']['value'].keys(): continue
                                if str(item['mainsnak']['datavalue']['value']['numeric-id']) == '7187':
                                    is_gene = True
                                if str(item['mainsnak']['datavalue']['value']['numeric-id']) == '8054':
                                    is_protein = True
                                if str(item['mainsnak']['datavalue']['value']['numeric-id']) == '11173':
                                    is_chemical = True
                                if str(item['mainsnak']['datavalue']['value']['numeric-id']) == '12136':
                                    is_disease = True
                                if str(item['mainsnak']['datavalue']['value']['numeric-id']) == '139677':
                                    is_operon = True
                                if str(item['mainsnak']['datavalue']['value']['numeric-id']) == '11158':
                                    is_acid = True
            all_items += 1
            all_statements += statement_ctr            
            if is_gene:
                genes += 1
                gene_statements += statement_ctr
            if is_protein:
                proteins += 1
                protein_statements += statement_ctr
            if is_chemical:
                chemicals += 1
                chemical_statements += statement_ctr
            if is_disease:
                diseases += 1
                disease_statements += statement_ctr
            if is_operon:
                operons += 1
            if is_acid:
                acids += 1
    
    return genes, proteins, chemicals, diseases, operons, acids, gene_statements, protein_statements, chemical_statements, disease_statements, all_items,  all_statements


if __name__ == '__main__':
    dump = sys.argv[1]
    lines = int(sys.argv[2])
    cores = int(sys.argv[3])

    chunk_size = lines // cores
    chunks = [(i * chunk_size + 1, (i + 1) * chunk_size) for i in range(cores - 1)]
    chunks.append(((cores - 1) * chunk_size + 1, lines))

        
    pool = multiprocessing.Pool(cores)
    start_time = datetime.now()
    results = pool.starmap(count_instances_worker, [(dump, start_line, end_line) for start_line, end_line in chunks])
    end_time = datetime.now()
    
    output_dict = {
        'Genes': sum(result[0] for result in results),
        'Proteins': sum(result[1] for result in results),
        'Chemicals': sum(result[2] for result in results),
        'Diseases' : sum(result[3] for result in results),
        'Operons': sum(result[4] for result in results),
        'Acids': sum(result[5] for result in results),
        'Gene Statements': sum(result[6] for result in results),
        'Protein Statements': sum(result[7] for result in results),
        'Chemical Statements': sum(result[8] for result in results),
        'Disease Statements': sum(result[9] for result in results),
        'All Items': sum(result[10] for result in results),
        'All Statements': sum(result[11] for result in results)
    }

    with open('output.txt', 'w') as o:
        for key, value in output_dict.items():
            print('{0}: {1}'.format(key, value), file=o)
            print('{0}: {1}'.format(key, value))
        print('\nComputed in: {0:.1f} seconds'.format((end_time-start_time).total_seconds()), file=o)
        print('\nComputed in: {0:.1f} seconds'.format((end_time-start_time).total_seconds()))
