import locale
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# load the data
df = pd.read_csv("#TalkPay Tweets - Sheet1.csv")
df['pay_'] = df['Yearly Pay'].map(lambda s: float(s.replace("$", "").replace(",", "")))
df = df.ix[df['pay_'] > 0]  # filter at least $1000 (to remove guff tweets)
# we could strip out data
#df['sweng'] = df['Tweet'].map(lambda s: 'software' in s.lower() or 'engineer' in s.lower())
#df = df[df['sweng']]

# set US locale
locale.setlocale(locale.LC_ALL, 'en_US.utf8')
# setlocale maybe can edit the monetary frac_digits, but I can't figure it out

plt.figure(1)
plt.clf()
fontsize="medium"
normed=True
x_max = 260001  # 280000
step = 10000
bins = np.arange(0, x_max, step)
#x_labels = [locale.currency(x, grouping=True)[:-3]+"+" for x in np.arange(0, x_max, step)]
x_labels = ["$"+str(x)[:-3]+"k+" for x in np.arange(0, x_max-1, step)]
x_labels[0] = ">$0"
res=plt.hist(df['pay_'], bins=bins, normed=normed, cumulative=normed)
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
    plt.ylabel("Number of {} People".format(len(df)), fontsize=fontsize)
plt.title("#TalkPay Tweets by @echen May 2015 (viz @IanOzsvald)")
plt.xlim((0, x_max))
plt.tight_layout()
if normed:
    plt.savefig("talkpay_summary_normed.png")
else:
    plt.savefig("talkpay_summary.png")
plt.show()
