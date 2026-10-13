document.addEventListener("DOMContentLoaded", function () {

    // 1. Auto-hide Django messages
    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(function (alert) {
        setTimeout(function () {
            alert.style.transition = "opacity 0.5s ease";
            alert.style.opacity = "0";

            setTimeout(function () {
                alert.remove();
            }, 500);

        }, 4000);
    });

    // 2. Logout confirmation
    const logoutLinks = document.querySelectorAll(
        'a[href*="/logout/"]'
    );

    logoutLinks.forEach(function (link) {
        link.addEventListener("click", function (event) {
            const confirmLogout = confirm(
                "Are you sure you want to logout?"
            );

            if (!confirmLogout) {
                event.preventDefault();
            }
        });
    });

    // 3. Highlight active sidebar link
    const currentPath = window.location.pathname;

    const sidebarLinks = document.querySelectorAll(".sidebar a");

    sidebarLinks.forEach(function (link) {
        const linkPath = new URL(link.href).pathname;

        if (linkPath === currentPath) {
            link.classList.add("active");
        }
    });

    // 4. Password show/hide toggle (works on every password field)
    document
        .querySelectorAll('input[type="password"]')
        .forEach(function (input) {

            const toggle = document.createElement("button");
            toggle.type = "button";
            toggle.textContent = "Show";
            toggle.style.cssText =
                "position:absolute; right:12px; top:50%; " +
                "transform:translateY(-50%); border:none; " +
                "background:none; color:#1e40af; " +
                "font-size:13px; cursor:pointer;";

            // Wrap input so the button can sit inside it
            const wrapper = document.createElement("div");
            wrapper.style.position = "relative";
            input.parentNode.insertBefore(wrapper, input);
            wrapper.appendChild(input);
            wrapper.appendChild(toggle);

            input.style.paddingRight = "60px";

            toggle.addEventListener("click", function () {
                const isHidden = input.type === "password";
                input.type = isHidden ? "text" : "password";
                toggle.textContent = isHidden ? "Hide" : "Show";
            });
        });

    // 5. Register page: live "passwords match" check
    const password = document.getElementById("password");
    const confirmPassword = document.getElementById("confirm_password");

    if (password && confirmPassword) {

        const message = document.createElement("small");
        confirmPassword.parentNode.parentNode.appendChild(message);

        const checkMatch = function () {
            if (!confirmPassword.value) {
                message.textContent = "";
                return;
            }

            if (password.value === confirmPassword.value) {
                message.textContent = "Passwords match";
                message.style.color = "green";
            } else {
                message.textContent = "Passwords do not match";
                message.style.color = "red";
            }
        };

        password.addEventListener("input", checkMatch);
        confirmPassword.addEventListener("input", checkMatch);
    }

    // 6. Generic confirm popup
    //    Usage: add data-confirm="Your message" to any link, button or form.
    //    Job Activate/Deactivate forms get it automatically below.
    document
        .querySelectorAll('form[action*="/toggle/"]')
        .forEach(function (form) {
            if (!form.dataset.confirm) {
                form.dataset.confirm =
                    "Are you sure you want to change this job's status?";
            }
        });

    document.addEventListener("click", function (event) {
        const target = event.target.closest(
            "a[data-confirm], button[data-confirm]"
        );

        if (target && !confirm(target.dataset.confirm)) {
            event.preventDefault();
        }
    });

    document.addEventListener("submit", function (event) {
        const form = event.target;

        if (
            form.matches &&
            form.matches("form[data-confirm]") &&
            !confirm(form.dataset.confirm)
        ) {
            event.preventDefault();
        }
    });

    // 7. Count-up animation for dashboard numbers
    //    Targets: .count-up, [data-count], and bold headings that
    //    contain only a number (e.g. the recruitment dashboard cards).
    const reduceMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    ).matches;

    const countCandidates = document.querySelectorAll(
        ".count-up, [data-count], h2.fw-bold, h3.fw-bold"
    );

    countCandidates.forEach(function (element) {
        const raw = element.textContent.trim().replace(/,/g, "");

        if (!/^\d+(\.\d+)?$/.test(raw)) {
            return;
        }

        const finalValue = parseFloat(raw);
        const decimals = raw.includes(".") ? raw.split(".")[1].length : 0;

        if (reduceMotion || finalValue === 0) {
            return;
        }

        const duration = 1000;
        const startTime = performance.now();

        function step(now) {
            const progress = Math.min((now - startTime) / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3);
            const current = finalValue * eased;

            element.textContent = current.toLocaleString("en-IN", {
                minimumFractionDigits: decimals,
                maximumFractionDigits: decimals
            });

            if (progress < 1) {
                requestAnimationFrame(step);
            } else {
                element.textContent = raw;
            }
        }

        element.textContent = "0";
        requestAnimationFrame(step);
    });

    // 8. Sortable tables (click a column header to sort)
    //    Applies to every table that has a <thead> and <tbody>.
    //    Add class "no-sort" to any <th> you want to skip.
    function cellText(row, index) {
        const cell = row.children[index];
        return cell ? cell.textContent.replace(/\s+/g, " ").trim() : "";
    }

    function toNumber(text) {
        const cleaned = text.replace(/[₹$,\s]/g, "");
        return /^-?\d+(\.\d+)?$/.test(cleaned) ? parseFloat(cleaned) : null;
    }

    function toDate(text) {
        let match;

        // 2026-10-05
        if (/^\d{4}-\d{2}-\d{2}/.test(text)) {
            return Date.parse(text.slice(0, 10));
        }

        // 05/10/2026 (day first)
        match = text.match(/^(\d{1,2})[\/.\-](\d{1,2})[\/.\-](\d{4})$/);
        if (match) {
            return new Date(match[3], match[2] - 1, match[1]).getTime();
        }

        // Oct 5, 2026  or  5 Oct 2026
        if (
            /^[A-Za-z]{3,9}\.? \d{1,2},? \d{4}$/.test(text) ||
            /^\d{1,2} [A-Za-z]{3,9}\.? \d{4}$/.test(text)
        ) {
            const parsed = Date.parse(text);
            return isNaN(parsed) ? null : parsed;
        }

        return null;
    }

    function compareCells(a, b) {
        const numA = toNumber(a);
        const numB = toNumber(b);

        if (numA !== null && numB !== null) {
            return numA - numB;
        }

        const dateA = toDate(a);
        const dateB = toDate(b);

        if (dateA !== null && dateB !== null) {
            return dateA - dateB;
        }

        return a.localeCompare(b, undefined, {
            numeric: true,
            sensitivity: "base"
        });
    }

    document.querySelectorAll("table").forEach(function (table) {
        const headRow = table.querySelector("thead tr");
        const body = table.querySelector("tbody");

        if (!headRow || !body) {
            return;
        }

        const headers = Array.from(headRow.children);

        headers.forEach(function (th, index) {
            const label = th.textContent.trim();

            if (
                !label ||
                th.classList.contains("no-sort") ||
                /^actions?$/i.test(label)
            ) {
                return;
            }

            th.style.cursor = "pointer";
            th.style.userSelect = "none";
            th.title = "Click to sort";

            const arrow = document.createElement("span");
            arrow.style.cssText = "margin-left:6px; font-size:11px; opacity:0.6;";
            arrow.textContent = "↕";
            th.appendChild(arrow);

            th.addEventListener("click", function () {
                const ascending = th.dataset.sortDir !== "asc";

                // Rows with colspan are "no records" messages, leave them
                const rows = Array.from(body.querySelectorAll("tr")).filter(
                    function (row) {
                        return !row.querySelector("td[colspan]");
                    }
                );

                rows.sort(function (rowA, rowB) {
                    const result = compareCells(
                        cellText(rowA, index),
                        cellText(rowB, index)
                    );
                    return ascending ? result : -result;
                });

                rows.forEach(function (row) {
                    body.appendChild(row);
                });

                headers.forEach(function (other) {
                    delete other.dataset.sortDir;
                    const otherArrow = other.querySelector("span");
                    if (otherArrow && other !== th) {
                        otherArrow.textContent = "↕";
                    }
                });

                th.dataset.sortDir = ascending ? "asc" : "desc";
                arrow.textContent = ascending ? "▲" : "▼";
            });
        });
    });

});