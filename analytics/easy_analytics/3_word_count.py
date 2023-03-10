# export SPARK_LOCAL_IP="127.0.0.1"

from pyspark import SparkContext, SparkConf
import datetime
import csv


confCluster = SparkConf().setAppName("WordCount")
sc = SparkContext(conf=confCluster)


def get_columns(tweet):
    return tweet.split(';')


def name_and_word(name, word_list):
    name_and_word = []
    for w in word_list:
        name_and_word.append((name, w))
    return name_and_word


def word_count_per_user():
    """
        Analytic 3_1
    """
    text_file = sc.textFile("data_sanitized_2")  # /A._McEachin.csv

    # 3_1 Wordcount per user
    rdd = text_file.map(lambda line: [get_columns(line)[0], get_columns(line)[4]]).flatMap(
        lambda user_text: name_and_word(user_text[0], user_text[1].split(' '))
    ).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b).sortBy(lambda x: x[1]).sortBy(lambda x: x[0][0]).collect()

    # open the CSV file and write the headers
    with open('data_preprocessed/3_word_count_per_user.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["name lastname", "word", "wordcount"])
        f.close()

    # Output ((a=name_lastname, b=word) c=wordcount)
    # This is sorted by user and by wordcount
    for i in rdd:
        ((a, b), c) = i
        print(a, b, c)
        with open('data_preprocessed/3_word_count_per_user.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([a, b, c])
            f.close()


def word_count_per_party():
    """
        Analytic 3_2 
    """

    text_file = sc.textFile("data_sanitized_2")  # /A._McEachin.csv

    # 3_1 Wordcount per user
    rdd = text_file.map(lambda line: [get_columns(line)[1], get_columns(line)[4]]).flatMap(
        lambda user_text: name_and_word(user_text[0], user_text[1].split(' '))
    ).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b).sortBy(lambda x: x[1]).sortBy(lambda x: x[0][0]).collect()

    # open the CSV file and write the headers
    with open('data_preprocessed/3_word_count_per_party.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["party", "word", "wordcount"])
        f.close()

    # Output ((a=party, b=word) c=wordcount)
    # This is sorted by party and by wordcount
    for i in rdd:
        ((a, b), c) = i
        print(a, b, c)
        with open('data_preprocessed/3_word_count_per_party.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([a, b, c])
            f.close()


def date_greater_than(d1, d2='2022-03-01'):
    try:
        d1 = datetime.datetime.strptime(d1, '%Y-%m-%d')
        d2 = datetime.datetime.strptime(d2, '%Y-%m-%d')
    except:
        return False
    return d1 > d2


def word_count_per_party_after_date(date_after):
    """
        Analytic 3_3
    """

    text_file = sc.textFile("data_sanitized_2")  # /A._McEachin.csv

    # 3_1 Wordcount per user
    rdd = text_file.map(lambda line: [get_columns(line)[1], get_columns(line)[2], get_columns(line)[4]]).filter(
        lambda party_date_text: date_greater_than(
            party_date_text[1], date_after)
    ).flatMap(
        lambda user_text: name_and_word(user_text[0], user_text[2].split(' '))
    ).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b).sortBy(lambda x: x[1]).sortBy(lambda x: x[0][0]).collect()

    # Output ((a=party, b=word) c=wordcount)
    # This is sorted by party and by wordcount
    # And filtered for tweets after the given date.

    # open the CSV file and write the headers
    with open('data_preprocessed/3_word_count_per_party_after_date.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["party", "word", "wordcount"])
        f.close()

    for i in rdd:
        ((a, b), c) = i
        print(a, b, c)
        # append the rest of data
        if (c > 400): # only for words that are used more than 400 times
            with open('data_preprocessed/3_word_count_per_party_after_date.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([a, b, c])
                f.close()


word_count_per_user()
# word_count_per_party()
# word_count_per_party_after_date('2022-03-01')
