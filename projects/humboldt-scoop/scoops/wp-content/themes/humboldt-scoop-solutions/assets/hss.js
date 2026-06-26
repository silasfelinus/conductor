/* Humboldt Scoop Solutions — front-end interactions */
(function () {
	"use strict";

	/* Mobile nav toggle */
	var toggle = document.querySelector(".hss-nav-toggle");
	var links  = document.getElementById("hss-nav-links");
	if (toggle && links) {
		toggle.addEventListener("click", function () {
			var open = links.classList.toggle("hss-open");
			toggle.setAttribute("aria-expanded", open ? "true" : "false");
		});
		links.addEventListener("click", function (e) {
			if (e.target.tagName === "A") { links.classList.remove("hss-open"); }
		});
	}

	/* Pricing: keep the "Choose" link's dog count in sync with the selector */
	document.querySelectorAll(".hss-plan").forEach(function (card) {
		var select = card.querySelector("[data-plan-dogs]");
		var cta    = card.querySelector(".hss-plan-cta");
		if (!select || !cta) { return; }
		var base = cta.getAttribute("href");
		function sync() {
			try {
				var url = new URL(base, window.location.origin);
				url.searchParams.set("dogs", select.value);
				cta.setAttribute("href", url.pathname + url.search);
			} catch (e) { /* noop */ }
		}
		select.addEventListener("change", sync);
		sync();
	});

	/* Quote form — submit to the portal plugin REST endpoint if available,
	   otherwise fall back to a mailto so the form is never a dead end. */
	var form = document.getElementById("hss-quote-form");
	if (form) {
		var status = form.querySelector("[data-quote-status]");
		form.addEventListener("submit", function (e) {
			e.preventDefault();
			if (form.querySelector(".hss-hp") && form.querySelector(".hss-hp").value) { return; } // honeypot

			var data = Object.fromEntries(new FormData(form).entries());
			var cfg  = window.HSS_QUOTE || null;

			if (status) { status.className = "hss-form-status"; status.textContent = "Sending…"; }

			if (cfg && cfg.endpoint) {
				fetch(cfg.endpoint, {
					method: "POST",
					headers: { "Content-Type": "application/json", "X-WP-Nonce": cfg.nonce || "" },
					body: JSON.stringify(data)
				})
					.then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); })
					.then(function (res) {
						if (res.ok) {
							form.reset();
							if (status) { status.className = "hss-form-status ok"; status.textContent = "Thanks! We'll be in touch soon."; }
						} else {
							throw new Error((res.j && res.j.message) || "error");
						}
					})
					.catch(function () {
						if (status) { status.className = "hss-form-status err"; status.textContent = "Something went wrong — please email info@humboldtscoopsolutions.com."; }
					});
			} else {
				// Fallback: open a pre-filled email.
				var body = encodeURIComponent(
					"Name: " + (data.name || "") + "\nPhone: " + (data.phone || "") +
					"\nEmail: " + (data.email || "") + "\nCity: " + (data.city || "") +
					"\nDogs: " + (data.dogs || "") + "\nInterested in: " + (data.interest || "") +
					"\n\n" + (data.message || "")
				);
				window.location.href = "mailto:info@humboldtscoopsolutions.com?subject=" +
					encodeURIComponent("Quote request from " + (data.name || "website")) + "&body=" + body;
				if (status) { status.className = "hss-form-status ok"; status.textContent = "Opening your email app…"; }
			}
		});
	}
})();
