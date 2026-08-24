const tg = window.Telegram
    ? window.Telegram.WebApp
    : null;

if (tg) {
    tg.ready();
    tg.expand();
}


// ================================
// SAHIFA OCHISH
// ================================

function openPage(page) {

    const pages = document.querySelectorAll(".page");

    pages.forEach(function(item) {
        item.classList.remove("active");
    });

    const target = document.getElementById(page);

    if (target) {
        target.classList.add("active");
    }

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}


// ================================
// ANIME OCHISH
// ================================

function anime(name) {

    alert(
        "🎬 " + name +
        "\n\nAnime sahifasi ochiladi."
    );
}


// ================================
// QIDIRUV
// ================================

function searchAnime() {

    const input =
        document.getElementById("searchInput");

    const result =
        document.getElementById("result");

    if (!input || !result) {
        return;
    }

    const query =
        input.value.trim();

    if (!query) {

        result.innerHTML =
            "<p style='margin-top:20px;color:#8e96aa'>" +
            "🔎 Anime nomini kiriting." +
            "</p>";

        return;
    }

    result.innerHTML =

        "<div class='list-item' style='margin-top:15px'>" +

        "<div class='icon'>🎬</div>" +

        "<div>" +

        "<b>" +
        escapeHtml(query) +
        "</b>" +

        "<small>" +
        "Anime qidirilmoqda..." +
        "</small>" +

        "</div>" +

        "</div>";
}


// ================================
// XAVFSIZ TEXT
// ================================

function escapeHtml(text) {

    return text
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


// ================================
// TELEGRAM USER
// ================================

function getTelegramUser() {

    if (
        tg &&
        tg.initDataUnsafe &&
        tg.initDataUnsafe.user
    ) {

        return tg.initDataUnsafe.user;
    }

    return null;
}


// ================================
// PROFILNI TELEGRAMDAN OLISH
// ================================

function loadProfile() {

    const user =
        getTelegramUser();

    if (!user) {
        return;
    }

    const profile =
        document.querySelector(".profile h2");

    if (!profile) {
        return;
    }

    let name = "";

    if (user.first_name) {
        name += user.first_name;
    }

    if (user.last_name) {
        name += " " + user.last_name;
    }

    if (!name) {
        name = "Anime Hunter";
    }

    profile.textContent = name;
}


// ================================
// HAPTIC
// ================================

function haptic() {

    if (
        tg &&
        tg.HapticFeedback
    ) {

        tg.HapticFeedback.impactOccurred(
            "light"
        );
    }
}


// ================================
// BOTTOM MENU HAPTIC
// ================================

document
    .querySelectorAll(".bottom-nav button")
    .forEach(function(button) {

        button.addEventListener(
            "click",
            function() {

                haptic();

            }
        );

    });


// ================================
// VIP BUTTON
// ================================

const vipButton =
    document.querySelector(".vip-button");

if (vipButton) {

    vipButton.addEventListener(
        "click",
        function() {

            haptic();

            if (tg) {

                tg.showPopup({

                    title: "👑 ANIMEVERSE VIP",

                    message:
                        "VIP paketni bot orqali tanlashingiz mumkin.",

                    buttons: [
                        {
                            id: "ok",
                            type: "ok",
                            text: "Tushunarli"
                        }
                    ]

                });

            } else {

                alert(
                    "👑 VIP paketni bot orqali tanlang."
                );

            }

        }
    );
}


// ================================
// INPUT ENTER
// ================================

const searchInput =
    document.getElementById(
        "searchInput"
    );

if (searchInput) {

    searchInput.addEventListener(
        "keydown",
        function(event) {

            if (event.key === "Enter") {

                searchAnime();

            }

        }
    );
}


// ================================
// TELEGRAM MAIN BUTTON
// ================================

if (tg) {

    tg.MainButton.setText(
        "🌌 ANIMEVERSE"
    );

}


// ================================
// START
// ================================

document.addEventListener(
    "DOMContentLoaded",
    function() {

        loadProfile();

        openPage("home");

    }
);
