import json

with open('sample_data.json', 'r', encoding='utf-8') as input_file, open('processed_data.json', 'a', encoding='utf-8') as output_file:
    for i,line in enumerate(input_file):
        if i % 10000 == 0:
            print(i)
        if i == 5000000:
            break
        json_object = json.loads(line)
        also_buy_data = list(json_object['also_buy'])
        also_buy_data.append(json_object['asin'])
        sample = {'sample': also_buy_data}
        #print(sample)
        output_file.write(json.dumps(sample) + '\n')
