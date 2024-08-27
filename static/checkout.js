// Replace with your own test publishable API key
const stripe = Stripe("pk_test_51PrwGXI3rn6BpbALKwh82i3pufZLtvYupcy4ZVkZq9KFl0T1qzd03hE5zuXASeBu8m8apoLSR1vvam7wyHD7hoQ5006zqJjiTJ");

// Initialize Stripe Elements
let elements;

initialize();

async function initialize() {
    const response = await fetch("/create-payment-intent", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
    });

    const { clientSecret } = await response.json();

    elements = stripe.elements({ clientSecret });

    const paymentElement = elements.create("payment");
    paymentElement.mount("#payment-element");
}

// Handle form submission
document.querySelector("#payment-form").addEventListener("submit", async (event) => {
    event.preventDefault();

    const { error } = await stripe.confirmPayment({
        elements,
        confirmParams: {
            return_url: "http://localhost:8000/success", // Change to your desired URL
        },
    });

    if (error) {
        // Show error message to your customer
        const messageContainer = document.querySelector("#payment-message");
        messageContainer.classList.remove("hidden");
        messageContainer.textContent = error.message;
    }
});
