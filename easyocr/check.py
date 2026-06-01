import easyocr

class Check_detecter:
    def __init__(self):
        
        self.model = easyocr.Reader(['ru'], gpu=False)

    def result_check(self, path_check):
        
        result = self.model.readtext(path_check)
        
        return self.processing_check(result)

    def processing_check(self, result):
        
        start_words = ['документ', 'плательщик', 'рн скко']
        stop_words = ['итого', 'к оплате', 'всего', 'сумма']
        musor = ['свеж', 'вес', 'кг', 'свежий', 'сорт', 'крупный', 'мелкий',
                       'док', 'све', 'платемный', 'документ', 'плательщик', '&']

        rub = False   #rubilnik
        tov = []

        for box, text, acc in result:
            text_lower = text.lower()

            if not rub:
                for word in start_words:
                    if word in text_lower:
                        rub = True
                        break
                continue 


            for word in stop_words:
                if word in text_lower:
                    return tov


            words = text.split()
            clean_words = []
            for simv in words:

                clean = simv.strip('.,;:!?()"\'')
                if clean.lower() not in musor and len(clean) > 1:
                    clean_words.append(clean)
            cleanes = ' '.join(clean_words).strip()

            if len(cleanes) > 2 and any(s.isalpha() for s in cleanes):
                tov.append(cleanes.lower())

        return tov