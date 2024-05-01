let cart = [];
let rooms = [];
const addToCartButtons = $$(".add-to-cart");
const cartItemList = $(".cart-list");
const cartBtn = $(".cart-icon");
const totalCart = $(".badge");
const alert = $(".alert");
const trash = $$(".cart-trash");
const total = $(".total");

addToCartButtons.forEach((item) => {
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
        cart = data.items;
        totalCart.innerHTML = data.items.length;
        addCartToHTML();
        total.innerHTML = `$${data.total_amount}`;
      });

    alert.classList.add("show");

    setTimeout(() => {
      alert.classList.remove("show");
      alert.classList.add("hide");
    }, 1000);
  });
});

cartItemList.addEventListener("click", (e) => {
  e.preventDefault();
  let positionClick = e.target;
  const id = positionClick.closest(".cart-item").dataset.id;

  if (e.target.getAttribute("href")) {
    window.location.href = e.target.getAttribute("href");
  } else if (positionClick.classList.contains("cart-trash")) {
    jsToggle(positionClick);
    const confirmBtn = $(".confirm");
    confirmBtn.addEventListener("click", () => {
      const isHidden = $("#loader").classList.contains("hide");

      requestAnimationFrame(() => {
        $("#loader").classList.toggle("hide", !isHidden);
        $("#loader").classList.toggle("show", isHidden);
      });

      setTimeout(() => {
        fetch(`/api/cart/${id}`, {
          method: "delete",
        })
          .then((res) => res.json())
          .then((data) => {
            cart = data.items;
            totalCart.innerHTML = data.items.length;
            addCartToHTML();
            total.innerHTML = `$${data.total_amount}`;
          });

        const isHidden = $("#loader").classList.contains("hide");

        requestAnimationFrame(() => {
          $("#loader").classList.toggle("hide", !isHidden);
          $("#loader").classList.toggle("show", isHidden);
        });
      }, 1000);
    });
  } else if (positionClick.classList.contains("fa-regular")) {
    const quantity = cart.find((item) => item.id === id).quantity;
    fetch(`/api/cart/${id}`, {
      method: "put",
      body: JSON.stringify({
        quantity: positionClick.classList.contains("fa-square-plus")
          ? quantity + 1
          : quantity - 1,
      }),
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((res) => res.json())
      .then((data) => {
        cart = data.items;
        totalCart.innerHTML = data.items.length;
        addCartToHTML();
        total.innerHTML = `$${data.total_amount}`;
      });
  }
});

const addCartToHTML = () => {
  cartItemList.innerHTML = "";
  if (cart.length > 0) {
    cart.forEach((item) => {
      const newItem = document.createElement("article");
      newItem.classList.add("cart-item");
      newItem.dataset.id = item.id;

      const info = rooms.find((room) => room.id == item.id);

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
            <button class="cart-item__input-btn descrease">
              <i class="fa-regular fa-square-minus"></i>
            </button>
            <span>${item.quantity}</span>
            <button class="cart-item__input-btn increase">
              <i class="fa-regular fa-square-plus"></i>
            </button>
          </div>
        </div>
      </div>
      <div class="cart-item__info-right">
        <p class="cart-item__total-price">$${info.price}</p>
        <div class="cart-item__ctrl">
          <button
            class="cart-item__ctrl-btn cart-trash"
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
};

const initCart = () => {
  // get data
  fetch("/api/rooms")
    .then((response) => response.json())
    .then((data) => {
      rooms = data.data;
    });

  fetch("/api/cart")
    .then((res) => res.json())
    .then((data) => {
      cart = data.items;
      totalCart.innerHTML = data.items.length;
      addCartToHTML();
      total.innerHTML = `$${data.total_amount}`;
    });
};

initCart();

function jsToggle(button) {
  const target = button.getAttribute("toggle-target");
  if (!target) {
    document.body.innerText = `Cần thêm toggle-target cho: ${button.outerHTML}`;
  }
  button.onclick = (e) => {
    e.preventDefault();

    if (!$(target)) {
      return (document.body.innerText = `Không tìm thấy phần tử "${target}"`);
    }
    const isHidden = $(target).classList.contains("hide");

    requestAnimationFrame(() => {
      $(target).classList.toggle("hide", !isHidden);
      $(target).classList.toggle("show", isHidden);
    });
  };

  document.onclick = function (e) {
    if (!e.target.closest(target)) {
      const isHidden = $(target).classList.contains("hide");
      if (!isHidden) {
        button.click();
      }
    }
  };
}
