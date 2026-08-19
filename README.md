# Host Header Injection (`host-header-injection`)

**Category:** web · **Difficulty:** medium · **Points:** 275

Password-reset / cache keys trust the Host header; poison it to steal the key.

## Run it

```bash
docker build -t sparflag/host-header-injection .
# `deca-ai start host-header-injection` (or the web UI) prints the docker run line with your
# SPARFLAG_SERVER + SPARFLAG_INSTANCE_TOKEN
```

## Recover the flag

The delivery blob is XOR-encrypted then base64-encoded. Discover the challenge key, then invert XOR+base64.

The plaintext flag is never written to disk or served — only the encoded delivery blob
is. When you have it:

```bash
deca-ai submit host-header-injection 'sparflag{...}'
```

## Hints

- Send a password-reset with an attacker-controlled Host.
- The reset token or debug page includes the XOR key.
