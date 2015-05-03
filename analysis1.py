import locale
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

normed = True
# filters can be an empty list, or positive items to extract from the data
#text_filters = ['software', 'engineer', 'programmer']
#text_filters = ['teach']  # teacher, teaching
text_filters = []

# load the data
df = pd.read_csv("#TalkPay Tweets - Sheet1.csv")
df['pay_'] = df['Yearly Pay'].map(lambda s: float(s.replace("$", "").replace(",", "")))
df = df.ix[df['pay_'] > 0]  # filter at least $1000 (to remove guff tweets)

# we could strip out data
def filter_keywords_present(s):
    "True if any text_filters are present in lowercased s"
    for fltr in text_filters:
        if fltr in s.lower():
            return True
    return False

if text_filters:
    df['text_filter'] = df['Tweet'].map(filter_keywords_present)
    print("Applying filter:", text_filters)
    df = df[df['text_filter']]

# set US locale
locale.setlocale(locale.LC_ALL, 'en_US.utf8')
# setlocale maybe can edit the monetary frac_digits, but I can't figure it out

plt.figure(1)
plt.clf()
fontsize = "medium"
x_max = 260001  # 280000
step = 10000
bins = np.arange(0, x_max, step)
#x_labels = [locale.currency(x, grouping=True)[:-3]+"+" for x in np.arange(0, x_max, step)]
x_labels = ["$"+str(x)[:-3]+"k+" for x in np.arange(0, x_max-1, step)]
x_labels[0] = ">$0"
# Note that masked arrays aren't supportd by plt.hist, so we extract the raw
# values
pay = df['pay_'].values
res=plt.hist(pay, bins=bins, normed=normed, cumulative=normed)
ticks = plt.xticks(np.arange(0, x_max, step),
                   x_labels,
                   rotation=45,
                   ha="center",
                   fontsize=fontsize)

plt.yticks(fontsize=fontsize)

plt.xlabel("USD Annual Salary", fontsize=fontsize)
if normed:
    plt.ylabel("Cumulative percentage of {} People".format(len(df)), fontsize=fontsize)
    percentiles = [0.9, 0.75, 0.5, 0.25]
    plt.hlines(percentiles, 0, x_max, colors='r')
    for percentile in percentiles:
        plt.annotate("{:n}%".format(percentile*100), (10000, percentile+0.01))
else:
    plt.ylabel("Number of People (of {})".format(len(df)), fontsize=fontsize)
title = "#TalkPay Tweets by @echen May 2015 (viz @IanOzsvald)"
if text_filters:
    title += "\nFiltered for any of: " + ", ".join(text_filters)
plt.title(title)
plt.xlim((0, x_max))
plt.tight_layout()
if normed:
    plt.savefig("talkpay_summary_normed.png")
else:
    plt.savefig("talkpay_summary.png")
plt.show()
