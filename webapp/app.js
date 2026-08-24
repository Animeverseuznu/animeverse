const animeList = [
    {
        id: "solo",
        title: "Solo Leveling",
        genre: ["Action", "Fantasy"],
        type: "Serial",
        emoji: "⚔️",
        description: "Sung Jin-Woo dunyodagi eng zaif hunterlardan biri edi. Sirli tizim unga kuchli bo‘lish imkoniyatini beradi."
    },
    {
        id: "onepiece",
        title: "One Piece",
        genre: ["Action", "Comedy"],
        type: "Serial",
        emoji: "🏴‍☠️",
        description: "Luffy va uning jamoasi afsonaviy One Piece xazinasini izlab buyuk sayohatga chiqadi."
    },
    {
        id: "naruto",
        title: "Naruto",
        genre: ["Action", "Fantasy"],
        type: "Serial",
        emoji: "🍥",
        description: "Naruto Uzumaki eng kuchli ninja bo‘lish va Hokage unvoniga erishishni orzu qiladi."
    },
    {
        id: "demonslayer",
        title: "Demon Slayer",
        genre: ["Action", "Fantasy", "Horror"],
        type: "Serial",
        emoji: "⚡",
        description: "Tanjiro oilasini himoya qilish va singlisini qutqarish uchun demonlarga qarshi kurashadi."
    },
    {
        id: "jujutsu",
        title: "Jujutsu Kaisen",
        genre: ["Action", "Horror"],
        type: "Serial",
        emoji: "👹",
        description: "Yuji Itadori la'natlar olamiga kirib, insoniyatni xavfli mavjudotlardan himoya qiladi."
    },
    {
        id: "aot",
        title: "Attack on Titan",
        genre: ["Action", "Fantasy"],
        type: "Serial",
        emoji: "🪽",
        description: "Insoniyat devorlar ichida yashaydi va ulkan titanlar tahdidiga qarshi kurashadi."
    },
    {
        id: "yourname",
        title: "Your Name",
        genre: ["Romance", "Fantasy"],
        type: "Film",
        emoji: "🌠",
        description: "Ikki yosh sirli tarzda bir-birining tanasida uyg‘ona boshlaydi."
    },
    {
        id: "spyfamily",
        title: "SPY x FAMILY",
        genre: ["Comedy", "Action"],
        type: "Serial",
        emoji: "🕵️",
        description: "Soxta oila tuzgan josus, assassin va telepat qizning noodatiy hayoti."
    }
];


let currentAnime = null;


// ============================================
// 🏠 HOME
// ============================================

function goHome() {

    document.querySelector(".hero").style.display = "flex";
    document.querySelector(".search-section").style.display = "block";

    document.querySelectorAll(".section").forEach(section => {
        section.classList.remove("hidden");
    });

    document.querySelector(".vip-section").style.display = "flex";

    const content = document.getElementById("contentSection");

    if (content) {
        content.classList.add("hidden");
    }

    setActiveNav(0);

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}


// ============================================
// 🎴 CARD
// ============================================

function createAnimeCard(anime) {

    return `
        <div class="anime-card" onclick="openAnime('${anime.id}')">

            <div class="anime-poster">
                ${anime.emoji}
            </div>

            <div class="anime-info">

                <h3>${anime.title}</h3>

                <p>
                    ${anime.type} • ${anime.genre[0]}
                </p>

            </div>

        </div>
    `;
}


// ============================================
// 🔥 TOP ANIME
// ============================================

function renderTopAnime() {

    const container = document.getElementById("topAnime");

    if (!container) return;

    container.innerHTML = animeList
        .slice(0, 6)
        .map(createAnimeCard)
        .join("");
}


// ============================================
// 🆕 NEW ANIME
// ============================================

function renderNewAnime() {

    const container = document.getElementById("newAnime");

    if (!container) return;

    container.innerHTML = animeList
        .slice(2)
        .reverse()
        .map(createAnimeCard)
        .join("");
}


// ============================================
// 🔥 SHOW TOP
// ============================================

function showTopAnime() {

    hideHomeSections();

    showContent(
        "🔥 TOP ANIME",
        animeList.slice(0, 6)
    );

    setActiveNav(1);
}


// ============================================
// 🆕 SHOW NEW
// ============================================

function showNewAnime() {

    hideHomeSections();

    showContent(
        "🆕 YANGI ANIME",
        animeList.slice(2).reverse()
    );

    setActiveNav(3);
}


// ============================================
// 🎭 GENRE
// ============================================

function filterGenre(genre) {

    const results = animeList.filter(anime =>
        anime.genre.includes(genre)
    );

    hideHomeSections();

    showContent(
        `🎭 ${genre}`,
        results
    );
}


function showAllGenres() {

    hideHomeSections();

    showContent(
        "🎭 BARCHA JANRLAR",
        animeList
    );
}


