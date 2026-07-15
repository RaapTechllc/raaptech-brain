---
type: Reference
title: Fleet Workflow Audit 2026-07-13
description: Gate-0 fleet workflow audit and remediation proof.
tags: [okf, auto-frontmatter]
timestamp: 2026-07-15T13:55:19Z
---

# Fleet + Workflow Audit — 2026-07-13

**Status:** Gate 0 COMPLETE (2026-07-13 evening). Backup/restore proven; NFS+PBS active; NVMe temp alert dismissed with evidence. Remaining audit cadence items are Gate 1+.

**Evidence rule:** `VERIFIED` = live command/API output collected on 2026-07-13. `PARTIAL` = a live observation exists but a key layer is unverified. `STALE` = a document contradicts present evidence. No remediation was performed.

## Executive verdict

The fleet is usable, but it is **not operationally dialed in yet**. The biggest issue is not lack of hardware; it is lack of enforced roles, health truth, and maintenance ownership.

1. **Backup protection (Gate 0 closed):** NFS `truenas-backups` and PBS `pbs-main` are active; CT 200 on `10.0.0.25:8007` proven; controlled backup + isolated restore captured 2026-07-13. Original finding was correct at discovery; remediated under approved Gate 0.
2. **TrueNAS remains storage-only:** temp CRITICAL was latched history (current 36°C, critical_warning=0) and was dismissed with evidence; residual `media_errors=11` on nvme0n1 still forbids compute-worker use.
3. **The Docker VM is the clear Linux workflow plane**, but it needs service inventory/health ownership before it receives more workload.
4. **Mac is an overloaded operator endpoint**: it is an 8 GB machine showing substantial swap activity. It should orchestrate/observe, not execute browser agents or long coding jobs.
5. **The old Obsidian infrastructure overview is materially stale** and is actively dangerous as a setup reference.

## Findings

