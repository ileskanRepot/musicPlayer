const formSubmit = (event) => {
  const request = new Request(`/products/${item.ItemCode}?_method=POST`, {
    method: 'POST',
    body: new FormData(e.target),
  });
  fetch(request)
}