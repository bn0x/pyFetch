def time_metric(secs=60):
    """\
    Returns user-readable string representing given number of seconds.

    :param secs: int
    :rtype: string
    """
    time = ''
    for metric_secs, metric_char in [[7*24*60*60, 'w'], [24*60*60, 'd'], [60*60, 'h'], [60, 'm']]:
        if secs > metric_secs:
            time += '{}{}'.format(int(secs / metric_secs), metric_char)
            secs -= int(secs / metric_secs) * metric_secs
    if secs > 0:
        time += '{}s'.format(secs)
    return time

def sizeof_fmt(num):
    """\
    Return a human-readable representation of a number of bytes.

    :param num: int
    :rtype: string
    """
    for x in [ 'bytes', 'KB', 'MB', 'GB' ]:
        if num < 1024.0 and num > -1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')