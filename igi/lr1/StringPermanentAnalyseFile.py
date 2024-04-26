def find_substrings():
    """Function that operate with string: determine the number of words whose length is less than 7 characters, find
    the shortest word ending with the letter 'a' and display all words in descending order of their lengths."""
    str = ("So she was considering in her own mind, as well as she could, for the hot day made her feel very sleepy and "
           "stupid, whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking "
           "the daisies, when suddenly a White Rabbit with pink eyes ran close by her.")
    str.replace(",", "")

    all_words = str.split(" ")

    dict = {}

    for word in all_words:
        if len(word) in dict:
            dict[len(word)].append(word)
        else:
            dict[len(word)] = [word]

    print("\nAll words with their lenght:")
    for key in sorted(dict.keys(), reverse=True):
        print(f"{key}: {dict[key]}")

    print(f"\nNumber of words with lenght < 7: {len([len(word) for word in all_words if len(word) < 7])}")

    print(f"\nShortest word that ends with 'a' symbol: {min([word for word in all_words if word.endswith('a')], key=len)}")