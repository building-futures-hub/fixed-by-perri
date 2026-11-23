// Fixed by Perri — nav toggle + service request form
(function () {
  var t = document.querySelector('.menu-toggle'), nav = document.getElementById('nav');
  if (t && nav) t.addEventListener('click', function () {
    var open = nav.classList.toggle('open'); t.setAttribute('aria-expanded', open);
    t.textContent = open ? 'Close' : 'Menu';
  });

  var f = document.getElementById('lead-form');
  if (!f) return;
  var status = f.querySelector('.form-status'), btn = f.querySelector('button[type=submit]');
  function say(msg, ok) { status.className = 'form-status ' + (ok ? 'ok' : 'err'); status.innerHTML = msg; }

  f.addEventListener('submit', function (e) {
    e.preventDefault();
    var missing = [].filter.call(f.querySelectorAll('[required]'), function (el) { return !el.value.trim(); });
    if (missing.length) { missing[0].focus(); say('Please fill in your name, phone, appliance and what it’s doing.', false); return; }
    var data = {}; new FormData(f).forEach(function (v, k) { data[k] = v; });
    data.page = location.pathname;
    btn.disabled = true; btn.style.opacity = .6;
    fetch(f.action, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function () {
        f.reset();
        say('Thanks! Your request is in. Perri will reach out shortly to schedule. Need it sooner? Call <a href="tel:+15209545559">(520) 954-5559</a>.', true);
      })
      .catch(function () {
        say('Sorry, the form didn’t go through. Please call <a href="tel:+15209545559">(520) 954-5559</a> or email <a href="mailto:fixedbyperri@gmail.com">fixedbyperri@gmail.com</a>.', false);
      })
      .finally(function () { btn.disabled = false; btn.style.opacity = 1; });
  });
})();
