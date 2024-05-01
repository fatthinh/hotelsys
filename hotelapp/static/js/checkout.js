let rooms = [];
let cart = [];
const moreBtn = $(".js-more-passenger");
const passengerList = $(".passenger-list");
const cartItemList = $(".cart-info__list");
const totalAmount = $(".total-amount");
const totalRooms = $(".total-rooms");

moreBtn.addEventListener("click", () => {
  const newItem = document.createElement("li");
  newItem.classList.add("passenger-item");

  newItem.innerHTML = `
    <div class="form__row">
      <div class="form__group">
        <div class="form__text-input form__text-input--small">
          <input
            type="text"
            name=""
            placeholder="Name"
            id="passenger"
            class="form__input"
          />
        </div>
        <p class="form__error">
          Phone must be at least 11 characters
        </p>
      </div>

      <div class="form__group">
        <div class="form__text-input form__text-input--small">
          <input
            type="text"
            name=""
            placeholder="Identity number"
            id="passenger-id"
            class="form__input"
            pattern="[0-9]{12}"
            maxlength="12"
            required
          />
        </div>
      </div>

      <div class="form__group form__group--inline" style="flex: 0.4">
        <label class="form__checkbox">
          <input
            type="checkbox"
            name=""
            id=""
            class="form__checkbox-input d-none"
            checked
          />
          <span class="form__checkbox-label">Vietnamese</span>
        </label>
      </div>

      <div class="form__group" style="flex: 0.2">
        <button
          class="btn btn--small btn--danger js-remove-passenger"
        >
          <i class="fa-solid fa-trash"></i>
        </button>
      </div>
    </div>`;

  passengerList.appendChild(newItem);

  passengerList.querySelectorAll(".js-remove-passenger").forEach((item) => {
    item.addEventListener("click", (e) => {
      e.preventDefault();
      if (passengerList.children.length !== 1)
        item.closest(".passenger-item").remove();
    });
  });

  calSurcharge();
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
          style="height: 100px"
        />
      </a>
      <div class="cart-item__info">
        <div class="cart-item__info-left">
          <h3 class="cart-item__title">
            <a href="/"> ${info.name} </a>
          </h3>
          <p class="cart-item__price-wrap">x${item.quantity}</p>
        </div>
        <div class="cart-item__info-right">
          <p class="cart-item__total-price">$${info.price}</p>
        </div>
      </div>
                  `;
      cartItemList.appendChild(newItem);
    });
  }
};

const calSurcharge = () => {
  let vietnamses = passengerList.children.length;

  $$(".form__checkbox-input").forEach((item) => {
    item.addEventListener("change", () => {
      if (item.checked) {
        vietnamses++;
      } else {
        vietnamses--;
      }
      //   $(".surcharge").innerHTML = `$${vietnamses}`;
    });
  });
};

const initCheckout = () => {
  // get data
  fetch("/api/rooms")
    .then((response) => response.json())
    .then((data) => {
      rooms = data.data;
      console.log(rooms);
    });

  fetch("/api/cart")
    .then((res) => res.json())
    .then((data) => {
      cart = data.items;
      totalAmount.innerHTML = `$${data.total_amount}`;
      totalRooms.innerHTML = data.total_quantity;
      addCartToHTML();
    });

  calSurcharge();
};

initCheckout();
