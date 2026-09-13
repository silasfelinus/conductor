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

---

# RESULT — 2026-09-13

Silas ran steps 1–2 on Alexandria. The MCE is **benign**, and the interesting finding is
what the same output revealed about the host's blind spots.

## The event

```
[Sat Sep 12 15:44:38 2026] mce: [Hardware Error]: CPU 10: Machine Check: 0 Bank 5: bea0000000000108
[Sat Sep 12 15:44:38 2026] mce: [Hardware Error]: TSC 0 ADDR 1ffff810e36c6 MISC d012000100000000 SYND 4d000000
[Sat Sep 12 15:44:38 2026] mce: [Hardware Error]: PROCESSOR 2:870f10 TIME 1789253077 SOCKET 0 APIC b microcode 8701034
[Sat Sep 12 15:45:23 2026] EDAC MC: Ver: 3.0.0
```

One event. Not repeating.

**CPU:** `PROCESSOR 2:870f10` — vendor 2 is AMD; CPUID `0x870F10` decodes to family `0x17`,
model `0x71` — Zen 2 "Matisse", i.e. a Ryzen 3000-series desktop part.

**Bank 5:** `IPID 500b000000000` gives HardwareID `0xB0`, McaType `0x5`, which is
`SMCA_EX` — the **Execution Unit**, not the memory controller. No DIMM is implicated.

**Status `bea0000000000108`** decodes to Val=1, UC=1, En=1, MiscV=1, AddrV=1, **PCC=1**,
TCC=1, Scrub=1, error code `0x108` (generic cache-hierarchy error). PCC — processor
context corrupt — reads alarming, and on its own it would be the urgent row of the table
above.

## Why it is benign anyway

**`TSC 0` is the tell.** A real machine-check *exception* captures a timestamp counter
value. Zero means this was logged by `machine_check_poll()` reading the MCA banks, not by
a live fault — and the boot-time poll of all banks runs without `MCP_TIMESTAMP`, so it
always records `TSC 0`. Corroborating that: EDAC initialises 45 seconds *after* the event,
so the log line lands about a minute into a boot. A genuine uncorrected PCC error would
have panicked the machine, not been quietly logged and survived.

So: stale status sitting in bank 5, read out and printed during boot. The specific
signature — Bank 5, `bea0000000000108`, once at boot, on a Ryzen desktop part — is very
widely reported on Zen 2/Zen 3 systems and is the known-spurious one. (Reported pattern,
not a citation to a numbered erratum.)

## The correlation check: negative

MCE at **Sat 2026-09-12 15:44:38 PDT**. Against the windows in step 4:

| Incident | Local (PDT) | Gap from MCE |
|---|---|---|
| healthcheck stop | 09-01 02:26 | 11 days before |
| t-014 | 09-04 06:25 | 8 days before |
| t-015 | 09-07 19:56 | 5 days before |
| t-017 | 09-12 ~04:45 | ~11 h before |
| t-018 | 09-13 ~02:29 | ~11 h after |

Nothing lands inside an incident window. The nearest, t-017's failed migration, is eleven
hours earlier — and on a *previous boot*, since this MCE was logged during a boot that
started ~15:43 on the 12th.

Stronger still: `dmesg` covers the current boot only, which began ~15:43 on 09-12 and
therefore **contains t-018 in full**. No MCE was logged anywhere near 09-13 02:29.
That is a clean negative result: hardware machine checks did not cause t-018.

For t-014, t-015, t-017 and the healthcheck stop, the evidence is simply gone — see below.

## What this actually exposed

Three things matter more than the MCE did.

**1. `/var/log` is RAM-only, so every incident before the last reboot has no evidence.**
`/var/log/mcelog` does not exist and `dmesg` starts at the current boot. Four incidents
have now been investigated after the fact with nothing to read. Fix: *Settings → Syslog
Server → Mirror syslog to flash*. It is a toggle, and it is the single highest-value
action on this host.

**2. Alexandria has no memory error detection at all.**
`/sys/devices/system/edac/mc/*/dimm*/` does not exist — EDAC core loaded, but no memory
controller driver bound, because the RAM is non-ECC: 4 × 16 GB **TEAMGROUP UD4-3600**
UDIMMs across P0 CHANNEL A DIMM 0/1 and CHANNEL B DIMM 0/1. There will never be a
`ce_count` to read. This is not "no errors found" — it is *no detector installed*. A host
serving production with no ECC cannot distinguish a healthy DIMM from a failing one; bad
memory just corrupts silently.

**3. That memory configuration is aggressive for this CPU.**
DDR4-3600 is above JEDEC and requires XMP/DOCP. Four UDIMMs at 3600 on a Matisse memory
controller is a well-known marginal configuration — many 4-DIMM AM4 builds are not stable
above 3200, and the Infinity Fabric clock is the usual limiter. Marginal memory on a
non-ECC host produces exactly the observed symptom set: containers dying at random, a
schema write failing mid-flight (t-017), no hardware error logged anywhere.

**4. An unexplained reboot.** Alexandria booted ~15:43 PDT on 09-12, between t-017 and
t-018. Worth knowing whether that was planned.

Follow-on work is tracked at `t-020`. `t-019` closes here: the MCE class is identified
(spurious boot-time poll of a stale Execution Unit status, not memory, not repeating) and
confirmed a benign one-off, which is this task's stated close-out condition.
