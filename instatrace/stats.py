# Copyright (C) 2010 Peter Teichman

import math

class Statistics:
    def __init__(self):
        self.statistics = {}

    def add_sample(self, stat_name, sample):
        stat = self.statistics.setdefault(stat_name, Histogram(stat_name))
        stat.add_sample(sample)

class Histogram:
    def __init__(self, name):
        self._name = name
        self._samples = []

        self._buckets = {}

    def _get_bucket(self, sample):
        if sample == 0:
            bucket = 0
        else:
            # use exponential buckets
            bucket = math.floor(math.exp(math.floor(math.log(sample))))

        return self._buckets.setdefault(bucket, [])

    def add_sample(self, sample):
        bucket = self._get_bucket(sample)
        bucket.append(sample)

    def stats(self):
        buckets = self._buckets.keys()
        buckets.sort()

        count = 0
        total = 0

        stats = {}

        for bucket_id in buckets:
            samples = self._buckets[bucket_id]

            bucket_stats = self._bucket_stats(samples)

            stats.setdefault("buckets", []).append((bucket_id, bucket_stats))

            count = count + bucket_stats["count"]
            total = total + bucket_stats["total"]

        stats["count"] = count
        stats["total"] = total

        stats["mean"] = mean = float(total)/count
        sum_squares = 0

        # calculate the standard deviation of the whole set
        for bucket in self._buckets.values():
            for sample in bucket:
                sum_squares = sum_squares + pow(sample-mean, 2)

        stats["stddev"] = math.sqrt(sum_squares/count)

        return stats

    def _bucket_stats(self, samples):
        count = len(samples)
        total = 0
        sum_squares = 0

        for sample in samples:
            total = total + sample

        mean = float(total) / count

        sum_squares = 0
        for sample in samples:
            sum_squares = sum_squares + pow(sample-mean, 2)

        stddev = math.sqrt(sum_squares / count)

        stats = { "count" : count,
                  "total" : total,
                  "mean" : mean,
                  "stddev" : stddev }

        return stats

    def text(self, fd):
        bar_width = 60
        stats = self.stats()

        fd.write("Histogram: %s recorded %d samples, avg = %.1f, std = %.1f\n"
                 % (self._name, stats["count"], stats["mean"], stats["stddev"]))

        # largest sample count of all buckets
        max_count = 0
        for bucket, bucket_stats in stats["buckets"]:
            if bucket_stats["count"] > max_count:
                max_count = bucket_stats["count"]

        total_pct = 0

        for bucket, bucket_stats in stats["buckets"]:
            pct = float(bucket_stats["count"]) / stats["count"] * 100

            graph = '-' * int(bar_width * pct/100) + "O"

            bar = graph + (' ' * (bar_width-len(graph)))

            percentile = ""
            if total_pct > 0:
                percentile = " {%.1f%%}" % total_pct

            total_pct = total_pct + pct

            fd.write("%-6d %s (%d = %.1f%%)%s\n" % (bucket, bar, bucket_stats["count"], pct, percentile))
