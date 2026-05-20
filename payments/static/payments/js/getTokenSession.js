export async function GetTokenSession(transactionId, {
    // requestSource = 'ECOMMERCE',
    // merchantCode = '',
    // orderNumber = '',
    // publicKey = '',
    // amount = '',
    orderUUID = '',
}) {

    //llamado al backend interno de esta app
    try {
        const response = await fetch('/payments/token/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'transactionId': transactionId },
            body: JSON.stringify({
                // requestSource,
                // merchantCode,
                // orderNumber,
                // publicKey,
                // amount,
                orderUUID,  // nuevo
            }),
        });
        return await response.json();
    } catch (e) {
        console.log('REVISA QUE EL ARCHIVO SERVER SE ESTE EJECUTANDO!');
        return {
            response: {
                token: undefined,
                error: '01_NODE_API'
            }
        };

    }
}
