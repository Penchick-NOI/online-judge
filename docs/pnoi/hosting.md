# Hosting PNOI: the plan

How PNOI goes from the owner's computer to a real website everyone can use. **This is a plan; none of it has
been done yet.** Each phase says who does it. Tick phases off in [AGENTS.md](../../AGENTS.md) as they are finished.

## The setup (decided 2026-11-17)

Two small servers at **OVHcloud, Singapore** (the closest big-provider location to the Philippines):

| Server | OVHcloud plan | Runs | Why separate |
| --- | --- | --- | --- |
| **Site server** | VPS-2: 4 cores, 8 GB, 75 GB | website, database, Redis, background worker, the judge bridge, nginx | holds all the data |
| **Judge server** | VPS-1: 2 cores, 4 GB, 40 GB | the DMOJ judge only | runs untrusted student code; if it is ever broken into, there are no passwords or student data on it |

The two servers talk over a private, encrypted link (**Tailscale**), so the judge bridge is never open to the
internet. **Cloudflare** sits in front of the site server for the padlock (HTTPS), the domain name and protection
from attacks.

### Monthly cost (about)

| Item | Cost |
| --- | --- |
| VPS-2 (site) | about US$8.50 a month before tax |
| VPS-1 (judge) | about US$4.54 a month before tax |
| Domain name (`.com` or `.org`) | about US$10–15 a **year** |
| Cloudflare, Tailscale, email service (free plans), uptime alerts | free |
| Off-server backups (cloud storage) | a few cents a month |
| **Total** | **about US$14–15 a month** |

Prices were checked on 17 November 2026 and change; check them on the providers' pages before paying.

### Fair timing

These VPS plans share their processors with other customers, so a program's running time can vary a little.
For practice this does not matter. For rated rounds:

- set time limits at **2 to 3 times** the setter's own solution, so small differences never decide a verdict;
- for an important round, rent an extra **dedicated-processor** judge by the hour (from a provider with hourly
  billing) for the contest only, and connect it like the normal judge. It costs a few dollars per contest.

## Phase 0: accounts and a name (owner)

Only the owner can do this phase: the accounts must be in the owner's name and paid with the owner's card.
Claude never sees passwords or card details.