| Severity | Finding | Live evidence | Decision / next action |
|---|---|---|---|
| **CRITICAL** | Proxmox backup target chain is unavailable | `pvesm status`: `truenas-backups` inactive; `pbs-main` inactive with `500 Can't connect to 10.0.0.25:8007 (No route to host)`; no response from `10.0.0.25` on Proxmox bridge | Treat backups as failed until one known-good backup + restore verification is captured. Diagnose underlay reachability, NFS mount, then PBS CT before changing backup jobs. |
| **HIGH** | TrueNAS has a current critical NVMe temperature alert | TrueNAS API reports `CRITICAL`: `/dev/nvme0n1`, critical warning `0x02` (temperature). Pool status/capacity were not collected because the appliance shell does not expose `zpool` to this SSH account. | Storage-first only. Collect pool status plus full NVMe SMART/temperature counters; decide cooling/drive-risk action. No Codex worker, containers, or testing load until cleared. |
| **HIGH** | The operational topology documentation is internally inconsistent | Obsidian `Agentic Brain/infrastructure.md` calls Atlas pending decommission and lists unverified Docker VM services/ports; live evidence shows Atlas active and a different current service inventory. `fleet/backups.md` correctly says PBS integration is pending, but its stated daily target/retention is not demonstrated. | Preserve historical docs, but add an accepted live baseline and point operating runbooks to it. |
| **HIGH** | A plaintext credential was discovered in a legacy local note during document scanning | Read-only scan encountered a credential-shaped value in a legacy `.openclaw` note. Value is intentionally not reproduced. | Treat as potential exposure: rotate that credential, remove the legacy plaintext note from active paths, and scan for other plaintext secrets using a redacting scanner. |
| **HIGH** | TrueNAS and backup reachability are inconsistent across planes | TrueNAS responds at LAN `10.0.0.30` with SSH/NFS/SMB active, while Tailnet listed its `100.72.235.14` endpoint offline for 11 days. Separately, Proxmox cannot ARP/reach PBS CT `10.0.0.25`; its NFS mount operation hung. | Make the reachability matrix explicit: Windows→NAS, Proxmox→NAS, Proxmox→PBS CT, and Tailnet→NAS. Do not declare the backup path healthy from NAS service status alone. |
| **MEDIUM** | Docker VM has container sprawl and at least one unhealthy workload | Ubuntu 24.04, 46 GiB RAM and 122 GiB free; Docker active with many stacks. `raaptech-website-web-1` has been `unhealthy` for 13 days. | Make Docker VM the designated workflow/data-services plane, but first inventory each stack owner, public exposure, health endpoint, backup requirement, and keep/retire decision. Repair or retire the unhealthy site. |
| **MEDIUM** | Atlas is functional but behind on Hermes and has restart history | Atlas has Hermes Agent `v0.17.0`, reports 1,634 commits behind; Hermes gateway active now, but failed repeatedly Jun 25–30. | Keep Atlas as the headless agent/automation worker. Capture cause of gateway exits, then update in a maintenance window with rollback plan. |
| **MEDIUM** | Headed Windows VM is not automation-ready | VM 101 is running with 20 GiB RAM, 4 vCPU, 100 GB disk. QEMU Guest Agent is not configured/running, so host cannot inventory/control it reliably. | Install/enable QGA, verify from Proxmox, then make it the disposable Windows browser/computer-use test surface. |
| **MEDIUM** | Mac is resource-constrained for heavy local agent work | MacBook Air: 8 GB RAM, 8 CPUs, Hermes/RustDesk/Tailscale active; memory-pressure output shows very high accumulated swap I/O. | Keep Mac as mobile command/approval/remote-desktop surface. Move browser-agent, multi-MCP, indexing, and long coding runs to Windows VM/Docker VM/Atlas. |
| **MEDIUM** | Windows Archon execution is platform-fragile | Windows has 64 GiB RAM, RTX 3080 (10 GB), 864 GiB free. Archon path crashes under Windows Bun; validation works in Linux/WSL. | Windows is command center / headed GPU plane. Run Archon workflows on Linux; deploy the already-validated workflow to Docker VM, not native Windows Bun. |
| **MEDIUM** | GPU inventory and allocation are ambiguous | Windows live `nvidia-smi` reports RTX 3080; Proxmox also reports RTX 3080 PCI device. VM 101 currently uses VirtIO VGA in observed config, not a demonstrated GPU assignment. | Do not make GPU workflow decisions until we reconcile whether there are two GPUs, dual-boot/shared hardware, or a documentation/config mismatch. |
| **MEDIUM** | Falcon has no proven business role | VPS is healthy: Ubuntu 24.04, Docker, nginx :80, `yt-kb-api`, Hermes and OpenClaw gateways. No current external workload/owner was verified. | Write one sentence defining its required external-facing role. If none exists, plan decommission to reduce cost and attack surface. |
| **LOW** | OPNsense is live but needs a defined maintenance ticket | OPNsense API reachable; LAN and WAN physical links up at 2.5 Gb; WAN DHCP `192.168.1.249/24` via `192.168.1.254`; default gateway and VPN gateways report online. Firmware `26.1.9`, latest `26.1.10`; Suricata stopped. | This is not proven as the root cause of the backup failure. Create a scoped routing/backup-path investigation before upgrading or editing firewall rules. |
| **LOW** | Daily operations tools exist but are stale as operational signals | Lab Pulse and Morning Ops Brief artifacts last changed/run June 30; Super Brain had activity July 10. | Fix the source service matrix first, then rebuild Lab Pulse from verified endpoints and schedule the brief. Do not automate stale assumptions. |

## Verified current topology

| Plane | Host | Verified role | Current status |
|---|---|---|---|
| Command / primary workstation | Windows `desktop-2qf5hun` | Main operator, GPU/headed work | Windows 11 Pro, 64 GiB RAM, RTX 3080 10 GB, 55% disk used; Tailnet online |
| Mobile operator | MacBook Air | Remote control, approvals, light coding | macOS 26.3.1; 8 GB RAM; Hermes, RustDesk, Tailscale active; do not use for heavy workloads |
| Hypervisor | Proxmox | Runs core VMs/CTs and sees RTX 3080 PCI device | PVE 9.2.3, running VM 100 Docker VM, 101 Windows VM, 111 Atlas; CT 200 PBS running (post–Gate 0), CT 201 Ollama GPU stopped |
| Linux services / workflow candidate | Docker VM | Containers, application services, intended Archon workflow host | Ubuntu 24.04, 46 GiB RAM, Docker 29.1.5 active, many services, no verified Archon deployment yet |
| Agent worker | Atlas | Headless Hermes/OpenClaw agent plane | Ubuntu 24.04; gateways active; needs controlled Hermes update/reliability review |
| Storage | TrueNAS SCALE | NFS/SMB storage and intended backup target | `fast` mirror and `bulk` RAIDZ1 pools online with clean last scrubs; SSH/NFS/SMB active; NVMe temp alert dismissed (36°C, critical_warning=0); residual media_errors=11 keeps storage-only policy |
| Router | OPNsense | LAN DHCP/DNS/firewall/Tailscale routing | API and LAN/WAN links working; routing/backup-path behavior unresolved |
| External | Falcon VPS | External ingress / gateway candidate | Healthy but role not justified |
| Browser test plane | Windows VM 101 | Intended disposable headed agent/browser plane | Running; QEMU Guest Agent absent; not ready |

