// Cloudflare Pages Function: POST /api/lead
// Forwards the service request to the CRM webhook and/or emails it via Resend.
// Set these in Cloudflare Pages > Settings > Environment variables:
//   LEAD_WEBHOOK_URL  (optional) inbound webhook from the CRM (Sulus workflow trigger, etc.)
//   RESEND_API_KEY    (optional) Resend API key for email notifications
//   LEAD_EMAIL_TO     (optional) where to send notifications, default fixedbyperri@gmail.com
//   LEAD_EMAIL_FROM   (optional) verified Resend sender, e.g. "Fixed by Perri <leads@fixedbyperri.com>"

const FIELDS = ['first_name','last_name','phone','email','appliance','brand','address','city','zip','message','source','page'];

export async function onRequestPost({ request, env }) {
  let body;
  try { body = await request.json(); } catch { return json({ ok: false, error: 'bad_request' }, 400); }

  // Honeypot: bots fill hidden fields. Pretend success.
  if (body.company_website) return json({ ok: true });

  const lead = {};
  for (const k of FIELDS) lead[k] = String(body[k] ?? '').slice(0, 2000).trim();
  if (!lead.first_name || !lead.phone || !lead.message) return json({ ok: false, error: 'missing_fields' }, 422);
  lead.submitted_at = new Date().toISOString();
  lead.business = 'Fixed by Perri';

  const jobs = [];
  if (env.LEAD_WEBHOOK_URL) {
    jobs.push(fetch(env.LEAD_WEBHOOK_URL, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(lead) }));
  }
  if (env.RESEND_API_KEY) {
    const rows = FIELDS.filter(k => lead[k]).map(k => `<tr><td style="padding:4px 12px 4px 0;color:#7A6555">${k.replace('_',' ')}</td><td style="padding:4px 0"><b>${esc(lead[k])}</b></td></tr>`).join('');
    jobs.push(fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        from: env.LEAD_EMAIL_FROM || 'Fixed by Perri Website <onboarding@resend.dev>',
        to: [env.LEAD_EMAIL_TO || 'fixedbyperri@gmail.com'],
        reply_to: lead.email || undefined,
        subject: `New service request: ${lead.appliance || 'Appliance'} — ${lead.first_name} ${lead.last_name} (${lead.city || 'no city'})`,
        html: `<h2>New service request</h2><table>${rows}</table>`,
      }),
    }));
  }
  if (!jobs.length) return json({ ok: false, error: 'no_destination_configured' }, 500);

  const results = await Promise.allSettled(jobs);
  const anyOk = results.some(r => r.status === 'fulfilled' && r.value.ok);
  return anyOk ? json({ ok: true }) : json({ ok: false, error: 'delivery_failed' }, 502);
}

function esc(s) { return s.replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c])); }
function json(o, status = 200) { return new Response(JSON.stringify(o), { status, headers: { 'Content-Type': 'application/json' } }); }
