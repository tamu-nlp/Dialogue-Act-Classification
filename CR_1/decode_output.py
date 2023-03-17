import json

def convert_mention(mention, output, comb_text):
    start = output['subtoken_map'][mention[0]]
    end = output['subtoken_map'][mention[1]] + 1
    nmention = (start, end)
    mtext = ''.join(' '.join(comb_text[mention[0]:mention[1]+1]).split(" ##"))
    return (nmention, mtext)


def get_clusters(out_filename):
    output = json.load(open(out_filename))
    comb_text = [word for sentence in output['sentences'] for word in sentence]
    seen = set()
    #print('Clusters:')
    op_cluster = []
    for cluster in output['predicted_clusters']:
        mapped = []
        for mention in cluster:
            seen.add(tuple(mention))
            mapped.append(convert_mention(mention, output, comb_text))
        #print(mapped, end=",\n")

        op_cluster.append(mapped)


    #print('\nMentions:')
    for mention in output['top_spans']:
        if tuple(mention) in seen:
            continue
        #print(convert_mention(mention, output, comb_text), end=",\n")

    cluster_json = {}
    for i, cl in enumerate(op_cluster):
        cluster_json[f'cluster_{i}'] = cl

    return cluster_json


#cluster_json = get_clusters('out.jsonlines')

#print(cluster_json)