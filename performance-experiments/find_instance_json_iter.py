import sys
import json
import itertools
import multiprocessing
from datetime import datetime


def count_instances_worker(dump: str, qid: str, start_line: int, end_line: int, strip_len: int, lock: multiprocessing.Lock, terminate_flag: multiprocessing.Value):
    with open(dump, 'r') as d:
        for _ in itertools.islice(d, start_line-1):
            pass

        for line_number, line in enumerate(itertools.islice(d, end_line - start_line + 1), start=start_line):
            with lock:
                if terminate_flag.value:
                    return

            try:
                data = json.loads(line[:strip_len])
            except Exception as e:
                print('Error processing line {0}: {1}'.format(line_number, e))
                continue

            if data['id'] == qid:
                with open('item-{0}-found.json'.format(qid), 'w') as fout:
                    json.dump(data, fout, ensure_ascii=False, indent=4)

                with lock:
                    terminate_flag.value = 1
                    return


if __name__ == '__main__':
    dump = sys.argv[1]
    qid = sys.argv[2]
    lines = int(sys.argv[3])
    cores = int(sys.argv[4])
    if len(sys.argv) == 6 and sys.argv[5] == 'wdf':
        strip_len = -1
    else:
        strip_len = -2

    chunk_size = lines // cores
    chunks = [(i * chunk_size + 1, (i + 1) * chunk_size) for i in range(cores - 1)]
    chunks.append(((cores - 1) * chunk_size + 1, lines))

    manager = multiprocessing.Manager()
    lock = manager.Lock()
    terminate_flag = manager.Value('i', 0)

    pool = multiprocessing.Pool(cores)
    start_time = datetime.now()
    results = pool.starmap(
        count_instances_worker,
        [(dump, qid, start_line, end_line, strip_len, lock, terminate_flag) for start_line, end_line in chunks]
    )
    end_time = datetime.now()

    with lock:
        terminate_flag.value = 1  # Signal termination to all processes

    pool.close()
    pool.join()