1. **Choose the domain name**, for example `pnoi.org` or `pnoi.ph` (`.ph` costs noticeably more per year).
2. Create these accounts, each with a strong password and two-step login where offered:
   - **Cloudflare** (free). Buying the domain through Cloudflare Registrar is simplest, at cost price.
   - **OVHcloud** (do not order servers yet; Phase 2).
   - **Tailscale** (free personal plan; sign in with the owner's Google or GitHub account).
   - An **email-sending service** with a free plan (for example Brevo).
   - **GitHub** is already set up.
3. Tell Claude the domain name. Nothing else needs to be shared.

## Phase 1: prepare the code (Claude, no cost)

Work done on the owner's computer before any server is rented, in pull requests as usual:

1. **Our own copy of the Docker setup.** The local setup in `/srv/pnoi-docker` is Ninjaclasher's `dmoj-docker`
   with PNOI changes (Python 3.12, which the admin pages need; judge languages; settings). Put it in a new
   private repository, `Penchick-NOI/pnoi-docker`, with every password and key removed and replaced by
   placeholders, so the servers can be built from it.
2. **Production settings template**: `DEBUG` off, a new secret key generated on the server, the real domain in
   `ALLOWED_HOSTS` and the site's address, secure cookies, the email service, the rules link, Philippine time.
3. **Bridge only on the private link**: change the bridge's published port from `9999:9999` (open to everyone)
   to the site server's Tailscale address only.
4. **Problem data sync**: the judge needs a copy of every problem's test data. A small script copies new or
   changed test data from the site server to the judge server every minute over the private link (the judge
   notices changes by itself).
5. **Backup script**: every night, dump the database and pack the problem data, keep 14 days on the server and
   send a copy to off-server storage.
6. A short **server checklist** (this file's later phases, made exact).

## Phase 2: rent the servers (owner, with Claude guiding)

1. On the owner's computer, create an **SSH key** (a login key; Claude gives the one command). The private half
   never leaves the computer.
2. Order **VPS-2** and **VPS-1** at OVHcloud, location **Singapore**, system **Ubuntu 24.04 LTS**, and paste the
   public half of the SSH key during the order.
3. Tell Claude the two servers' addresses (they are not secret).

## Phase 3: lock the servers down (Claude, over SSH)

On both servers:

1. Install security updates and turn on automatic security updates.
2. Create a normal user for running PNOI; turn off password logins and root logins (SSH key only).
3. Install **Tailscale** and join both servers to the owner's Tailscale network (the owner approves each
   server in the Tailscale page).
4. Firewall:
   - **Site server**: allow SSH, and web traffic (80/443) only from Cloudflare. The bridge port only on the
     Tailscale link.
   - **Judge server**: allow SSH only. Nothing else comes in; it connects out to the bridge.

## Phase 4: the site server (Claude)

1. Install Docker and the PNOI Docker setup from Phase 1.
2. Generate **new** database passwords and secret keys on the server itself. They are never typed in chat,
   never copied from the owner's computer, and never committed.
3. Start the site with a **fresh database** (not a copy of the local one, which contains demo accounts and test
   data), then load PNOI's saved content: languages, About and Rules pages, the welcome news post, the
   navigation bar.
4. The **owner creates the real administrator account** by typing its username and password on the server
   (Claude starts the command). The local demo `admin` account never goes to the server.
5. In the admin pages, set the site's domain name (used in email links).

## Phase 5: the judge server (Claude)

1. Install Docker and the DMOJ judge image with C++17, C++20 and Python 3 only.
2. Give the judge its own name and a **new** key, and register it in the site's admin pages.
3. Connect it to the bridge over the Tailscale link; turn on the problem data sync from Phase 1.
4. Test: the judge shows as online, and a sample problem is judged correctly in all three languages.

## Phase 6: the domain and HTTPS (owner and Claude)

1. In Cloudflare, point the domain at the site server, with the orange cloud (proxy) on.
2. Create a Cloudflare **origin certificate** and install it in nginx on the site server; set Cloudflare's SSL
   mode to **Full (strict)**.
3. Test the site at `https://` the domain, on a computer and a phone.

## Phase 7: email and Google sign-in (owner and Claude)

Follow [accounts-setup.md](accounts-setup.md):

1. Verify the domain in the email service; put its SMTP details in the server's settings (the owner pastes the
   password straight into the server file, not into chat).
2. Create Google sign-in keys for the real domain; add them to the server's settings the same way.
3. Test: sign up with a real email address, receive the confirmation email, log in; sign up with Google.

## Phase 8: backups and alerts (Claude, owner creates the storage account)

1. Turn on the nightly backup from Phase 1, sending copies to off-server storage (for example OVHcloud Object
   Storage or Backblaze B2).
2. **Test a restore** into a scratch copy, so we know the backups work.
3. Set up a free uptime monitor that emails the owner if the site goes down.

## Phase 9: soft launch, then launch (owner)

1. Give the problem-setting team accounts with the "problem setter" permissions; they write problems on the
   real site. Sign-up can stay open but unannounced, or be closed for now.
2. Run a private practice contest with the team and a few students. Check judging speed, time limits and the
   rating step.
3. When ready, announce PNOI.

## After launch: looking after it

- **Updates**: automatic security updates on both servers; PNOI changes are deployed after they are merged and
  tested locally (pull, rebuild, migrate, restart site, celery and bridged).
- **Watch costs**: OVHcloud's bill and the email service's daily limit.
- **Growing**: if contests get busy, add a second judge (another VPS-1, or an hourly dedicated one for
  contest days). The site server can be upgraded in place.
