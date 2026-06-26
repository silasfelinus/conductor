/* Humboldt Scoop Solutions — customer portal interactions */
(function () {
	"use strict";
	var cfg = window.HSS_PORTAL || null;

	function post(url, body) {
		return fetch(url, {
			method: "POST",
			headers: { "Content-Type": "application/json", "X-WP-Nonce": cfg ? cfg.nonce : "" },
			body: JSON.stringify(body || {})
		}).then(function (r) {
			return r.json().then(function (j) {
				if (!r.ok) { throw new Error((j && j.message) || "Something went wrong."); }
				return j;
			});
		});
	}

	function busy(btn, on, labelWhenBusy) {
		if (!btn) { return; }
		if (on) {
			btn.dataset.label = btn.textContent;
			btn.textContent = labelWhenBusy || "Working…";
			btn.disabled = true;
		} else {
			if (btn.dataset.label) { btn.textContent = btn.dataset.label; }
			btn.disabled = false;
		}
	}

	/* Auth tabs */
	document.querySelectorAll(".hss-tab").forEach(function (tab) {
		tab.addEventListener("click", function () {
			var name = tab.dataset.tab;
			document.querySelectorAll(".hss-tab").forEach(function (t) { t.classList.toggle("is-active", t === tab); });
			document.querySelectorAll(".hss-auth-panel").forEach(function (p) {
				p.classList.toggle("is-hidden", p.dataset.panel !== name);
			});
		});
	});

	if (!cfg) { return; } // not on the portal page

	/* Checkout buttons (plan confirm + one-time) */
	document.querySelectorAll("[data-hss-checkout]").forEach(function (btn) {
		btn.addEventListener("click", function () {
			busy(btn, true, "Redirecting…");
			post(cfg.checkout, { plan: btn.dataset.plan, dogs: btn.dataset.dogs || 1 })
				.then(function (res) { window.location.href = res.url; })
				.catch(function (err) { busy(btn, false); alert(err.message); });
		});
	});

	/* Manage / cancel billing */
	document.querySelectorAll("[data-hss-billing]").forEach(function (btn) {
		btn.addEventListener("click", function () {
			busy(btn, true, "Opening…");
			post(cfg.billing, {})
				.then(function (res) { window.location.href = res.url; })
				.catch(function (err) { busy(btn, false); alert(err.message); });
		});
	});

	/* Save service details */
	var profile = document.querySelector("[data-hss-profile]");
	if (profile) {
		var status = profile.querySelector("[data-profile-status]");
		profile.addEventListener("submit", function (e) {
			e.preventDefault();
			var data = Object.fromEntries(new FormData(profile).entries());
			if (status) { status.className = "hss-form-status"; status.textContent = "Saving…"; }
			post(cfg.profile, data)
				.then(function () { if (status) { status.className = "hss-form-status ok"; status.textContent = "Saved."; } })
				.catch(function (err) { if (status) { status.className = "hss-form-status err"; status.textContent = err.message; } });
		});
	}
})();
