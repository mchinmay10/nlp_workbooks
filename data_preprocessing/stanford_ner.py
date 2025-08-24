import os
from nltk.tag import StanfordNERTagger

# Defining paths to Stanford NER files
stanford_ner_path = "/Users/admin/stanford-ner-2020-11-17"
stanford_ner_jar = os.path.join(
    stanford_ner_path,
    "stanford-ner-4.2.0.jar",
)
stanford_ner_model = os.path.join(
    stanford_ner_path,
    "classifiers/english.all.3class.distsim.crf.ser.gz",
)


# Perform NER on the master output file
def ner_tagging(input_file):
    output_file = "tagged_entities.txt"
    total_tags = []
    try:
        st = StanfordNERTagger(stanford_ner_model, stanford_ner_jar, encoding="utf-8")
    except:
        print(f"Error initializing StanfordNERTagger: {e}")
        print("Please check your file paths and Java installation.")
        exit()
    with open(input_file, "r") as f_in:
        text = f_in.readlines()
        tagged_entities = st.tag(text)
        total_tags.extend(tagged_entities)
    with open(output_file, "w") as f_out:
        f_out.write(f"{len(tagged_entities)}" + "\n")
        for entity in tagged_entities:
            f_out.write(str(entity) + "\n")
    return output_file