## Target role boundaries

```text
Mac                = mobile operator / approvals / remote access only
Windows workstation = command center + local GPU/headed work only
Proxmox             = hypervisor; no casual workloads
Docker VM           = durable Linux workflow + containers + data services
Atlas               = headless agent and scheduled automation worker
Windows VM          = isolated browser/computer-use and Windows test plane
TrueNAS             = storage + backup only until SMART and backup path are resolved
Falcon              = strictly external/public ingress, otherwise retire
OPNsense            = network control plane; changes only through a scoped ticket/runbook
```

## Workflow system to build after the safety blockers

| Workflow | Trigger | Execution plane | Output / gate |
|---|---|---|---|
| **Lab Pulse** | Daily + on-demand | Atlas or Docker VM | JSON + HTML, only verified host/service targets |
| **Morning Ops Brief** | Daily after Pulse | Docker VM | 5-minute exception report: outages, backups, capacity, stale docs, today’s work |
| **Research Intake** | Manual/webhook | Atlas | Raw source → evidence note → tagged summary → human publish gate |
| **Knowledge Capture** | Post-session | Atlas | Session outcome → candidate fact/decision → review queue; no automatic canonical overwrites |
| **Repo Chore Factory** | Manual, low-risk only | Docker VM | isolated worktree, explicit `VERIFY:`, approval before build, max 3 repair iterations, evidence artifact |
| **Computer-use testing** | Manual | Windows VM | disposable browser profile, recorded test evidence, no production credentials by default |

This is an **AI Developer Workflow** system, not a generic agent loop. Code owns routing, isolation, retries, deterministic verification and evidence. Agents perform bounded reasoning. Kyle approves intent and risk-bearing changes.

## Documentation truth ledger

| Source | Status | Why | Required action |
|---|---|---|---|
| `raaptech-brain/research/indydevdan-ai-developer-workflows.md` | CURRENT | Updated 2026-07-13; correct workflow doctrine | Keep |
| `raaptech-brain/docs/plans/next-steps-plan.md` | PARTIAL | Directionally correct; needs this audit’s actual backup/TrueNAS findings | Update after accepted remediation decisions |
| `raaptech-brain/fleet/backups.md` | PARTIAL | Correctly records that PBS integration is pending and offsite is absent, but describes an intended daily backup schedule not proven by live storage state | Update from accepted backup/restore evidence |
| Obsidian `Agentic Brain/infrastructure.md` | STALE | Marks active Atlas as pending decommission and lists unverified/outdated Docker service claims | Archive/mark historical; do not use for operations |
| Obsidian `20-Areas/Fleet-Ops/foreman-playbook.md` | PARTIAL | Good cadence, but command/host claims are not live-validated | Rewrite its checks from the verified service matrix |
| Lab Pulse / Morning Brief reports from 2026-06-30 | STALE AS STATUS | Useful historical artifacts, not current health evidence | Retain history; regenerate after inventory cleanup |
| Super Brain project | PARTIAL | Active July 10 but no operational ownership/backup contract verified | Inventory and classify before expanding |

## Remediation sequence

### Gate 0 — no new infrastructure until this is done
1. Repair/verify `Proxmox → TrueNAS NFS → PBS` reachability.
2. Capture one successful backup and a controlled restore test.
3. Investigate all four TrueNAS SMART warnings; make an explicit storage-risk decision.
4. Rotate the credential discovered in legacy plaintext and remove the active plaintext copy.

