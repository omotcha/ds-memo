## faq

---

Q: (**Python SDK connection**) ImportError: Cannot import encode-abi from eth-abi.

A: Downgrade the eth-abi to 3.0.0. Chainmaker python sdk uses outdated eth-abi, so may not be compatible with web3.py.