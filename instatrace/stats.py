# Copyright (C) 2010 Peter Teichman

import logging
import math
import simplejson as json

_log = logging.getLogger("instatrace")

DUMP_MAGIC_HEADER = "Instatrace:"

class Accumulator:
    def __init__(self, configfile=None):
        self.statistics = {}

    def add_sample(self, stat_name, sample):
        stat = self.statistics.setdefault(stat_name, [])
        stat.append(sample)

    def dump(self, fd):
        fd.write("%s1\n" % DUMP_MAGIC_HEADER)
        json.dump(self.statistics, fd)
        fd.write("\n")

    def _load_dump_v1(self, fd):
        self.statistics = json.load(fd)

    def load(self, filename, stat_names=None, filter_with=None):
        fd = open(filename)

        magic = fd.read(len(DUMP_MAGIC_HEADER))
        if magic == DUMP_MAGIC_HEADER:
            ver = fd.read(1)
            if ver == "1":
                return self._load_dump_v1(fd)
        else:
            # rewind back to the first line
            fd.seek(0)

            for line in fd.xreadlines():
                if filter_with is not None:
                    pos = line.find(filter_with)
                    if pos == -1:
                        continue
                    line = line[pos+len(filter_with):]

                if stat_names and not self._line_matches(line, stat_names):
                    continue

                line = line.strip()

                stat = line.split(" ", 2)
                if len(stat) >= 2:
                    try:
                        self.add_sample(stat[0], int(stat[1]))
                    except ValueError:
                        _log.warn("skipped bad trace value (non-integer?): %s %s",
                                  stat[0], stat[1])

        fd.close()

    def _line_matches(self, line, stats):
        for stat in stats:
            if line.find(stat) != -1:
                return True
        return False

class Statistic:
    def __init__(self, name, samples, config):
        self._name = name
        self._samples = samples

        # pull in this Histogram's options from the config file
        self._options = {}
        self._options.update(config.defaults())
        if config.has_section(name):
            self._options.update(config.items(name))

        self._buckets = {}

        # load our samples
        for sample in self._samples:
            self.add_sample(sample)

    def _get_bucket(self, sample):
        if sample == 0:
            bucket = 0
        else:
            if self._options["layout"] == "linear":
                bucket = math.floor(sample)
            else:
                # use exponential buckets
                bucket = math.floor(math.exp(math.floor(math.log(sample))))

        return self._buckets.setdefault(bucket, [])

    def add_sample(self, sample):
        scale = self._options.get("scale")
        if scale is not None:
            sample = sample / int(scale)

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

    def write_text_histogram(self, fd):
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