### Gate 1 — establish durable execution surfaces
1. Install and verify QEMU Guest Agent in Windows VM.
2. Put Archon repository/workflow execution on Docker VM; run one low-risk chore end-to-end.
3. Reconcile actual GPU inventory/allocation.
4. Declare Falcon keep/retire decision.

### Gate 2 — make daily life simpler
1. Convert the verified host/service matrix into `services.yaml`.
2. Regenerate Lab Pulse and Morning Brief on Docker VM or Atlas.
3. Add clear freshness timestamps and “last known good backup” to the brief.
4. Use one research inbox and one canonical knowledge base per domain; raw transcript stores remain raw.

### Gate 3 — maintenance window
1. OPNsense: diagnose backup-path/routing first; then decide firmware update and Suricata policy.
2. Atlas: capture gateway failures, then controlled Hermes update.
3. Docker VM: repair/retire unhealthy web container, classify public ports, document container owners.

## Explicit decision on TrueNAS as a Codex/computer-use worker

**No.** It is technically a Linux appliance with 62 GiB RAM and available capacity, and SSH/NFS/SMB services exist. That does **not** make it an appropriate compute worker. The four-drive SMART warning condition and the broken backup path make reliability more valuable than spare CPU/RAM. Revisit only after storage health is resolved and a purpose-built, isolated worker environment is approved.

## Acceptance criteria for the actual baseline

This audit becomes the canonical current-state baseline when:

- [x] backup and restore are demonstrated, not assumed;
- [x] TrueNAS drive-risk decision is documented (temp alert dismissed with SMART proof; residual media_errors=11 keeps storage-only);
- [ ] Windows VM management/control works through QGA;
- [ ] Docker VM workflow run proves a real low-risk task;
- [ ] Mac/Windows/GPU role boundary is accepted;
- [ ] stale Obsidian pages are marked historical and the new operational runbook points to verified sources.

## Evidence captured

Live collections: Windows workstation/Tailnet; Proxmox VM/CT/storage/backup configuration; Docker VM services/resources; Atlas gateways/log warnings; Falcon services; Mac resource/process state; OPNsense authenticated API; TrueNAS pool/services/alerts. Timestamp: 2026-07-13.

## Gate 0 — remediation resolution (2026-07-13)

**Owner execute path:** approved Gate 0 maintenance (NFS path, PBS CT 200, backup+restore proof, TrueNAS NVMe temp disposition).

### What changed
1. **Proxmox → TrueNAS NFS `truenas-backups`** is **active** on LAN (`server 10.0.0.30`, export `/mnt/bulk/proxmox-backups`, clientaddr `10.0.0.20`, NFS 4.2). Live write/readback under `/mnt/pve/truenas-backups` succeeded.
2. **PBS CT 200** started and is **running** at `10.0.0.25`; datastore mount `mp0` → `/mnt/datastore` healthy; `proxmox-backup` + `proxmox-backup-proxy` active; **:8007 open**.
3. **PVE storage `pbs-main`** flipped from inactive/no-route → **active** against datastore `main`.
4. **TrueNAS `nvme0n1` temperature CRITICAL alert dismissed** after live SMART proved current warning clear (see disposition below).
5. Two unkillable D-state leftovers remain on Proxmox (`[100.72.235.14-manager]`, a stuck historic `stat` on the NFS path). They did **not** block operations after hung `pct start` was cleared. Optional clean reboot later to reap them; **not required for Gate 0 close**.

### Backup proof (VERIFIED)
| Path | Job | Result |
|---|---|---|
| NFS `truenas-backups` | `vzdump 200 --mode snapshot --compress zstd` notes `gate0-nfs-verify-2026-07-13` | **OK** — archive `/mnt/pve/truenas-backups/dump/vzdump-lxc-200-2026_07_13-19_08_57.tar.zst` (~382 MiB), finished 2026-07-13 19:09 CDT |
| PBS `pbs-main` | `vzdump 200 --mode snapshot` notes `gate0-pbs-verify-2026-07-13` | **OK** — `pbs-main:backup/ct/200/2026-07-14T00:09:18Z` (~1.07 GiB logical / ~413 MiB compressed upload), finished 2026-07-13 19:09 CDT |

