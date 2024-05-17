import zipfile
import re

#Creator Mikhail Kupreichyk from group 253503
#version 1
#Lab number 4
#08.05.2024
#Variant 14
class Analyser:
    Text = ""

    def __init__(self, text):
        self.text = text
        Analyser.Text = text

    def num_of_sentences(self):
        """Calc num of sentences"""
        sen = re.findall(r"([^.?;!]+[.?!]{1})", self.text)
        return len(sen)
    def num_of_sentences_types(self):
        """Calc num of sentences[! . ... ?]"""
        inter = re.findall(r"([^.?!;]+\?{1})", self.text) #?
        imper = re.findall(r"([^.?!;]+\!{1})", self.text) #!
        tree_dots = re.findall(r"([^.?!;]+\.{3})", self.text) #...

        default = self.num_of_sentences() - len(inter) - len(imper) - len(tree_dots)

        return default, len(inter), len(imper), len(tree_dots)

    def average_sent_len(self):
        """Calc average len of sentences in text"""
        sen = re.findall(r"([^.?;!]+[.?;!]{1})", self.text)

        all_ch = 0

        for sentence in sen:
            words = re.findall(r"[а-яА-ЯёЁ]+", sentence)

            all_ch += sum([len(word) for word in words])

        if len(sen) == 0:
            return 0

        return all_ch / len(sen)

    def average_word_len(self):
        """Calc average len of words in text"""
        words = re.findall(r"[а-яА-ЯёЁ]+", self.text)

        return sum([len(word) for word in words]) / len(words)

    def count_smiles(self):
        """Finds all smiles in text"""
        smiles = re.findall(r"([:;]{1}\-*((\(+)|(\)+)|(\[+)|(\]+)))", self.text)
        return len(smiles)

    def __str__(self):
        return self.text

class MixinTwoCharactersInRow:
    def TwoCharactersInRow(self):
        """Find all words with 2 chars in row in text"""
        words_2char_match = re.findall(r"([^0-9\'\" .?!,\n()[\]-]*([^0-9\'\" .?!,\n()[\]-])\2[^0-9\'\" !?.,\n()[\]-]*)", self.text)
        words = re.findall(r"[а-яА-ЯёЁ]+", self.text)

        words_2char = [match[0] for match in words_2char_match]

        list = []

        i = 0

        for word2char in words_2char:
            for word in words:
                if(word == word2char):
                    if i in list:
                        i += 1
                        continue

                    list.append(i + 1)
                    i = 0
                    break
                else:
                    i += 1

        #print(sorted(words_2char))

        #print("Indexes: ")
        #print(list)

        return sorted(words_2char), list

class OptionTextAnalyser(Analyser, MixinTwoCharactersInRow):

    def __init__(self, text):
        super().__init__(text)

    def all_dates(self):
        """Finds all dates in text"""
        dates = re.findall(r"([0-9]{2}\-[0-9]{2}\-[0-9]{4})", self.text)

        #print(dates)

        return dates

    def from_end_third_con_pen_vow(self):
        """Finds words with from end third char is con and last char is vow"""
        words_match = re.findall(r"(([А-ЯЁа-яё]*[БбВвГгДдЖжЗзЙйКкЛлМмНнПпРрСсТтФфХхЦцЧчШщЩщ][а-яё][аеёио"
                           r"уыэюя])[^а-яА-яёЁ])", self.text)

        words = [match[0] for match in words_match]

        print(words)

        return words

    def vow_in_begin(self):
        """Finds words with from begin char is vow"""
        words_match = re.findall(r"(([АЕЁИОУЫЭЮЯ]|(\ [аеёиоуыэюя])){1}[а-яё-]*)", self.text)

        words = [match[0] for match in words_match]

        print(words)

        return words


class Zipper:
    """Class for zipping and getting info from zip"""

    def __init__(self, filename):
        self.filename = filename

    def zip_results(self, results):
        """Method for zipping results"""
        try:
            with zipfile.ZipFile(self.filename, 'w') as zip_file:
                for key, value in results.items():
                    # zip_file.writestr(key + '.txt', '\n'.join(map(str, value)))
                    zip_file.writestr(key + '.txt', str(value))
        except FileNotFoundError:
            print(f"Error: File '{self.filename}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def get_zip_info(self):
        """Method for getting info from zip"""
        try:
            with zipfile.ZipFile(self.filename, 'r') as zip_file:
                for info in zip_file.infolist():
                    file_content = zip_file.read(info.filename).decode('utf-8')
                    print(f"Filename: {info.filename}")
                    print(f"File size: {info.file_size}")
                    print(f"Compressed size: {info.compress_size}")
                    print(f"Compress type: {info.compress_type}")
                    print(f"Content:\n{file_content}\n")
        except FileNotFoundError:
            print(f"Error: File '{self.filename}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

def main():
    text = ''

    try:
        with open("D:\\253503_KUPREICHYK_14\igi\\text.txt", 'r', encoding="utf-8") as readfile:
            text = readfile.read()
    except Exception as e:
        print("Ошибка при работе с файлом!")

    cl = OptionTextAnalyser(text)

    zip = Zipper("D:\\253503_KUPREICHYK_14\igi\z.txt")

    list = {}

    list["num_of_sentences()"] = (cl.num_of_sentences())

    list["num_of_sentences_types()"] = (cl.num_of_sentences_types())

    list["TwoCharactersInRow()"] = (cl.TwoCharactersInRow())

    list["vow_in_begin()"] = (cl.vow_in_begin())

    list["all_dates()"] = (cl.all_dates())

    list["from_end_third_con_pen_vow()"] = (cl.from_end_third_con_pen_vow())

    zip.zip_results(list)

    zip.get_zip_info()

if __name__ == '__main__':
    main()



