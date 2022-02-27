import os

from pathlib import Path
from trdg.generators import GeneratorFromStrings
from arabic_reshaper import ArabicReshaper
from bidi.algorithm import get_display


arabic_reshaper = ArabicReshaper()

def generate_data(strings, image_dir='SynthData_generator/images/', skewing_angle=0, size=32, output_dir="synthData", limit=1000, prefx=''):
    strings = [get_display(arabic_reshaper.reshape(str(w))) for w in strings]
    generator = GeneratorFromStrings(
        strings,
        language= 'ar',
        word_split=True,
        background_type=3,
        size=size,
        skewing_angle=skewing_angle,
    )
    
    generated_labels = []
    for (img, label) in generator:
        if limit <= 0:
            break
        
        file_name = os.path.join(output_dir, 'syn_' + str(limit)+f"{prefx}.jpg")
        in_label_file_name = os.path.join(output_dir, 'syn_' + str(limit)+f"{prefx}.jpg")
        
        img.save(file_name)
        
        generated_labels.append((in_label_file_name, label))

        limit -= 1
    
    return output_dir + '/' + save_txt(generated_labels, output_dir)
       
def save_txt(strings, path):
    name = 'synth.txt'
    
    label_file = open(os.path.join(path, name), 'w', encoding='utf8')
    
    for l in strings: 
        line = '\t'.join(l)
        label_file.write(line)
        label_file.write('\n')
    return name