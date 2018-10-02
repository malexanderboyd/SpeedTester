import os
import time
import datetime
import speedtest
from slackclient import SlackClient


def do_speedtest():
    print('Starting speed test...')
    s = speedtest.Speedtest()
    s.get_best_server()
    s.download()
    s.upload()
    return s.results.dict()


def convert_to_mbps(bits_sec):
    return bits_sec / pow(10, 6)


def formatted_time():
    timestamp = time.time()
    value = datetime.datetime.fromtimestamp(timestamp)
    return value.strftime('%Y-%m-%d %H:%M:%S')


def convert_for_human(speedtest_results):
    if speedtest_results is None:
        return speedtest_results

    for test_type in ['download', 'upload']:
        if test_type not in speedtest_results:
            continue
        to_mb = convert_to_mbps(speedtest_results.get(test_type))
        speedtest_results[test_type] = round(to_mb, 2)

    return speedtest_results


def send_speedtest_results(results):
    slack_token = os.environ["SLACK_API_TOKEN"]
    sc = SlackClient(slack_token)

    sc.api_call(
        "chat.postMessage",
        channel="C0XXXXXX",
        text="SpeedTest Results ({})\nDownload: {} (Mbps)\nUpload: {} (Mbps)\n\n".format(
            formatted_time(),
            results['download'],
            results['upload']
        )
    )


speedtest_results = do_speedtest()
speedtest_results = convert_for_human(speedtest_results)
print(formatted_time())
print(speedtest_results)
