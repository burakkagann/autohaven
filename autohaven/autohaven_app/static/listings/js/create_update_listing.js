function selectImages() {}
function formSetup() {
  const addImagesBtn = document.getElementById("add-images-btn");
  const imagesContainer = document.getElementById("images-container");

  addImagesBtn.addEventListener("click", selectImages());
}
window.addEventListener("load", formSetup);
