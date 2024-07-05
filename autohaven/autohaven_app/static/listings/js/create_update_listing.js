function selectImages(event, fileInput) {
  event.preventDefault();
  fileInput.click();
}

const imageElementsList = [];

function drawImages(imagesToDraw) {
  imagesToDraw.forEach((newImageElement, index) => {
    let imgContainer;
    if (index === 0) {
      imgContainer = document.getElementById("main-image-container");
    } else {
      const otherImagesContainer = document.getElementById(
        "other-images-container"
      );
      imgContainer = document.createElement("div");
      imgContainer.classList.add("column");
      if (index === 1) otherImagesContainer.innerHTML = "";
      otherImagesContainer.append(imgContainer);
    }
    const closeSpan = document.createElement("span");
    closeSpan.innerHTML = "X";
    imgContainer.innerHTML = "";
    imgContainer.append(closeSpan);
    imgContainer.append(newImageElement);
  });
}

function onImagesChange(filesInput) {
  const newImages = Array.from(filesInput.files);
  console.log({ newImages });
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
  console.log({ newImageElements, imageElementsList });
  drawImages(imageElementsList);
}

function onSubmit(event, filesInput) {
  event.preventDefault();
  dtObject = new DataTransfer();
  imageElementsList.forEach((imgElement) => {
    console.log({ imgElement });
    dtObject.items.add(imgElement.file);
  });
  filesInput.files = dtObject.files;
  const form = document.getElementById("new-listing-form");
  form.requestSubmit();
}

function formSetup() {
  const addImagesBtn = document.getElementById("add-images-btn");
  const submitBtn = document.getElementById("submit-form-btn");
  const filesInput = document.querySelector('input[type="file"]');

  addImagesBtn.addEventListener("click", (event) =>
    selectImages(event, filesInput)
  );
  filesInput.addEventListener("change", (_) => onImagesChange(filesInput));
  submitBtn.addEventListener("click", (event) => onSubmit(event, filesInput));
}
window.addEventListener("load", formSetup);
