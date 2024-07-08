function selectImages(event, fileInput) {
  event.preventDefault();
  fileInput.click();
}

function onDelete(event) {
  const imgToDelete = event.target.nextSibling;
  if (imgToDelete instanceof HTMLImageElement) {
    imageElementsList = imageElementsList.filter(
      (imgElement) => imgElement !== imgToDelete
    );
    if (imgToDelete.dataset.id) {
      const imagesToDeleteSelect = document.querySelector(
        "[name=imagesToDelete]"
      );
      for (const option of imagesToDeleteSelect.options) {
        if (option.value === imgToDelete.dataset.id) option.selected = true;
      }
    }
    imgToDelete.remove();
    drawImages(imageElementsList);
  }
}

let imageElementsList = [];
let imagesToDelete = [];

function drawImages(imagesToDraw) {
  console.log({ imagesToDraw });
  const mainImageContainer = document.getElementById("main-image-container");
  const otherImagesContainer = document.getElementById(
    "other-images-container"
  );
  mainImageContainer.innerHTML = "";
  otherImagesContainer.innerHTML = "";
  imagesToDraw.forEach((newImageElement, index) => {
    let imgContainer;
    if (index === 0) {
      imgContainer = document.getElementById("main-image-container");
    } else {
      imgContainer = document.createElement("div");
      imgContainer.classList.add("column");
      otherImagesContainer.append(imgContainer);
    }
    const closeSpan = document.createElement("span");
    closeSpan.innerHTML = "X";
    closeSpan.addEventListener("click", onDelete);
    imgContainer.innerHTML = "";
    console.log({ closeSpan, newImageElement });
    imgContainer.append(closeSpan);
    imgContainer.append(newImageElement);
  });
}

function onImagesChange(filesInput) {
  const newImages = Array.from(filesInput.files);
  const newImageElements = newImages.map((newImage) => {
    const imgElement = document.createElement("img");
    imgElement.file = newImage;
    const fileReader = new FileReader();
    fileReader.onload = (loadEvent) => {
      imgElement.src = loadEvent.target.result;
    };
    fileReader.readAsDataURL(newImage);
    return imgElement;
  });

  imageElementsList.push(...newImageElements);
  drawImages(imageElementsList);
}

function loadListingImages(previousImages, mediaPrefix) {
  if (previousImages) {
    const previousImageElements = previousImages.map((previousImage) => {
      const imgElement = document.createElement("img");
      imgElement.dataset.id = previousImage.id;
      imgElement.src = mediaPrefix + previousImage.imagepath;
      return imgElement;
    });

    imageElementsList.push(...previousImageElements);
    drawImages(imageElementsList);
  }
}

function onSubmit(event, filesInput) {
  event.preventDefault();
  dtObject = new DataTransfer();
  imageElementsList.forEach((imgElement) => {
    if (imgElement.file) dtObject.items.add(imgElement.file);
  });
  filesInput.files = dtObject.files;
  const form = document.getElementById("new-listing-form");
  form.requestSubmit();
}

function formSetup() {
  const addImagesBtn = document.getElementById("add-images-btn");
  const submitBtn = document.getElementById("submit-form-btn");
  const filesInput = document.querySelector('input[type="file"]');

  const previousImages = JSON.parse(
    document.getElementById("listing-images").textContent
  );
  const mediaPrefix = JSON.parse(
    document.getElementById("media-prefix").textContent
  );
  console.log({ previousImages });
  loadListingImages(previousImages, mediaPrefix);

  addImagesBtn.addEventListener("click", (event) =>
    selectImages(event, filesInput)
  );
  filesInput.addEventListener("change", (_) => onImagesChange(filesInput));
  submitBtn.addEventListener("click", (event) => onSubmit(event, filesInput));
}
window.addEventListener("load", formSetup);
