import gevent
import requests
from urllib3 import Retry
from timeit import default_timer
from requests.adapters import HTTPAdapter
BASE_URL = 'http://127.0.0.1:5000'
MAX_ELEMENTS = 10000000

# Setting up retry adapter
retry = Retry(connect=10, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)


def push_request(val, s) -> None:
    # perform a max request every 1000 push requests
    if val!= 0 and val % 1000 == 0:
        max_request(val, s)
    s.post(f'{BASE_URL}/push', json={'value': val})


def max_request(val, s) -> None:
    start = default_timer()
    s.get(f'{BASE_URL}/max')
    elapsed = default_timer() - start
    print(f"PUSH# {val} Max latency --> {elapsed}")


def pop_request(s) -> None:
    s.post(f'{BASE_URL}/pop')


def stress_test() -> None:
    start = default_timer()
    with requests.Session() as session:
        push_jobs = []
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        push_start = default_timer()

        print("----Now pushing----")
        # performing MAX_ELEMENTS number of PUSH requests concurrently
        for val in range(MAX_ELEMENTS):
            push_jobs.append(gevent.spawn(push_request, val, session))

        gevent.wait(push_jobs)
        push_elapsed = default_timer() - push_start
        print(f"{MAX_ELEMENTS} PUSH requests performed for {push_elapsed} seconds")
        print("----Now Popping----")
        pop_start = default_timer()
        pop_jobs = []

        # performing MAX_ELEMENTS number of POP requests concurrently
        for i in range(MAX_ELEMENTS):
            pop_jobs.append(gevent.spawn(pop_request(session)))
        gevent.wait(pop_jobs)
        pop_elapsed = default_timer() - pop_start
        print(f'{MAX_ELEMENTS} POP requests performed for {pop_elapsed} seconds')

    elapsed = default_timer() - start
    print(f'Total elapsed time: {elapsed} seconds')


if __name__ == '__main__':
    stress_test()
