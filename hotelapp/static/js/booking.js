let cart = [];
let room_types = [];
let rooms = [];
const cartItemList = $(".cart-list");
const totalCart = $(".badge");
const total = $(".total");

// Add to cart action
$$(".add-to-cart").forEach((item) => {
  item.addEventListener("click", () => {
    fetch("/api/cart", {
      method: "post",
      body: JSON.stringify({
        id: item.closest(".room-item").dataset.id,
        checkIn: checkIn.value,
        checkOut: checkOut.value,
      }),

      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((res) => res.json())
      .then((data) => {
        cartChanges(data);
      });

    const alert = $(".alert");
    alert.classList.add("show");

    setTimeout(() => {
      alert.classList.remove("show");
      alert.classList.add("hide");
    }, 1000);
  });
});

// Cart modal actions
cartItemList.addEventListener("click", (e) => {
  e.preventDefault();
  const target = e.target;
  const room_id = target.closest(".cart-item").dataset.room;

  if (e.target.getAttribute("href")) {
    window.location.href = e.target.getAttribute("href");
  } else if (target.classList.contains("cart-trash")) {
    const confirmBtn = $(".confirm");
    confirmBtn.addEventListener("click", () => {
      fetch(`/api/cart/${room_id}`, {
        method: "delete",
      })
        .then((res) => res.json())
        .then((data) => {
          loading();
          cartChanges(data);
        })
        .finally(loading());
    });
  }
});

const renderCart = () => {
  cartItemList.innerHTML = "";
  if (cart.length > 0) {
    cart.forEach((item) => {
      const newItem = document.createElement("article");
      newItem.classList.add("cart-item");
      newItem.dataset.room = item.room;

      const info = room_types.find((room) => room.id == item.room_type);

      newItem.innerHTML = `
      <a href="/" class="cart-item__img">
      <img
        src="https://res.cloudinary.com/dzjhqjxqj/image/upload/v1703404014/samples/chair-and-coffee-table.jpg"
        class="cart-item__thumb"
        alt=""
      />
    </a>
    <div class="cart-item__info">
      <div class="cart-item__info-left">
        <h3 class="cart-item__title">
          <a href="/"> ${info.name} </a>
        </h3>
        <p class="cart-item__price-wrap">Capacity: 5 persons</p>
        <div class="cart-item__ctrl cart-item__ctrl--md-block">
          <div class="cart-item__input">
            <span>Room: </span>
            <span>${rooms.find((room) => room.id === item.room)?.name}</span>
          </div>
        </div>
      </div>
      <div class="cart-item__info-right">
        <p class="cart-item__total-price">$${info.price}</p>
        <div class="cart-item__ctrl">
          <button
            class="cart-item__ctrl-btn cart-trash js-toggle"
            toggle-target="#delete-confirm"
            >
            <i class="fa-solid fa-trash"></i>
            Delete
          </button>
        </div>
      </div>
    </div>
                `;
      cartItemList.appendChild(newItem);
    });
  }
  initJsToggle();
};

const cartChanges = async (data) => {
  cart = await data.items;
  totalCart.innerHTML = cart.length;
  renderCart();
  total.innerHTML = `$${data.total_amount}`;
};

// Initialize booking page
const initPage = () => {
  // get data
  fetch("/api/room_types")
    .then((response) => response.json())
    .then((data) => {
      room_types = data.data;
    });

  fetch("/api/rooms")
    .then((response) => response.json())
    .then((data) => {
      rooms = data.data;
    });

  fetch("/api/cart")
    .then((res) => res.json())
    .then((data) => {
      cartChanges(data);
    });
};

initPage();
