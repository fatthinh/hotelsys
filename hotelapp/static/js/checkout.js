let roomTypes = [];
let cart = [];
let rooms = [];
const guestList = $(".guest-list");
const cartItemList = $(".cart-info__list");
const totalAmount = $(".total-amount");
const totalRooms = $(".total-rooms");

$(".js-more-guest").addEventListener("click", () => {
  const newItem = document.createElement("li");
  newItem.classList.add("guest-item");

  newItem.innerHTML = `
  <div class="form__row">
    <div class="form__group">
      <div class="form__text-input form__text-input--small">
        <input
          type="text"
          placeholder="Name"
          class="form__input guest-name"
        />
      </div>
    </div>

    <div class="form__group">
      <div class="form__text-input form__text-input--small">
        <input
          type="text"
          placeholder="Identity number"
          class="form__input guest-id"
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
          class="form__checkbox-input d-none guest-vietnamese"
          checked
        />
        <span class="form__checkbox-label">Vietnamese</span>
      </label>
    </div>

    <div class="form__group form__group--inline" style="flex: 0.4">
    <label class="form__checkbox">
      <input
        type="checkbox"
        class="form__checkbox-input d-none info-saved"
      />
      <span class="form__checkbox-label">Done</span>
    </label>
  </div>

    <div class="form__group" style="flex: 0.2">
      <button
        class="btn btn--small btn--danger js-remove-guest"
      >
        <i class="fa-solid fa-trash"></i>
      </button>
    </div>
  </div>`;

  const adults = roomTypes.find(
    (type) =>
      type.id ===
      rooms.find((room) => room.id === parseInt(guestList.dataset.room))
        .room_type
  ).adults;

  if (guestList.children.length < adults + 1) guestList.appendChild(newItem);

  queryRemoveBtn();
  addGuest();
});

const queryRemoveBtn = () => {
  guestList.querySelectorAll(".js-remove-guest").forEach((item) => {
    item.addEventListener("click", (e) => {
      e.preventDefault();
      const target = item.closest(".guest-item");
      fetch(`/api/guests/${target.querySelector(".guest-id").value}`, {
        method: "delete",
      });

      console.log(`/api/guests/${target.querySelector(".guest-id").value}`);
      target.remove();
    });
  });
};

const addCartToHTML = () => {
  cartItemList.innerHTML = "";
  if (cart.length > 0) {
    cart.forEach((item) => {
      const newItem = document.createElement("article");
      newItem.classList.add("cart-item");
      newItem.dataset.room = item.room;

      const info = roomTypes?.find((room) => room.id === item.room_type);
      const roomName = rooms?.find((room) => room.id === item.room)?.name;

      newItem.innerHTML = `
      <div class="cart-item__img">
        <img
          src="https://res.cloudinary.com/dzjhqjxqj/image/upload/v1703404014/samples/chair-and-coffee-table.jpg"
          class="cart-item__thumb"
          alt=""
          style="height: 120px"
        />
      </div>
      <div class="cart-item__info">
        <div class="cart-item__info-left">
          <h3 class="cart-item__title">
          ${info.name}
          </h3>
          <p class="cart-item__price-wrap">Room: ${roomName}</p>

        </div>
        <div class="cart-item__info-right">
          <p class="cart-item__total-price">$${info.price}</p>
          <button class="btn btn--small cart-item__ctrl"><i class="fa-solid fa-circle-info"></i></button>
        </div>
      </div>
                  `;
      cartItemList.appendChild(newItem);
    });
  }
};

const addGuest = () => {
  $$(".info-saved").forEach((item) => {
    item.addEventListener("change", () => {
      if (item.checked) {
        const target = item.closest(".guest-item");
        const name = target.querySelector(".guest-name").value;
        const identity = target.querySelector(".guest-id").value;
        const isVietnamese = item.checked;

        fetch("/api/guests", {
          method: "post",
          body: JSON.stringify({
            identity: identity,
            name: name,
            room_id: $(".guest-list").dataset.room,
            is_vietnamese: isVietnamese,
          }),

          headers: {
            "Content-Type": "application/json",
          },
        });
      }
    });
  });
};

const renderGuests = () => {
  fetch("/api/guests")
    .then((response) => response.json())
    .then((data) => {
      const guests = data;
      const room_id = guestList.dataset.room;
      guestList.innerHTML = "";
      if (guests.length) {
        guests
          .filter((guest) => parseInt(guest.room) === parseInt(room_id))
          .forEach((guest) => {
            guestList.innerHTML += ` <li class="guest-item" data-id="${guest.identity}">
      <div class="form__row">
        <div class="form__group">
          <div class="form__text-input form__text-input--small">
            <input
              type="text"
              placeholder="Name"
              class="form__input guest-name"
              value=${guest?.name}
            />
          </div>
        </div>

        <div class="form__group">
          <div class="form__text-input form__text-input--small">
            <input
              type="text"
              placeholder="Identity number"
              class="form__input guest-id"
              pattern="[0-9]{12}"
              maxlength="12"
              required
              value=${guest?.identity}
            />
          </div>
        </div>
        <div class="form__group form__group--inline" style="flex: 0.4">
          <label class="form__checkbox">
            <input
              type="checkbox"
              class="form__checkbox-input d-none guest-vietnamese"
              checked
            />
            <span class="form__checkbox-label">Vietnamese</span>
          </label>
        </div>

        <div class="form__group form__group--inline" style="flex: 0.4">
          <label class="form__checkbox">
            <input
              type="checkbox"
              class="form__checkbox-input d-none info-saved"
              checked
            />
            <span class="form__checkbox-label">Saved</span>
          </label>
        </div>

        <div class="form__group" style="flex: 0.2">
          <button
            class="btn btn--small btn--danger js-remove-guest"
          >
            <i class="fa-solid fa-trash"></i>
          </button>
        </div>
      </div>
    </li>`;
          });
        queryRemoveBtn();
      }
    });
};

const initCheckout = () => {
  // get data
  fetch("/api/room_types")
    .then((response) => response.json())
    .then((data) => {
      roomTypes = data.data;
    });

  fetch("/api/rooms")
    .then((res) => res.json())
    .then((data) => {
      rooms = data.data;
    });

  fetch("/api/cart")
    .then((res) => res.json())
    .then((data) => {
      cart = data.items;
      totalAmount.innerHTML = `$${data.total_amount}`;
      totalRooms.innerHTML = data.total_quantity;

      setTimeout(() => {
        addCartToHTML();
        $$(".cart-item__ctrl").forEach((item) => {
          item.addEventListener("click", () => {
            guestList.dataset.room = item.closest(".cart-item").dataset.room;
            $(".room-name").innerHTML = `(${
              rooms.find(
                (room) =>
                  room.id === parseInt(item.closest(".cart-item").dataset.room)
              )?.name
            })`;
            renderGuests();
          });
        });
        renderGuests();
      }, 500);
      renderGuests();
    });
};

initCheckout();
