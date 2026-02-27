document.addEventListener("DOMContentLoaded", function () {

    const fotoInput = document.getElementById("foto");
    const previewImg = document.getElementById("previewImg");
    const previewArea = document.getElementById("previewArea");

    if (fotoInput) {
        fotoInput.addEventListener("change", function () {

            const file = this.files[0];

            if (!file) {
                previewArea.style.display = "none";
                return;
            }

            // Validação básica de tipo
            if (!file.type.startsWith("image/")) {
                alert("Selecione apenas imagens.");
                fotoInput.value = "";
                return;
            }

            // Limite de tamanho (ex: 5MB)
            if (file.size > 5 * 1024 * 1024) {
                alert("Imagem muito grande (máx 5MB).");
                fotoInput.value = "";
                return;
            }

            const reader = new FileReader();

            reader.onload = function (e) {
                previewImg.src = e.target.result;
                previewArea.style.display = "block";
            };

            reader.readAsDataURL(file);
        });
    }

});