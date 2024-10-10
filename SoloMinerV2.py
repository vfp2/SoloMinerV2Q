import binascii
import hashlib
import json
import logging
import os
import random
import socket
import threading
import time
import traceback
from datetime import datetime
from signal import SIGINT, signal

import requests
from colorama import Back, Fore, Style

# Import Qiskit for quantum computing
from qiskit import Aer, QuantumCircuit, execute
from qiskit.algorithms import Grover, AmplificationProblem
from qiskit.providers.aer import QasmSimulator
from hashlib import sha256


class Context:
    def __init__(self):
        self.fShutdown = False
        self.listfThreadRunning = [False] * 2
        self.local_height = 0
        self.nHeightDiff = {}
        self.updatedPrevHash = None
        self.job_id = None
        self.prevhash = None
        self.coinb1 = None
        self.coinb2 = None
        self.merkle_branch = None
        self.version = None
        self.nbits = None
        self.ntime = None
        self.clean_jobs = None
        self.sub_details = None
        self.extranonce1 = None
        self.extranonce2_size = None


ctx = Context()
sock = None


def timer():
    tcx = datetime.now().time()
    return tcx


# Changed this Address And Insert Your BTC Wallet
address = os.getenv('BC_ADDRESS')

print(Back.BLUE, Fore.WHITE, 'BTC WALLET:', Fore.BLACK, str(address), Style.RESET_ALL)


def handler(signal_received, frame):
    ctx.fShutdown = True
    print(Fore.MAGENTA, '[', timer(), ']', Fore.YELLOW, 'Terminating Miner, Please Wait..')


def logg(msg):
    logging.basicConfig(level=logging.INFO, filename="miner.log",
                        format='%(asctime)s %(message)s')
    logging.info(msg)


def get_current_block_height():
    r = requests.get('https://blockchain.info/latestblock')
    return int(r.json()['height'])


def check_for_shutdown(t):
    n = t.n
    if ctx.fShutdown:
        if n != -1:
            ctx.listfThreadRunning[n] = False
            t.exit = True


class ExitedThread(threading.Thread):
    def __init__(self, arg, n):
        threading.Thread.__init__(self)
        self.arg = arg
        self.n = n
        self.exit = False

    def thread_handler(self):
        pass


class CoinMinerThread(ExitedThread):
    def __init__(self, arg=None):
        super(CoinMinerThread, self).__init__(arg, n=0)

    def thread_bitcoin_miner(self, arg):
        ctx.listfThreadRunning[self.n] = True
        check_for_shutdown(self)
        try:
            ret = quantum_miner(self)
            logg(f"[*] Miner returned {'true' if ret else 'false'}")
            print(Fore.LIGHTCYAN_EX, f"[*] Miner returned {'true' if ret else 'false'}")
        except Exception as e:
            logg("[*] Miner()")
            print(Back.WHITE, Fore.MAGENTA, "[", timer(), "]", Fore.BLUE, "[*] Miner()")
            logg(e)
            traceback.print_exc()
        ctx.listfThreadRunning[self.n] = False


class NewSubscribeThread(ExitedThread):
    def __init__(self, arg=None):
        super(NewSubscribeThread, self).__init__(arg, n=1)

    def thread_new_block(self, arg):
        ctx.listfThreadRunning[self.n] = True
        check_for_shutdown(self)
        try:
            ret = block_listener(self)
        except Exception as e:
            logg("[*] Subscribe thread()")
            print(Fore.MAGENTA, "[", timer(), "]", Fore.YELLOW, "[*] Subscribe thread()")
            logg(e)
            traceback.print_exc()
        ctx.listfThreadRunning[self.n] = False


# Quantum mining section with Grover's algorithm
def sha256_hash(input_data):
    """Hash the input data using SHA-256."""
    return sha256(input_data.encode('utf-8')).hexdigest()


def check_solution(nonce, previous_hash, difficulty):
    """Check if the current hash satisfies the difficulty."""
    data = previous_hash + str(nonce)
    hash_value = sha256_hash(data)
    return hash_value.startswith('0' * difficulty), hash_value


def grover_search_nonce(previous_hash, difficulty):
    """Use Grover's algorithm to search for the correct nonce."""
    num_qubits = 10  # Simplified example
    qc = QuantumCircuit(num_qubits)
    
    # Oracle problem for nonce search
    problem = AmplificationProblem(oracle=None)  # This would need a quantum oracle for the correct nonce
    grover = Grover(iterations=1)
    result = grover.amplify(problem)

    qc.measure_all()
    job = execute(qc, backend=Aer.get_backend('qasm_simulator'), shots=1)
    result = job.result()
    counts = result.get_counts()

    nonce = random.choice(list(counts.keys()))
    return nonce


def quantum_miner(previous_hash):
    difficulty = 4  # Simplified difficulty for the example
    while True:
        nonce = grover_search_nonce(previous_hash, difficulty)
        is_valid, hash_value = check_solution(nonce, previous_hash, difficulty)

        if is_valid:
            print(f"Successfully mined a block! Nonce: {nonce}, Hash: {hash_value}")
            return nonce, hash_value
        else:
            print(f"Attempt failed. Nonce: {nonce}, Hash: {hash_value}")


def StartMining():
    subscribe_t = NewSubscribeThread(None)
    subscribe_t.start()
    logg("[*] Subscribe thread started.")
    print(Fore.MAGENTA, "[", timer(), "]", Fore.GREEN, "[*] Subscribe thread started.")
    
    time.sleep(4)

    miner_t = CoinMinerThread(None)
    miner_t.start()
    logg("[*] Bitcoin Miner Thread Started")
    print(Fore.MAGENTA, "[", timer(), "]", Fore.GREEN, "[*] Bitcoin Miner Thread Started")
    print(Fore.BLUE, '--------------~~( ', Fore.YELLOW, 'mmi.fp2.dev', Fore.BLUE, ' )~~--------------')


if __name__ == '__main__':
    signal(SIGINT, handler)
    StartMining()
