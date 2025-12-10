import pandas as pd
from ..cleaners.symptom_cleaner import clean_symptom
from ..cleaners.disease_cleaner import clean_disease

class DatasetMerger:
    def __init__(self, synonyms=None):
        self.synonyms = synonyms or {}

    def merge(self, staged_list):
        """staged_list: list of (source_name, df) where df has disease and symptoms(list)"""
        rows = []
        all_symptoms = set()
        for source_name, df in staged_list:
            for _, r in df.iterrows():
                disease = clean_disease(r['disease'])
                # ensure symptoms is list
                symptoms = r.get('symptoms') or []
                if isinstance(symptoms, str):
                    symptoms = [s.strip() for s in symptoms.split(',') if s.strip()]
                cleaned = []
                for s in symptoms:
                    cs = clean_symptom(s, self.synonyms)
                    if cs:
                        cleaned.append(cs)
                        all_symptoms.add(cs)
                rows.append({'disease': disease, 'symptoms': list(set(cleaned)), 'source': source_name})

        master_df = pd.DataFrame(rows)
        # deduplicate by disease+sorted symptoms signature
        master_df['sig'] = master_df.apply(lambda r: r['disease'] + '|' + '|'.join(sorted(r['symptoms'])), axis=1)
        master_df = master_df.drop_duplicates('sig').drop(columns=['sig'])

        # build feature index
        feature_index = {s: i for i, s in enumerate(sorted(all_symptoms))}
        return master_df, feature_index
