function handleFormSubmit(event) {
    event.preventDefault();

    Swal.fire({
        title: "Processing...",
        text: "Please wait while we process your file.",
        allowOutsideClick: false,
        didOpen: () => {
            Swal.showLoading();
        }
    });

    let form = event.target;
    let formData = new FormData(form);

    fetch(form.action, {
        method: "POST",
        body: formData
    })
        .then(response => {
            if (!response.ok) {
                throw new Error("File processing failed.");
            }
            return response.blob(); // Convert response to file blob
        })
        .then(blob => {
            let a = document.createElement("a");
            a.href = URL.createObjectURL(blob);
            a.download = "anonymized_file.csv"; // Set filename
            document.body.appendChild(a);
            a.click();
            a.remove();

            Swal.fire({
                title: "Success!",
                text: "Processing complete! Your file has been downloaded.",
                icon: "success"
            });

            form.reset();
        })
        .catch(error => {
            Swal.fire({
                title: "Error!",
                text: error.message,
                icon: "error"
            });
        });
}