Production guests 100/101/111 were **not** disrupted for the control backups (CT 200 only).

### Restore proof (VERIFIED, isolated)
1. `pct restore 9001 pbs-main:backup/ct/200/2026-07-14T00:09:18Z --storage local-lvm --unique 1` → success.
2. Before boot: `net0` set with **`link_down=1`**, hostname `gate0-restore-test`, `onboot 0`.
3. `pct start 9001` → **running**; hostname `gate0-restore-test`; eth0 **DOWN**/link_down (no LAN collision with CT 200).
4. `pct stop 9001` → `pct destroy 9001 --purge` → config/disks gone.

### Full-VM restore proof (VERIFIED, isolated)

A second post-reboot recovery proof restored the full Atlas VM backup, not just CT 200:

1. `qmrestore pbs-main:backup/vm/111/2026-07-14T04:47:29Z 9001 --storage local-lvm --unique 1` completed: **48,318,382,080 bytes** in **125.01 seconds**.
2. Before boot: restored VM 9001 had `net0 link_down=1` and `onboot=0`, preventing LAN and startup collisions.
3. `qm start 9001` → **running** observed.
4. Cleanup passed: VM stopped, `qm destroy 9001 --destroy-unreferenced-disks 1 --purge 1` removed config and all restored logical volumes (`vm-9001-cloudinit`, `vm-9001-disk-0`, `vm-9001-disk-1`).
5. Post-cleanup: production VMs 100/101/111 and PBS CT 200 were running; `pbs-main` and `truenas-backups` were active.

**Maintenance warning confirmed:** the restored VM emitted the known UEFI 2011 certificate-expiry warning. No EFI certificate enrollment was performed because BitLocker-safe preparation is required first. Track this as Gate 1 maintenance for the Windows-capable VM restore path; it did not block this isolated restore.

### TrueNAS thermal disposition (VERIFIED)
| Metric | Value |
|---|---|
| Live temps API | `nvme0n1=36°C`, `nvme1n1=29°C`; HDDs 30–51°C |
| SMART `critical_warning` | **0** (not set now) |
| SMART temperature | 36°C (sensors 36/39) |
| `warning_temp_time` | 1 (minute) historical only |
| `critical_comp_time` | 0 |
| spare / used | available_spare 98% (threshold 10); percentage_used 2% |
| Dismissed alert | UUID `373fb422-2be0-4d24-a157-42da1b06385e` (SMART temp 0x02) via TrueNAS `alert/dismiss` after proof; SMART-class alerts count → 0 |

**Residual storage risk (not Gate 0 temperature):** `media_errors=11`, `num_err_log_entries=11`, `unsafe_shutdowns=27` on `nvme0n1`. Keep TrueNAS **storage-only**; schedule SMART long self-test + scrub attention; do **not** treat media_errors as cleared by the temp-alert dismiss.

**Other open TrueNAS alerts (non-Gate-0):** CatalogSyncFailed CRITICAL (apps clone/git), NTPHealthCheck WARNING, cert `truenas_default` NOTICE (~9 days), several AppUpdate INFO.

### Gate 0 acceptance checklist
- [x] Proxmox → TrueNAS NFS backup path repaired/proven
- [x] PBS CT 200 up and :8007 reachable; `pbs-main` active
- [x] Controlled NFS backup succeeded with on-disk artifact
- [x] Controlled PBS backup succeeded with datastore snapshot
- [x] Isolated scratch restore booted and destroyed (VMID 9001)
- [x] NVMe temperature alert disposition with live thresholds

### What comes next (not Gate 0)
1. **Gate 1:** QGA on VM 101; Archon on Docker VM; GPU inventory settle; Falcon keep/retire.
2. Reap orphan D-state NFS client threads with a planned Proxmox reboot when convenient.
3. Rebuild lab pulse / `fleet/backups.md` from this evidence (daily NFS + PBS jobs already configured; prove next scheduled window for 100/101/111).
4. Track residual NVMe media_errors and TrueNAS catalog/NTP/cert notices in a storage ticket.
5. Credential plaintext rotation from original audit finding remains open (Gate 0 scope excluded).

---
**Gate 0 closed 2026-07-13 ~19:10 CDT. No credentials in this document.**

---
**This document intentionally contains no credentials, API keys, or passwords.**
