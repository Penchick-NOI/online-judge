# Accounts: email confirmation and Google sign-in

How signing up works on PNOI, and the two things that must be set up on a real server before students can sign
up there. This is for whoever sets up the server; students do not need it.

## How signing up works

- **With a password:** the student fills in the sign-up form, ticks the two boxes (age or parent's agreement, and
  the rules), and gets an email with a link. The account works only after they open the link. The link lasts 7
  days. If it is lost or expired, the log-in page and the "check your email" page link to **Send me a new link**
  (at most three new links an hour per address).
- **With Google:** the student clicks **Continue with Google**, picks a username, optionally adds their school,
  and ticks the same two boxes. Google has already checked the email address, so no link is sent.
- The rules are the page `/rules/` ("Rules and privacy"). Its text is saved in `judge/fixtures/pnoi_pages.json`
  together with the About page; load both with `python3 manage.py loaddata pnoi_pages`.

On the owner's computer, emails are not really sent: they are printed in the site's log
(`docker compose logs site`). Google sign-in is switched off there because it needs a real web address.

## 1. Sending email

PNOI needs an email-sending service. Free plans of services such as Brevo, Mailjet or Amazon SES are enough at
PNOI's size. Set it up when the site has its own domain.

1. Create an account with the service and verify the domain (the service shows which DNS records to add).
2. Pick a sending address on the domain, for example `no-reply@` the domain.
3. In the server's `dmoj/local_settings.py` (never in the repository), set the service's SMTP details:

   ```python
   EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
   EMAIL_HOST = '...'          # from the service
   EMAIL_PORT = 587
   EMAIL_USE_TLS = True
   EMAIL_HOST_USER = '...'     # from the service
   EMAIL_HOST_PASSWORD = '...' # from the service; keep it secret
   DEFAULT_FROM_EMAIL = 'PNOI <no-reply@your-domain>'
   SERVER_EMAIL = DEFAULT_FROM_EMAIL
   ```

4. In the admin pages, open **Sites** and change the one site's **Domain name** from `localhost` to the real
   domain. The links in the emails are built from it.
5. Sign up with a test address and check that the email arrives and its link works.

## 2. Google sign-in

1. Go to the Google Cloud console, create a project for PNOI, and open **APIs & Services → OAuth consent
   screen**. Choose **External**, fill in the app name (PNOI), a support email, and the links to the site's
   About and Rules pages.
2. Open **Credentials → Create credentials → OAuth client ID**, type **Web application**.
3. Under **Authorised redirect URIs** add `https://your-domain/complete/google-oauth2/`.
4. Google shows a **client ID** and a **client secret**. Put them in the server's `dmoj/local_settings.py`:

   ```python
   SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '...'     # the client ID
   SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '...'  # the client secret; keep it secret
   ```

5. Restart the site. The **Continue with Google** button appears on the sign-up page and a **Google** button on
   the log-in page. They stay hidden while these two settings are empty.

## How this guide was checked

On the owner's computer on 17 November 2026: a password sign-up was refused without the tick boxes, then created,
the confirmation email appeared in the log, logging in before confirming showed the "not confirmed yet" message,
**Send me a new link** sent new links (and stopped after three), and the newest link confirmed the account. The
Google step's form and profile creation were tested on their own, and with temporary fake keys the Google buttons
appeared and sent the browser to Google. A real Google sign-in and a real email service were **not** tried; they
need the real server.
