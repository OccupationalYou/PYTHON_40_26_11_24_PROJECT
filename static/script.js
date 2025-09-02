// Глобальні змінні
let products = [];
let cart = {}; // Використовуємо об'єкт для зручного оновлення
let db;
let auth;
let userId = '';

// Конфігурація Firebase
const firebaseConfig = JSON.parse(typeof __firebase_config !== 'undefined' ? __firebase_config : '{}');
const appId = typeof __app_id !== 'undefined' ? __app_id : 'default-app-id';

// Імпорт необхідних модулів Firebase
import { initializeApp } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-app.js";
import { getAuth, signInAnonymously, signInWithCustomToken, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-auth.js";
import { getFirestore, doc, onSnapshot, setDoc, getDocs, collection, query, where } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-firestore.js";

// DOM-елементи
const catalogGrid = document.getElementById('catalog-grid');
const productDetailsContainer = document.getElementById('product-details-container');
const cartItemsContainer = document.getElementById('cart-items');
const cartTotalElement = document.getElementById('cart-total');
const cartCountElement = document.getElementById('cart-count');
const favoritesGrid = document.getElementById('favorites-grid');
const messageModal = document.getElementById('messageModal');
const modalTitle = document.getElementById('modalTitle');
const modalMessage = document.getElementById('modalMessage');

// Ініціалізація Firebase
async function initializeFirebaseAndAuth() {
    try {
        const app = initializeApp(firebaseConfig);
        db = getFirestore(app);
        auth = getAuth(app);

        await new Promise(resolve => {
            const unsubscribe = onAuthStateChanged(auth, async (user) => {
                if (user) {
                    userId = user.uid;
                } else {
                    const anonymousUser = await signInAnonymously(auth);
                    userId = anonymousUser.user.uid;
                }
                unsubscribe();
                resolve();
            });
        });

        console.log("Firebase initialized. User ID:", userId);
        setupRealtimeCartListener();
    } catch (error) {
        console.error("Error initializing Firebase:", error);
    }
}

async function fetchProductsFromDB() {
    try {
        const response = await fetch("/api/products");
        if (response.ok) {
            products = await response.json();
            renderCatalog(products);
        } else {
            console.error("Failed to fetch products:", response.status);
        }
    } catch (error) {
        console.error("Error fetching products:", error);
    }
}

function renderCatalog(filteredProducts) {
    catalogGrid.innerHTML = '';
    if (filteredProducts.length === 0) {
        catalogGrid.innerHTML = '<p class="text-lg">Продукти не знайдено.</p>';
        return;
    }
    filteredProducts.forEach(product => {
        const productCard = document.createElement('div');
        productCard.className = 'bg-white dark:bg-gray-800 rounded-lg shadow-md p-4 transition-transform transform hover:scale-105 cursor-pointer';

        // Витягуємо перше зображення для картки
        let imageUrl = '';
        try {
            const images = JSON.parse(product.image_url);
            if (Array.isArray(images) && images.length > 0) {
                imageUrl = images[0];
            }
        } catch (e) {
            console.error('Failed to parse image URLs:', e);
        }

        productCard.innerHTML = `
            <img src="${imageUrl}" alt="${product.name}" class="w-full h-48 object-cover rounded-lg mb-4" onerror="this.src='https://placehold.co/400x300/e5e7eb/1f2937?text=Зображення+недоступне'">
            <h3 class="text-xl font-bold mb-2 text-gray-900 dark:text-white">${product.name}</h3>
            <p class="text-gray-600 dark:text-gray-400 mb-2">${product.description.substring(0, 70)}...</p>
            <p class="text-2xl font-bold text-blue-600 dark:text-blue-400">${product.price} грн</p>
            <div class="flex items-center justify-between mt-4">
                <button class="py-2 px-4 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors duration-200" onclick="event.stopPropagation(); showProductDetails(${product.id})">Детальніше</button>
                <button class="p-2 text-gray-500 hover:text-red-500 transition-colors duration-200" onclick="event.stopPropagation(); toggleFavorite(${product.id})">
                    <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5A5.4 5.4 0 017.5 3C9.36 3 11 4.3 12 6.13c1-1.83 2.64-3.13 4.5-3.13A5.4 5.4 0 0122 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>
                </button>
            </div>
        `;
        catalogGrid.appendChild(productCard);
    });
}

function showPage(id) {
    document.querySelectorAll('.page').forEach(page => page.classList.add('hidden'));
    document.getElementById(id).classList.remove('hidden');
    if (id === 'catalog') {
        renderCatalog(products);
    }
}

function showCatalogCategory(categoryName) {
    const filteredProducts = products.filter(p => p.category === categoryName);
    renderCatalog(filteredProducts);
    showPage('catalog');
}

async function showFavs() {
    if (!userId) {
        showMessageModal('Помилка', 'Для перегляду обраних товарів потрібно бути увійденним.');
        return;
    }

    favoritesGrid.innerHTML = '';
    const favsRef = collection(db, 'artifacts', appId, 'users', userId, 'favorites');
    const q = query(favsRef);

    try {
        const querySnapshot = await getDocs(q);
        if (querySnapshot.empty) {
            favoritesGrid.innerHTML = '<p class="text-lg text-center">У вас ще немає обраних товарів.</p>';
            return;
        }

        querySnapshot.forEach(async (docSnap) => {
            const favProduct = products.find(p => p.id === docSnap.data().productId);
            if (favProduct) {
                const productCard = document.createElement('div');
                productCard.className = 'bg-white dark:bg-gray-800 rounded-lg shadow-md p-4 transition-transform transform hover:scale-105 cursor-pointer';

                let imageUrl = '';
                try {
                    const images = JSON.parse(favProduct.image_url);
                    if (Array.isArray(images) && images.length > 0) {
                        imageUrl = images[0];
                    }
                } catch (e) {
                    console.error('Failed to parse image URLs:', e);
                }

                productCard.innerHTML = `
                    <img src="${imageUrl}" alt="${favProduct.name}" class="w-full h-48 object-cover rounded-lg mb-4" onerror="this.src='https://placehold.co/400x300/e5e7eb/1f2937?text=Зображення+недоступне'">
                    <h3 class="text-xl font-bold mb-2 text-gray-900 dark:text-white">${favProduct.name}</h3>
                    <p class="text-gray-600 dark:text-gray-400 mb-2">${favProduct.description.substring(0, 70)}...</p>
                    <p class="text-2xl font-bold text-blue-600 dark:text-blue-400">${favProduct.price} грн</p>
                    <div class="flex items-center justify-between mt-4">
                        <button class="py-2 px-4 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors duration-200" onclick="event.stopPropagation(); showProductDetails(${favProduct.id})">Детальніше</button>
                        <button class="p-2 text-red-500 hover:text-red-700 transition-colors duration-200" onclick="event.stopPropagation(); toggleFavorite(${favProduct.id})">
                            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5A5.4 5.4 0 017.5 3C9.36 3 11 4.3 12 6.13c1-1.83 2.64-3.13 4.5-3.13A5.4 5.4 0 0122 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>
                        </button>
                    </div>
                `;
                favoritesGrid.appendChild(productCard);
            }
        });
        showPage('favorites');
    } catch (error) {
        console.error("Error fetching favorites:", error);
        showMessageModal('Помилка', 'Не вдалося завантажити обрані товари.');
    }
}

async function toggleFavorite(productId) {
    if (!userId) {
        showMessageModal('Помилка', 'Для додавання до обраного потрібно бути увійденним.');
        return;
    }

    const favDocRef = doc(db, 'artifacts', appId, 'users', userId, 'favorites', `product_${productId}`);

    try {
        const docSnap = await getDoc(favDocRef);
        if (docSnap.exists()) {
            await deleteDoc(favDocRef);
            showMessageModal('Видалено з обраного', `Товар було видалено з обраного.`);
        } else {
            await setDoc(favDocRef, { productId });
            showMessageModal('Додано до обраного', `Товар було додано до обраного.`);
        }
    } catch (error) {
        console.error("Error toggling favorite:", error);
        showMessageModal('Помилка', 'Не вдалося додати/видалити товар з обраного. Спробуйте пізніше.');
    }
}

async function showProductDetails(id) {
    const product = products.find(p => p.id === id);
    if (!product) {
        showMessageModal('Помилка', 'Продукт не знайдено.');
        return;
    }

    productDetailsContainer.innerHTML = `
        <div id="product-gallery" class="w-full md:w-1/2">
            <img id="main-product-image" src="" alt="${product.name}" class="w-full rounded-lg shadow-md mb-4" onerror="this.src='https://placehold.co/600x400/e5e7eb/1f2937?text=Зображення+недоступне'">
            <div id="thumbnails" class="flex gap-2 overflow-x-auto p-2"></div>
        </div>
        <div class="w-full md:w-1/2">
            <h2 class="text-3xl font-bold mb-2 text-gray-900 dark:text-white">${product.name}</h2>
            <p class="text-xl text-blue-600 dark:text-blue-400 font-semibold mb-4">${product.price} грн</p>
            <p class="text-gray-600 dark:text-gray-400 mb-4">${product.description}</p>
            <div class="flex space-x-4">
                <button onclick="addToCart(${product.id})" class="flex-1 py-3 px-6 bg-blue-500 text-white rounded-lg text-lg font-bold hover:bg-blue-600 transition-colors duration-200">Додати до кошика</button>
                <button class="p-3 text-gray-500 hover:text-red-500 transition-colors duration-200" onclick="toggleFavorite(${product.id})">
                    <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 24 24"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5A5.4 5.4 0 017.5 3C9.36 3 11 4.3 12 6.13c1-1.83 2.64-3.13 4.5-3.13A5.4 5.4 0 0122 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>
                </button>
            </div>
        </div>
    `;

    const images = JSON.parse(product.image_url);
    const mainImage = document.getElementById('main-product-image');
    const gallery = document.getElementById('thumbnails');

    if (images && images.length > 0) {
        mainImage.src = images[0];
        images.forEach(url => {
            const thumb = document.createElement('img');
            thumb.src = url;
            thumb.className = 'w-16 h-16 object-cover rounded-lg cursor-pointer border-2 border-transparent hover:border-blue-500 transition-colors duration-200';
            thumb.onclick = () => mainImage.src = url;
            thumb.onerror = function() { this.src = 'https://placehold.co/100x100/e5e7eb/1f2937?text=Зображення+недоступне'; }
            gallery.appendChild(thumb);
        });
    } else {
        mainImage.src = 'https://placehold.co/600x400/e5e7eb/1f2937?text=Зображення+недоступне';
    }

    showPage("productDetails");
}

async function addToCart(productId) {
    if (!userId) {
        showMessageModal('Помилка', 'Не вдалося додати товар. Користувач не ідентифікований.');
        return;
    }

    const product = products.find(p => p.id === productId);
    if (!product) {
        showMessageModal('Помилка', 'Товар не знайдено.');
        return;
    }

    const cartRef = doc(db, 'artifacts', appId, 'users', userId, 'cart', 'items');

    // Используем productId в качестве ключа для объекта cart
    cart[productId] = cart[productId] ? { ...cart[productId], quantity: cart[productId].quantity + 1 } : { ...product, quantity: 1 };

    try {
        await setDoc(cartRef, cart);
        updateCartCount();
        showMessageModal('Додано в кошик', `"${product.name}" було додано в кошик.`);
    } catch (error) {
        console.error("Error adding to cart:", error);
        showMessageModal('Помилка', 'Не вдалося додати товар до кошика. Спробуйте пізніше.');
    }
}

function setupRealtimeCartListener() {
    if (userId) {
        const cartRef = doc(db, 'artifacts', appId, 'users', userId, 'cart', 'items');
        onSnapshot(cartRef, (docSnap) => {
            if (docSnap.exists()) {
                cart = docSnap.data();
                renderCart();
                updateCartCount();
            } else {
                cart = {};
                renderCart();
                updateCartCount();
            }
        }, (error) => {
            console.error("Error listening to cart changes:", error);
        });
    }
}

function updateCartCount() {
    const totalItems = Object.values(cart).reduce((sum, item) => sum + item.quantity, 0);
    cartCountElement.textContent = totalItems;
}

function renderCart() {
    cartItemsContainer.innerHTML = '';
    let total = 0;
    if (Object.keys(cart).length === 0) {
        cartItemsContainer.innerHTML = '<p class="text-lg text-center">Кошик порожній.</p>';
        return;
    }
    for (const productId in cart) {
        const item = cart[productId];
        total += item.price * item.quantity;
        const cartItemDiv = document.createElement('div');
        cartItemDiv.className = 'flex items-center justify-between p-4 rounded-lg bg-gray-200 dark:bg-gray-800';
        cartItemDiv.innerHTML = `
            <div class="flex items-center gap-4">
                <img src="${JSON.parse(item.image_url)[0] || 'https://placehold.co/100x100/e5e7eb/1f2937?text=Зображення+недоступне'}" alt="${item.name}" class="w-16 h-16 object-cover rounded-lg">
                <div>
                    <h4 class="font-bold">${item.name}</h4>
                    <p class="text-sm text-gray-600 dark:text-gray-400">${item.price} грн x ${item.quantity}</p>
                </div>
            </div>
            <button onclick="removeFromCart(${item.id})" class="py-1 px-3 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors duration-200">Видалити</button>
        `;
        cartItemsContainer.appendChild(cartItemDiv);
    }
    cartTotalElement.textContent = `${total.toFixed(2)} грн`;
    showPage('cart');
}

function removeFromCart(productId) {
    const cartRef = doc(db, 'artifacts', appId, 'users', userId, 'cart', 'items');
    if (cart[productId]) {
        delete cart[productId];
        setDoc(cartRef, cart);
    }
}

function showModal(id) {
    document.getElementById(id).classList.add('open');
}

function closeModal(id) {
    document.getElementById(id).classList.remove('open');
}

function showMessageModal(title, message) {
    document.getElementById('modalTitle').textContent = title;
    document.getElementById('modalMessage').textContent = message;
    showModal('messageModal');
}

// Логіка перемикання теми
const toggleBtn = document.getElementById('toggle-theme');
const html = document.documentElement;
const savedTheme = localStorage.getItem('theme');

if (savedTheme) {
    html.setAttribute('data-theme', savedTheme);
}

toggleBtn.addEventListener('click', () => {
    const currentTheme = html.getAttribute('data-theme') || 'light';
    const nextTheme = currentTheme === 'light' ? 'dark' : 'light';
    html.setAttribute('data-theme', nextTheme);
    localStorage.setItem('theme', nextTheme);
});

// Ініціалізація
window.onload = async () => {
    await initializeFirebaseAndAuth();
    await fetchProductsFromDB();
};

// Глобалізація функцій для HTML
window.showPage = showPage;
window.showProductDetails = showProductDetails;
window.addToCart = addToCart;
window.removeFromCart = removeFromCart;
window.showCatalogCategory = showCatalogCategory;
window.showFavs = showFavs;
window.toggleFavorite = toggleFavorite;
window.closeModal = closeModal;