// ============================================
// 🔎 SEARCH
// ============================================

function searchAnime() {

    const input = document.getElementById("searchInput");

    if (!input) return;

    const query = input.value
        .toLowerCase()
        .trim();

    if (!query) {

        goHome();

        return;
    }

    const results = animeList.filter(anime =>

        anime.title
            .toLowerCase()
            .includes(query)

        ||

        anime.genre.some(genre =>
            genre.toLowerCase().includes(query)
        )
    );

    hideHomeSections();

    showContent(
        `🔎 "${input.value}"`,
        results
    );

    setActiveNav(2);
}


// ============================================
// 🔎 SEARCH BUTTON
// ============================================

function focusSearch() {

    const search = document.getElementById("searchInput");

    if (!search) return;

    goHome();

    setTimeout(() => {

        search.focus();

        search.scrollIntoView({
            behavior: "smooth",
            block: "center"
        });

    }, 150);

    setActiveNav(2);
}


// ============================================
// 📺 SHOW CONTENT
// ============================================

function showContent(title, list) {

    const section =
        document.getElementById("contentSection");

    const titleElement =
        document.getElementById("contentTitle");

    const grid =
        document.getElementById("contentGrid");

    if (!section || !grid) return;

    titleElement.textContent = title;

    if (list.length === 0) {

        grid.innerHTML = `
            <div style="
                grid-column:1/-1;
                text-align:center;
                padding:40px 10px;
                color:#9292a6;
            ">
                😔 Anime topilmadi
            </div>
        `;

    } else {

        grid.innerHTML =
            list.map(createAnimeCard).join("");
    }

    section.classList.remove("hidden");

    section.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}


// ============================================
// 🎬 OPEN ANIME
// ============================================

function openAnime(id) {

    const anime =
        animeList.find(item => item.id === id);

    if (!anime) return;

    currentAnime = anime;

    const modal =
        document.getElementById("animeModal");

    document.getElementById("modalTitle")
        .textContent = anime.title;

    document.getElementById("modalDescription")
        .textContent = anime.description;

    document.getElementById("modalPoster")
        .textContent = anime.emoji;

    document.getElementById("modalBadge")
        .textContent = anime.type;

    const genres =
        document.getElementById("modalGenres");

    genres.innerHTML =
        anime.genre
            .map(g => `<span>${g}</span>`)
            .join("");

    modal.classList.add("show");
}


// ============================================
// ❌ CLOSE ANIME
// ============================================

function closeModal() {

    const modal =
        document.getElementById("animeModal");

    if (modal) {
        modal.classList.remove("show");
    }

    currentAnime = null;
}


// ============================================
// ▶️ WATCH
// ============================================

function startWatching() {

    if (!currentAnime) return;

    closeModal();

    alert(
        `🎬 ${currentAnime.title}\n\n` +
        `▶️ Qismlar oynasi keyingi bosqichda ulanadi.`
    );
}


// ============================================
// 👤 PROFILE
// ============================================

function openProfile() {

    const modal =
        document.getElementById("profileModal");

    if (!modal) return;

    modal.classList.add("show");
}


function closeProfile() {

    const modal =
        document.getElementById("profileModal");

    if (modal) {
        modal.classList.remove("show");
    }
}


// ============================================
// 👑 VIP
// ============================================

function openVIP() {

    alert(
        "👑 ANIMEVERSE VIP\n\n" +
        "VIP tizimi keyingi bosqichda ulanadi."
    );
}


// ============================================
// 🧹 HIDE HOME
// ============================================

function hideHomeSections() {

    const hero =
        document.querySelector(".hero");

    const search =
        document.querySelector(".search-section");

    const vip =
        document.querySelector(".vip-section");

    if (hero) hero.style.display = "none";

    if (search) search.style.display = "none";

    if (vip) vip.style.display = "none";

    document.querySelectorAll(".section")
        .forEach(section => {

            if (section.id !== "contentSection") {
                section.classList.add("hidden");
            }

        });
}


// ============================================
// 📱 BOTTOM NAV
// ============================================

function setActiveNav(index) {

    const buttons =
        document.querySelectorAll(".bottom-nav button");

    buttons.forEach((button, i) => {

        button.classList.toggle(
            "active",
            i === index
        );

    });
}


// ============================================
// 🧠 INITIALIZE
// ============================================

document.addEventListener(
    "DOMContentLoaded",
    () => {

        renderTopAnime();

        renderNewAnime();

        goHome();

    }
);


// ============================================
// ❌ MODAL BACKGROUND
// ============================================

document.addEventListener(
    "click",
    event => {

        const animeModal =
            document.getElementById("animeModal");

        const profileModal =
            document.getElementById("profileModal");

        if (
            event.target === animeModal
        ) {
            closeModal();
        }

        if (
            event.target === profileModal
        ) {
            closeProfile();
        }

    }
);
