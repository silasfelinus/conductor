# Alexandria: Machine Check Event triage

Filed 2026-09-13 from an Unraid notification Silas relayed: *"Machine Check Events
detected on your server — your server has detected hardware errors. The output of
mcelog has been logged. Post your diagnostics and ask for assistance on the Unraid
forums."*

Alexandria is the Unraid host that runs the `kindrobots.org` production container, the
MariaDB/ProxySQL stack behind it, and ~50 other containers. A Machine Check Event is the
CPU reporting a hardware-level fault — bad RAM, a failing memory controller, a CPU cache
or bus error, or (less often) an unstable power/clock condition. It is the first
*physical-layer* signal this project has had, and it arrives on a host with four
unexplained production incidents in the last nine days.

No agent session has shell or UI access to Alexandria, so everything below is for Silas
to run. Nothing here prints a credential.

## 1. Capture the evidence before rebooting

Unraid keeps `/var/log` in RAM unless *Settings → Syslog Server → Mirror syslog to flash*
is on. **A reboot erases the mcelog record.** Capture first, reboot second.

```sh
# What mcelog actually recorded (the notification's source)
tail -n 100 /var/log/mcelog

# The kernel's own view, with human-readable timestamps
dmesg -T | grep -iE 'mce|machine check|hardware error|corrected|edac' | tail -n 60
```

On an AMD CPU `mcelog` is often thin or empty — it is an Intel-oriented tool. The
`dmesg` line above is the reliable one on either vendor.

## 2. Find out which part

```sh
# Per-DIMM error counters: which slot is accumulating errors
grep -H . /sys/devices/system/edac/mc/mc*/dimm*/dimm_label
grep -H . /sys/devices/system/edac/mc/mc*/dimm*/dimm_ce_count   # correctable
grep -H . /sys/devices/system/edac/mc/mc*/dimm*/dimm_ue_count   # uncorrectable

# Map an EDAC slot label to the physical stick
dmidecode -t memory | grep -E 'Locator|Size:|Part Number|Manufacturer'

# Only if the board has a BMC (server boards; most consumer boards don't)
ipmitool sel elist
```

## 3. How to read it

| What you see | What it means | What to do |
|---|---|---|
| `Corrected error` / rising `dimm_ce_count` on **one** slot | That DIMM is failing. ECC caught it, so nothing was corrupted — yet. | Schedule a replacement. Reseat first; if the count keeps climbing on the same slot, swap the stick. |
| Correctable errors spread evenly across **all** slots | More likely the memory controller, the CPU's IMC, or an unstable XMP/EXPO profile than the sticks. | Drop memory to JEDEC/stock speed and watch for a few days before buying RAM. |
| `Uncorrected` / `UE` / `Processor context corrupt` | Serious. Data in flight can be silently wrong, and processes die at random. | Treat as urgent. Run MemTest86 (Unraid ships it on the boot menu) and stop trusting writes from that window. |
| CPU cache / bus / internal errors, no DIMM named | CPU or motherboard, or an overclock. | Reset BIOS to stock, re-test. |
| A single event, never repeating over several days | Often cosmic-ray-grade noise. | Note it, watch it, don't buy anything. |

Non-ECC RAM does not report correctable errors at all — it either works or it corrupts
silently — so if Alexandria is running non-ECC memory, any MCE at all is worth taking
more seriously than the table above suggests.

## 4. The correlation worth checking first

This is the highest-value thing in this document. Four production incidents on this host
have closed with root cause **unconfirmed**, plus one silent stoppage of the healthcheck
script. Compare the MCE timestamps against these windows. `mcelog`/`dmesg -T` print
**local time (PDT, UTC-7)**; the incident records are in **UTC**.

| Incident | UTC | Local (PDT) | Note |
|---|---|---|---|
| `t-014` | 2026-09-04 13:25 | 06:25 | site-wide 502, ~4h15m, root cause unknown |
| `t-015` | 2026-09-08 02:56 | 2026-09-07 19:56 | site-wide 502, ~2h57m, root cause unknown |
| healthcheck stop | 2026-09-01 09:26 | 02:26 | `healthcheck.ps1` stopped and never said so |
| `t-017` | 2026-09-12 ~11:45 | ~04:45 | 1 failed + 1 unapplied DB migration |
| `t-018` | 2026-09-13 ~09:29 | ~02:29 | site-wide 502, recovered ~03:40 |

If MCE timestamps land inside these windows, the recurring-502 mystery this project has
been chasing since 2026-09-04 is a hardware fault, not the
container-recreate-without-restart theory — and `t-016`'s external probe becomes a
nice-to-have rather than the main lead. If the MCEs are nowhere near them, that is
genuinely useful too: it rules the hardware out and keeps the container theory alive.

A failing DIMM is a very plausible mechanism for a *failed migration* specifically
(`t-017`) — a corrupted page in the middle of a schema write is exactly the shape of
that incident.

## 5. Before posting diagnostics publicly

The Unraid notification tells you to post your diagnostics to the forums. **Don't post
the whole zip without opening it first.** An Unraid diagnostics bundle includes your
Docker container templates from `/boot/config/plugins/dockerMan/templates-user/`, and
those XML files carry container environment *values* — which on this host means the
MariaDB credentials, `KR_API_TOKEN`, and whatever else the Kind Robots stack is
configured with. The anonymizer scrubs identifiers; do not assume it scrubs those.

For an MCE question the forum does not need the bundle anyway. Post only:

- the `mcelog` / `dmesg -T` MCE lines from step 1,
- the `dimm_label` / `ce_count` / `ue_count` output from step 2,
- the `dmidecode -t memory` locator and part-number lines (skip serials),
- your CPU and motherboard model.

If someone insists on the full bundle, unzip it locally and read `system/docker.txt` and
the template XMLs before uploading.

## 6. Close-out

Set `t-019` to `done` once the MCE class is identified (which part, correctable or not)
and either the part is replaced/scheduled or the event is confirmed as a benign one-off.
If the timestamps do correlate with the incident windows above, say so in the note — that
finding should feed straight back into `t-016` and the still-open root-cause question.
